#!/usr/bin/env python3
"""Check packing constructions and constants; proofs live in the solution JSON."""
import json
import math
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/constant-width-geometry/scripts'))
from cwgeom import regular_reuleaux, irregular_reuleaux, disk_arcs, boundary, arc_support


def check_copies(vertices, contacts):
    points=boundary(disk_arcs(vertices),4000)
    for p in contacts:
        assert np.max(np.linalg.norm(points-p,axis=1)) <= 1+1e-10
    for i,p in enumerate(contacts):
        for q in contacts[i+1:]:
            n=q-p
            assert abs(np.linalg.norm(n)-1)<1e-10
            # Direct separating-plane check, independent of plotting.
            assert np.min((points-p)@n)>-1e-10
            assert np.max((points-q)@n)<1e-10


def main():
    tri=regular_reuleaux(3);check_copies(tri,tri)
    irr=irregular_reuleaux(5,[.08,-.04])
    distances=np.linalg.norm(irr[:,None,:]-irr[None,:,:],axis=2)
    i,j=np.unravel_index(np.argmax(distances),distances.shape)
    check_copies(irr,irr[[i,j]])
    # Compare the farthest-point and support computations at inside/outside points.
    directions=np.linspace(0,2*np.pi,24000,endpoint=False)
    normals=np.column_stack([np.cos(directions),np.sin(directions)])
    arcs=disk_arcs(tri);points=boundary(arcs,24000)
    h=arc_support(arcs,directions)
    errors=[]
    for c in np.array([[0,0],[.1,.1],[.8,.3],[-1.2,.5]]):
        far=np.max(np.linalg.norm(points-c,axis=1))
        signed=np.max(normals@c-h)
        errors.append(abs(far-(1+signed)))
    assert max(errors)<1e-7,errors
    a=1-1/math.sqrt(3);lower=(1+math.sqrt(2))*a;upper=(1+math.sqrt(2))/2
    assert 1<lower<upper
    centers=np.array([[x,y] for x in [-.5,.5] for y in [-.5,.5]])
    assert np.max(np.linalg.norm(centers,axis=1))+.5<=upper+1e-14
    assert min(np.linalg.norm(c-d) for i,c in enumerate(centers) for d in centers[i+1:])>=1
    result=dict(three_body_area=3*(math.pi-math.sqrt(3))/2,
                three_body_disk_fraction=3*(math.pi-math.sqrt(3))/(2*math.pi),
                four_body_radius_bounds=[lower,upper],
                reuleaux_lattice_density=math.pi/math.sqrt(3)-1,
                max_sampled_distance_identity_error=max(errors),
                checks=['three translated Reuleaux triangles','two translated irregular pentagons','analytic separating planes','farthest-distance identity','four-disk upper construction'],
                qualification='Floating-point checks of constructions and formulas; not a proof of optimality.')
    (ROOT/'build/packing-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
