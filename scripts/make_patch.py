"""Generate a reviewable upstream patch; no remote repository is modified."""
import difflib
from source_loader import ROOT

TARGET = "vesuvius/src/vesuvius/tifxyz/types.py"
TEST_TARGET = "vesuvius/tests/tifxyz/test_patch_cache.py"


def main():
    before = (ROOT / "upstream" / TARGET).read_text(encoding="utf-8").splitlines(keepends=True)
    after = (ROOT / "candidate" / TARGET).read_text(encoding="utf-8").splitlines(keepends=True)
    patch = "".join(difflib.unified_diff(before, after, "a/" + TARGET, "b/" + TARGET))
    tests = (ROOT / "tests" / "test_patch_cache.py").read_text(encoding="utf-8").splitlines(keepends=True)
    patch += "".join(difflib.unified_diff([], tests, "/dev/null", "b/" + TEST_TARGET))
    (ROOT / "upstream-fix.patch").write_text(patch, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
