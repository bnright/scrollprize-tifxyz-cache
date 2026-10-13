# October Progress Prize submission draft

Prepared **2026-10-12**. Official destination: [October 2026 Progress Prize form](https://docs.google.com/forms/d/e/1FAIpQLSc4flEfgK2nyjoczz2_U_XrIGMlgrnSknWatLqrFPnbtKfZwg/viewform). Deadline: October 31, 2026, 11:59 pm Pacific. **Draft only; no submission or terms acceptance has occurred.**

## Fields to complete

| Official field | Draft value |
|---|---|
| Email | Supplied privately; omitted from public source. |
| Your full name | Supplied privately; omitted from public source. |
| Team description | Proposed individual entry; **user must confirm actual entrant/team membership.** |
| Optional Discord identifier | Unknown; leave blank unless the user supplies their real display name. |
| Public contribution URL(s) | https://github.com/bnright/scrollprize-tifxyz-cache; reviewed package: https://github.com/bnright/scrollprize-tifxyz-cache/releases/tag/v0.1.0 |
| Contribution narrative | Text below, with evidence links updated to public URLs after approved publication. |
| Terms checkbox | **Unchecked — user must review and authorize agreement/submission.** |

## Contribution narrative

This contribution fixes incorrect cache reuse in `Tifxyz.get_patches_3d`, a public surface-patch preparation API in ScrollPrize/villa. When a researcher changes the desired 3D context size or tiling overlap, the upstream memory cache can silently return the earlier layout. Its disk cache distinguishes size and scale but omits four layout settings. This can invalidate comparisons of training/inference patch settings without an explicit error.

The tested baseline is [villa revision 25f3c93c65b492be3b90e402213a1ba6b5fd624c](https://github.com/ScrollPrize/villa/tree/25f3c93c65b492be3b90e402213a1ba6b5fd624c). The patch makes both caches identify the requested target size, scale, resolution mode, overlap, coarse multiplier, calibration sample count and minimum new coverage. It versions disk keys, rejects ambiguous legacy entries, preserves identical-request reuse and leaves the tiler unchanged. Tuple representations also distinguish NumPy scalar parameters whose short strings can coincide with different Python float values in the tested environment.

Evaluation uses two unchanged publicly released surfaces: **PHerc0139**, segment `20250108000000-w025_2025010863`, mesh on volume `20250728140407` at 9.362 µm; and **PHerc0800**, segment `20251028213516-auto_grown_20251028213516907`, mesh on volume `20250521135224` at 8.64 µm. Provenance manifests record official retrieval URLs, lengths and SHA-256 hashes. Dataset attribution follows the [official data documentation](https://scrollprize.org/data#how-to-cite).

Four request scenarios per surface cover memory target changes, memory overlap changes, disk overlap changes and disk target-change controls. Each runs in three fresh-process repetitions. The candidate matches ordered 2D/3D bounds from forced recomputation in **24/24 replays**, versus **6/24** for upstream; all six upstream passes are the disk-size controls. For example, PHerc0139's 128-to-256 context request returns 215 stale patches upstream; the fresh result and candidate contain 104. An overlap change from 0 to 0.5 returns 62 stale patches upstream versus 261 fresh patches. Initial uncached outputs match before/after, repeat requests hit the cache, and original coordinate hashes remain unchanged.

[Evaluation JSON](https://github.com/bnright/scrollprize-tifxyz-cache/blob/a8df8fd3f933dccdb899a2cce6cb5587a2371e7b/results/evaluation.json) and [replay log](https://github.com/bnright/scrollprize-tifxyz-cache/blob/a8df8fd3f933dccdb899a2cce6cb5587a2371e7b/evidence/real-data-evaluation.txt) provide commands, settings, counts and exact-output hashes. **75 relevant tests pass**, including 20 cache checks; unchanged upstream fails 14 of those 20 cache checks. The [patch](https://github.com/bnright/scrollprize-tifxyz-cache/blob/a8df8fd3f933dccdb899a2cce6cb5587a2371e7b/upstream-fix.patch) and reproduction scripts make the result reviewable.

This enables correct repeated exploration of patch contexts and coverage settings while retaining caching. Evidence establishes this bounded correctness improvement; adoption, downstream ink-reading gains and new text discoveries have not been measured. Three repetitions test reproducibility, not 24 independent datasets. Remaining cache limitations include geometry/mask mutation, concurrent writes and malformed cache data.

**AI disclosure:** Codex assisted research, implementation, tests, evaluation and drafting. Human entrant identity was supplied privately. Personal code/evidence review and genuinely human-written upstream relevance commentary remain pending. Generic software and nontextual evidence have been published with approval; source dataset files remain excluded. Award eligibility and significance remain subject to organizer review.
