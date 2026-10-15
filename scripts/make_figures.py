#!/usr/bin/env python3
"""Rebuild the collection's illustrations using its reusable geometry skill."""
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/constant-width-geometry/scripts'))
from draw import render
from cwgeom import regular_reuleaux
F=ROOT/'figures';(F/'scenes').mkdir(parents=True,exist_ok=True)
scenes={}
def add(name,scene,caption,alt,problems,ext='svg'):
 scenes[name]=dict(scene=scene,caption=caption,alt=alt,problems=problems,extension=ext)
tri=regular_reuleaux(3);R=1/np.sqrt(3);r=1-R
add('triangle-radii',dict(title='A width-one Reuleaux triangle',bodies=[dict(type='reuleaux',show_vertices=True,vertex_polygon=True,labels=['A','B','C'])],objects=[dict(type='circle',center=[0,0],radius=R,color='#b65b35'),dict(type='circle',center=[0,0],radius=r,color='#735ba5'),dict(type='point',at=[0,0],label='O',offset=[-16,-4]),dict(type='segment',a=[0,0],b=tri[0].tolist(),label='$R=1/\\sqrt{3}$',offset=[8,-6]),dict(type='segment',a=[0,0],b=[r,0],label='$r=1-R$',offset=[3,10])]),'The incircle and circumcircle share the symmetry center; their radii sum to the width.','Reuleaux triangle with vertex triangle, concentric inscribed and enclosing circles, and labeled radii.',['cw-triangle-measures','cw-concentric-balls','cw-inradius-extrema','cw-high-moment-counterexample'])
add('regular-family',dict(figsize=[12,4],panels=[dict(title=f'Reuleaux {n}-gon',bodies=[dict(type='reuleaux',n=n,show_vertices=False,vertex_polygon=True)]) for n in [3,5,9]]),'Regular Reuleaux polygons of width one; their areas increase toward the disk.','Three equal-width outlines: Reuleaux triangle, regular pentagon, and regular nonagon.',['cw-regular-reuleaux','cw-disk-maximizes-area'])
add('irregular-pentagon',dict(title='An irregular Reuleaux pentagon',bodies=[dict(type='reuleaux',variant='irregular',perturb=[.08,-.04],show_vertices=True,vertex_polygon=True,supports=[.35],width_arrow=True)],limits=[-.9,.9,-.8,.8]),'A perturbed and exactly closed unit-edge pentagram gives unequal boundary arc angles. The support lines remain one unit apart.','Irregular five-arc Reuleaux polygon with labeled vertices, chord polygon, and parallel supporting lines.',['cw-irregular-construction','cw-arc-polygon-area','cw-binormals'])
add('lens-intersection',dict(title='Intersection support is smaller than the minimum',bodies=[dict(type='disk-polygon',centers=[[-.5,0],[.5,0]],radius=1,construction_disks=True)],objects=[dict(type='segment',a=[-1.4,1],b=[1.4,1],linestyle='--',color='#b65b35'),dict(type='segment',a=[-.95,np.sqrt(.75)],b=[.95,np.sqrt(.75)],linestyle='--'),dict(type='point',at=[0,np.sqrt(.75)],label='$\\sqrt{1-a^2}$',offset=[8,-18]),dict(type='point',at=[-.5,0],label='$(-a,0)$'),dict(type='point',at=[.5,0],label='$(a,0)$')],limits=[-1.65,1.65,-1.15,1.35]),'Two unit disks centered at ±a on the horizontal axis; here a=1/2.','Lens formed by two overlapping unit disks, with horizontal support lines at heights one and square root of one minus a squared.',['cw-intersection-trap'])
add('smooth-support',dict(title='A smooth noncircular body of width one',bodies=[dict(type='support',harmonics=[[3,.045,0]],supports=[0,1.05])]),'Support function h(θ)=1/2+0.045 cos(3θ); curvature radius stays positive.','Rounded threefold constant-width curve with two pairs of parallel supporting lines.',['cw-odd-harmonics','cw-support-parametrization','cw-fourier-area','cw-convexity-certificate'])
add('triangle-erosion',dict(title='Inner parallel sets of the Reuleaux triangle',legend=True,bodies=[dict(type='reuleaux',erosion=t,color=c,fill_alpha=.035,legend=f't = {t:g}') for t,c in [(0,'#177e89'),(.12,'#735ba5'),(.23,'#b65b35'),(.34,'#7e9638')]]),'Erosion retains the three disk centers and reduces every disk radius from one to 1−t.','Four nested rounded triangles illustrating increasing erosion distances.',['cw-erosion-disks','cw-regular-inner-parallel','cw-perimeter-to-area','cw-cheeger-root','cw-cheeger-bisection','cw-cheeger-extrema'])
# For the upward triangle the support triple at theta=0,2pi/3,4pi/3 has zero sum.
hexagon=unit_angles=np.arange(6)*np.pi/3+np.pi/6
verts=(1/np.sqrt(3))*np.stack([np.cos(hexagon),np.sin(hexagon)],axis=1)
add('pal-hexagon',dict(title='A circumscribed regular hexagon',bodies=[dict(type='polygon',vertices=verts.tolist(),color='#b65b35',fill_alpha=.025),dict(type='reuleaux')]),'Six equally spaced supporting lines can be chosen at equal distance from a common center.','A width-one Reuleaux triangle inside its circumscribed regular hexagon.',['cw-pal-hexagon','cw-blaschke-lebesgue','cw-symmetric-cover'])
add('outer-parallel',dict(title='Outer parallel body and original body',bodies=[dict(type='support',width=1.3,harmonics=[[3,.045,0]],color='#b65b35',fill_alpha=.08),dict(type='support',width=1,harmonics=[[3,.045,0]],color='#177e89')]),'Adding a radius-0.15 disk adds 0.15 to the support function and 0.30 to the width.','Nested smooth constant-width curves representing a body and its outer parallel body.',['cw-steiner-parallel'])
add('dual-edge-helpers',dict(type='dual-edges',title='Helper midpoints for a dual edge pair',u=.35,v=.5,azimuth=-30,elevation=24),'The midpoints O and H reduce the four cross-distance constraints to h²+u²+v²=1.','Three-dimensional diagram of two perpendicular opposite edges, their midpoints, and four dashed unit cross edges.',['cw-dual-edge-coordinates','cw-dual-dihedral','cw-extremal-bookkeeping'],ext='png')
add('meissner-two-types',dict(figsize=[11,5],panels=[dict(type='meissner',title='Star smoothing',smoothing='star'),dict(type='meissner',title='Face smoothing',smoothing='face')]),'Spherical patches are blue, wedges pale green, and spindle patches orange. Both choices have the same exact area and volume. Triangulated illustrations.','Side-by-side rendered Meissner tetrahedra with the star and face choices of smoothed edges.',['cw-meissner-tetra-volume','cw-tetra-smoothings','cw-open-meissner','cw-blaschke-volume'],ext='png')
add('spherical-helper',dict(type='spherical-triangle',title='Triangulating a spherical face from q',helper=[1,1,1],elevation=24,azimuth=35),'An auxiliary interior point divides the spherical octant into three geodesic triangles.','Spherical octant with its three coordinate-axis vertices and geodesic spokes from an interior helper point.',['cw-spherical-helper','cw-spherical-partition-check'],ext='png')
# A circle-segment diagram for the spindle generator, with helper points at the axis.
a=np.pi/6;c=np.cos(a)
add('spindle-generator',dict(title='The circular generator of a spindle',objects=[dict(type='circle',center=[0,-c],radius=1),dict(type='angle',center=[0,-c],radius=1,start=np.pi/3,end=2*np.pi/3,color='#177e89',linewidth=2.5),dict(type='segment',a=[-.65,0],b=[.65,0],color='#263238'),dict(type='point',at=[-.5,0],label='A',offset=[-14,7]),dict(type='point',at=[.5,0],label='B'),dict(type='point',at=[0,-c],label='C'),dict(type='segment',a=[0,-c],b=[-.5,0],linestyle='--'),dict(type='segment',a=[0,-c],b=[.5,0],linestyle='--'),dict(type='angle',center=[0,-c],radius=.25,start=np.pi/3,end=2*np.pi/3),dict(type='text',at=[0,-.55],text='$\\theta$',offset=[-4,0])],limits=[-.75,.75,-1.05,.3]),'Rotate the minor arc AB around its chord; the distance from C to the chord is cos(θ/2).','Unit circle center below a horizontal chord, with two unit radii and the central angle marked.',['cw-spindle-area'],ext='svg')
from mixed_geometry import tangent_polygon, hull
from cwgeom import irregular_reuleaux
panels=[]
for vertices, title in [(tri, 'Triangle'), (irregular_reuleaux(5,[.08,-.04]), 'Irregular pentagon')]:
 panels.append(dict(title=title, legend=True, bodies=[
  dict(type='polygon',vertices=tangent_polygon(vertices).tolist(),color='#b65b35',fill_alpha=.035,legend='Tangent polygon C'),
  dict(type='reuleaux',variant='vertices',vertices=vertices.tolist(),color='#177e89',fill_alpha=.08,show_vertices=False,legend='Reuleaux polygon P'),
  dict(type='polygon',vertices=vertices.tolist(),color='#735ba5',fill_alpha=.13,legend='Skeleton S')],limits=[-.8,.8,-.85,.85]))
