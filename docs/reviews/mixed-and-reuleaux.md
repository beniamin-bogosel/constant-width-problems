# Review of Reuleaux polygons and mixed volumes

Reviewed by **ChatGPT 6 Astra**, 15 October 2026. This is an AI mathematical and editorial review, not human certification. All entries retain `checked-draft` and `ready-for-review`; human review remains pending.

Read every statement, hint, and proof in Chapter 2 (7 entries) and Chapter 4 (25 entries): **32 reviewed entries**. Statements or proofs were enriched in **19 entries**; the remaining 13 were retained after checking their assumptions, constants, and argument. Stable IDs and chapter ordering were preserved.

## Material findings and improvements

- No incorrect main formula was found in these two chapters. Several proofs needed intermediate geometry or normalization details to make the existing conclusion independently checkable.
- The irregular-pentagon construction now gives exact coordinates, checks the strictly convex cyclic order and all non-star distances, and explains why every proposed arc lies in all five disks. “Sufficiently small perturbations” is no longer the only construction offered.
- The regular erosion proof now identifies the correct circle-intersection branch, the principal inverse-sine branch, and both endpoint limits. The endpoint is a singleton; erosion generally loses constant width.
- The skeleton-to-tangent-polygon plateau proof now states the antipodally invariant endpoint-normal set and displays both uses of the polygon edge formula.
- Mixed-area polarization, segment addition, and projected spatial identities now make their factors of 2, 3, and 4 explicit. Proper inclusion yields a strict mixed-area inequality under a positive curvature-density assumption, while general bodies can exhibit plateaus.
- Pál’s theorem is explicitly named in the universal-cover equality discussion. A regular hexagon with opposite-side separation one is not asserted to be a constant-width body.
- Allowed substantial inputs remain visible: Rogers–Shephard, Jung, Cauchy projection, Blaschke selection, and the cited Meissner competitor volume are not presented as newly proved short lemmas. The annulus relaxation is still distinguished from the original constant-width optimization.

## Sources and checks

The local source and extraction notes for B. Bogosel, *Mixed volumes and the Blaschke–Lebesgue theorem*, were inspected, especially §2.2 and the theorem connecting skeleton and tangent polygons. Existing source locators and attribution were retained. The new exact-coordinate pentagon is a supplied illustrative construction.

Targeted checks performed during this pass:

- The geometry kernel accepted the exact pentagon: five active arcs, positive hull turns, perimeter π, and maximum sampled directional-width error `8.881784197001252e-16`. The analytic proof is in the solution; the floating-point result is only a consistency check.
- The expanded regular-erosion formula agreed with independent circular-arc integration for n = 3, 5, 7, 9 at four erosion depths each, with absolute errors below `1e-12`.
- Both chapter JSON pairs passed their schemas and the text was checked for accidental control characters. All 645 math fragments in these chapters rendered successfully through the HTML reader’s strict math renderer. Final collection-wide prerequisite, HTML, and browser checks are performed by the main rebuild.

The new [segment-sweep illustration](../../figures/mixed-segment-sweep.svg) shows the added band of area ℓb and the nonzero diameter-segment correction. It was rendered and visually inspected. Its exact parameters and diagnostics are saved beside the SVG; reproduce it with `python scripts/make_mixed_review_figure.py`. The figure is intended for `cw-segment-mixed-area` and `cw-valuation-segment-correction`.

## Entry-by-entry ledger

