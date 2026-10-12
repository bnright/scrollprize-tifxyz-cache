"""Load the pinned tifxyz subpackage without the unrelated ML/Volume initializer.

Only the parent namespace is supplied. Every tifxyz function, dependency and
numerical algorithm is imported from the on-disk upstream or candidate source.
"""
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]


def load_source(variant="candidate"):
    source = ROOT / variant / "vesuvius" / "src" / "vesuvius"
    for name in list(sys.modules):
        if name == "vesuvius" or name.startswith("vesuvius."):
            del sys.modules[name]
    package = types.ModuleType("vesuvius")
    package.__path__ = [str(source)]
    sys.modules["vesuvius"] = package
    from vesuvius.tifxyz import read_tifxyz
    return read_tifxyz
