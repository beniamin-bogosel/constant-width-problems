# Henrot–Pierre: set topologies and distance functions

The local book is Antoine Henrot and Michel Pierre, *Shape Variation and Optimization: A Geometrical Analysis*, EMS Tracts in Mathematics 28 (2018), ISBN 978-3-03719-178-1. This is the English edition corresponding to the user's “Shape Variation and Analysis” reference. Machine-specific location and fingerprint are in local-inventory.json (retained locally, excluded from Git); the PDF is not redistributed.

This pass inspected Chapter 2, principally §§2.2.2–2.2.6 (printed pp. 27–45) and selected exercises in §2.5 (pp. 61–65). It adds **16 exercises** to Generalities, with independently written hints and short proofs. It does not claim coverage of the BV/perimeter development in §2.3 or the uniform-cone results in §2.4. All proofs remain checked drafts awaiting human review.

## Reading path and conventions

Start with distance functions, then the Hausdorff identity, then the existing support-function identity. Follow with sequential convergence, set operations, nested limits, and the compact selection theorem. The domain exercises then compare complementary Hausdorff convergence, compact convergence, and convergence of indicators. Finish with convex volume and boundary stability.

| Objects | Distance or convergence | What it retains |
| --- | --- | --- |
| Nonempty compact sets | Hausdorff distance, equal to the uniform distance between distance functions | The entire closed set; convexity is unnecessary |
| Nonempty compact convex sets | Uniform distance between support functions | Exactly the same metric as Hausdorff distance; support functions of nonconvex sets only retain their convex hulls |
| Bounded open domains | Hausdorff distance between compact complements in a containing ball | Equivalently uniform distance between clearance functions; detects punctures |
| Measurable sets in a bounded region | Measure of symmetric difference | A metric only after identifying sets equal almost everywhere; equivalent to every finite indicator Lp convergence |
| Open domains, compact convergence | Eventual containment of compact interior and exterior subsets | Uses the exterior of the closure; distinct open sets can have the same limit sequence |

For nonempty compact convex K,L, the three quantities agree:

$$d_H(K,L)=\|h_K-h_L\|_{L^\infty(\mathbb S^{d-1})}=\|d_K-d_L\|_{L^\infty(\mathbb R^d)}.$$

The second equality with distance functions extends to arbitrary nonempty compact sets. The support-function equality is already present in the collection and retains Schneider as its primary source; Henrot–Pierre supplies the connection with distance functions, not an attribution for every convex companion result.

## Exercise-to-book mapping

Locators use printed page numbers. “Companion” or “specialization” means a short extension developed for this collection rather than a claim that the book states that exact exercise.

