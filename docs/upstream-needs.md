Final outcome: the selected cache defect was reproduced on two real meshes and fixed. The final suite has 20 cache tests (upstream 14 failed / 6 passed) and 75 total candidate tests passing. Real evaluation: candidate 24/24 exact matches, upstream 6/24 controls. The scouting notes below describe intermediate hypotheses and the earlier 16-test suite. See technical-report.md for final evidence.

# Upstream need assessment

Verified 2026-10-12 against official public sources. This is a local research record, not a public submission or evidence of organizer endorsement.

## Selected contribution

Correct `Tifxyz.get_patches_3d()` cache identity in `vesuvius/src/vesuvius/tifxyz/types.py` at official main revision `25f3c93c65b492be3b90e402213a1ba6b5fd624c`.

Intended task: inspect real scroll surfaces while comparing 3D patch sizes and tiling overlap, so each requested model context receives its own tiling. The public method accepts `target_size`, `overlap_fraction`, `coarse_multiplier`, `num_calibration_samples`, and `min_new_coverage`.

The in-memory cache currently returns the first non-null cached result without checking any request parameter. Its disk key contains target size and scale but omits the four other layout parameters. Consequently, supported repeated requests can silently reuse patch bounds created for a different request. A small fix should key both caches on the complete request and avoid trusting legacy incomplete disk keys.

Source: [types.py at verified revision](https://github.com/ScrollPrize/villa/blob/25f3c93c65b492be3b90e402213a1ba6b5fd624c/vesuvius/src/vesuvius/tifxyz/types.py#L1107). Algorithm: [hierarchical_tiling.py](https://github.com/ScrollPrize/villa/blob/25f3c93c65b492be3b90e402213a1ba6b5fd624c/vesuvius/src/vesuvius/tifxyz/hierarchical_tiling.py).

This is a code-derived hypothesis until the real-data baseline finishes. Define success as exact equality between each cached result and an uncached computation with identical parameters, while identical repeated requests still reuse their result. No ink-reading or model-quality improvement is claimed.

Independent cache-contract tests completed: the untouched upstream fails 10 of 16 tests, while the candidate passes all 16. Failures match the five unkeyed memory parameters, four omitted disk parameters, and acceptance of an incomplete legacy identity. Tests mock the tiler to isolate cache behavior; the parent task evaluates the complete real-surface algorithm separately. Exact commands and results are in `scrollprize-entry/evidence/unit-cache-contract.txt`.

## Current relevance and competing work

The official wishlist is now [Open Problems](https://scrollprize.org/2026_open_problems), updated July 10, 2026. It identifies reliable surface geometry, damaged/compressed regions, and traceable inspection as continuing needs. `Tifxyz` is explicitly described as the Python representation of surfaces in the current pipeline.

The types module changed September 18, 2026 in [#1699](https://github.com/ScrollPrize/villa/pull/1699); its interpolation utility was corrected on the verification date in [#1923](https://github.com/ScrollPrize/villa/pull/1923). The wider tifxyz representation is active. **No in-repository caller of `get_patches_3d` was found in the checked `vesuvius` sparse source.** The function's availability and surrounding active format are evidence of potential utility, not evidence that researchers currently use this specific cache API. Organizer interest and adoption remain uncertain.

Official GitHub issue/PR search at verification time:

- `get_patches_3d`: zero results.
- `patches_cache`: one result, [#802](https://github.com/ScrollPrize/villa/pull/802), unrelated training/runtime changes; its file list does not touch `tifxyz/types.py`.
- `hierarchical tiling`: [#1478](https://github.com/ScrollPrize/villa/pull/1478), a different binary-search defect, and [#666](https://github.com/ScrollPrize/villa/pull/666), the original tiling implementation.

This bounded search found no matching proposed fix; it does not establish global novelty.

## Rejected alternatives

1. [#1481](https://github.com/ScrollPrize/villa/issues/1481), robust normalization after depth/spatial padding, remains present but duplicates existing implementations [#1483](https://github.com/ScrollPrize/villa/pull/1483), [#1646](https://github.com/ScrollPrize/villa/pull/1646), and [#1773](https://github.com/ScrollPrize/villa/pull/1773). The last author's real-data survey found ordinary inference on all 340 checked eligible meshes did not trigger padding. Reimplementing it has weak novelty and demonstrated default impact.
2. [#1970](https://github.com/ScrollPrize/villa/issues/1970), wrong patch coordinates on plain Zarr arrays, has an open fix [#1980](https://github.com/ScrollPrize/villa/pull/1980).
3. [#1586](https://github.com/ScrollPrize/villa/issues/1586), persistent cache disk budget roughly doubled, already documents a ready fix and real-scroll results. It also requires considerably more dependency setup than this surface-only contribution.

## Real evaluation inputs

Downloaded anonymously from the official open-data S3 bucket into private local data, without redistributing them:

- `PHerc0139/segments/20250108000000-w025_2025010863/mesh/20250108000000-on-20250728140407-9.362um.tifxyz/`: complete metadata and x/y/z TIFFs, 1,485,937 bytes total.
- `PHerc0800/segments/20251028213516-auto_grown_20251028213516907/mesh/20251028213516-on-20250521135224-8.64um.tifxyz/`: complete metadata and x/y/z TIFFs, 145,839 bytes total.

Per-file source URLs, bytes, and SHA-256 hashes are recorded under `scrollprize-entry/private-data/*-provenance.json`. Both retain original voxel coordinates and scale; no letters or scan signal were created. [Official data page](https://scrollprize.org/data), [linked data license](https://dl.ash2txt.org/LICENSE.txt). Follow the parent task's licensing review before redistribution or publication.

Suggested real test: compute target `(64,64,64)` and then `(128,128,128)` on one instance and compare the second call with `force_recompute=True` or a fresh cache-free instance. Separately keep target size constant and change overlap `0.25` to `0.5` across fresh instances sharing a copied mesh directory, demonstrating the disk-key defect. Evaluate both complete surfaces; a documented exact crop is an acceptable fallback if tiling is unexpectedly expensive.

## Contribution conventions and limits

Root code is [MIT licensed](https://github.com/ScrollPrize/villa/blob/main/LICENSE). [CONTRIBUTING.md](https://github.com/ScrollPrize/villa/blob/main/CONTRIBUTING.md) welcomes LLM assistance but requires a real scroll-data task, before/after evidence, concise motivation, human-written relevance commentary, and human review. Synthetic unit regressions support the change; they do not substitute for the real-surface pipeline demonstration. Follow the [PR template](https://github.com/ScrollPrize/villa/blob/main/.github/pull_request_template.md).

The change does not fix stale caches after coordinate files or mutable geometry are modified under the same path. Explicit recomputation remains necessary for such changes unless geometry fingerprinting is separately implemented and evaluated. Prize suitability is discretionary and should not be inferred from technical correctness alone.
