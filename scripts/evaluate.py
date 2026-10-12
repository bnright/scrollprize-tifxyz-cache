"""Replay real mesh tiling requests against a fresh-computation oracle.

Each upstream/candidate repetition runs in an independent Python process. Source
meshes are read-only; caches go into results/work. No ink models or text recovery.
"""
import argparse
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

from source_loader import ROOT, load_source

MESHES = {
    "PHerc0139": "PHerc0139-w025-9.362um.tifxyz",
    "PHerc0800": "PHerc0800-auto-grown-8.64um.tifxyz",
}
CASES = [
    ("memory_target", False, {"target_size": (128, 128, 128)}, {"target_size": (256, 256, 256)}),
    ("memory_overlap", False, {"target_size": (256, 256, 256), "overlap_fraction": 0.0}, {"target_size": (256, 256, 256), "overlap_fraction": 0.5}),
    ("disk_overlap", True, {"target_size": (256, 256, 256), "overlap_fraction": 0.0}, {"target_size": (256, 256, 256), "overlap_fraction": 0.5}),
    ("disk_target_control", True, {"target_size": (128, 128, 128)}, {"target_size": (256, 256, 256)}),
]


def digest(patches):
    return hashlib.sha256(json.dumps(patches, separators=(",", ":")).encode()).hexdigest()


def invoke(surface, settings, **extra):
    started = time.perf_counter()
    with redirect_stdout(io.StringIO()):
        result = surface.get_patches_3d(**settings, **extra)
    return result, time.perf_counter() - started


