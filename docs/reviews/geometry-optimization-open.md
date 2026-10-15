# Geometry, optimization, numerical, and open-problem review

Review by **ChatGPT 6 Astra**, 2026-10-15. All 34 entries in chapters 05–08 were read in full: 30 proof drafts and four open-question discussions. Proof status remains `checked-draft`; this is an additional machine review, not human mathematical certification. No new literature search was performed in this pass; open-status dates/evidence describe the earlier recorded checks.

## Material changes

- Restricted the spindle rotation to $0<\phi\leq2\pi$; larger rotations count the surface with multiplicity.
- Completed the Cheeger bisection exercise with runnable Python, the specialized inner-area formula, and a precise distinction between approximate endpoints and certified enclosures.
- Carried out both requested spherical helper-point computations explicitly.
- Matched the local Meissner comparison question to its actual critical-base hypothesis and distinguished it from strong criticality.
- Expanded the tetrahedral support-plane, Jung equality, Cheeger continuity/endpoints, Fourier-area, and numerical-error arguments.

## Entry-by-entry findings

### 05-meissner-polyhedra

- **cw-reuleaux-tetra-not-width** — Expanded the upper supporting-plane argument into explicit ball inequalities; checked the two exceptional points and the tetrahedral height.
- **cw-dual-edge-coordinates** — Checked midpoint construction, perpendicular chord directions, and h>0 under u,v≤1/2. Existing helper figure is sufficient.
- **cw-dual-dihedral** — Checked both sine half-angle formulas and the interior-angle convention; existing helper diagram is sufficient.
- **cw-spindle-area** — Corrected missing rotation range 0<φ≤2π, specified radians, and evaluated the area integral explicitly. For larger φ the old formula counted multiplicity.
- **cw-spherical-helper** — Made the complete sum, orientation, atan2 argument order/branch, translated helper point, and small-circle limitation explicit.
- **cw-meissner-tetra-volume** — Checked all factors and the half-angle identity; displayed the exact Blaschke relation being substituted. General area theorem remains explicitly supplied.
- **cw-meissner-summand** — Checked derivatives and added the uniform denominator bound and equality/strictness cases; retained warning that scalar splitting alone is not a geometric refinement theorem.
- **cw-extremal-bookkeeping** — Checked double counting and k=3 equality; clarified that the three old neighbors need not be distinct.
- **cw-dangling-delete** — Checked remaining pair count and preservation of unit diameter; preserved distinction between graph counting and volume monotonicity.
- **cw-tetra-smoothings** — Checked all eight choices, path exclusion, and the two symmetry types. Existing two-type figure suffices.

### 06-shape-optimization

- **cw-jung-plane** — Specified positive diameter, expanded the weighted identity, justified the sum-of-squares bound, and completed both directions of the equality analysis.
- **cw-inradius-extrema** — Checked radius normalization and both equality cases using concentric-ball identity, Jung equality, and equal-width inclusion.
- **cw-cheeger-scaling** — Specified planar setting, made two-way scaling bijection explicit, and distinguished full from relative perimeter.
- **cw-cheeger-root** — Defined erosion/interior convention, justified area continuity and zero terminal area, and fixed the domain-of-comparison issue when inradii differ.
- **cw-cheeger-extrema** — Verified the comparison direction and specified what equality information actually follows: disk is unique at lower bound; supplied theorem alone does not establish unique upper attainer.
- **cw-layer-cake** — Checked Fubini domination and center dependence. Boundary spheres do not affect the integral, so open/closed-ball convention is immaterial.
- **cw-high-moment-counterexample** — Checked positivity of the exterior sliver and exponential comparison; added exact disk moment and explicit normalization.
- **cw-translate-collision** — Checked difference-body/interior argument, strict-convexity contact uniqueness, and boundary-contact convention. No correction needed.
- **cw-common-point-packing** — Checked shared-boundary argument and why an interior tangent-cone ray enters the body locally. Equality correctly invokes the supplied sharp corner theorem.
- **cw-unit-disk-packing** — Checked common-center lemma use, translated-triangle construction, uniqueness, total-area comparison, and closed-disjoint variant. Existing figure suffices.
- **cw-fixed-shape-disk-packing** — Checked both constructions, feasible-translation locus, equidistant-set argument, and equality via equal-width inclusion.
- **cw-four-body-disk-radius** — Checked zero-center branch, angular pigeonhole estimate, numerical lower bound, and square-centered-disk upper bound. Bounds are not presented as an exact packing result.
- **cw-lattice-translates-density** — Checked primitive shortest vector extension, reduced-basis determinant bound, triangular lattice attainability, and density/equality values. Rotation scope remains explicit.
- **cw-diameter-packing-counterexample** — Checked all triangle diameters via vertex distances, positive area, and arbitrarily large finite arrangements.