add('mixed-skeleton-tangents',dict(figsize=[11,6],panels=panels),'The skeleton S lies inside P, which lies inside the endpoint-tangent polygon C. Every convex K between S and C has the same reflected mixed area. Both panels have width-one Reuleaux polygons.','Triangle and irregular Reuleaux pentagon, each overlaid with its inner skeleton and outer tangent polygon.',['cw-triangle-hexagon-plateau','cw-reuleaux-skeleton-plateau','cw-skeleton-difference-area','cw-skeleton-area-extrema','cw-polygon-mixed-edge-sum'])
add('symmetric-hull-annulus',dict(title='The reflected hull of a centered Reuleaux triangle',legend=True,bodies=[
 dict(type='polygon',vertices=hull(np.vstack([tri,-tri])).tolist(),color='#b65b35',fill_alpha=.04,legend='Hull H'),
 dict(type='reuleaux',color='#177e89',fill_alpha=.10,show_vertices=False,legend='K'),
 dict(type='reuleaux',rotation=np.pi,color='#735ba5',fill_alpha=.08,show_vertices=False,legend='Reflection of K')],objects=[dict(type='circle',center=[0,0],radius=.5,color='#555555'),dict(type='circle',center=[0,0],radius=1/np.sqrt(3),color='#888888')],limits=[-.85,.85,-.85,.85]),'The hull H is a regular hexagon between concentric circles of radii 1/2 and 1/√3. The inner disk belongs to the hull, not necessarily to either Reuleaux triangle.','Two reflected Reuleaux triangles inside their common hexagonal convex hull, with inner and outer concentric circles.',['cw-convex-hull-mixed-identity','cw-planar-hull-objective','cw-symmetric-hull-annulus','cw-annulus-both-constraints'])
