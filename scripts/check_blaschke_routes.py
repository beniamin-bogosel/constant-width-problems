#!/usr/bin/env python3
"""Independent area/constraint checks for the new proof-route formulas."""
import json
import numpy as np
from make_blaschke_figures import ROOT,J,motion,lengths,removal,support_polygon,polygon_area
from cwgeom import regular_reuleaux,irregular_reuleaux,disk_arcs,arc_area,arc_support,validate_reuleaux

def area(v):return arc_area(disk_arcs(v))

def main():
    first_errors=[];second_errors=[];angle_errors=[];width_errors=[];reductions=[];mesh_errors=[]
    rng=np.random.default_rng(1907);bodies=[]
    for n in [5,7,9]:
        bodies.append(regular_reuleaux(n))
        bodies.append(irregular_reuleaux(n,rng.uniform(-.02,.02,n-3)))
    for v in bodies:
        n=len(v);k=n//2;ell=lengths(v)
        for i in range(n):
            j=(i+k)%n;step=2e-5;vp=motion(v,i,step);vm=motion(v,i,-step)
            for w in [vp,vm]:width_errors.append(validate_reuleaux(w)['max_width_error'])
            actual=(area(vp)-area(vm))/(2*step)
            predicted=np.sin(ell[i])*(np.tan(ell[i]/2)-np.tan(ell[j]/2))
            first_errors.append(abs(actual-predicted))
            assert abs(actual-predicted)<2e-8,(n,i,actual,predicted)
            if np.ptp(ell)<1e-10:
                step2=2e-4;vp=motion(v,i,step2);vm=motion(v,i,-step2)
                actual2=(area(vp)+area(vm)-2*area(v))/step2**2
                predicted2=2*np.tan(ell[i]/2)*(1-2*np.cos(ell[i]))
                second_errors.append(abs(actual2-predicted2));assert abs(actual2-predicted2)<2e-6
                angles=(lengths(vp)-lengths(vm))/(2*step2)
                ae=max(abs(angles[i]-(1-2*np.cos(ell[i]))),abs(angles[j]-(2*np.cos(ell[i])-1)))
                angle_errors.append(ae);assert ae<2e-6
        w=v
        while len(w)>3:
            new,pts=removal(w);diag=validate_reuleaux(new);width_errors.append(diag['max_width_error'])
            assert len(new)==len(w)-2
            gap=area(w)-area(new);assert gap>=-1e-10
            chord=np.linalg.norm(pts['a']-pts['b'])-np.linalg.norm(pts['c']-pts['d']);assert chord>=-1e-10
            reductions.append(dict(n=len(w),area_decrease=float(gap),chord_gap=float(chord)));w=new
        assert abs(area(w)-(np.pi-np.sqrt(3))/2)<1e-10
    for v in bodies+[regular_reuleaux(3)]:
        arcs=disk_arcs(v)
        for n in [4,6,12,24]:
            delta=2*np.pi/n;theta=.173+np.arange(n)*delta;h=arc_support(arcs,theta);p=support_polygon(h,theta)
            ell=(np.roll(h,1)+np.roll(h,-1)-2*np.cos(delta)*h)/np.sin(delta)
            perim=np.linalg.norm(np.roll(p,-1,axis=0)-p,axis=1).sum()
            a=sum(h*np.roll(h,-1))/np.sin(delta)-np.cos(delta)/np.sin(delta)*sum(h*h)
            err=max(abs(perim-n*np.tan(np.pi/n)),abs(a-polygon_area(p)),abs(sum(ell)-perim))
            mesh_errors.append(err);assert err<1e-10
            assert a<=n/4*np.tan(np.pi/n)+1e-10
    theta=np.arange(6)*np.pi/3
    for t in np.linspace(-1/6,1/6,21):
        h=.5+(-1.)**np.arange(6)*t;p=support_polygon(h,theta)
        assert abs(polygon_area(p)-(np.sqrt(3)/2-6*np.sqrt(3)*t*t))<1e-12
    # Analytic ODE pieces: h''+h=0 or 1, slopes match with the factor 1/2.
    for n in [3,5,7,9]:
        ell=np.pi/n;t=np.linspace(0,ell,101);z=np.cos(t-ell/2)/(2*np.cos(ell/2))
        assert abs(z[0]-.5)<1e-14 and abs(z[-1]-.5)<1e-14
        left_slope=np.sin(ell/2)/(2*np.cos(ell/2));assert abs(left_slope-.5*np.tan(ell/2))<1e-14
        assert np.all(z[1:-1]>.5)
    result=dict(first_derivatives=len(first_errors),max_first_derivative_error=max(first_errors),max_second_derivative_error=max(second_errors),max_angle_derivative_error=max(angle_errors),max_width_error=max(width_errors),arc_removal_steps=len(reductions),max_equiangular_formula_error=max(mesh_errors),reductions=reductions,qualification='Floating-point formula and construction checks, not a formal proof certificate.')
    out=ROOT/'build/blaschke-route-checks.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='reductions'},indent=2))

if __name__=='__main__':main()