### 07-numerical-methods

- **cw-fourier-area** — Displayed the area integral and full Fourier result, defined the Steiner point, and added the equality case while retaining convexity constraint.
- **cw-convexity-certificate** — Checked Lipschitz and coefficient bounds; added the explicit rounding-error margin and separated nonnegative from positive-curvature certification.
- **cw-grid-failure** — Checked aliasing at all nodes, negativity of the chosen off-grid point, odd-mode width identity, and absence of first-harmonic curvature obstruction. Recommended a plot to the main agent.
- **cw-cheeger-bisection** — Supplied the previously missing executable implementation, specialized area formula, accurate reference values, reciprocal interval rule, and certified-versus-floating distinction.
- **cw-spherical-partition-check** — Replaced the assertion that sums must agree with both requested explicit computations, exact expressions, branch check, and independent numerical values.
- **cw-scaling-checks** — Defined the torsional-rigidity normalization and boundary condition; expanded its PDE/change-of-variables derivation.

### 08-open-problems

- **cw-open-meissner** — Checked candidate normalization and area/volume equivalence; added existence-versus-identification distinction and prerequisites. Retained prior dated status evidence without claiming a new literature search.
- **cw-open-eigenvalue** — Specified the Sobolev space on the interior and the spectral/frequency normalization. Prior open-status evidence was not refreshed.
- **cw-open-helper-monotonicity** — Aligned the statement exactly with the source’s critical-base hypothesis; defined critical/strongly critical and broad smoothing convention; spelled out f, Φ, and inequality reversal. No fresh status claim.
- **cw-open-pair-distance** — Checked local README’s explicit unproved claim; added dimension/area normalization and distinction from centered radial moments. Did not perform or claim a fresh literature review.

## Source and verification scope

The local `Volume_Meissner.tex`, `Intermediary_Points_Meissner.tex` (definitions and exact area-comparison problem), and kernel-investigation README were checked against the relevant exercises. The general Meissner area formula, Cheeger characterization, sharp inner-parallel comparison, and corner equality theorem remain explicitly supplied results or linked prerequisites; this review does not re-prove those research theorems. Existing dated preprint claims in the open chapter remain attributed and are not independently established here.

The displayed bisection code was executed, giving $t_T\approx0.228028012974224$ and $h_C(T)\approx4.38542610163006$. The two unequal helper-triangle areas were evaluated independently and sum to $\pi/2$. Thirty independent numerical surface quadratures agreed with the spindle formula to maximum absolute error $4.45\times10^{-16}$; fifty random interior helper points reproduced spherical-octant area $\pi/2$. The embedded bisection code was extracted from its actual solution field and executed. `python scripts/validate.py` passed for all 127 entries; it checks structure rather than mathematical correctness. Shared builds and browser checks are handled by the main review.

## Figures and remaining limits

Existing helper-point, Meissner, and packing diagrams cover the geometric steps in these chapters. A plot of the sampled-positive but partly negative curvature density in `cw-grid-failure` was recommended to the main agent; it illustrates why a sampling margin is needed.

No unresolved mathematical defect was identified in the 30 reviewed solved entries after these changes. Four research questions remain open relative to their stated evidence. Numerical checks supplement the written arguments and do not certify all geometric constructions or the research inputs.
