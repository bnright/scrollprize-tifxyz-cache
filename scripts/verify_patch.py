"""Check that the proposed patch applies to the exact pinned upstream source."""
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path
from source_loader import ROOT
from make_patch import TARGET, TEST_TARGET


def main():
    with tempfile.TemporaryDirectory(prefix="tifxyz-patch-") as directory:
        checkout = Path(directory)
        shutil.copytree(ROOT / "upstream", checkout, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        subprocess.run(["git", "init", "-q", str(checkout)], check=True)
        subprocess.run(["git", "-C", str(checkout), "config", "core.autocrlf", "false"], check=True)
        subprocess.run(["git", "-C", str(checkout), "apply", "--check", str(ROOT / "upstream-fix.patch")], check=True)
        subprocess.run(["git", "-C", str(checkout), "apply", str(ROOT / "upstream-fix.patch")], check=True)
        if (checkout / TARGET).read_bytes() != (ROOT / "candidate" / TARGET).read_bytes():
            raise ValueError("Patched implementation differs from evaluated candidate")
        if (checkout / TEST_TARGET).read_bytes() != (ROOT / "tests" / "test_patch_cache.py").read_bytes():
            raise ValueError("Patched tests differ from evaluated tests")
        print("PASS: patch applies cleanly; implementation and tests match evaluated files byte for byte")


if __name__ == "__main__":
    main()