| Exercise | Chapter 2 locator |
| --- | --- |
| [A set encoded by its distance function](https://beniamin-bogosel.github.io/constant-width-problems/#cw-distance-function-basics) | §2.2.3.1, Definition 2.2.7, p. 30; proof of Theorem 2.2.25, p. 44 |
| [Hausdorff distance is uniform distance between distance functions](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-distance-functions) | Proposition 2.2.27 and equation (2.28), p. 43; equation (2.15), p. 33 |
| [Distance to a convex body from its support function](https://beniamin-bogosel.github.io/constant-width-problems/#cw-distance-from-support) | Distance-function framework, §2.2.6.1, pp. 43–44; convex support-function companion |
| [Recognizing a Hausdorff limit by convergent points](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-sequential) | §2.2.3.2, properties (3)–(4), pp. 32–33 |
| [Convex hull and union are stable; intersection need not be](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-set-operations) | Exercise 2.5, p. 63; compact-set Hausdorff properties in §2.2.3.2 |
| [Nested compact sets converge to the expected limit](https://beniamin-bogosel.github.io/constant-width-problems/#cw-nested-compact-limits) | §2.2.3.2, compact-set properties (1)–(2), p. 32 |
| [Compactness of sets from Arzelà–Ascoli](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-selection) | Theorem 2.2.25 and Proposition 2.2.27, pp. 42–44 |
| [Open domains: measure distance between the complements](https://beniamin-bogosel.github.io/constant-width-problems/#cw-complementary-hausdorff) | Definitions 2.2.8–2.2.10, pp. 30–31; Lemma 2.2.12 and Remarks 2.2.11–2.2.14, pp. 31–32 |
| [Compact subsets survive domain convergence](https://beniamin-bogosel.github.io/constant-width-problems/#cw-domain-interior-persistence) | Proposition 2.2.17 and Remark 2.2.18, p. 35; Proposition 2.2.23, pp. 41–42 |
| [One grid, three different notions of convergence](https://beniamin-bogosel.github.io/constant-width-problems/#cw-grid-topology-counterexample) | §2.2.5, third counterexample and equation (2.24), pp. 40–41 |
| [Compact convergence can have two different open limits](https://beniamin-bogosel.github.io/constant-width-problems/#cw-compact-domain-convergence) | Definition 2.2.21, p. 38; §2.2.5, first counterexample, p. 39; Exercise 2.7, p. 63 |
| [Symmetric difference and convergence of indicators](https://beniamin-bogosel.github.io/constant-width-problems/#cw-indicator-set-distance) | Proposition 2.2.1 and Remarks 2.2.4–2.2.5, pp. 27–29; Exercise 2.10(1)–(2), p. 64 |
| [Fine alternating intervals converge to a density, not a set](https://beniamin-bogosel.github.io/constant-width-problems/#cw-oscillating-indicators) | Exercise 2.1, p. 61; Proposition 2.2.28, p. 45 (uniform-cell variant) |
| [Convexity restores volume convergence](https://beniamin-bogosel.github.io/constant-width-problems/#cw-convex-hausdorff-volume) | Exercise 2.2, p. 61; volume counterexamples in §2.2.3.2, p. 37; convex specialization |
| [For convex bodies, boundary distance equals body distance](https://beniamin-bogosel.github.io/constant-width-problems/#cw-convex-boundary-distance) | Exercise 2.4(1)–(2), p. 62; convex specialization |
| [Diameter and enclosing radius are Lipschitz stable](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-geometric-stability) | Exercise 2.2, p. 61; compact-set topology in §2.2.3.2; radius companions |

The existing [Hausdorff/support-function exercise](https://beniamin-bogosel.github.io/constant-width-problems/#cw-hausdorff-support) now gives all three norm formulas and a nonconvex counterexample. The existing [least-volume existence exercise](https://beniamin-bogosel.github.io/constant-width-problems/#cw-compactness) now links the selection and convex-volume exercises as prerequisites.

## Hypotheses and notation checked

- Compact-set distance formulas here use nonempty sets. Open-domain complementary distance includes the empty domain: its clearance is zero and its distance from a domain is the inradius.
- Sequential compactness and the recovery-point criterion use a common compact containing set. Without confinement, points or parts of sets can escape to infinity.
- The maximum over K ∪ L in Proposition 2.2.27 is interpreted as a genuine pointwise supremum, not a Lebesgue essential supremum on a possibly lower-dimensional set. Global distance functions are continuous, so the global supremum does equal the essential supremum.
- Definition 2.2.21 was checked visually in the scanned page: exterior test compacts lie outside the **closure** of the limit domain, and eventually outside the closures of the approximating domains. This explains the nonunique punctured-ball example.
- Weak-* convergence of indicators to an indicator yields strong finite-Lp convergence on a bounded region and almost-everywhere convergence of a **subsequence**. It does not imply almost-everywhere convergence of the whole sequence. For example, enumerate all dyadic intervals of each level consecutively: their indicators tend to zero in Lp, but each point of [0,1) belongs to one interval at every level. The exercise does not repeat an unqualified full-sequence a.e. conclusion.
- Alternating intervals converge weak-* in L∞ to a fractional density. This is explicitly weak-* convergence, rather than a claim about the Banach-space weak topology of L∞.
- Convex volume estimates using a multiplicative sandwich require a positive inradius of the limit. Lower-dimensional limits are handled separately. Equality of boundary and body Hausdorff distances is stated for convex bodies with nonempty interior.

These exercises concern geometric set topologies. No implication about convergence of PDE solutions, capacity, or Γ-convergence is asserted without additional assumptions.

## Figures and checks

Two reproducible vector plots illustrate the distance-function gap for two endpoints versus their interval, and compact grids versus punctured open intervals. They are attached to the corresponding problems in the HTML reader and [figure gallery](../figures/gallery.md).

Run `python scripts/make_topology_figures.py` to regenerate these plots alone, or `python scripts/make_figures.py` to rebuild every collection figure and its problem attachments. These two plot scenes use the renderer named in their JSON, rather than the constant-width drawing skill's scene parser.

`python scripts/check_topologies.py` checks metric identities on random rotated rectangles, signed-distance bounds, the two-point example, and exact grid midpoints. Its report is `build/topology-checks.json`. These computations supplement the proofs; they are not mathematical certificates. The usual structural validator and HTML checks also cover all new entries.
