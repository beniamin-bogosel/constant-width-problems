# Source coverage and collection method

The collection is curated from inspected sources, with rewritten statements and proofs; it is not a wholesale transcription of books. Bibliography is in `data/sources.json`, machine-specific paths and SHA-256 fingerprints in `local-inventory.json`. The public repository and reading exports exclude that local inventory, the draft outline PDF, and all source books/manuscripts.

| Source | Material actually inspected | Use |
| --- | --- | --- |
| `Doc/CWbook2.pdf` | Full 35-page outline, especially Exercises 1.1–2.11 | Eight-chapter structure, exercise seeds, separate corrections log |
| Yaglom–Boltyanskii, *Convex Figures* | §7 extract, printed pp. 70–82 | Exercise references 7-1, 7-3–7-16; added 7-10–7-12 equiangular work and 7-19–7-20 approximation/descent, with the latter solution studied through Hynd |
| Martini–Montejano–Oliveros (2019) | Contents and relevant parts of Chapters 2, 3, 5–8; Blaschke identity cross-reference | Support geometry, projections, packing, balls, Meissner context |
| Henrot–Pierre, *Shape Variation and Optimization* (2018) | Chapter 2, §§2.2.2–2.2.6 and selected §2.5 exercises | 16 new generalities exercises; two existing entries cross-referenced; [coverage and topology conventions](henrot-pierre-extraction.md) |
| Schneider, second edition | Contents and relevant support/Hausdorff/mixed-volume material | Precise convex-geometric hypotheses and reference structure |
| Hynd, *The Blaschke–Lebesgue theorem revisited*, versions 1 and 2 | Local v1 §§2–4; v2 §3 Lemma 3.3 and version structure | Variational and shortest-arc exercises; [version distinctions and proof routes](blaschke-proof-routes.md) |
| Bogosel, *New variational arguments regarding the Blaschke–Lebesgue theorem* | Local `BL2D_optim.tex`, §§2–4 | Blaschke motions, first and second area variations, finite-class minimization |
| Bogosel, *Mixed volumes and the Blaschke–Lebesgue theorem* | Entire 16-page preprint dated 2 May 2024 | 19 new exercises; four existing entries cross-referenced; [coverage and normalization notes](mixed-volume-extraction.md) |
| `Cheeger_BL.tex` | Angle lemma, erosion formulas, perimeter/area and Cheeger comparisons | Several short exercises, with active-arc and t=0 qualifications |
| `Volume_Meissner.tex` | Dual-edge geometry, surface decomposition, spindle integral, area formula, Appendix A | Coordinate helpers, area and volume computations, summand convexity |
| `Intermediary_Points_Meissner.tex` | Counting, dual-cell coordinates, comparison question | Proved combinatorics and one explicitly local open question |
| `ConstantWidth/research` | README and selected kernel/counterexample/pair-energy sections | Layer cake, a large-power counterexample, local distance-energy question |
| User's WordPress blog | 2013 hexagon and BL posts, 2020 symmetric covers, 2023 properties | Three sourced exercises and cross-checks of book topics |
| Author's unit-disk packing proposal | Conversation of 15 October 2026; center-containment and angle proofs developed here | Ten related exercises; [packing exploration and attribution](packing-exploration.md) |
| Web articles/preprints | Primary-source abstracts and selected relevant passages | Open-status checks, newer dangling-point result, further reading |

The files named `03-YaglomCW.pdf` and `CW_Convex_Figures.pdf` are actually PostScript. The usable chapter extract was rendered with Ghostscript and OCR'd with Tesseract; exercise numbers and statements were inspected, and the proof formulations here were independently written. A pre-existing `yaglom.txt` extraction was largely encoding garbage and was not trusted. The full DjVu book was located, but Chapter 6 was not fully OCR'd in this pass. A reference to Chapter 6 in a newer article is recorded as indirect evidence, not claimed as direct extraction.

Large copyrighted source extractions stayed in `/tmp`; they are not bundled with the collection. The renderer is reused from the user's own local Meissner workspace and retains its conventions and fingerprint in the skill reference.

## Further material to develop

The initial 62 entries prioritize short complete arguments. The following larger source leads are intentionally not disguised as solved exercises:

- Yaglom–Boltyanskii §6: minimal-width incircle estimates and Pál's area theorem; retrieve and inspect the relevant full-book pages before assigning exact exercise text.
- Complete the geometric circle-center existence and curvilinear surgery lemmas still supplied as explicit inputs to the new support-splice and shortest-arc exercises; add the full lower equiangular-polygon comparison from Yaglom–Boltyanskii 7-12.
- Cheeger comparison after active arcs disappear: extract the disk-polygon replacement construction before presenting a full independent global proof.
- Extend the new two-center Blaschke exercises to the author's arbitrary three-vertex sensitivity and center-based Lagrangian formulations.
- Hynd's Meissner density theorem and general surface partitions: useful major prerequisites, usually longer than a short exercise.
- General Meissner wedge/sliver area: add a carefully oriented Gauss–Bonnet diagram and check the interior/exterior dihedral conventions.
- The new 2026 spectral lower-bound preprint: verify the full proof before turning its estimates into exercises.

`research-log.json` records the web search scope, selected links, and status qualifications. No statement of “still open” means an exhaustive search guarantee. The original draft and sibling workspaces were left unchanged.
