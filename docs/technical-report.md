# Correct request identity for TIFXYZ patch caches

Prepared October 12, 2026 for the ScrollPrize October Progress Prize round.

## Result and researcher benefit

This contribution fixes reproducible stale-layout reuse in `Tifxyz.get_patches_3d`. On two published scroll meshes, the unmodified source returned the wrong ordered patch bounds for **18 of 24** evaluated changed requests. The candidate matched fresh computation for **24 of 24**, retained identical-request cache hits, and preserved all eight downloaded source-file hashes. The combined candidate regression suite passed **75 tests**.

A researcher varying 3D model context or overlap needs the layout requested by the current experiment. Previously, reusing a TIFXYZ object could silently retain an earlier target or overlap, and reopening it could retain an overlap layout from disk. The fix permits parameter changes with normal caching rather than requiring the researcher to discover the problem and force every computation. It establishes cache correctness for the evaluated requests; no downstream ink-reading improvement or researcher adoption is claimed.

## Baseline, change and success criteria

The unchanged baseline is [ScrollPrize/villa](https://github.com/ScrollPrize/villa) revision `25f3c93c65b492be3b90e402213a1ba6b5fd624c`. The [source manifest](source-manifest.json) records original URLs and SHA-256 fingerprints. The final upstream recheck found the same current main revision and unchanged `types.py` blob; see [upstream recheck](upstream-final-recheck.json).

The old memory lookup returned `_patches_cache` without checking the request. Its disk key encoded target dimensions and scale but omitted overlap, coarse multiplier, calibration count and minimum new coverage. The [reviewable patch](../upstream-fix.patch) changes only cache bookkeeping in `vesuvius/src/vesuvius/tifxyz/types.py` and adds cache-contract regression tests. It gives both caches a versioned identity containing target size, scale, resolution mode, and every layout parameter, and records that identity on disk loads and fresh computations. Old ambiguous keys are ignored. Appending the dataclass field preserves existing positional argument locations.

The final key uses typed `repr` values. Python `0.9` and NumPy `float32(0.9)` can share a short string representation while differing numerically; the final regressions check both memory and disk separation. Resolution mode is included in cache identity, but its test replaces the tiler and establishes invalidation only. It does not establish numerical full-resolution tiling support. `verbose` does not affect identity; `force_recompute=True` still bypasses caches. The numerical hierarchical tiler is unchanged.

The [selection brief](selection-brief.md) recorded the success criteria before comparative evaluation: exact ordered 2D/3D bounds versus fresh computation, identical-request reuse, invalidation of changed parameters and legacy entries, unchanged first-request results, and unchanged original data hashes. Timing and peak memory were to be recorded as context, without claiming that stale cache results represent useful speed.

## Data and equivalent-condition evaluation

The input examples are original TIFXYZ meshes from newer Vesuvius Challenge scans:

| Sample | Scan/mesh provenance | Stored mesh shape | Valid vertices |
|---|---|---:|---:|
| PHerc0139 | [w025 provenance](PHerc0139-w025-provenance.json), 9.362 µm scan `20250728140407` | 364 × 340 | 102,285 |
| PHerc0800 | [auto-grown provenance](PHerc0800-auto-grown-provenance.json), 8.64 µm scan `20250521135224` | 108 × 112 | 5,998 |

The eight input files total 1,631,776 bytes. Each manifest includes exact official URLs, sizes and hashes. The source data are retained privately; the release supplies retrieval instructions and fingerprints rather than redistributing coordinates. [Attribution](attribution.md) provides the official newer-scan bibliography and separates MIT software from dataset licensing. The work reads surfaces and emits aggregate cache evidence; it does not infer ink or generate letters.

`scripts/evaluate.py` ran three repetitions per variant, each in a separate Python process, alternating source order between repetitions. Each worker first warmed JIT kernels on actual PHerc0139 data; this initial warmup is recorded separately and excluded from request timings. It used the same source meshes and request settings for both variants, with caches written only to isolated `results/work/` directories. A newly read surface with `force_recompute=True` and no persistence served as the fresh-computation oracle. Comparisons checked the entire ordered patch list, including 2D and 3D bounds; JSON digests retain that result without publishing the coordinates.

PHerc0139 used target cubes 128→256; PHerc0800 used 64→128. Overlap cases held the larger target constant and changed overlap 0→0.5. Memory cases retained the object; disk cases reopened it after the initial request. The disk target change was a control: the old disk key already distinguished target dimensions.

## Quantitative correctness results

Counts are identical across all three repetitions. “Unexpected/missing” counts compare complete patch-bound tuples against the fresh oracle, rather than estimating uncovered scan volume. Candidate unexpected/missing counts were zero in every row.

| Mesh | Case | Upstream patches → candidate | Fresh oracle | Upstream unexpected / missing | Exact matches upstream → candidate |
|---|---|---:|---:|---:|---:|
| PHerc0139 | Memory, target change | 215 → 104 | 104 | 215 / 104 | 0/3 → 3/3 |
| PHerc0139 | Memory, overlap change | 62 → 261 | 261 | 4 / 203 | 0/3 → 3/3 |
| PHerc0139 | Disk, overlap change | 62 → 261 | 261 | 4 / 203 | 0/3 → 3/3 |
| PHerc0139 | Disk, target control | 104 → 104 | 104 | 0 / 0 | 3/3 → 3/3 |
| PHerc0800 | Memory, target change | 52 → 4 | 4 | 52 / 4 | 0/3 → 3/3 |
| PHerc0800 | Memory, overlap change | 6 → 8 | 8 | 0 / 2 | 0/3 → 3/3 |
| PHerc0800 | Disk, overlap change | 6 → 8 | 8 | 0 / 2 | 0/3 → 3/3 |
| PHerc0800 | Disk, target control | 4 → 4 | 4 | 0 / 0 | 3/3 → 3/3 |

The machine-readable [final evaluation](../results/evaluation.json) records every repetition. All six assertions passed: candidate matches fresh, candidate repeated requests reuse the same result object, the baseline defect reproduces, fresh oracle outputs agree across source variants, the initial-request output fingerprints agree, and original data fingerprints remain unchanged. Thus the candidate corrects request-dependent reuse while preserving the tested fresh numerical outputs.

## Runtime and peak memory

The [hardware record](hardware.json) identifies an Intel Core Ultra 9 185H, 16 physical cores/22 logical processors and 33.78 GB RAM, on Windows 11. Evaluation used Python 3.14.6 and CPU execution only; installed GPU devices were unused. Purchased compute cost was $0. [Dependency versions](../requirements-lock.txt) include NumPy 2.5.4, SciPy 1.18.1 and Numba 0.68.0.

Changed-request elapsed time in **milliseconds**, median [minimum–maximum], across three repetitions:

| Mesh | Case | Upstream | Candidate |
|---|---|---:|---:|
| PHerc0139 | Memory, target change | 0.0171 [0.0161–0.0358] † | 51.1352 [49.9265–56.7529] |
| PHerc0139 | Memory, overlap change | 0.0229 [0.0167–0.0727] † | 105.0170 [97.6693–113.8709] |
| PHerc0139 | Disk, overlap change | 19.3386 [15.2288–21.1079] † | 127.9436 [119.4816–132.0653] |
| PHerc0139 | Disk, target control | 73.5008 [73.1828–78.2754] | 84.6360 [72.4154–85.3819] |
| PHerc0800 | Memory, target change | 0.0111 [0.0102–0.0113] † | 7.2307 [7.1158–7.6391] |
| PHerc0800 | Memory, overlap change | 0.0191 [0.0107–0.0205] † | 7.3838 [7.1911–8.1769] |
| PHerc0800 | Disk, overlap change | 1.4688 [1.1823–11.7488] † | 11.7090 [10.2969–15.9310] |
| PHerc0800 | Disk, target control | 27.1013 [17.0284–28.2644] | 25.4223 [24.6034–27.0319] |

† These upstream requests returned incorrect cached layouts. Their lower latency cannot be counted as a successful performance advantage. Correct invalidation requires fresh work. The correct disk controls show ordinary variation; three small local repetitions do not establish a speed improvement or regression. This is a correctness contribution.

Across 24 correct candidate repeated-request hits, latency was median **23.65 µs**, range **13.40–29.20 µs**. This supports retained cache reuse; it is not a comparison with the baseline's wrong-result hit timings.

Peak process resident memory includes imports, JIT warmup, both meshes and all cases within a worker. With decimal MB (1 MB = 1,000,000 bytes), upstream median was **181.875 MB** [181.826–182.231]; candidate median was **181.391 MB** [181.035–181.920]. These similar ~182 MB process peaks do not establish a memory reduction or a bound for larger meshes.

## Regression tests and development record

The final cache-contract suite has 20 cases. On unchanged upstream it produced **14 expected failures and 6 passes**; the [baseline log](../evidence/baseline-regressions.txt) identifies failures for changed request identity, legacy entries, scalar representation and resolution mode. The combined candidate run passed **75/75 in 5.47 seconds**, including cache regressions and relevant existing TIFXYZ shape/interpolation/reader/label tests; see [candidate test log](../evidence/candidate-tests.txt). Mocked-tiler regressions isolate cache behavior, while the real-mesh evaluation provides the separate numerical usefulness evidence.

Earlier tests had 16 cache cases, with 10 baseline failures/6 passes and 16 candidate passes. That [intermediate contract record](../evidence/unit-cache-contract.txt) is retained as development history; it is superseded by the final 20-case suite. One selected upstream integration test initially failed because the focused source snapshot lacked `tifxyz_label_transfer/core.py`. Adding that original pinned module, rather than modifying its behavior, resolved the failure. The manifest records the added source. A release audit also caught generated pytest cache metadata in the first source manifest; those entries were excluded, and all 22 remaining files were matched against the official pinned Git-tree blob IDs before archive extraction checks.

The first patch-application check encountered Windows Git line-ending conversion. The verifier now sets `core.autocrlf=false` in its temporary checkout, applies the patch, and compares the resulting implementation and tests byte for byte with evaluated files. It does not require changing user-wide Git settings.

An initial PHerc0800 target trial used 128→256. Fresh computation produced zero patches for the larger request; the candidate correctly returned zero, but an empty result was less useful for demonstrating a researcher changing context. The [exploratory evaluation](../results/evaluation-exploratory.json) is retained rather than discarded. The final replay reduced that sample's target to 64→128, yielding four oracle patches, while preserving the same correctness criterion and overlap/control checks. No measured failure was converted into an invented improvement.

## Reproduction

From the project root, use the pinned environment and scripts described in the repository README. The substantive checks are:

```powershell
.venv\Scripts\python.exe scripts\verify_sources.py
.venv\Scripts\python.exe scripts\verify_patch.py
.venv\Scripts\python.exe scripts\fetch_inputs.py
.venv\Scripts\python.exe -m pytest -q tests upstream\vesuvius\tests\tifxyz candidate\vesuvius\src\vesuvius\tifxyz\test_reader_bbox.py candidate\vesuvius\src\vesuvius\tifxyz\test_labels.py
.venv\Scripts\python.exe scripts\evaluate.py --repetitions 3
```

The fetch script verifies existing copies or retrieves only the eight small original files. Review applicable data terms before retrieval. `TIFXYZ_SOURCE_VARIANT=upstream` selects the unchanged snapshot for the cache regression comparison; those baseline failures are expected. Source loading supplies only the parent namespace to import the actual focused official TIFXYZ modules, avoiding unrelated ML/volume package initialization. It does not replace the reader or tiler algorithm. Output evidence, hashes and full timings are retained in `results/evaluation.json` and `evidence/`.

## Limits and prize readiness

Only two small real meshes, target changes and overlap changes received numerical replay. Other key fields are covered by cache-contract tests. This is not full-package installation/CI certification, GPU execution, a trained model experiment, full-scroll unrolling, or end-to-end text recovery. Full-resolution numerical tiling support is not claimed. Existing limitations around mutable geometry/masks, mutation of returned cached lists, malformed cache contents, concurrent writers and persistence errors remain outside this change. The versioned key safely declines old results but can leave legacy entries in the existing disk-cache file.

No community adoption, upstream acceptance, or human-written relevance review has happened. Those remain useful next evidence, and an upstream AI-assisted PR requires the human steps documented in [submission requirements](submission-requirements.md). [Final prize recheck](rules-final-recheck.md) confirms the October 31, 2026, 11:59 pm Pacific deadline. Actual award suitability, lawful personal payability, and the scope of anonymous-access data terms remain subject to organizer review/clarification. The completed technical evidence supports a reviewable entry; it does not promise a prize. Publication, organizer contact, terms acceptance, and final submission remain pending the user's approval.
