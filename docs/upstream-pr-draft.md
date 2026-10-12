# Draft PR: Make Tifxyz patch caches distinguish layout requests

**Status:** Prepared locally only. No upstream PR has been opened. The human verification checkbox and required human-written relevance commentary below remain incomplete.

**In one sentence:** Researchers can change the context size or tiling settings of a surface-patch request and receive the requested layout while retaining identical-request caching.

**One real example:** An automated replay loaded the official PHerc0139 surface `20250108000000-w025_2025010863`, requested a 128³ context, then changed to 256³. The patched API returned the same 104 ordered patches as a fresh 256³ computation.

**Before:** The same memory sequence returned the earlier 215-patch layout. On a 256³ overlap change from 0 to 0.5, memory and disk reuse returned 62 earlier patches instead of the fresh 261-patch layout.

**After this PR:** Memory and disk keys include the target size, scale, resolution mode and all four computational tiling settings. Old keys lacking those settings are ignored. Repeated identical requests reuse their result. Tiling calculations and initial uncached outputs are unchanged.

**Proof:** [Real-data replay log](../evidence/real-data-evaluation.txt) and [evaluation JSON](../results/evaluation.json). Two published surfaces, four scenarios each, three process repetitions: candidate 24/24 exact fresh-result matches; baseline 6/24, all in disk target-size controls. Inspect ordered-bound hashes as well as patch counts. [Candidate tests](../evidence/candidate-tests.txt) report 75 passes; the [baseline cache checks](../evidence/baseline-regressions.txt) reproduce 14 failures out of 20. **Attach actual terminal screenshots of baseline failure and candidate success before opening a bugfix PR**, as required by CONTRIBUTING.md; text logs alone do not satisfy that screenshot requirement.

**Why / where this is useful:** Users preparing patches from published scroll surfaces can compare context and coverage settings reliably. The previous workaround was forcing recomputation on every request. No adoption or downstream ink-reading improvement is claimed.

- [ ] I personally verified that the example and proof above were produced by this PR on the stated data.

## Required human-written relevance commentary

**Not written yet.** The submitting human must explain, in their own words, their actual scroll-data workflow, why this issue mattered, and what they personally reviewed or ran. Do not paste an AI-written paragraph here and label it human-written. Do not claim the human used the tool merely because the assistant executed the replay.

## Details

Tested upstream revision: `25f3c93c65b492be3b90e402213a1ba6b5fd624c`.

Changes are limited to the cache-identity field and `get_patches_3d`, plus cache regression coverage. A schema-prefixed tuple representation avoids legacy entries and distinguishes tested NumPy/Python scalar representations. The new field is appended, preserving prior positional constructor argument locations. `verbose` does not affect layout identity; `force_recompute` bypasses both caches.

Inputs are the original PHerc0139 9.362 µm and PHerc0800 8.64 µm published TIFXYZ surfaces. Their [PHerc0139](PHerc0139-w025-provenance.json) and [PHerc0800](PHerc0800-auto-grown-provenance.json) manifests contain exact segment/volume IDs, official URLs and file hashes. Downloaded meshes are excluded from the release package. Cite *Vesuvius Challenge - CT Scans of Herculaneum Papyri* according to the [official dataset citation](https://scrollprize.org/data#how-to-cite).

From the package root, using the prepared environment:

```powershell
.\.venv\Scripts\python.exe scripts\verify_sources.py
.\.venv\Scripts\python.exe scripts\verify_patch.py
.\.venv\Scripts\python.exe scripts\evaluate.py --repetitions 3
.\.venv\Scripts\python.exe -m pytest tests candidate\vesuvius\tests\tifxyz candidate\vesuvius\src\vesuvius\tifxyz\test_reader_bbox.py candidate\vesuvius\src\vesuvius\tifxyz\test_labels.py -q
```

Use `scripts/fetch_inputs.py` to retrieve and verify original inputs when they are not already present. Inspect the data terms and provenance before downloading; the script makes no account registration or form submission. Locked dependencies are in `requirements-lock.txt`. The replay loads the real reader/tiler source through a minimal parent namespace to avoid unrelated ML initialization; it is not a full installed-package integration run.

Limits: measured on Windows with the pinned environment; Ubuntu/macOS were not run. Resolution-key tests establish invalidation, not full-resolution tiler support. Mutation of coordinates/masks or returned lists, disk concurrency, malformed cache entries and write failures remain outside this fix. Numeric scalar representation tests were run with NumPy 2.5.4. A correct changed request must recompute, so a fast stale cache hit is not a valid performance baseline.

**AI assistance:** Codex prepared the patch, reproduction, tests and this draft. Human review, personal verification and human-written commentary are required before submission under the [upstream AI contribution guidelines](https://github.com/ScrollPrize/villa/blob/main/CONTRIBUTING.md#ai-guidelines).
