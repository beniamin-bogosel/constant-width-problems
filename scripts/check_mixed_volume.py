#!/usr/bin/env python3
"""Independent numerical checks of the new formulas; not mathematical proofs."""
import json
import math
import numpy as np
from mixed_geometry import ROOT, hull, area, mixed_area, tangent_polygon
from cwgeom import regular_reuleaux, irregular_reuleaux, disk_arcs, arc_area


def main():
    errors = []
    for vertices in [regular_reuleaux(3), regular_reuleaux(5), regular_reuleaux(9),
                     irregular_reuleaux(5, [.08, -.04]),
                     irregular_reuleaux(7, [.02, -.03, .01, -.01])]:
        for width in (.4, 1., 2.3):
            s = vertices * width
            c = tangent_polygon(s, width)
            arcs = disk_arcs(s, width)
            m = mixed_area(s, -s)
            errors.extend([abs(m - mixed_area(c, -c)),
                           abs(m - (math.pi*width**2/2 - arc_area(arcs)))])
            diff = hull((s[:, None, :] - s[None, :, :]).reshape(-1, 2))
            errors.append(abs(area(diff) - width**2*sum(math.sin(a.sweep) for a in arcs)))
            # Interpolate in the inclusion interval using Minkowski addition.
            k = hull((.37*s[:, None, :] + .63*c[None, :, :]).reshape(-1, 2))
            errors.append(abs(mixed_area(k, -k) - m))
    rng = np.random.default_rng(732)
    for _ in range(25):
        k, l = hull(rng.normal(size=(12, 2))), hull(rng.normal(size=(11, 2)) + [1.7, -.3])
        h = hull(np.vstack([k, l]))
        errors.append(abs(area(h)-mixed_area(h,k)-mixed_area(h,l)+mixed_area(k,l)))
    assert max(errors) < 1e-11, max(errors)
    vm = math.pi*(2/3-math.sqrt(3)/4*math.acos(1/3))
    rm = 9*vm/(2*math.pi+6*vm)
    assert abs(2*math.pi*rm/(3*(3-2*rm))-vm) < 1e-14
    # Check three-dimensional normalizations on a radius-w/2 ball.
    for w in (.4, 1., 2.3):
        r=w/2; v=4*math.pi*r**3/3; surface=4*math.pi*r*r
        assert abs(2*v+6*v-4*math.pi*w**3/3) < 1e-12
        assert abs(surface/3+4*math.pi*r*r/3-2*math.pi*w*w/3) < 1e-12
    result = dict(max_polygon_identity_error=max(errors),
                  configurations='regular and irregular polygons at three scales; 25 random hull pairs',
                  meissner_volume=vm, inradius_threshold=rm,
                  chakerian_lower_bound=math.pi/3*(3*math.sqrt(6)-7),
                  qualification='Floating-point checks; proofs and explicit allowed theorems are in solutions.json.')
    (ROOT/'build').mkdir(exist_ok=True)
    (ROOT/'build/mixed-volume-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