# All three copies are translates of one fixed Reuleaux triangle. Each original
# vertex is moved to the disk center in turn; tangent sectors partition the plane.
packing_bodies=[dict(type='reuleaux',translation=(-vertex).tolist(),
 color=color,fill_alpha=.17,show_vertices=False) for vertex,color in
 zip(tri,['#177e89','#b65b35','#735ba5'])]
packing_objects=[dict(type='circle',center=[0,0],radius=1,color='#263238',linestyle='-'),
 dict(type='point',at=[0,0],label='O',offset=[5,5])]
for angle in np.pi/2+np.arange(3)*2*np.pi/3:
 packing_objects.extend([
  dict(type='segment',a=[0,0],b=[np.cos(angle),np.sin(angle)],linestyle='--',color='#7a8589'),
  dict(type='angle',center=[0,0],radius=.17,start=angle,end=angle+2*np.pi/3),
  dict(type='text',at=(.34*np.array([np.cos(angle+np.pi/3),np.sin(angle+np.pi/3)])).tolist(),text='$120^\\circ$',offset=[-13,-4])])
add('three-in-unit-disk',dict(title='Three unit-width Reuleaux triangles in a unit disk',figsize=[7,7],bodies=packing_bodies,objects=packing_objects,limits=[-1.13,1.13,-1.13,1.13]),'Three translates share only the disk center O. Their tangent sectors have angle 120° and partition the full angle; the curved bodies leave gaps farther from O. Boundary contacts are allowed.','Three differently colored Reuleaux triangles in a unit-radius circle, touching at its center, with three dashed tangent rays and 120-degree angle marks.',['cw-unit-disk-packing','cw-common-point-packing','cw-fixed-shape-disk-packing'])
iv=irregular_reuleaux(5,[.08,-.04]);dist=np.linalg.norm(iv[:,None,:]-iv[None,:,:],axis=2)
i,j=np.unravel_index(np.argmax(dist),dist.shape);p,q=iv[i],iv[j]
normal=q-p;tangent=np.array([-normal[1],normal[0]])
add('two-translates-in-disk',dict(title='Two translates of an irregular Reuleaux pentagon',figsize=[7,7],bodies=[dict(type='reuleaux',variant='vertices',vertices=(iv-v).tolist(),color=color,fill_alpha=.17,show_vertices=False) for v,color in [(p,'#177e89'),(q,'#b65b35')]],objects=[dict(type='circle',center=[0,0],radius=1,color='#263238',linestyle='-'),dict(type='segment',a=(-1.03*tangent).tolist(),b=(1.03*tangent).tolist(),linestyle='--'),dict(type='point',at=[0,0],label='O')],limits=[-1.13,1.13,-1.13,1.13]),'Moving each endpoint of a diameter to O gives two translates in the unit disk. They lie on opposite sides of a common supporting line and touch only at O.','Two identical irregular Reuleaux pentagons, translated to touch at the center of a unit circle, with a dashed separating tangent line.',['cw-fixed-shape-disk-packing','cw-translate-collision','cw-enclosing-ball-core'])
scenes['triangle-erosion']['problems'].append('cw-covering-center-locus')
manifest=[]
for name,entry in scenes.items():
 path=F/'scenes'/f'{name}.json';path.write_text(json.dumps(entry['scene'],indent=2)+'\n')
 output=F/f"{name}.{entry['extension']}";render(entry['scene'],output)
 manifest.append(dict(id=name,path=str(output.relative_to(ROOT)),scene=str(path.relative_to(ROOT)),caption=entry['caption'],alt=entry['alt'],problem_ids=entry['problems'],role='illustration'))
from make_topology_figures import make_figures as make_topology_figures
manifest.extend(make_topology_figures())
from make_blaschke_figures import make_figures as make_blaschke_figures
manifest.extend(make_blaschke_figures())
from make_review_figures import make_figures as make_review_figures
manifest.extend(make_review_figures())
from make_mixed_review_figure import make_figures as make_mixed_review_figure
manifest.extend(make_mixed_review_figure())
(F/'manifest.json').write_text(json.dumps(dict(schema_version='1.0',figures=manifest),indent=2)+'\n')
for path in (ROOT/'data/chapters').glob('*/problems.json'):
 data=json.loads(path.read_text())
 for p in data['problems']:
  p['figures']=[dict(figure_id=f['id'],path=f['path'],caption_md=f['caption'],alt=f['alt']) for f in manifest if p['id'] in f['problem_ids']]
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Rebuilt {len(manifest)} illustrations and attached them to problem records.')
