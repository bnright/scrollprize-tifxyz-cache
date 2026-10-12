"""Prepare and audit a code-only review archive; never publish or upload it."""
import hashlib
import json
from pathlib import Path
import zipfile
from source_loader import ROOT

TOP_LEVEL = ["README.md", "LICENSE", ".gitignore", ".gitattributes", ".python-version", "requirements-lock.txt", "upstream-fix.patch"]
GROUPS = {"scripts": {".py"}, "tests": {".py"}, "docs": {".md", ".json"},
          "evidence": {".txt", ".png", ".svg"}, "upstream": {".py", ".md", ".toml"},
          "candidate": {".py", ".md", ".toml"}}
RESULTS = ["results/evaluation.json", "results/evaluation-exploratory.json"]
FORBIDDEN_PARTS = {"private-data", ".venv", ".git", "__pycache__", ".pytest_cache", "work"}


def main():
    files = {ROOT / name for name in TOP_LEVEL + RESULTS}
    for directory, extensions in GROUPS.items():
        for path in (ROOT / directory).rglob("*"):
            if path.is_file() and not FORBIDDEN_PARTS.intersection(path.relative_to(ROOT).parts):
                if path.suffix in extensions or path.name == "LICENSE":
                    files.add(path)
    manifest = []
    for path in sorted(files):
        relative = path.relative_to(ROOT).as_posix()
        contents = path.read_bytes()
        if FORBIDDEN_PARTS.intersection(Path(relative).parts):
            raise ValueError(f"Forbidden archive path: {relative}")
        manifest.append({"file": relative, "bytes": len(contents), "sha256": hashlib.sha256(contents).hexdigest()})
    release = ROOT / "release"
    release.mkdir(exist_ok=True)
    archive = release / "scrollprize-tifxyz-cache-2026-10-12.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for item in manifest:
            info = zipfile.ZipInfo("scrollprize-tifxyz-cache/" + item["file"], (2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, (ROOT / item["file"]).read_bytes())
        info = zipfile.ZipInfo("scrollprize-tifxyz-cache/MANIFEST.json", (2026, 10, 12, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        bundle.writestr(info, json.dumps({"verified_date": "2026-10-12", "files": manifest}, indent=2) + "\n")
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError("ZIP CRC verification failed")
        for name in bundle.namelist():
            if FORBIDDEN_PARTS.intersection(Path(name).parts) or Path(name).suffix.lower() in {".tif", ".tiff", ".nrrd", ".npy", ".npz"}:
                raise ValueError(f"Data or environment leaked into release: {name}")
        for item in manifest:
            content = bundle.read("scrollprize-tifxyz-cache/" + item["file"])
            if hashlib.sha256(content).hexdigest() != item["sha256"]:
                raise ValueError(f"Archive mismatch: {item['file']}")
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (release / (archive.name + ".sha256")).write_text(checksum + "  " + archive.name + "\n", encoding="utf-8")
    (release / "inventory.json").write_text(json.dumps({"archive": archive.name, "bytes": archive.stat().st_size,
                                                       "sha256": checksum, "files": manifest,
                                                       "audit": "CRC and all hashes verified; no source data, caches, environments or Git metadata"}, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(manifest)} files packaged, {archive.stat().st_size} bytes, SHA256 {checksum}")
    print(archive)


if __name__ == "__main__":
    main()