| Entry | Review result |
| --- | --- |
| [cw-triangle-measures](https://beniamin-bogosel.github.io/constant-width-problems/#cw-triangle-measures) | Explained opposite support pairing and proved that the entire arcs, not only the vertices, lie in the circumdisk. |
| [cw-arc-polygon-area](https://beniamin-bogosel.github.io/constant-width-problems/#cw-arc-polygon-area) | Clarified cyclic orientation, the outward-bulge sign, radians, and vanishing arcs. |
| [cw-regular-reuleaux](https://beniamin-bogosel.github.io/constant-width-problems/#cw-regular-reuleaux) | Expanded construction and half-angle simplification; added geometric Hausdorff convergence supporting the title. |
| [cw-turning-budget](https://beniamin-bogosel.github.io/constant-width-problems/#cw-turning-budget) | Specified smooth junctions and distinguished the turning identity from the extra constant-width pairing. |
| [cw-erosion-disks](https://beniamin-bogosel.github.io/constant-width-problems/#cw-erosion-disks) | Included the degenerate maximizer case, extinction, and the warning that erosion does not preserve constant width. |
| [cw-regular-inner-parallel](https://beniamin-bogosel.github.io/constant-width-problems/#cw-regular-inner-parallel) | Explained which circle-intersection branch is used and checked both endpoints of the admissible erosion range. |
| [cw-irregular-construction](https://beniamin-bogosel.github.io/constant-width-problems/#cw-irregular-construction) | Replaced an unspecified sufficiently-small perturbation by exact reproducible coordinates, with analytic convexity/arc/width checks. |
| [cw-mixed-area-polarization](https://beniamin-bogosel.github.io/constant-width-problems/#cw-mixed-area-polarization) | Made the mixed-area coefficient convention explicit and displayed the translation-cancellation calculation. |
| [cw-mixed-area-monotonicity](https://beniamin-bogosel.github.io/constant-width-problems/#cw-mixed-area-monotonicity) | Explained inclusion-preserving smoothing and separated monotonicity from the extra positive-density condition for strictness. |
| [cw-polygon-mixed-edge-sum](https://beniamin-bogosel.github.io/constant-width-problems/#cw-polygon-mixed-edge-sum) | Verified the atom weights, factor 2, and closure identity for the edge-normal sum; retained the proof. |
| [cw-segment-mixed-area](https://beniamin-bogosel.github.io/constant-width-problems/#cw-segment-mixed-area) | Expanded the exact slice/Fubini argument, normalization and parallel-segment case. |
| [cw-valuation-segment-correction](https://beniamin-bogosel.github.io/constant-width-problems/#cw-valuation-segment-correction) | Verified all factors: each half-disk contributes (π+2)r²/2 and the diameter contributes 2r². The source typo remains corrected. |
| [cw-cap-chord-replacement](https://beniamin-bogosel.github.io/constant-width-problems/#cw-cap-chord-replacement) | Defined the normal cone directly in the statement; retained the valid balance-of-normals proof. |
| [cw-mixed-area-complement](https://beniamin-bogosel.github.io/constant-width-problems/#cw-mixed-area-complement) | Verified the difference-body expansion and both disk/Reuleaux-triangle values; retained the proof. |
| [cw-triangle-hexagon-plateau](https://beniamin-bogosel.github.io/constant-width-problems/#cw-triangle-hexagon-plateau) | Explained the reflected-inclusion step and why the Reuleaux triangle is actually inside the specified hexagon. |
| [cw-reuleaux-skeleton-plateau](https://beniamin-bogosel.github.io/constant-width-problems/#cw-reuleaux-skeleton-plateau) | Made the two edge-measure evaluations and antipodal endpoint-normal set explicit; explained boundedness and equality mechanism. |
| [cw-skeleton-difference-area](https://beniamin-bogosel.github.io/constant-width-problems/#cw-skeleton-difference-area) | Verified the cap subtraction and cancellation of the equal mixed areas; retained the proof. |
| [cw-skeleton-area-extrema](https://beniamin-bogosel.github.io/constant-width-problems/#cw-skeleton-area-extrema) | Identified the arc constraints and Rogers–Shephard as permitted external inputs instead of implicit short lemmas. |
| [cw-steiner-parallel](https://beniamin-bogosel.github.io/constant-width-problems/#cw-steiner-parallel) | Verified width, perimeter, Steiner coefficients, and uniform support convergence to the disk centered at the fixed origin. |
| [cw-convex-hull-mixed-identity](https://beniamin-bogosel.github.io/constant-width-problems/#cw-convex-hull-mixed-identity) | Verified the positive-part derivative rule on the zero set and the bilinear expansion for Lipschitz supports. |
| [cw-planar-hull-objective](https://beniamin-bogosel.github.io/constant-width-problems/#cw-planar-hull-objective) | Verified both identities and translation invariance of the objective despite changes to the reflected hull; retained the restricted feasible family. |
| [cw-symmetric-hull-annulus](https://beniamin-bogosel.github.io/constant-width-problems/#cw-symmetric-hull-annulus) | Verified the support maximum identity, the circumcenter requirement only for the outer bound, and the 2D/3D Jung constants. |
| [cw-annulus-both-constraints](https://beniamin-bogosel.github.io/constant-width-problems/#cw-annulus-both-constraints) | Verified the square and thin-rectangle counterexamples and the strict inequalities for positive-area competitors. |
| [cw-symmetric-cover](https://beniamin-bogosel.github.io/constant-width-problems/#cw-symmetric-cover) | Made the sharpness dependence on Pál explicit and avoided confusing hexagon opposite-side separation with constant width. |
| [cw-blaschke-volume](https://beniamin-bogosel.github.io/constant-width-problems/#cw-blaschke-volume) | Verified reflection symmetry, the volume expansion coefficients 2 and 6, and surface-area normalization. |
| [cw-spatial-mixed-objectives](https://beniamin-bogosel.github.io/constant-width-problems/#cw-spatial-mixed-objectives) | Verified both objective identities and their cubic/quadratic scalings with the first unit-ball argument fixed. |
| [cw-projected-hull-identity](https://beniamin-bogosel.github.io/constant-width-problems/#cw-projected-hull-identity) | Displayed the polarization factors 6 and 8 and stated the normalization and scope of the projection argument. |
| [cw-spatial-hull-objective](https://beniamin-bogosel.github.io/constant-width-problems/#cw-spatial-hull-objective) | Verified the spherical-average convention and coefficients; kept the annulus problem explicitly identified as a relaxation. |
| [cw-annulus-inner-contact](https://beniamin-bogosel.github.io/constant-width-problems/#cw-annulus-inner-contact) | Added compactness/continuity attainment and kept the distinction from the constant-width hull family. |
| [cw-spatial-cover-obstruction](https://beniamin-bogosel.github.io/constant-width-problems/#cw-spatial-cover-obstruction) | Specified convexity of the assumed spatial container, needed for mixed-volume monotonicity. |
| [cw-spatial-inradius-volume](https://beniamin-bogosel.github.io/constant-width-problems/#cw-spatial-inradius-volume) | Explained why the support integral handles nonsmooth bodies and derived the stated inradius input from Jung plus concentric balls. |
| [cw-minimizer-inradius-threshold](https://beniamin-bogosel.github.io/constant-width-problems/#cw-minimizer-inradius-threshold) | Verified the threshold algebra and numerical values. The endpoint remains included because the supplied argument has no equality exclusion. |

## Remaining limits

No unresolved proof gap was identified in this scope after the clarifications above. This does not establish human-reviewed status. The nontrivial allowed theorems still require their stated references or prerequisite exercises, and the equality endpoint in the inradius-threshold exercise deliberately remains unresolved by that argument.