def worker(variant, repetition):
    import psutil
    import numpy as np
    read = load_source(variant)
    rows = []
    # Warm JIT kernels on actual data before recording request latencies.
    warm = read(ROOT / "private-data" / MESHES["PHerc0139"])
    warm.path = None
    _, warmup_seconds = invoke(warm, {"target_size": (128, 128, 128)}, force_recompute=True)

    for mesh_id, directory in MESHES.items():
        mesh = ROOT / "private-data" / directory
        geometry = read(mesh)
        geometry_info = {"shape": list(geometry.shape), "scale": list(geometry.get_scale_tuple()),
                         "valid_vertices": int(geometry._valid_mask.sum())}
        for name, reload_from_disk, initial, requested in CASES:
            # The smaller complete PHerc0800 mesh has much less usable area.
            # Use 64 -> 128 contexts; retain the exploratory 128 -> 256 result
            # (including its empty fresh tiling) in evaluation-exploratory.json.
            if mesh_id == "PHerc0800":
                initial = {**initial, "target_size": tuple(d // 2 for d in initial["target_size"])}
                requested = {**requested, "target_size": tuple(d // 2 for d in requested["target_size"])}
            cache_path = ROOT / "results" / "work" / f"{variant}-{repetition}-{mesh_id}-{name}"
            cache_path.mkdir(parents=True, exist_ok=True)
            cache_file = cache_path / "patches_cache.json"
            if cache_file.exists():
                cache_file.unlink()
            surface = read(mesh)
            surface.path = cache_path if reload_from_disk else None
            seeded, initial_seconds = invoke(surface, initial)
            if reload_from_disk:
                surface = read(mesh)
                surface.path = cache_path
            observed, observed_seconds = invoke(surface, requested)
            oracle_surface = read(mesh)
            oracle_surface.path = None
            expected, oracle_seconds = invoke(oracle_surface, requested, force_recompute=True)
            repeat, hit_seconds = invoke(surface, requested)
            observed_set = set(observed)
            expected_set = set(expected)
            rows.append({
                "mesh": mesh_id, "case": name, "variant": variant,
                "repetition": repetition, "initial": initial, "requested": requested,
                "geometry": geometry_info, "initial_count": len(seeded),
                "initial_sha256": digest(seeded),
                "observed_count": len(observed), "oracle_count": len(expected),
                "exact_match": observed == expected,
                "observed_sha256": digest(observed), "oracle_sha256": digest(expected),
                "unexpected_patches": len(observed_set - expected_set),
                "missing_patches": len(expected_set - observed_set),
                "repeat_same_object": repeat is observed, "repeat_exact_match": repeat == expected,
                "initial_seconds": initial_seconds, "changed_request_seconds": observed_seconds,
                "oracle_seconds": oracle_seconds, "same_request_hit_seconds": hit_seconds,
            })
        del geometry
    info = psutil.Process().memory_info()
    peak = getattr(info, "peak_wset", None)
    if peak is None:
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
    return {"variant": variant, "repetition": repetition, "warmup_seconds": warmup_seconds,
            "peak_process_rss_bytes": peak, "rows": rows}


def verify_files():
    checked = []
    for manifest in sorted((ROOT / "docs").glob("*-provenance.json")):
        metadata = json.loads(manifest.read_text(encoding="utf-8-sig"))
        directory = MESHES[metadata["scroll"]]
        for item in metadata["files"]:
            data = (ROOT / "private-data" / directory / item["file"]).read_bytes()
            checksum = hashlib.sha256(data).hexdigest()
            if checksum != item["sha256"] or len(data) != item["bytes"]:
                raise ValueError(f"Provenance mismatch: {directory}/{item['file']}")
            checked.append({"mesh": directory, "file": item["file"], "sha256": checksum, "bytes": len(data)})
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=["upstream", "candidate"])
    parser.add_argument("--repetition", type=int, default=0)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker, args.repetition)))
        return
    verified = verify_files()
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    workers = []
    for rep in range(args.repetitions):
        # Alternate source order to reduce systematic order bias in latency.
        order = ["upstream", "candidate"] if rep % 2 == 0 else ["candidate", "upstream"]
        for variant in order:
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--worker", variant,
                                  "--repetition", str(rep)], check=True, text=True, capture_output=True)
            result = json.loads(run.stdout)
            workers.append(result)
            print(f"{variant} repetition {rep}: " + ", ".join(
                f"{r['mesh']}/{r['case']}={'PASS' if r['exact_match'] else 'FAIL'}"
                for r in result["rows"]), flush=True)
    rows = [row for w in workers for row in w["rows"]]
    summary = []
    for mesh in MESHES:
        for case, *_ in CASES:
            for variant in ["upstream", "candidate"]:
                selected = [r for r in rows if r["mesh"] == mesh and r["case"] == case and r["variant"] == variant]
                latencies = [r["changed_request_seconds"] for r in selected]
                summary.append({"mesh": mesh, "case": case, "variant": variant,
                                "passed": sum(r["exact_match"] for r in selected), "runs": len(selected),
                                "observed_count": selected[0]["observed_count"], "oracle_count": selected[0]["oracle_count"],
                                "unexpected_patches": selected[0]["unexpected_patches"],
                                "missing_patches": selected[0]["missing_patches"],
                                "changed_request_mean_seconds": statistics.mean(latencies),
                                "changed_request_median_seconds": statistics.median(latencies),
                                "changed_request_min_seconds": min(latencies), "changed_request_max_seconds": max(latencies)})
    checks = {
        "candidate_all_match_fresh": all(r["exact_match"] for r in rows if r["variant"] == "candidate"),
        "candidate_same_request_cache_hits": all(r["repeat_same_object"] for r in rows if r["variant"] == "candidate"),
        "upstream_defect_reproduced": any(not r["exact_match"] for r in rows if r["variant"] == "upstream"),
        "fresh_oracle_outputs_identical": all(
            next(r for r in rows if r["variant"] == "upstream" and r["mesh"] == mesh and r["case"] == case and r["repetition"] == rep)["oracle_sha256"] ==
            next(r for r in rows if r["variant"] == "candidate" and r["mesh"] == mesh and r["case"] == case and r["repetition"] == rep)["oracle_sha256"]
            for mesh in MESHES for case, *_ in CASES for rep in range(args.repetitions)),
        "unchanged_first_request_outputs": all(
            next(r for r in rows if r["variant"] == "upstream" and r["mesh"] == mesh and r["case"] == case and r["repetition"] == rep)["initial_sha256"] ==
            next(r for r in rows if r["variant"] == "candidate" and r["mesh"] == mesh and r["case"] == case and r["repetition"] == rep)["initial_sha256"]
            for mesh in MESHES for case, *_ in CASES for rep in range(args.repetitions)),
        "source_data_unchanged": verified == verify_files(),
    }
    report = {"verified_date": "2026-10-12", "python": sys.version, "platform": platform.platform(),
              "source_revision": "25f3c93c65b492be3b90e402213a1ba6b5fd624c", "checks": checks,
              "verified_source_data": verified, "summary": summary, "workers": workers}
    (results / "evaluation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
