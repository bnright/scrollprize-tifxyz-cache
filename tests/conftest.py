import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from source_loader import load_source

load_source(os.environ.get("TIFXYZ_SOURCE_VARIANT", "candidate"))
