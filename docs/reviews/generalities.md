# Generalities review — 2026-10-15

Reviewer: **ChatGPT 6 Astra**. This is an additional AI mathematical and exposition review, not human certification. All 35 entries were read together with their hints, complete proof drafts, prerequisites, and source labels. The `checked-draft` and `ready-for-review` statuses remain unchanged.

The pass changed the statement, proof, or prerequisite links of **18 entries** (15 received mathematical/expository text changes; three received prerequisite links only). All 35 solution records identify this review in `checked_by`. Stable IDs and source attributions were preserved.

The main repairs supply a previously implicit support-function reconstruction lemma, justify the zero-curvature endpoint of the Fourier family, complete the Reuleaux-triangle equality step in the corner theorem, and derive volume minimizer existence from the chapter’s already-proved Hausdorff selection theorem. They also distinguish strict convexity from smoothness and make several boundary/empty-set cases explicit. No false theorem or unresolved logical gap was identified in these 35 entries under their stated prerequisites.

## Entry-by-entry record

| Entry | Review result |
| --- | --- |
| [cw-distance-function-basics](https://beniamin-bogosel.github.io/constant-width-problems/#cw-distance-function-basics) | Checked closure invariance, zero sets, reversed inclusion, and union formula for nonempty sets; no change needed. |
| [cw-hausdorff-distance-functions](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-distance-functions) | Checked attainment and the pointwise supremum convention on possibly null sets; no change needed. |
| [cw-support-calculus](https://beniamin-bogosel.github.io/constant-width-problems/#cw-support-calculus) | Added the half-space reconstruction and support-order criterion used repeatedly throughout the chapter. |
| [cw-hausdorff-support](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-support) | Checked the three identities, the factor two for widths, and circle/disk counterexample; no change needed. |
| [cw-distance-from-support](https://beniamin-bogosel.github.io/constant-width-problems/#cw-distance-from-support) | Explained why the support margin is the interior boundary distance, rather than merely asserting it. |
| [cw-hausdorff-sequential](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-sequential) | Checked both directed-distance arguments and the common compact confinement hypothesis; no change needed. |
| [cw-hausdorff-set-operations](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-set-operations) | Checked Carathéodory compactness, convex-combination error estimate, and segment-intersection counterexample; no change needed. |
| [cw-nested-compact-limits](https://beniamin-bogosel.github.io/constant-width-problems/#cw-nested-compact-limits) | Checked nonempty decreasing intersection and confinement for increasing unions; no change needed. |
| [cw-hausdorff-selection](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-selection) | Checked the nonempty zero set and nearest-point identification of the limit distance function; no change needed. |
| [cw-complementary-hausdorff](https://beniamin-bogosel.github.io/constant-width-problems/#cw-complementary-hausdorff) | Checked containing-ball independence, the empty domain, and punctured-ball distance one; no change needed. |
| [cw-domain-interior-persistence](https://beniamin-bogosel.github.io/constant-width-problems/#cw-domain-interior-persistence) | Handled the empty compact subset before taking a positive minimum. |
| [cw-grid-topology-counterexample](https://beniamin-bogosel.github.io/constant-width-problems/#cw-grid-topology-counterexample) | Checked both exact distances and the distinct closure, indicator, and complement limits; no change needed. |
| [cw-compact-domain-convergence](https://beniamin-bogosel.github.io/constant-width-problems/#cw-compact-domain-convergence) | Checked the complement-of-closure definition and null-boundary local dominated-convergence argument; no change needed. |
| [cw-indicator-set-distance](https://beniamin-bogosel.github.io/constant-width-problems/#cw-indicator-set-distance) | Checked the quotient by null sets, weak-* test functions, and subsequential (not full-sequence) almost-everywhere convergence; no change needed. |
| [cw-oscillating-indicators](https://beniamin-bogosel.github.io/constant-width-problems/#cw-oscillating-indicators) | Checked weak-* density argument, failure of strong convergence, and clearance factor 1/(4n); no change needed. |
| [cw-convex-hausdorff-volume](https://beniamin-bogosel.github.io/constant-width-problems/#cw-convex-hausdorff-volume) | Clarified the lower-dimensional volume limit without assuming monotonicity of the Hausdorff errors; handled the empty compact subset. |
| [cw-convex-boundary-distance](https://beniamin-bogosel.github.io/constant-width-problems/#cw-convex-boundary-distance) | Linked the grid counterexample explicitly as a prerequisite. |
| [cw-hausdorff-geometric-stability](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-geometric-stability) | Checked constants, the r below delta case for inradius, and sharpness using concentric balls; no change needed. |
| [cw-intersection-trap](https://beniamin-bogosel.github.io/constant-width-problems/#cw-intersection-trap) | Made compactness, convexity, and nonempty-intersection hypotheses explicit and linked support calculus. |
| [cw-difference-body](https://beniamin-bogosel.github.io/constant-width-problems/#cw-difference-body) | Spelled out the Minkowski-combination conclusion and its degenerate zero-coefficient case. |
| [cw-binormals](https://beniamin-bogosel.github.io/constant-width-problems/#cw-binormals) | Excluded the zero chord, made diameter attainment explicit, and distinguished strict convexity from smoothness. |
| [cw-central-symmetry](https://beniamin-bogosel.github.io/constant-width-problems/#cw-central-symmetry) | Linked the support reconstruction used in the proof. |
| [cw-projections](https://beniamin-bogosel.github.io/constant-width-problems/#cw-projections) | Specified intrinsic width and excluded the zero-dimensional subspace, which has no unit directions. |
| [cw-concentric-balls](https://beniamin-bogosel.github.io/constant-width-problems/#cw-concentric-balls) | Expanded the optimization over centers and justified that the common center is inside the body. |
| [cw-ball-intersection](https://beniamin-bogosel.github.io/constant-width-problems/#cw-ball-intersection) | Checked the separating opposite contact point and the direction of the spindle inclusion; no change needed. |
| [cw-support-parametrization](https://beniamin-bogosel.github.io/constant-width-problems/#cw-support-parametrization) | Replaced the initially assumed differentiability of the contact map with a direct support-inequality derivation; expanded the orientation and area calculation. |
| [cw-barbier](https://beniamin-bogosel.github.io/constant-width-problems/#cw-barbier) | Checked the factor two in projected boundary variation and the explicitly permitted perimeter-continuity step; no change needed. |
| [cw-odd-harmonics](https://beniamin-bogosel.github.io/constant-width-problems/#cw-odd-harmonics) | Proved the curvature criterion directly, justified endpoint cases where the strict-positive-curvature prerequisite does not apply, and strengthened the uncountability explanation. |
| [cw-corner-angle](https://beniamin-bogosel.github.io/constant-width-problems/#cw-corner-angle) | Made the turning-angle range explicit and supplied the constant-width fact about the Reuleaux triangle needed for the equality case. |
| [cw-pal-hexagon](https://beniamin-bogosel.github.io/constant-width-problems/#cw-pal-hexagon) | Expanded the step from three equations to six supporting sides, including why the circumscription is tangential. |
| [cw-packing-two](https://beniamin-bogosel.github.io/constant-width-problems/#cw-packing-two) | Specified positive similarity scales and wrote the separating inequalities that justify adding projection lengths. |
| [cw-compactness](https://beniamin-bogosel.github.io/constant-width-problems/#cw-compactness) | Replaced the unexplained sublinear-support representation step by the already-proved Hausdorff selection theorem; verified the limit is full-dimensional and the minimizing class is nonempty. |
| [cw-enclosing-ball-core](https://beniamin-bogosel.github.io/constant-width-problems/#cw-enclosing-ball-core) | Checked the common positive-radius ball and the endpoint R=w, where only a common point follows; no change needed. |
| [cw-farthest-nearest-duality](https://beniamin-bogosel.github.io/constant-width-problems/#cw-farthest-nearest-duality) | Linked the signed-distance lemma that supplies the two branches. |
| [cw-covering-center-locus](https://beniamin-bogosel.github.io/constant-width-problems/#cw-covering-center-locus) | Checked erosion/parallel-body signs, empty eroded sets, and the shared endpoint R=w; no change needed. |

## Figures and verification

The existing distance-function, punctured-grid, support-curve, concentric-ball, and circumscribed-hexagon figures remain suitable for the revised arguments. No new global figure or manifest was added by this review. A future signed-distance diagram could show an interior point, its nearest supporting line, and the largest centered inball; the proof now gives the full argument without relying on such a figure.

Chapter-local JSON checks confirmed 35 distinct problem IDs, matching solution IDs, nonempty hints and proof bodies, and preserved draft status. All prerequisite links resolve in the collection, and the dependency graph has no cycle. Full schema, formula rendering, HTML, and browser checks are performed by the coordinating review pass after the parallel edits are merged.

The mathematical review is analytical rather than a numerical proof check. In particular the endpoint area formula is now justified by Hausdorff/volume continuity, not inferred from sampling.

## Independent check of the variational proof chain

At the coordinating reviewer’s request, this pass also read `cw-two-moment-duality`, `cw-variational-switching-rule`, `cw-switching-ode-regularity`, and `cw-blaschke-lebesgue-variational`, with their curvature-moment and area-variation prerequisites. No chapter 03 files were edited by this reviewer.

The finite-dimensional duality argument is valid with its explicitly permitted subgradient formula: coercivity yields a minimizing multiplier, its zero subgradient supplies a feasible selector, and equality in the integral inequality forces the sign rule almost everywhere. The half-circle moment reduction and objective pairing in the switching rule are correct. Nonzero endpoint derivatives in the ODE argument exclude zero plateaus, force equal neighboring interval lengths, and yield the odd regular-polygon classification. The monotonicity of the regular polygon areas completes the stated equality characterization.

Two gaps in presentation were reported to the coordinating reviewer. First, the sign rule for measurable minimizers must say “almost everywhere,” since changing a function at an isolated point leaves every constraint and objective unchanged; that wording has been corrected. Second, the chain needs to justify that an arbitrary minimizing support is `C^{1,1}` before applying the curvature formulation. Its nonnegative distributional curvature measure and its antipodal translate sum to `dθ`, so the curvature measure has a density between zero and one; consequently `h'' = ρ − h` is essentially bounded. The coordinating reviewer has added this bridge to `cw-curvature-moment-constraints`, with the distributional support characterization an explicit prerequisite. A malformed Parseval summation label was also reported and corrected by that reviewer.

The revised `cw-reuleaux-finite-compactness` was independently checked as well. Passing the finitely many disk centers to a subsequence gives one inclusion. Interpolating toward a common interior point gives uniform slack in all limiting disks, establishing the reverse inclusion for nearby centers. The resulting finite intersection has at most the original number of active unit-circle arcs: each circle’s admissible parameter intervals are short geodesically convex arcs, whose intersection is connected. No gap was found in this replacement for the previously supplied finite-class closedness assertion. Its proof explicitly retains polygonal density as an external input and does not claim that density alone settles arbitrary equality cases.
