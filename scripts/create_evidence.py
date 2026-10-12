"""Create a figure and a labeled rendering of captured actual demo output."""
import json
import subprocess
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from source_loader import ROOT


def main():
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    transcripts = []
    for variant, expected_exit in [("upstream", 1), ("candidate", 0)]:
        run = subprocess.run([sys.executable, str(ROOT / "scripts" / "demo.py"), "--variant", variant],
                             capture_output=True, text=True)
        if run.returncode != expected_exit:
            raise ValueError(f"Unexpected {variant} demonstration status: {run.returncode}")
        output = run.stdout + run.stderr
        (evidence / f"demo-{variant}.txt").write_text(output, encoding="utf-8")
        # Show actual output lines; shorten Python environment-specific traceback
        # paths only for this visual, with complete originals retained as text.
        lines = run.stdout.rstrip().splitlines()
        if variant == "upstream":
            lines.append(run.stderr.rstrip().splitlines()[-1])
        transcripts.append((variant, "\n".join(lines)))
    fig, axes = plt.subplots(2, 1, figsize=(12, 5.7))
    fig.patch.set_facecolor("#111827")
    fig.suptitle("Actual real-mesh cache reproduction: captured output", color="white", fontsize=17)
    for ax, (variant, transcript) in zip(axes, transcripts):
        ax.set_facecolor("#182235")
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.text(0.02, 0.95, "$ python scripts/demo.py --variant " + variant + "\n\n" + transcript,
                transform=ax.transAxes, va="top", fontsize=10, fontfamily="monospace",
                color="#fca5a5" if variant == "upstream" else "#86efac")
    fig.text(0.02, 0.025, "Rendered from executed stdout/stderr; no scan imagery or text predictions. Complete logs: evidence/demo-*.txt",
             color="#cbd5e1", fontsize=9)
    fig.subplots_adjust(top=0.87, bottom=0.09, hspace=0.16)
    fig.savefig(evidence / "before-after-output.png", dpi=160)
    plt.close(fig)

    report = json.loads((ROOT / "results" / "evaluation.json").read_text())
    selected = [r for r in report["summary"] if r["mesh"] == "PHerc0139" and r["case"] in ["memory_target", "disk_overlap"]]
    baseline = [next(r["observed_count"] for r in selected if r["case"] == case and r["variant"] == "upstream")
                for case in ["memory_target", "disk_overlap"]]
    corrected = [next(r["observed_count"] for r in selected if r["case"] == case and r["variant"] == "candidate")
                 for case in ["memory_target", "disk_overlap"]]
    expected = [next(r["oracle_count"] for r in selected if r["case"] == case and r["variant"] == "candidate")
                for case in ["memory_target", "disk_overlap"]]
    fig, ax = plt.subplots(figsize=(8, 4.8))
    positions = np.arange(2)
    for offset, values, label, color in [(-0.26, baseline, "Upstream cached request", "#d46b60"),
                                       (0.0, corrected, "Patched cached request", "#318479"),
                                       (0.26, expected, "Fresh computation", "#536898")]:
        bars = ax.bar(positions + offset, values, 0.24, label=label, color=color)
        ax.bar_label(bars, padding=4)
    ax.set_xticks(positions, ["Memory: 128 -> 256 voxels", "Disk: overlap 0.0 -> 0.5"])
    ax.set_ylabel("Number of returned patches")
    ax.set_ylim(0, max(expected) * 1.3)
    ax.set_title("PHerc0139: a changed request must match fresh tiling")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.03, 0.025, "Patch count alone is illustrative. Validation compared every ordered 2D/3D bound exactly (3 repetitions).", fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(evidence / "cache-correctness.png", dpi=180)
    fig.savefig(evidence / "cache-correctness.svg")
    plt.close(fig)
    print("PASS: baseline fails and candidate passes actual demo; visual evidence created")


if __name__ == "__main__":
    main()
