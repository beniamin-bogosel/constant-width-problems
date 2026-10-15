#!/usr/bin/env python3
"""Check geometric invariants, invalid inputs, and 3D patch convergence."""
import math
import unittest
import numpy as np
from cwgeom import (regular_reuleaux,irregular_reuleaux,disk_arcs,arc_area,arc_support,
                    validate_reuleaux,regular_inner_area,support_curve,spherical_triangle_area)

class GeometryChecks(unittest.TestCase):
 def test_regular_areas_perimeters_and_widths(self):
  for n in (3,5,7,11):
   for w in (.7,1.,2.3):
    d=validate_reuleaux(regular_reuleaux(n,w),w)
    self.assertAlmostEqual(d['area'],w*w/2*(math.pi-n*math.tan(math.pi/(2*n))),places=12)
    self.assertAlmostEqual(d['perimeter'],math.pi*w,places=12)
    self.assertLess(d['max_width_error'],2e-14)
 def test_irregular_closed_star(self):
  for n in (5,7,9):
   v=irregular_reuleaux(n);d=validate_reuleaux(v)
   angles=[a.sweep for a in disk_arcs(v)]
   self.assertGreater(np.ptp(angles),.001)
   self.assertLess(d['max_width_error'],1e-12)
 def test_rotation_translation_covariance(self):
  v=irregular_reuleaux();angle=.73;R=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
  transformed=v@R.T+[3,-2]
  a=validate_reuleaux(v);b=validate_reuleaux(transformed)
  self.assertAlmostEqual(a['area'],b['area'],places=12)
 def test_invalid_polygon_is_rejected(self):
  v=regular_reuleaux(5);v[0]+=[.03,0]
  with self.assertRaises(ValueError):validate_reuleaux(v)
  with self.assertRaises(ValueError):regular_reuleaux(4)
 def test_lens_support(self):
  arcs=disk_arcs([[-.5,0],[.5,0]])
  self.assertAlmostEqual(float(arc_support(arcs,math.pi/2)),math.sqrt(.75),places=12)
  self.assertAlmostEqual(arc_area(arcs),2*math.pi/3-math.sqrt(3)/2,places=12)
 def test_erosion_formula_matches_arc_integration(self):
  for n in (3,5,7):
   v=regular_reuleaux(n)
   for t in (0,.1,.23,.35):
    self.assertAlmostEqual(arc_area(disk_arcs(v,1-t)),regular_inner_area(n,t),places=12)
 def test_erosion_derivative_is_negative_perimeter(self):
  for n in (3,5):
   t=.2;eps=1e-6
   derivative=(regular_inner_area(n,t+eps)-regular_inner_area(n,t-eps))/(2*eps)
   perimeter=sum(a.radius*a.sweep for a in disk_arcs(regular_reuleaux(n),1-t))
   self.assertAlmostEqual(derivative,-perimeter,places=8)
 def test_support_curvature_guard(self):
  points,check=support_curve(1,[[3,.045,0]])
  self.assertGreater(check['convexity_margin'],0)
  with self.assertRaises(ValueError):support_curve(1,[[3,.08,0]])
  with self.assertRaises(ValueError):support_curve(1,[[2,.01,0]])
 def test_spherical_helper_independence(self):
  v=np.eye(3)
  for q in (np.ones(3),np.array([2,1,1])):
   q=q/np.linalg.norm(q)
   area=sum(spherical_triangle_area(q,v[i],v[(i+1)%3]) for i in range(3))
   self.assertAlmostEqual(area,math.pi/2,places=13)
 def test_spindle_area_quadrature(self):
  from scipy.integrate import quad
  theta=.83;phi=1.1;a=math.sin(theta/2);c=math.cos(theta/2)
  integral=phi*quad(lambda x:1-c/math.sqrt(1-x*x),-a,a)[0]
  self.assertAlmostEqual(integral,2*phi*(a-theta*c/2),places=13)
 def test_meissner_area_convergence(self):
  from meissner_mesh import DualPairChoice,build_surface_patches,total_mesh_area
  v=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/(2*math.sqrt(2))
  raw=[((2,3),(0,1)),((1,3),(0,2)),((1,2),(0,3))]
  exact=2*math.pi-math.pi*math.sqrt(3)/2*math.acos(1/3)
  for reverse in (False,True):
   choices=[DualPairChoice(b,a) if reverse else DualPairChoice(a,b) for a,b in raw]
   errors=[]
   for n in (8,18):
    patches,_=build_surface_patches(v,choices,face_resolution=n,longitudinal_samples=3*n,transverse_samples=n+4)
    errors.append(abs(total_mesh_area(patches)-exact))
   self.assertLess(errors[1],errors[0]);self.assertLess(errors[1],.003)
 def test_meissner_invalid_dual_pairs(self):
  from meissner_mesh import DualPairChoice,validate_choices
  v=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/(2*math.sqrt(2))
  with self.assertRaises(ValueError):validate_choices(v,[DualPairChoice((0,1),(2,3))]*3)
if __name__=='__main__':unittest.main(verbosity=2)
