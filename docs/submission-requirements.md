# Submission requirements and human review

Prepared on **2026-10-12** for the October 2026 ScrollPrize Progress Prize round. This file maps the actual official form and records remaining submission requirements. It does not submit a form, accept legal terms, publish a repository, or send a message.

## Official submission route

[October Progress Prize form](https://docs.google.com/forms/d/e/1FAIpQLSc4flEfgK2nyjoczz2_U_XrIGMlgrnSknWatLqrFPnbtKfZwg/viewform), linked from the [live rules](https://scrollprize.org/prizes#progress-prizes). Deadline: **October 31, 2026, 11:59 pm Pacific**. Recheck the live rules and form immediately before submission.

Field order below is the form's actual order. Short labels identify the corresponding visible field; explanatory cells paraphrase the instructions. The completed contribution narrative is in `submission.md`.

| Order | Form field | Required | Proposed mapping / current status |
|---|---|---|---|
| 1 | Email | Yes | **Missing:** user's chosen submission email. Do not infer it from the computer account or enter an invented address. The form records the submitter's email and emails a response copy. |
| 2 | Your full name | Yes | **Missing:** user's actual full name as they wish to submit. The Windows account name is not sufficient. |
| 3 | Team description | Yes | Proposed route: individual. State the actual human entrant(s); if a team, identify every member and have its leader submit. **Pending user confirmation** of individual/team status and any real collaborators. AI assistance belongs in attribution, not an invented human teammate. |
| 4 | Optional Discord identifier | No | **Unknown:** use the user's real display name if already a server member; otherwise leave blank. This form does not make Discord membership compulsory. Grand Prize membership rules should not be imported into this field. |
| 5 | Public contribution URL(s) | Yes | **Pending publication approval and actual URL:** accessible repository or PR containing the patch, reproduction instructions, evidence and license. The form accepts more than one URL. A local filesystem path cannot satisfy this field. |
| 6 | Contribution narrative | Yes | Completed text is in `submission.md`. It must identify the exact scroll data; explain how the change helps someone read scrolls; state the previously unavailable capability; link concrete evidence. Bound claims to verified cache correctness, not ink detection gains, new letters, or an assured prize. |
| 7 | Terms checkbox | Yes | **Pending human review and explicit permission:** the form requires agreement to its prize terms. Never tick or submit it on the user's behalf before the user's authorized review step. |

The form allows individuals and teams. Its public-contribution URL field should be satisfied before submission even though the general prize terms allow open-sourcing by award acceptance. The current text of the form and rules controls.

## Remaining personal and eligibility information

- The submission email and full name are mandatory and have not been supplied.
- Confirm the entrant is an individual, or record team membership and its leader accurately.
- Confirm lawful prize payability. The [official FAQ](https://scrollprize.org/faq) supports international entrants if payment is legally permitted and excludes current organizer employees/team members. Residence, sanctions eligibility and organizer affiliation have not been established from the user's timezone or local account.
- If registering for the separate data/Discord agreement, every actual team member must individually agree. No registration or agreement acceptance is assumed.
- Payment information is required only if awarded, within 30 days of announcement. It is not a field to invent or collect in this project now.

Cash and prize tiers are discretionary. These checks establish a plausible route to entry; they do not prove a payout or organizer acceptance of this particular contribution.

## Human review required for an upstream PR

The [official CONTRIBUTING guidelines](https://github.com/ScrollPrize/villa/blob/main/CONTRIBUTING.md#ai-guidelines) allow LLM coding assistance but require an LLM-generated upstream PR to include **human-written relevance commentary**, follow actual human interaction with the codebase for scroll-data work, and undergo human code review. Real-data usefulness evidence is required; synthetic cache tests alone do not qualify. Relevant fixes need direct before/after evidence, and a bugfix PR needs screenshots of the error and successful tool execution.

Before an upstream PR:

- The user reviews the small source diff for simplicity and accuracy.
- The user runs or personally examines the real-scroll reproduction and confirms what workflow they were trying to accomplish. Do not claim the user has already used the upstream tool if only the assistant ran it.
- The user writes a short motivation/relevance comment in their own words. An AI-drafted paragraph merely labeled human-written does not satisfy this requirement.
- Attach the completed reproduction log, numeric before/after evidence and terminal screenshots; distinguish regression tests from real-data evidence.
- Follow the repository PR template and accurately disclose AI-assisted preparation. Do not characterize the patch as a new tiling algorithm or claim demonstrated downstream ink-reading improvements.

These are upstream PR requirements. A standalone Progress Prize repository is not itself an upstream PR, and no separate standalone AI-assistance prohibition was found in the inspected prize rules. Preserve honest attribution in either route. Human-written relevance commentary and personal review remain pending rather than silently treated as completed.

## Publication boundary

Ordinary public release of generic cache-fix source code, tests, retrieval instructions, provenance manifests, and nontextual evaluation summaries is encouraged by Progress Prize rules. The hidden-text restriction is **not a blanket prohibition on generic software publication**. The [FAQ](https://scrollprize.org/faq) and [Data Agreement](https://forms.gle/HV1J6dJbmCB2z5QL8) restrict revelations of hidden text and code associated with those revelations; this patch changes cache identity and makes no new-text claim.

The separate agreement also restricts redistribution of provided data. Keep downloaded source meshes/scan crops outside the publication package; use exact official retrieval URLs and recorded hashes. Do not accidentally publish discovered letters, textual interpretations, ink labels, or hidden-text renders with this generic correctness contribution. A public code license does not relicense dataset content.

The [official open-data README](https://github.com/ScrollPrize/open-data) and [AWS registry](https://registry.opendata.aws/vesuvius-challenge-herculaneum-scrolls/) document anonymous access under CC BY-NC 4.0. The scope of the separate registration agreement for anonymous access remains unresolved in the inspected sources. Preserve asset-specific provenance and citations; do not represent this uncertainty as either a signed agreement or an express exemption.

The user's external-action approval is a separate requirement: no public repository, PR, submission, message, account registration or terms acceptance is authorized merely because the artifacts are prepared locally. The final review step should present the concrete files, real URL destination, final contribution text, unresolved personal fields and exact action for approval.

## Evidence and packaging checklist

| Official requirement / favored judging signal | Prepared evidence | Status |
|---|---|---|
| Specific scroll-data problem and implemented solution | `upstream-fix.patch`, `scripts/demo.py`, two original mesh provenance manifests | Complete locally |
| Demonstrated advantage over existing behavior | `results/evaluation.json`: 24/24 exact fresh matches versus 6/24 baseline controls; rendered output and actual logs | Correctness established; award significance unconfirmed |
| Real-data demonstration and traceability | Two complete public meshes, eight original file hashes unchanged, precise scan/segment IDs | Complete locally |
| Comprehensive documentation and usage examples | README, locked dependencies, technical report, fetch/evaluate/demo scripts | Complete locally |
| Standard community formats and modular integration | Actual TIFXYZ reader/tiler; unchanged return format and API; clean upstream patch application | Verified in focused harness |
| Early release and actual researcher use | Code-only archive prepared; no publication or community use yet | Pending approval and real adoption |
| Permissive source release | MIT software notices preserved; data excluded from release | Prepared; public URL pending |
| Human upstream motivation/review and literal error screenshots | PR draft, actual logs, accurately labeled output rendering | Human steps pending if pursuing an upstream PR |
| Personal eligibility, form terms and final submission | Official form mapping and unsent organizer question | User/organizer action pending |

- Pin the unchanged upstream revision and the candidate patch.
- Provide exact reproduction commands and environment versions, plus real-data sample/segment/volume identifiers, official URLs and file hashes.
- Compare ordered 2D and 3D bounds against forced recomputation; show that identical requests still reuse caches and that each changed layout setting misses stale caches.
- Include results from the two selected real published meshes, and confirm original downloaded coordinate hashes remain unchanged.
- State limitations: no adoption demonstrated, no end-to-end ink-reading gain established, and cache correctness depends on the documented object/parameter scope.
- Keep source dataset files private in the package; publish fetch instructions and attribution notices instead.
- Preserve upstream MIT notices for reused software, and keep data attribution/license notices distinct.
- Present final public contribution URL and human-approved narrative before any form submission.

## Independent patch review record

Review scope: `get_patches_3d` and its added `_patches_cache_key` field compared with the pinned upstream file. No source or test files were edited during this review.

The final schema-prefixed tuple representation covers target size, both scale components, resolution mode, overlap, coarse multiplier, calibration sample count, and minimum new coverage. Memory cache lookup checks its key; both fresh computation and disk loading store the matching key. The schema prefix avoids trusting legacy entries whose layout settings were not recorded. `verbose` appropriately does not affect layout identity, and `force_recompute` bypasses both caches. Appending the new dataclass field preserves existing positional argument locations. The final cache regression suite passed: **20 tests**. The full relevant suite also passed: **75 tests**, including those 20 checks. Both were rerun during final independent review.

Remaining inherited limitations include mutable geometry/masks, mutation of the returned list, malformed cache content, concurrent writers, and persistence failures. They are outside the narrow change; claim parameter-aware cache reuse rather than fully content-addressed geometry caching. Resolution-mode tests establish cache separation rather than verifying full-resolution tiler support.

The earlier scalar-string collision was addressed in the final patch using tuple `repr` rather than shortened f-string components. NumPy/Python scalar identity is covered in both memory and disk regression cases on installed NumPy 2.5.4. Input arguments passed to the tiler are unchanged. Behavior with other NumPy versions was not tested.

The final real-data report records **24/24** candidate fresh-result matches over two surfaces, four request scenarios and three repetitions, versus **6/24** for upstream. The six baseline passes are expected disk target-size controls. Ordered-bound equality, identical initial uncached outputs, same-request cache hits and original file hashes were verified in `results/evaluation.json`. The baseline additionally fails 14 of the 20 cache checks. These numbers establish bounded correctness and repeatability, not adoption or ink-reading performance.
