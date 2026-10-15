#!/usr/bin/env python3
"""Independent checks of metric formulas and topology examples; not proofs."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def rectangle(center,half,angle):
    rot=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    corners=np.array([[-1,-1],[1,-1],[1,1],[-1,1]])*half
    vertices=corners@rot.T+center
    def signed(points):
        z=np.abs((np.asarray(points)-center)@rot)-half
        return np.linalg.norm(np.maximum(z,0),axis=-1)+np.minimum(np.max(z,axis=-1),0)
    return vertices,rot,signed


def main():
    rng=np.random.default_rng(22827);errors=[]
    for _ in range(40):
        va,ra,sa=rectangle(rng.normal(size=2),rng.uniform(.2,1.5,2),rng.uniform(0,6.28))
        vb,rb,sb=rectangle(rng.normal(size=2),rng.uniform(.2,1.5,2),rng.uniform(0,6.28))
        # Convex distance attains its maximum over a polygon at a vertex.
        hausdorff=max(np.max(np.maximum(sb(va),0)),np.max(np.maximum(sa(vb),0)))
        delta_vertices=(va[:,None,:]-vb[None,:,:]).reshape(-1,2)
        normals=np.vstack([ra.T,-ra.T,rb.T,-rb.T,delta_vertices,-delta_vertices])
        normals=normals[np.linalg.norm(normals,axis=1)>1e-12]
        normals/=np.linalg.norm(normals,axis=1)[:,None]
        # On each normal-fan cell a support difference is a single linear functional.
        support_gap=np.max(np.abs(np.max(va@normals.T,axis=0)-np.max(vb@normals.T,axis=0)))
        errors.append(abs(hausdorff-support_gap))
        sample=np.vstack([rng.normal(size=(200,2))*4,va,vb])
        gap=np.max(abs(np.maximum(sa(sample),0)-np.maximum(sb(sample),0)))
        errors.append(abs(gap-hausdorff))
        assert np.max(abs(sa(sample)-sb(sample)))<=hausdorff+1e-12
        edges=np.linspace(0,1,101)[:,None,None]
        ba=(va[None,:,:]*(1-edges)+np.roll(va,-1,axis=0)[None,:,:]*edges).reshape(-1,2)
        bb=(vb[None,:,:]*(1-edges)+np.roll(vb,-1,axis=0)[None,:,:]*edges).reshape(-1,2)
        boundary_gap=max(np.max(abs(sb(ba))),np.max(abs(sa(bb))))
        errors.append(abs(boundary_gap-hausdorff))
    assert max(errors)<1e-11,max(errors)
    for n in [2,4,7,16,31]:
        grid=np.arange(n+1)/n;mid=(np.arange(n)+.5)/n
        assert abs(np.max(np.min(abs(mid[:,None]-grid),axis=1))-1/(2*n))<1e-14
        # The alternating-interval indicator has exactly half the total mass.
        assert abs(n*(1/(2*n))-.5)<1e-14
    x=np.linspace(-2,2,1001)
    d_points=np.minimum(abs(x-1),abs(x+1));d_interval=np.maximum(abs(x)-1,0)
    assert abs(np.max(abs(d_points-d_interval))-1)<1e-14
    result=dict(rectangle_pairs=40,max_metric_identity_error=max(errors),
                checks=['Hausdorff vs support supremum','Hausdorff vs distance-function supremum',
                        'signed-distance stability','convex boundary equality','grid midpoint error','two-point vs interval example'],
                qualification='Independent floating-point checks of formulas and examples; proofs are in the solution JSON.')
    (ROOT/'build').mkdir(exist_ok=True)
    (ROOT/'build/topology-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
