#!/usr/bin/env python3
"""Reproduce selected mathematical/numerical checks; these are not proofs."""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/constant-width-geometry/scripts'))
from cwgeom import regular_inner_area

def main():
 r=1-1/math.sqrt(3);lo=0.;hi=r
 for _ in range(55):
  mid=(lo+hi)/2
  if regular_inner_area(3,mid)-math.pi*mid*mid>0:lo=mid
  else:hi=mid
 t=(lo+hi)/2
 assert abs(1/t-4.385426101630063)<2e-11
 # Check sign and normalization of curvature integrals and area formulas.
 a=.045
 integral=quad(lambda x: ((.5+a*math.cos(3*x))**2-(-3*a*math.sin(3*x))**2)/2,0,2*math.pi)[0]
 assert abs(integral-(math.pi/4-4*math.pi*a*a))<1e-13
 # Independent derivatives of the angular erosion lemma and edge summand.
 q=.8;x=.31;eps=1e-4
 alpha=lambda x:math.asin(math.sin(x)/q)-x
 diff=(alpha(x+eps)-2*alpha(x)+alpha(x-eps))/eps**2
 exact=(1-q*q)*math.sin(x)/(q*q-math.sin(x)**2)**1.5
 assert abs(diff-exact)<1e-6
 f=lambda s,t:t*math.cos(t/2)*math.asin(math.sin(s/2)/math.cos(t/2))
 s=.6;t2=.9;D=1-math.sin(s/2)**2-math.sin(t2/2)**2
 diff=(f(s+eps,t2)-2*f(s,t2)+f(s-eps,t2))/eps**2
 exact=t2/4*math.cos(t2/2)*math.sin(s/2)*math.sin(t2/2)**2/D**1.5
 assert abs(diff-exact)<1e-6
 # Aliasing counterexample from cw-grid-failure.
 N=12;k=2*N+3;theta=np.arange(N)*2*np.pi/N
 assert np.max(abs(np.sin(k*theta)-np.sin(3*theta)))<1e-12
 witness=3*np.pi/(2*k)
 assert .5+math.sin(k*witness)-math.sin(3*witness)<0
 V=2*math.pi/3-math.pi*math.sqrt(3)/4*math.acos(1/3)
 result=dict(reuleaux_triangle_area=(math.pi-math.sqrt(3))/2,cheeger_radius=t,cheeger_constant=1/t,meissner_tetrahedron_volume=V,checks=['support area integral','erosion angle second derivative','edge-summand second derivative','curvature aliasing counterexample'],qualification='Floating-point regression checks; the solutions contain the mathematical arguments.')
 out=ROOT/'build';out.mkdir(exist_ok=True);(out/'formula-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
