# AIcrowd eligibility audit

Verified on **2026-10-12**, using the user's America/Chicago calendar date. All deadlines below preserve the organizers' UTC times. Research only: no account creation, registration, terms acceptance, organizer contact, publication, or submission occurred.

## Decision

**Do not start an ARC place-prize entry as a new individual entrant.** Registration froze on October 2; continuing submissions do not reopen entry. No other currently eligible cash competition was confirmed in AIcrowd's current running directory. Completed competitions and ongoing post-challenge benchmarks must not be counted as available cash.

## Concrete opportunities compared

| Opportunity | Confirmed current status | Cash vs other rewards | New entrant decision |
|---|---|---|---|
| ARC White-Box Estimation Challenge 2026, Phase 2 | Registration/team freeze October 2, 2026 23:59 UTC; submissions October 17 23:59 UTC; algorithmic writeup October 24 23:59 UTC | Phase 2 place prizes: $50,000/$20,000/$10,000; algorithmic $20,000. $150,000 total advertised includes already-closed Phase 1 | Ineligible for a newly registered place/algorithmic entry after freeze. An already registered user's status was not inspected |
| Global Chess Challenge 2025 | Round 2 closed January 31, 2026 23:55 UTC; directory says completed | Historical $17,000 cash, **separate** $8,000 compute credits | Expired; $0 confirmed available to a new entrant |
| ECCV 2020 Commands 4 Autonomous Vehicles | Running directory contains an ongoing **post-challenge** round; actual award challenge ended August 1, 2020 | Historical €1,500/€500/€250 awards | Expired prize round; ongoing benchmark submissions are insufficient for cash eligibility |

Sources: [ARC current rules](https://www.aicrowd.com/challenges/arc-white-box-estimation-challenge-2026/challenge_rules), [ARC Phase 2 organizer announcement](https://discourse.aicrowd.com/t/phase-2-of-the-arc-white-box-estimation-challenge-is-live/18197), [Chess page](https://www.aicrowd.com/challenges/global-chess-challenge-2025), [Chess rules](https://www.aicrowd.com/challenges/global-chess-challenge-2025/challenge_rules), [C4AV page](https://www.aicrowd.com/challenges/eccv-2020-commands-4-autonomous-vehicles), and [running directory](https://www.aicrowd.com/challenges?status=running). Each accessed October 12, 2026.

## ARC contract details

Current official rules are **version 14**. Sections 1 and 4 expressly close new individual/team entry at the October 2 freeze; embedded public registration state additionally reports `canRegister=false`. Rules §5.7 permit LLM code assistance; technical writeups must disclose its extent and label uncertain explanations.

Eligible adults must meet geographic sanctions and insider exclusions (§3). Individual entrants are allowed, subject to timely registration. Winner identity/tax verification remains necessary. Algorithmic writeups must reference one successfully graded submission (§6).

Phase 2 packages Python source and data; `estimator.py` follows the current starter kit. All numerical computation uses flopscope. CPU-only evaluation, no network, 8 GB solution memory, 120 seconds/MLP, 0.4-second residual allowance, 10 submissions/team/UTC day. The Phase 2 announcement specifies a 2^41 FLOP budget, `v2-phase2` dataset, flopscope >=0.12.0 and whestbench >=0.16.0. Meaningful unmetered computation remains prohibited even within residual time.

Place winners release the prize-determining code and artifacts under an OSI-approved license within 30 days and keep them public for three years (§8); Phase 1 had a seven-day exception. No pre-award publication prohibition was identified. Broad submission-content licenses apply. Final prize ranking uses fresh private re-evaluation, not public rank.

ARC also lists discretionary community cash recognition, typically $500–$5,000, with **no application, fixed number, or allocated pool** (§6). Whether a new unregistered contributor can receive this recognition after the freeze is **unconfirmed**; it is not a defensible replacement for established entry eligibility. Organizer outreach would require user approval.

## Global Chess constraints (historical, rejected)

Official rules allowed adult individual entries, excluded specified locations and organizer insiders, required original work/appropriate external-data licenses, and capped submissions at 20/day. Winning reports were required for publication. Derivatives of the organizer base model had to remain permissively open-sourced. Runtime allowed only language-model token inference: no chess engines, tools, retrieval, search or hidden rules; fewer than 8.5 billion parameters and supported Trainium backends. AI coding assistance was not explicitly resolved by these rules, and no clarification was pursued because the deadline has expired. No general pre-award publication ban was identified. The page's team-freeze year appears erroneous; the unambiguous January 31, 2026 submission close and completed status are sufficient to exclude this opportunity.

## Directory completeness and misleading status

The current running directory returned ARC, Spotify MPD, Trajnet++, EPFL ML Project 1, C4AV post-challenge submissions, MEDIQA 2021 post-challenge, Test P, and a completed reasoning track. The non-ARC entries did not establish a current eligible cash award. The default directory also displayed Global Chess, Orak, Flextrack, Sony dialogue, and Meta CRAG as completed. AIcrowd's home page still labels some historical challenges ongoing; challenge deadlines and prize-round status take priority over that label.

## Prepared organizer question, if later approved

Destination: `arc-whestbench@aicrowd.com`, the address explicitly designated for rules questions in the organizer's Phase 2 announcement.

> I did not register for ARC White-Box Estimation Challenge 2026 before the October 2 freeze. Can a new individual who contributes a reproducible public bug fix or useful improvement to flopscope/whestbench after that date still be considered for the discretionary community-contribution cash awards in §6? If yes, which eligibility, licensing, deadline, and disclosure requirements apply, and where should the contribution evidence be provided? I understand that place and algorithmic awards require timely registration and that community awards are discretionary.

This is a prepared draft only; it has not been sent.

## Recheck procedure and retained evidence

The ARC Rules page renders legal content from HTML-encoded `data-react-props`; the web text extractor omitted it. A read-only HTTPS fetch decoded the JSON and extracted `props.data.challenge.rules.termsHtml`. Local evidence is in `research/aicrowd-evidence/`: rules HTML/text, rules-version and registration metadata, and Chess rules text. Treat raw official text as research evidence rather than project code; do not apply the contribution's license to it.

ARC rules HTML SHA-256: `BFE8BF9DC910F8ABB7CD1A52B6FFAC868131B2F1677966085C083FFA2BBE4747`.

Before any external action, refetch the cited current rules and announcement, compare deadlines/version, inspect the actual account's prior registration only with relevant access, and obtain the user's approval for the exact terms/publication/contact/submission action. No substantial ARC implementation is justified for a new entrant on the evidence above.
