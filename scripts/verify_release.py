"""Extract the prepared release and run its commands using the locked runtime."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile
from source_loader import ROOT


def main():
    archive = ROOT / "release" / "scrollprize-tifxyz-cache-2026-10-12.zip"
    results = []
    with tempfile.TemporaryDirectory(prefix="tifxyz-release-") as directory:
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.namelist():
                name = PurePosixPath(member)
                if name.is_absolute() or ".." in name.parts or name.parts[0] != "scrollprize-tifxyz-cache":
                    raise ValueError(f"Unsafe archive member: {member}")
            bundle.extractall(directory)
        extracted = Path(directory) / "scrollprize-tifxyz-cache"
        commands = [
            ["scripts/verify_sources.py"],
            ["scripts/verify_patch.py"],
            ["scripts/fetch_inputs.py"],
            ["-m", "pytest", "-q", "tests", "upstream/vesuvius/tests/tifxyz",
             "candidate/vesuvius/src/vesuvius/tifxyz/test_reader_bbox.py",
             "candidate/vesuvius/src/vesuvius/tifxyz/test_labels.py"],
            ["scripts/demo.py", "--variant", "candidate"],
        ]
        for command in commands:
            run = subprocess.run([sys.executable, *command], cwd=extracted, capture_output=True, text=True)
            results.append({"command": ["python", *command], "exit_code": run.returncode,
                            "stdout": run.stdout, "stderr": run.stderr})
            if run.returncode != 0:
                raise RuntimeError(f"Extracted package command failed: {command}\n{run.stdout}\n{run.stderr}")
            print("PASS: extracted package " + " ".join(command), flush=True)
    report = {"archive_sha256_tested": hashlib.sha256(archive.read_bytes()).hexdigest(),
              "verified_date": "2026-10-12", "environment": "Same installed Python runtime and dependency lock; new extracted source/data tree",
              "checks": results, "all_passed": True}
    (ROOT / "release" / "extraction-check.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
