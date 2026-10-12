"""First real-data baseline; no coordinate modification or model inference."""
from source_loader import ROOT, load_source
import time
import json

read = load_source("upstream")
surface = read(ROOT / "private-data" / "PHerc0139-w025-9.362um.tifxyz")
surface.path = None  # Keep downloaded official dataset read-only; memory probe.
print("Stored shape", surface.shape, "valid vertices", surface._valid_mask.sum(), flush=True)
started = time.perf_counter()
first = surface.get_patches_3d((128, 128, 128))
print("First request", len(first), "patches in", time.perf_counter()-started, flush=True)
changed = surface.get_patches_3d((256, 256, 256))
print("Changed request", len(changed), "patches; reused same object:", changed is first, flush=True)
started = time.perf_counter()
expected = surface.get_patches_3d((256, 256, 256), force_recompute=True)
print("Forced request", len(expected), "patches in", time.perf_counter()-started, flush=True)
print(json.dumps({"first_count":len(first), "changed_count":len(changed), "fresh_count":len(expected), "matches_fresh": changed == expected}))
