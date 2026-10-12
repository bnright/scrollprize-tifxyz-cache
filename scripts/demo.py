"""Print a minimal, actual real-data before/after cache reproduction."""
import argparse
from contextlib import redirect_stdout
import io
from source_loader import ROOT, load_source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["upstream", "candidate"], required=True)
    args = parser.parse_args()
    read = load_source(args.variant)
    surface = read(ROOT / "private-data" / "PHerc0139-w025-9.362um.tifxyz")
    surface.path = None
    with redirect_stdout(io.StringIO()):
        first = surface.get_patches_3d((128, 128, 128))
        changed = surface.get_patches_3d((256, 256, 256))
        oracle = read(ROOT / "private-data" / "PHerc0139-w025-9.362um.tifxyz")
        oracle.path = None
        expected = oracle.get_patches_3d((256, 256, 256), force_recompute=True)
    print(f"Source: ScrollPrize/villa 25f3c93; variant: {args.variant}", flush=True)
    print("Input: original PHerc0139 w025 mesh, scan 20250728140407, 9.362 um", flush=True)
    print(f"First request 128^3: {len(first)} patches", flush=True)
    print(f"Changed request 256^3: {len(changed)} patches", flush=True)
    print(f"Fresh reference 256^3: {len(expected)} patches", flush=True)
    assert changed == expected, "STALE CACHE: changed request does not match fresh tiling"
    print("PASS: every ordered 2D/3D patch bound equals fresh computation", flush=True)


if __name__ == "__main__":
    main()
