# Blaschke–Lebesgue review — 15 October 2026

Reviewed all 26 statements, hints, and solutions. Revised 24 entries. Status remains checked-draft; this is an AI mathematical review, not human sign-off.

## Main findings

- Corrected the missing nonnegative erosion-time bound and positive interval-length hypothesis.
- Corrected pointwise/a.e. wording in the moment-duality problem and a malformed Fourier parity label.
- Expanded the closure, ODE, and equality steps in the variational route, including the missing C¹,¹ regularity bridge for arbitrary minimizers, identified by an independent reviewer.
- Proved finite-class closedness, removing one external hypothesis from the polygon compactness exercise.
- Specified the curved cap pieces in shortest-arc removal; the surgery/comparison lemma itself remains a supplied premise.

## Entry-by-entry record

| ID | Review outcome |
| --- | --- |
| `cw-disk-maximizes-area` | Made constant width and positive normalization explicit. |
| `cw-angle-convexity` | Explained branch validity, positivity of the first derivative, and strict convexity at the endpoint. |
| `cw-convex-budget` | Specified a positive interval length and a finite list; explained impossible equality when too few terms are available. |
| `cw-local-perimeter-comparison` | Added the missing lower bound on erosion time and treated the zero-time endpoint. |
| `cw-perimeter-to-area` | Stated the needed absolute continuity and wrote the backward integral explicitly. |
| `cw-blaschke-lebesgue` | Made constant width explicit and unpacked monotonicity in both mixed-area arguments. |
| `cw-curvature-moment-constraints` | Added the distributional curvature-measure proof that every width-one support is C¹,¹; clarified a.e. conditions and closure moments. |
| `cw-support-area-second-variation` | Repaired a malformed Fourier parity label and made the function regularity explicit. |
| `cw-curvature-bang-bang` | Explained the measurable slack set and why the perturbation preserves all constraints. |
| `cw-two-moment-duality` | Corrected pointwise wording to almost everywhere and explained the dual vector and zero-set freedom. |
| `cw-variational-switching-rule` | Distinguished the first-order necessary condition from a sufficient test for minimality. |
| `cw-switching-ode-regularity` | Filled the a.e.-ODE regularity and interval-counting steps. |
| `cw-blaschke-lebesgue-variational` | Explained why the comparison classifies all equality cases, not just the selected minimizer. |
| `cw-arc-normal-integral` | Made the vector integration and normal-velocity convention explicit. |
| `cw-blaschke-two-vertex-motion` | Unpacked the shared-diameter velocity equation and local nature of the motion. |
| `cw-blaschke-negative-second-variation` | Explained the two-sided local-minimum test and why the derivative formula can be differentiated. |
| `cw-reuleaux-finite-compactness` | Replaced the assumed closedness of finite Reuleaux classes with a proof using their disk centers. |
| `cw-shortest-arc-chord-lemma` | Explained why the nontriangular case has strict base-angle bounds. |
| `cw-smallest-arc-removal` | Defined the lost/gained curvilinear pieces and separated local surgery from its iterated limit. |
| `cw-support-parallel-regularization` | Checked; statement and concise proof retained. |
| `cw-reuleaux-approximation-support-splice` | Explained the contact-point identity behind both uniform bounds and degenerate splice pieces. |
| `cw-polygon-descent-limit` | Checked; statement and concise proof retained. |
| `cw-equiangular-support-perimeter` | Explained indexed zero-length sides and the absence of a circular perimeter argument. |
| `cw-equiangular-area-quadratic` | Made the discrete spectrum and equality kernel explicit. |
| `cw-hexagon-strip-sliding` | Clarified active constraints and why the endpoint triangles are outside the constant-width class. |
| `cw-equiangular-mesh-error` | Separated the two directed inclusions and covered the radial zero case. |

## Remaining explicit inputs

Polygonal density, the geometric center-existence step in the support splice, and the shortest-arc surgery/comparison lemma remain explicitly allowed source results. The support-function variational route uses the stated finite-dimensional subgradient formula. No full lower equiangular comparison is claimed. These are dependencies of the exercises, not unstated completed proofs.
