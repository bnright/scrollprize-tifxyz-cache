# Selection and success criteria

Decision made 2026-10-12, before comparative evaluation of the candidate fix.

Selected opportunity: October 2026 ScrollPrize Progress Prizes, deadline October
31, 11:59 pm Pacific. This is discretionary cash recognition for useful open
source contributions; neither a prize nor a particular award tier is assured.

Problem: while preparing real scroll surfaces for different model context sizes
and overlap settings, `Tifxyz.get_patches_3d` can silently return the earlier
layout. Its memory cache does not check any request parameter; its disk cache
omits four layout parameters. A researcher comparing training patch sizes or
coverage settings needs the layout actually requested, with traceability to the
original mesh and scan.

Baseline: unchanged ScrollPrize/villa revision
`25f3c93c65b492be3b90e402213a1ba6b5fd624c`. The official hierarchical tiler remains
unchanged. Existing workaround: `force_recompute=True`, which defeats caching
and requires callers to know that cache reuse is unsafe.

Contribution: a small upstream-compatible fix identifying both caches by target
size, scale, resolution mode, overlap, coarse multiplier, calibration count and minimum new
coverage, plus versioning to avoid trusting ambiguous old disk entries. An
independent real-data replay and regression tests make the fix reviewable.

Success criteria: on two original published meshes, each changed request must
exactly equal a fresh `force_recompute=True` result, including ordered 2D/3D
bounds; identical requests must still hit the cache; changed parameters must
invalidate both caches; old disk keys must be ignored. Original coordinate files
must retain their hashes. A successful first request must remain numerically
identical before and after. Runtime and peak resident memory will be recorded as
context, without presenting a cache hit returning wrong results as a speedup.

Validation: run unmodified and patched official tifxyz readers/tilers in separate
processes on the same real meshes and compare target changes and overlap changes
against uncached upstream outputs. Use small synthetic unit cases only to verify
cache invalidation for every parameter. These tests supplement real-data
usefulness evidence and do not substitute for it.

Prior art: checked the official help-wanted wishlist, current issues/PRs and
recent merges. Rejected robust-normalization #1481 because competing real-data
fixes already exist; rejected plain-Zarr patch-scaling #1970 because #1980 is
open. No matching `get_patches_3d` cache fix was found on October 12. This is a
bounded search result, not proof of worldwide novelty.

Uncertainties: no researcher adoption yet; the method's documented API is
available, but active downstream users have not been confirmed. This is a
correctness contribution rather than a new tiling algorithm or validated ink
model improvement. The organizer decides whether this scope merits a prize.
AI-assisted preparation must be disclosed; an upstream PR still needs human
review and human-written relevance commentary under CONTRIBUTING.md. Personal
cash payability and the scope of the separate data agreement remain unconfirmed.
Only code and retrieval instructions will be packaged for publication; source
meshes remain private local research copies.

## Opportunity comparison

| Opportunity | Eligibility/cash now | Need and competing approaches | Feasibility, measurable evidence, time/cost | Decision |
|---|---|---|---|---|
| ScrollPrize Progress Prizes | Open monthly; new individuals welcomed; $20,000 best monthly plus discretionary tiers | Reliable scroll tooling; exact cache correctness gap survives main; no matching fix found | CPU, two small real meshes, exact fresh-result oracle, hours of local work, $0 purchased compute | Selected |
| ScrollPrize First Letters | Open until June 25, 2027; $50,000 per eligible unread scroll | Genuine scan-backed letters; mature ML/segmentation pipelines and well-funded competitors | A new qualifying discovery cannot credibly be evaluated in this small local build; data/model/GPU needs much greater; no feasible success metric in session | Rejected for this build |
| AIcrowd ARC Phase 2 | New registration froze October 2, 2026; submissions continue to October 17 | Efficient white-box estimation; public starter and strong leaderboard | CPU evaluation possible but new entry ineligible, so effort cannot reach place/algorithmic cash | Rejected |
| AIcrowd Global Chess | Cash round closed January 31, 2026; historical $17k cash distinct from $8k credits | Language-model chess; established submitted systems | No current cash route; large language-model training inappropriate for disk budget | Rejected |

Sources and rule details: `docs/scroll-rules.md`, `docs/aicrowd-rules.md`.
