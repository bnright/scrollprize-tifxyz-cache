# Independent final review

Reviewed locally on 2026-10-12. This review does not authorize publication, submission, account registration, or acceptance of legal terms.

## Code and evidence

No blocking implementation finding identified in the final candidate. The patch is limited to cache identity and adds focused regressions. It keys memory and disk caches by target dimensions, scale, resolution mode, and all four numerical layout controls. The new field follows the existing dataclass fields, preserving the old positional argument order. Versioned keys prevent reuse of ambiguous legacy entries. Geometry, interpolation, and tiling algorithms are unchanged.

The source loader provides only the `vesuvius` parent namespace and imports the actual source subpackage. It does not mock readers, interpolation, or the numerical tiler during the real-data evaluation. This focused harness bypasses unrelated top-level package initialization; it does not demonstrate a complete ML/monorepo installation. Mocked tilers are confined to unit tests and are labeled as such.

Inspected the recorded evaluation and its implementation. Each candidate result is compared exactly, including order and every returned 2D/3D bound, to a separate uncached calculation. Both versions' initial-request hashes and fresh-calculation hashes also match. Original inputs are rehashed before and after. Corrected results pass 24/24 scenarios/repetitions; baseline passes only the six disk-target controls and fails the 18 intended defect cases. Baseline cache-contract tests fail 14 cases and pass six controls; final candidate test evidence records 75 passing tests, including 20 new regressions and 55 selected upstream tests. These are bounded test and real-surface results, not model accuracy or the full upstream test suite.

Independently executed the strengthened source verification: all 22 pinned official source files match their lengths, SHA-256 fingerprints and Git blob SHA-1 values. Independently compared all 22 manifest paths/blob identities with the official pinned GitHub tree: zero mismatches. Generated test metadata are excluded from this official-source manifest. Independently executed patch verification: clean application to the snapshot, and resulting implementation/tests byte-identical to evaluated files.

## Freshness and claims

Independently rechecked the official GitHub API during this review. Main remains `25f3c93c65b492be3b90e402213a1ba6b5fd624c`; `types.py` blob remains `b7c9628f4d2a685629108a578163530f46034b93`. Search for `get_patches_3d` finds no issue/PR; `patches_cache` finds only unrelated closed #802; `cache tiling` finds only unrelated closed #1104. This establishes a bounded current search, not global novelty.

Supported claim: supported changed requests no longer silently reuse an incompatible cached layout on the evaluated complete PHerc0139 and PHerc0800 meshes. Unsupported claims deliberately excluded: ink discovery, improved model quality, speedup, adoption, confirmed active downstream use of this method, organizer endorsement, and prize winnings. A wrong baseline cache hit must never be described as a meaningful faster baseline. Runtime and whole-process peak memory are context only.

The patch still does not invalidate caches after arbitrary coordinate/mask or returned-list mutation; it does not address disk concurrency/corruption, tiling quality, or full-resolution numerical tiling support. Human review and human-written relevance commentary remain upstream requirements. Dataset-agreement scope and personal cash payability remain outside this technical review.

## Documentation corrections checked

During review, three preparation errors were reported to the parent agent: attribution named `reader.py` rather than `types.py`; README understated input bytes; plotting dependency `matplotlib` was absent from the initial lock. The parent corrected those items, included resolution in the final change description, and marked earlier 16-test scouting notes as intermediate. The input manifests sum to 1,631,776 bytes.

## Release audit

The release allowlist in `scripts/package_release.py` restricts included directories and extensions, names the two result reports explicitly, excludes data/environment/cache/Git paths, checks ZIP integrity, and verifies every bundled file against its SHA-256 manifest. Its result files contain aggregate settings, counts, hashes and timing summaries rather than complete output bounds or source coordinates.

Independently audited the completed `release/scrollprize-tifxyz-cache-2026-10-12.zip` including the technical report: **PASS**. Exact member names equal the manifest inventory; all file hashes and ZIP CRCs pass. No forbidden data/environment/cache/Git paths, TIFF signatures, complete bounds/coordinate fields in result reports, or tested credential patterns were found. Image evidence consists of the captured-output rendering and aggregate patch-count plot. This is a bounded content audit, not a guarantee that every possible sensitive string has been detected.

Inspected the completed extraction check: a newly extracted source tree and newly fetched anonymous S3 inputs passed strengthened official-source verification, clean patch application, all 75 selected tests, and the actual candidate real-surface demonstration. It used the same already-installed Python runtime and dependency lock; this does not claim a clean operating-system or newly installed dependency test. The checked archive's source code is identical to the final release source; the last review-document update requires only a documentation rebuild. The packager records and verifies the final archive's exact size, SHA-256 and inventory separately, avoiding a self-referential hash in this document.

Original coordinates, complete bounds arrays, TIFF/mesh metadata, `private-data`, `results/work`, caches, `.venv`, `.git`, and credentials remain excluded. User approval and unresolved external-action requirements remain separate from passing the package audit.
