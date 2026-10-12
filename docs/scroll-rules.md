# ScrollPrize rules and opportunity evidence

Checked against official live sources on **2026-10-12**, the user's America/Chicago client date. No account registration, signature, form submission, contact, publication, or scan-data download was performed in this research task. Website pages generally lack a displayed update date; repository history dates below are evidence about their source files, not a guarantee of deployment timing.

## Current prize rules

[Open Prizes](https://scrollprize.org/prizes#progress-prizes) confirms:

| Question | Current finding |
|---|---|
| Progress Prizes | Open; monthly evaluation; newcomers encouraged; multiple submissions/awards allowed. |
| Next deadline | **October 31, 2026, 11:59 pm Pacific**; November 1, 2026, 1:59 am Central. |
| Cash | Best monthly submission: $20,000. Other discretionary awards typically $250–$20,000. |
| Qualifying work | Solve a scroll-data problem; demonstrate advantages and use; document examples; integrate modularly with community formats. |
| Strong evidence | Real-data improvements, useful diagnostics, before/after bug evidence, adoption, early releases including relevant weights/data. |
| License/payment | Permissive open-source release required to accept an award; payment details due within 30 days of announcement. Awards and rule changes remain organizer-discretionary. |
| Other open opportunities | 2027 Grand Prize: $1m total; First Letters: $50k per eligible scroll, nine remaining; Paris 4 title: $50k. Deadline June 25, 2027. |
| Grand Prize compute | Generic training-data effort/compute unlimited; seeds fixed/reported; public experiment logs, training datasets and iterative checkpoints required; eight documented human-input hours maximum for unrolling. |

These compute conditions are in the **Grand Prize** section; no equivalent numeric compute cap was located in Progress Prize rules. Grand Prize reproducibility and discovery restrictions must not be silently transferred to unrelated progress-tool submissions.

Source-file latest commit: [34d4b260, 2026-10-11 21:02:44 UTC](https://github.com/ScrollPrize/villa/commit/34d4b260dd2a281d635227a71ab8bfb5eb45c4cd). Live rules supersede cached search snippets: the live First Letters section has 21 eligible volumes and nine remaining prizes; stale cards/snippets still show 22/ten.

## Individual eligibility and submission contents

The [October 2026 Progress Prize form](https://docs.google.com/forms/d/e/1FAIpQLSc4flEfgK2nyjoczz2_U_XrIGMlgrnSknWatLqrFPnbtKfZwg/viewform) explicitly supports **individual or team** submissions. It asks for email, full name, team description, a public contribution URL (repository or PR), and a contribution explanation covering scroll data, usefulness, newly enabled capability, and evidence. The Discord display-name question is optional in this form. Its public-URL requirement is worth noticing despite the general terms allowing deferred open-source release until an award. A public standalone repository with an explicit permissive license is the clearest route after publication approval. Form month verified live; no displayed publication/update date.

The [FAQ](https://scrollprize.org/faq) permits international participants if legally payable, excludes the current organizer team from prizes, welcomes small community contributions, and encourages progress sharing. Discoveries of previously hidden text and associated code require written organizer approval; milestone text discoveries must stay confidential until announcement. Publications and presentations must cite the applicable dataset. New individual participation is supported; cash eligibility is still conditional on lawful payment and organizer review, not a guaranteed award. FAQ source-file latest commit: [8d6284e4, 2026-08-07 19:05:03 UTC](https://github.com/ScrollPrize/villa/commit/8d6284e40163f272ed2c807547fb62484942b351).

## AI assistance

The official [villa contribution guidelines](https://github.com/ScrollPrize/villa/blob/main/CONTRIBUTING.md#ai-guidelines) support LLM coding assistants. **Upstream LLM-generated PRs** require human-written relevance commentary, human use of the codebase toward scroll-data work, human review of the code, and real scroll-data evidence. Synthetic/toy demonstrations are not accepted as upstream usefulness evidence. A speculative automated bug hunt is discouraged. This is an upstream PR policy; no separately stated Progress Prize ban on AI assistance was found. Preserve honest AI attribution in a standalone project and leave genuinely human-written upstream commentary to the user. Latest contribution-guidelines commit: [6cea5158, 2026-10-12 11:59:18 UTC](https://github.com/ScrollPrize/villa/commit/6cea5158ea880e90069950e31dc1ed8fc8371ca9).

The [2026 Open Problems](https://scrollprize.org/2026_open_problems) page describes an internally used autonomous-agent architecture search. This supports the inference that AI development tools are compatible with the project's research methods, but does not itself establish prize eligibility or waive PR requirements.

## Data access, licenses, release and attribution

The [Data Formats page](https://scrollprize.org/data#licenses) lists **CC BY-NC 4.0**, unless a specific asset states otherwise, and differentiates newer Vesuvius Challenge scans from the legacy EduceLab dataset. Source-file latest commit: [1ecdfc58, 2026-07-14 20:07:02 UTC](https://github.com/ScrollPrize/villa/commit/1ecdfc585666446f3c917b3a76567058e3ef57fe). For legacy Scrolls 1–4 and Fragments 1–6 scanned at DLS before 2025, the page requires EduceLab-Scrolls acknowledgment and [Parsons et al. 2023](https://doi.org/10.48550/arXiv.2304.02084). For newer scans, cite the dataset titled *Vesuvius Challenge - CT Scans of Herculaneum Papyri*, with the authors provided in that page's citation section. Record sample/volume IDs, exact source URLs, accessed date, licenses, and transformation provenance in the project manifest.

The [official open-data README](https://github.com/ScrollPrize/open-data#how-to-access-the-data) provides anonymous S3 reads with `fsspec`/`anon=True` and a CC BY-NC 4.0 license. It does not describe an account registration or checkbox prerequisite. Latest README commit: [f4d8ec2b, 2026-03-26 19:26:21 UTC](https://github.com/ScrollPrize/open-data/commit/f4d8ec2b895b10cf8535bd6504375b552ff5484a). The [AWS registry entry](https://registry.opendata.aws/vesuvius-challenge-herculaneum-scrolls/) also documents account-free `--no-sign-request` access and the same license. Technical public access is established; these sources do not explicitly exempt anonymous users from the separate agreement below.

The [Data Agreement](https://forms.gle/HV1J6dJbmCB2z5QL8), linked from the FAQ, resolves to [this Google form](https://docs.google.com/forms/d/e/1FAIpQLSf2lCOCwnO1xo0bc1QdlL0a034Uoe7zyjYBY2k33ZHslHE38Q/viewform). Its opening says: “By registering for downloads from the Vesuvius Challenge Data Server and Vesuvius Challenge Discord Server, I agree to license the data”. It then imposes terms including:

- Written approval before redistribution.
- Express written consent before hidden-text revelations or related code are disclosed outside official Discord; the scope includes interpretations, ink-label images, and associated commentary.
- Organizer use of submissions/results, including publication.
- Individually agreeing team members and special EduceLab citation requirements.

The form requires an agreement checkbox and repeated full name as digital signature. Reading its public text did not submit or accept it. No displayed agreement revision date was found. The agreement speaks about registration; it does not explicitly say an anonymous S3 GET constitutes registration or acceptance. Whether its additional restrictions govern anonymous open-bucket use is unresolved. The public-data license and separate no-redistribution term also need organizer clarification before a data-bundled release. Avoid publishing scan crops, meshes, labels or textual revelations until this is resolved; publish original general-purpose code and retrieval instructions only within approved scope.

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) requires attribution, a license link, modification notices, and noncommercial use. Its monetary-compensation definition warrants clarification for the specific intended competition use rather than claiming a blanket exemption. Code and data must carry separate notices. The [villa root software license](https://github.com/ScrollPrize/villa/blob/main/LICENSE) is MIT, requiring preservation of its copyright/permission notice if copying substantial code; subdirectories and pretrained resources can have different licenses.

## Current official wishlist and prior-art signals

The live prize page's [wishlist link](https://github.com/ScrollPrize/villa/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22help%20wanted%22) is a filtered issue list. Public GitHub API metadata on 2026-10-12 returned three open `help wanted` issues, each opened April 18, 2025:

| Issue | Requested useful output | Updated UTC |
|---|---|---|
| [#193 Methods for generating surface, fiber, or ink labels](https://github.com/ScrollPrize/villa/issues/193) | Better volume/label pairs than mesh voxelization, accepting array/Zarr and emitting Zarr. | 2026-08-20 06:43:08 |
| [#192 Accurate 3d ink labels](https://github.com/ScrollPrize/villa/issues/192) | Detectable-ink-only 3D labels, ready-to-run Zarr/TIFF. Also the only current `good first issue`. | 2026-10-09 11:49:32 |
| [#191 Surface and Fiber Predictions in Compressed or Highly Curved areas](https://github.com/ScrollPrize/villa/issues/191) | Improve hard-region surface/fiber predictions; connected, unbranched fibers; Zarr outputs. | 2026-08-28 20:17:08 |

#193 already has detailed community label-incompleteness QC, label snapping studies, normalization diagnostics and failed-method controls. A new label-QC tool must distinguish its contribution from that work. The referenced [normalization bug #1364](https://github.com/ScrollPrize/villa/issues/1364) is closed via #1386; do not market it as an unresolved new fix.

The [Open Problems](https://scrollprize.org/2026_open_problems) infrastructure section values streamed chunks, inspectable outputs, preserved coordinates, tiled processing, and avoiding full-volume copies. A small reproducible diagnostic on real data is plausible for a Progress Prize, but needs actionable evidence: show a downstream correction or improvement, not merely produce another generic report.

## Suggested organizer clarification, drafted only

> May a new individual submit an AI-assisted standalone diagnostic tool for October Progress Prizes, and may we anonymously read small local crops from the public CC BY-NC S3 bucket for cash-prize evaluation without registering for the Data Agreement? Please clarify permitted publication of derived diagnostics and whether the separate redistribution restrictions apply to anonymous bucket users. We will disclose AI assistance, preserve attribution, and publish no newly revealed text.

Unresolved: the user's individual lawful-payability details, organizer confirmation of standalone AI-assisted eligibility, data-agreement applicability to anonymous access, permitted derived-data publication, and any asset-specific license exceptions. Recheck the live form/rules immediately before actual submission.
