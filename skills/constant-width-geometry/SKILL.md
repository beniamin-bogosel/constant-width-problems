---
name: constant-width-geometry
description: Draw mathematically constructed constant-width curves, regular or irregular Reuleaux polygons, disk polygons, and related geometric diagrams; render Meissner polyhedron patches in 3D. Use for geometry figures and reproducible SVG, PDF, PNG, or mesh illustrations, not decorative raster art.
---

Use the bundled geometry code to produce reproducible figures with explicit width, angles, and coordinates. Prefer SVG or PDF for 2D publication figures, PNG for shaded 3D views, and preserve the input scene beside the output.

Run from this skill directory:

```bash
python scripts/draw.py path/to/scene.json --output path/to/figure.svg
```

Requires Python with NumPy and Matplotlib >=3.7; the 3D Meissner backend also uses SciPy. Use an available environment with these packages. The scripts select a noninteractive plotting backend and do not require a display.

Read [references/scenes.md](references/scenes.md) for the scene format and examples. For custom geometry, import `scripts/cwgeom.py` and compose a scene or a Matplotlib figure. It provides circle intersections, analytic disk-polygon arcs and supports, support-function curves, circular-arc areas, erosion areas, and spherical triangle areas.

Geometry constraints that matter:

- Width is explicit, positive, and Euclidean; angles in inputs are radians. Keep equal axis scales. Scaling all coordinates by `w` scales areas by `w²` and volumes by `w³`.
- A regular Reuleaux polygon has an odd number of sides. For irregular polygons, use the closed star construction or supply convex CCW vertices satisfying the opposite-vertex constraints. Call `validate_reuleaux`; arbitrarily perturbing vertices or drawing constant-radius arcs is insufficient.
- Disk intersections need not have constant width. Erosion decreases the generating disk radii, and active arcs may disappear. `disk_arcs` detects active arcs; it rejects empty or point-only intersections. Do not label an eroded Reuleaux polygon as constant width.
- For smooth curves, use odd Fourier harmonics and require `h+h'' >= 0`. `support_curve` checks an analytic coefficient bound or a Lipschitz margin; samples alone are insufficient. Support evaluations of arc polygons are analytic up to floating-point rounding; rendered boundaries are sampled.
- In 3D distinguish a Reuleaux tetrahedron from a Meissner tetrahedron. The former is not constant width. A smoothing choice consists of a `center_edge` and its dual `spindle_edge`; these roles are not interchangeable without changing the body. Read [references/meissner.md](references/meissner.md) before using supplied non-tetrahedral data.
- Keep geometric proof separate from a rendering check. `.geometry.json` records floating-point diagnostics; triangle meshes are illustrations with unwelded seams, not certified watertight solids or proofs of constant width.

After generating a figure, inspect it visually for clipped labels, excessive construction lines, incorrect angle branches, and misleading 3D perspective. State meaningful approximation limitations in the caption. Attach a caption and alt text when adding it to a problem collection. Reuse one diagram across related problems when it explains the same construction.

To check the bundled geometric invariants:

```bash
python scripts/check_geometry.py
```
