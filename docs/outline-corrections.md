# Corrections and qualifications to CWbook2.pdf

These are editorial findings from the June 9, 2025 draft. The PDF itself is unchanged. References use its printed exercise numbers/pages. The collection incorporates corrected versions where relevant.

| Location | Issue | Treatment |
| --- | --- | --- |
| Introduction, p. 5 | Reuleaux triangle said to minimize the Cheeger constant | It **maximizes** it at fixed constant width. The disk minimizes it. See `cw-cheeger-extrema`. |
| Exercise 1.2(iv), p. 9 | Area integral misses a factor | Use `A = (1/2) ∫(h²−h′²)`. See `cw-support-parametrization`. |
| Exercise 1.4(ii), p. 9 | Support of an intersection identified with pointwise minimum | Only `h(K∩L) ≤ min(hK,hL)` holds generally. A two-disk lens is a counterexample. |
| Exercise 1.7(iii), p. 10 | Boundary measure limit ends with `H^(d−1)(K)` | Intended limit is `H^(d−1)(∂K)` for a full-dimensional limiting convex body. |
| Exercise 1.9(iii), p. 11 | Closedness alone used to assert attainment | Need compactness or suitable coercivity/boundedness modulo translation. The fixed-width existence exercise explicitly normalizes translation and proves boundedness. |
| Exercise 1.13(ii), p. 12 | Corner angle inequality is reversed or convention ambiguous | With **interior angle**, use at least 120°; exterior turning is at most 60°. Equality characterizes the triangle. |
| Exercise 1.16, p. 13 | Incircle and circumcircle said to “coincide” | Their **centers** coincide; their radii add to the width. The circles themselves generally differ. |
| Exercise 1.18(ii), p. 13 | Inclusion between two constant-width shapes implies equality | Add “of the same width”; differently sized disks are a counterexample without this qualification. |
| Definition 2.1 / X_n, p. 15 | Unit-distance equalities alone treated as a sufficient polygon specification | Also require the correct convex cyclic order, diameter bound, active opposite arcs, and nondegeneracy. The construction code validates these. |
| Exercise 2.2, p. 16 | Dimension of X_n stated as n−3 without quotient | With n independent edge constraints on 2n coordinates, generic local dimension is n. Dimension n−3 is after quotienting by planar rigid motions. Independence and a nondegenerate neighborhood must be justified. Not imported as an established theorem here. |
| Exercise 2.3(i), p. 16 | Regular Reuleaux areas said to decrease | They **increase** toward the disk area. See `cw-regular-reuleaux`. |
| Exercise 2.3(ii), p. 16 | “arbitrary regular” and vertex-area formula | Recast as the more useful general convex arc-polygon segment formula. |
| Exercise 2.5(ii), p. 16 | Attainment needs translations controlled | Normalize a center or a marked point before applying compactness. |
| Exercise 2.9, p. 18 | “Young” / inradius formulation | The applicable result is **Jung's circumradius bound**. The planar proof is `cw-jung-plane`. |
| Exercise 2.11(iv), p. 18 | Unit Reuleaux triangle inradius written (3−√3)/2 | Correct value is `1−1/√3 = (3−√3)/3`. |

Additional source-reading care:

- Strict convexity/increase of the Cheeger angle function requires `t>0`; at `t=0` the function is identically zero.
- A fixed active-arc erosion formula is not automatically valid after arcs disappear. The local comparison exercise states that restriction.
- The blog universal-cover mixed-area argument requires a **centrally symmetric** container throughout. It is not a proof of optimality among all convex universal covers.
- Different Meissner references absorb a factor 2 into the scalar edge function. This collection fixes `S=2π−2Σf` with `f(s,t)=t cos(t/2) asin(sin(s/2)/cos(t/2))`.
- A local draft or a numerical experiment is not evidence of a completed proof. Strong-criticality and pair-distance questions remain explicitly qualified.
