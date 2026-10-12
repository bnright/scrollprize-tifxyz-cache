# Attribution and data provenance

Checked against the [official data citation guidance](https://scrollprize.org/data#how-to-cite) on October 12, 2026. Software and scroll data have separate licenses.

## Software

The baseline and candidate reader/tiler are derived from [ScrollPrize/villa](https://github.com/ScrollPrize/villa), revision `25f3c93c65b492be3b90e402213a1ba6b5fd624c`. Preserve its **MIT License** and `Copyright (c) 2024 Vesuvius Challenge` notice with copied code. This project modifies cache identification in `vesuvius/src/vesuvius/tifxyz/types.py`; the official hierarchical tiling algorithm is the baseline, not an original algorithm claimed by this contribution.

The original evaluation scripts, regression tests, and documentation may accompany the contribution under MIT. A software MIT notice does not license the research meshes, scans, official website text, or third-party dependencies. Dependency licenses remain their own.

AI assistance was used in research, implementation, experiment design, tests, and documentation. Execution evidence supports the stated results. The upstream contribution guidelines separately require human use/review and genuinely human-written relevance commentary; this document does not assert that those human steps have already happened.

## Real scroll data

Local evaluation uses published TIFXYZ surface coordinates traceable to these original scan volumes:

| Sample | Scan | Segment | Exact original mesh |
|---|---|---|---|
| PHerc0139 | `20250728140407-9.362um-1.2m-113keV-masked.zarr` | `20250108000000-w025_2025010863` | `20250108000000-on-20250728140407-9.362um.tifxyz` |
| PHerc0800 | `20250521135224-8.64um` | `20251028213516-auto_grown_20251028213516907` | `20251028213516-on-20250521135224-8.64um.tifxyz` |

The two provenance JSON documents beside this file retain every downloaded file's official URL, byte size and SHA-256. The scan identifiers date these volumes to 2025. The official data page distinguishes newer Vesuvius Challenge scans from the legacy pre-2025 DLS dataset; the newer dataset citation below therefore applies. No author credit for the individual segmentation is invented; any later asset-specific attribution must be preserved if discovered.

Methods acknowledgment: Evaluation used original surface meshes from *Vesuvius Challenge - CT Scans of Herculaneum Papyri*. Original coordinate files were kept as private local research inputs; benchmark working copies may contain cache artifacts. This cache-correctness work does not detect ink, identify characters, or reveal hidden text.

## Preferred dataset bibliography

The following BibTeX preserves the official author order, dataset title, and publisher. The official preferred citation does not specify a year, so no dataset publication year is invented.

```bibtex
@misc{vesuvius_challenge_ct_scans,
  author = {Angelotti, Giorgio and Parsons, Stephen and Johnson, Sean and
            Dal PrÃ , Elian Rafael and Rudolph, Johannes and Tafforeau, Paul and
            Mirone, Alessandro and Henderson, Paul and Schilling, Hendrik and
            McDonald, Forrest and Josey, David and Nader, Youssef and
            Parker, C. Seth and Seales, W. Brent},
  title = {Vesuvius Challenge - CT Scans of Herculaneum Papyri},
  publisher = {Vesuvius Challenge},
  url = {https://scrollprize.org/data},
  note = {Official preferred dataset citation; accessed 2026-10-12}
}
```

Source: [official newer-scan citation](https://scrollprize.org/data#vesuvius-challenge---ct-scans-of-herculaneum-papyri).

The legacy *EduceLab-Scrolls* acknowledgment and Parsons et al. (2023) apply to Scrolls 1â€“4 and Fragments 1â€“6 scanned at DLS before 2025. Those legacy scans are not the inputs listed above. If future evaluation uses them, add their required abstract/methods acknowledgment and [Parsons et al. 2023 reference](https://doi.org/10.48550/arXiv.2304.02084).

## Data license and publication boundary

The [official data page](https://scrollprize.org/data#licenses) specifies [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) unless an asset says otherwise. The separately published [data agreement](https://dl.ash2txt.org/LICENSE.txt) requires written approval for redistribution and restricts hidden-text revelations. Its applicability to anonymous open-bucket downloads and the intended cash-prize use remain unresolved; reading the terms did not accept them.

The publication package should contain code, software license notices, these citations, retrieval URLs/hashes, aggregate comparison results, and reproducibility instructions. It must exclude `private-data/`, downloaded coordinate TIFFs/mesh metadata, data caches, complete numeric coordinate/bounds arrays, scan crops, labels, and hidden-text material. Reviewer retrieval can use the original official sources subject to their terms. Do not label the data MIT or redistribute it merely because software publication is approved.

Final preparation audit: the original data are confined to `private-data/`; the two `docs/*-provenance.json` files contain URLs and fingerprints rather than coordinates. The allowlisted release archive has passed inventory, content-hash, CRC and data-exclusion checks. An extracted copy passed source verification, clean patch application, anonymous input retrieval, all 75 tests and the actual corrected demonstration. See `final-review.md` and the local `release/inventory.json` / `release/extraction-check.json` for the audit scope and final archive identity.
