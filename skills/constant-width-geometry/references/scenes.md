# Scene format and geometry API

A scene has `title`, optional `figsize: [width_inches,height_inches]`, `bodies`, and `objects`. For multiple side-by-side views, use `panels: [scene, ...]` and set the outer `figsize`. Inputs are JSON; outputs are SVG/PDF/PNG plus a `.geometry.json` diagnostic file. LaTeX labels use Matplotlib mathtext and must escape the backslash in JSON (`"$\\theta$"`).

## 2D bodies

```json
{
  "title": "An irregular Reuleaux pentagon",
  "bodies": [{
    "type": "reuleaux", "variant": "irregular", "n": 5,
    "perturb": [0.08, -0.04], "width": 1,
    "show_vertices": true, "vertex_polygon": true,
    "supports": [0.35], "width_arrow": true
  }]
}
```

`reuleaux` variants:

- `regular`: odd `n >= 3`; default `n=3`.
- `irregular`: odd `n >= 5`; `perturb` has `n-3` angle perturbations. Omit it for a small default perturbation. The algorithm closes the last two edges by intersecting circles and rejects a configuration when the metric or arc checks fail. This produces a local family around each regular polygon, not every possible irregular polygon.
- `vertices`: supply `vertices: [[x,y], ...]` in strict convex CCW order. All cyclic opposite distances must equal `width`. The validator checks pairwise diameter, active arcs, and sampled analytic widths.

All three accept `erosion: t`, with `t` below the inradius. The centers stay fixed; the disk radius becomes `width-t`. `show_vertices` displays **generating centers**, so for an erosion those points are not vertices of the eroded body. Do not describe them as such.

Other body types:

```json
{"type":"disk-polygon","centers":[[-0.5,0],[0.5,0]],"radius":1,"construction_disks":true}
```

```json
{"type":"support","width":1,"harmonics":[[3,0.045,0],[5,0.001,0]]}
```

```json
{"type":"circle","radius":0.5,"translation":[0,0]}
```

```json
{"type":"polygon","vertices":[[0,0],[1,0],[0,1]]}
```

Common styling: `color`, `fill_alpha`, `linewidth`, `linestyle`, `legend`, `rotation` (radians), and `translation`. The last two transform the body, not independent annotation objects. For regular Reuleaux vertices use radius `width/(2*cos(pi/(2*n)))`, not `width/2`.

`supports: [angle,...]` draws supporting lines for each normal direction. Set `support_extent` for line length, `width_arrow` to toggle arrows, and `width_label` for their text. For disk polygons the supports come from analytic arcs. For a general support-curve rendering they are evaluated on its dense display samples, so use the exact Fourier formula directly if a numerical support value is needed.

## Annotation objects

- Point: `{"type":"point","at":[0,0],"label":"O","offset":[6,6]}`.
- Segment: `{"type":"segment","a":[0,0],"b":[1,0],"label":"w"}`.
- Extended line: same with `type:"line"` and `extent`.
- Arrow: same with `type:"arrow"` and optional `style:"<->"`.
- Circle: `{"type":"circle","center":[0,0],"radius":0.5}`.
- Arc/angle mark: `{"type":"angle","center":[0,0],"radius":0.2,"start":0,"end":1.0472}`. It follows increasing angle from start to end; choose the intended branch explicitly.
- Text: `{"type":"text","at":[0,0],"text":"$r$"}`.

Objects accept `color`, most accept `linewidth`, and line/circle objects accept `linestyle`. Label offsets are display points. Set scene `limits:[xmin,xmax,ymin,ymax]` if auxiliary circles would make the diagram too small. Enable `legend:true` only when body legend strings are provided.

## 3D scenes

```json
{"type":"meissner","smoothing":"star","resolution":18,"title":"Meissner tetrahedron"}
```

Use `smoothing:"face"` for the other tetrahedral type. Set `azimuth` and `elevation` in **degrees**, following Matplotlib’s camera convention. Mesh resolution controls approximation, not width. A single Meissner scene supports `--obj path/to/mesh.obj`; the OBJ has unwelded seams and is for illustration.

```json
{"type":"dual-edges","u":0.35,"v":0.5,"title":"Dual edges and their helper midpoints"}
```

```json
{"type":"spherical-triangle","helper":[1,1,1],"title":"Spherical octant triangulation"}
```

The dual-edge input has `0<u,v<=1/2`; edge lengths are `2u,2v`. Spherical helper coordinates are normalized and must be strictly positive to lie inside the illustrated octant. General spherical polygons can be assembled with `meissner_mesh.great_circle_arc`, `triangular_spherical_mesh`, and `cwgeom.spherical_triangle_area`.

## Python geometry functions

- `regular_reuleaux(n, width)` and `irregular_reuleaux(n, perturb, width)` return CCW generating vertices.
- `disk_arcs(centers, radius)` returns active oriented `Arc` objects.
- `boundary(arcs, count)` samples for drawing; `arc_support(arcs, theta)` and `arc_area(arcs)` use arc formulas.
- `validate_reuleaux(vertices, width)` returns diagnostics or raises `ValueError`.
- `support_curve(width, harmonics, samples=1200)` returns boundary samples and convexity diagnostics.
- `regular_inner_area(n, t, width)` computes regular-Reuleaux erosion area.
- `spherical_triangle_area(a,b,c)` computes an oriented solid angle. Unit vertices and a suitable hemisphere/branch are the caller’s responsibility.

The scene renderer covers common diagrams; new geometric configurations can use these functions in ordinary Matplotlib code without extending the JSON format first.
