# Meissner backend and conventions

The bundled `scripts/meissner_mesh.py` is copied, without mathematical modification, from the user's `MeissnerSandbox/meissner_visualization.py`. The source snapshot and SHA-256 are recorded below. It provides parametrized spherical polygons, wedges, and spindle surfaces, triangulated for display. Its useful distinction is semantic: adding centers along a circular `center_edge` leaves that side as a wedge and smooths the dual `spindle_edge`.

A general input scene supplies unit-diameter `vertices` and `dual_pairs`, each `[[center_endpoint_1,center_endpoint_2],[spindle_endpoint_1,spindle_endpoint_2]]`. All indices are zero-based. There must be `m-1` choices for `m` extremal generating points. The four cross distances in each pair must equal one. Example for the default tetrahedron:

```json
{
  "type": "meissner",
  "dual_pairs": [[[2,3],[0,1]], [[1,3],[0,2]], [[1,2],[0,3]]],
  "resolution": 18
}
```

For custom vertices, supply the dual pairs from an established combinatorial construction. The backend checks diameter, extremal pair count, duplicate pairs, indices, and cross distances. These checks do **not** prove that arbitrary supplied combinatorics form a complete valid ball-polyhedron boundary. In particular, nonstandard or dangling-point cases may require care with digons and distinct arcs having the same endpoints. Never infer the whole dual structure from the count alone.

The rendering uses Euclidean chords of surface patches. Its mesh area should converge with refinement. For a unit-width Meissner tetrahedron compare it with

`S = 2*pi - pi*sqrt(3)/2*acos(1/3)`.

Exact constant-width volume follows from `V = S/2 - pi/3`; substituting the **mesh** area only gives a numerical estimate. An exported OBJ concatenates patch vertices and is not welded, so closed-solid volume routines and 3D-printing pipelines require a separate mesh repair/verification step.

For the scalar edge contribution this collection uses

`f(s,t) = t*cos(t/2)*asin(sin(s/2)/cos(t/2))`,

with `S = 2*pi - 2*sum(f)`. Some references put the factor 2 inside `f`; do not combine the two conventions.

Source snapshot SHA-256: `6b52fa4e175f5d53f81ec0ce61799e02400655eaba379772d6d1cc8ef6690485`.
