#!/usr/bin/env python3
"""Draw a reproducible JSON geometry scene to SVG, PDF, or PNG."""
import argparse
import json
import math
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/cw-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc as PlotArc
import numpy as np
from cwgeom import (regular_reuleaux, irregular_reuleaux, disk_arcs,
                    boundary, arc_support, arc_area, validate_reuleaux, support_curve, unit)

plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':11,
                     'axes.titlesize':13,'savefig.facecolor':'white'})
COLORS=['#177e89','#b65b35','#735ba5','#7e9638']

def closed(points):
    return np.vstack([points,points[0]])

def transform(points, spec):
    a=spec.get('rotation',0.); R=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
    return np.asarray(points)@R.T+np.asarray(spec.get('translation',[0.,0.]))

def label(ax,p,text,offset=(6,6),color='#263238'):
    ax.annotate(text,xy=p,xytext=offset,textcoords='offset points',color=color,fontsize=11)

def draw_2d(ax,scene):
    diagnostics=[]
    for j,s in enumerate(scene.get('bodies',[])):
        kind=s['type']; color=s.get('color',COLORS[j%len(COLORS)])
        width=s.get('width',1.); arcs=None; centers=None
        if kind=='reuleaux':
            variant=s.get('variant','regular')
            if variant=='regular': centers=regular_reuleaux(s.get('n',3),width)
            elif variant=='irregular': centers=irregular_reuleaux(s.get('n',5),s.get('perturb'),width)
            elif variant=='vertices': centers=np.asarray(s['vertices'],float)
            else: raise ValueError('unknown Reuleaux variant')
            centers=transform(centers,s)
            check=validate_reuleaux(centers,width)
            radius=width-s.get('erosion',0.)
            arcs=disk_arcs(centers,radius)
            points=boundary(arcs,1500)
            diagnostics.append(dict(type=kind,erosion=s.get('erosion',0.),**check))
        elif kind=='disk-polygon':
            centers=transform(s['centers'],s);radius=s['radius']-s.get('erosion',0.)
            arcs=disk_arcs(centers,radius);points=boundary(arcs,1500)
            diagnostics.append(dict(type=kind,area=arc_area(arcs),arc_count=len(arcs)))
        elif kind=='support':
            points,check=support_curve(width,s.get('harmonics',[]));points=transform(points,s)
            diagnostics.append(dict(type=kind,**check))
        elif kind=='polygon': points=transform(s['vertices'],s)
        elif kind=='circle':
            points=transform(s['radius']*unit(np.linspace(0,2*np.pi,1000,endpoint=False)),s)
        else: raise ValueError('unknown body type '+kind)
        if s.get('construction_disks',False) and centers is not None:
            for c in centers: ax.add_patch(Circle(c,radius,fill=False,color=color,ls=':',lw=.7,alpha=.28))
        ax.fill(points[:,0],points[:,1],color=color,alpha=s.get('fill_alpha',.12),zorder=2)
        line=closed(points);ax.plot(line[:,0],line[:,1],color=color,lw=s.get('linewidth',2),ls=s.get('linestyle','-'),label=s.get('legend'),zorder=3)
        if centers is not None and s.get('show_vertices',False):
            ax.scatter(centers[:,0],centers[:,1],color=color,s=19,zorder=6)
            if s.get('vertex_polygon',False):
                line=closed(centers);ax.plot(line[:,0],line[:,1],color=color,lw=.8,ls='--')
            for i,c in enumerate(centers): label(ax,c,s.get('labels',[f'$V_{i+1}$' for i in range(len(centers))])[i])
        for theta in s.get('supports',[]):
            n=unit(theta);t=unit(theta+np.pi/2)
            if arcs is not None:
                hi=float(arc_support(arcs,theta));lo=-float(arc_support(arcs,theta+np.pi))
            else: hi=float(np.max(points@n));lo=float(np.min(points@n))
            extent=s.get('support_extent',.85*width)
            for h in (hi,lo):
                segment=np.array([h*n-extent*t,h*n+extent*t]);ax.plot(segment[:,0],segment[:,1],color='#637079',lw=1,ls='--',zorder=1)
            if s.get('width_arrow',True):
                base=-extent*.85*t
                ax.annotate('',xy=base+hi*n,xytext=base+lo*n,arrowprops=dict(arrowstyle='<->',color='#263238',lw=1))
                label(ax,base+(hi+lo)/2*n,s.get('width_label','$w$'),offset=(6,0))
    for obj in scene.get('objects',[]):
        kind=obj['type'];color=obj.get('color','#54636c');lw=obj.get('linewidth',1.1)
        if kind=='circle': ax.add_patch(Circle(obj['center'],obj['radius'],fill=False,color=color,lw=lw,ls=obj.get('linestyle','--')))
        elif kind in ('segment','line','arrow'):
            p,q=np.asarray(obj['a']),np.asarray(obj['b'])
            if kind=='line':
                direction=(q-p)/np.linalg.norm(q-p);p,q=p-obj.get('extent',1)*direction,q+obj.get('extent',1)*direction
            if kind=='arrow': ax.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle=obj.get('style','->'),color=color,lw=lw))
            else: ax.plot([p[0],q[0]],[p[1],q[1]],color=color,lw=lw,ls=obj.get('linestyle','-'))
            if obj.get('label'): label(ax,(p+q)/2,obj['label'],obj.get('offset',[5,5]),color)
        elif kind=='point':
            ax.scatter(*obj['at'],s=obj.get('size',20),color=color,zorder=7)
            if obj.get('label'): label(ax,obj['at'],obj['label'],obj.get('offset',[6,6]),color)
        elif kind=='text': label(ax,obj['at'],obj['text'],obj.get('offset',[0,0]),color)
        elif kind=='angle':
            ax.add_patch(PlotArc(obj['center'],2*obj['radius'],2*obj['radius'],theta1=np.degrees(obj['start']),theta2=np.degrees(obj['end']),color=color,lw=lw))
        else: raise ValueError('unknown annotation '+kind)
    if scene.get('legend'): ax.legend(frameon=False,loc='upper right')
    ax.set_aspect('equal');ax.axis('off');ax.margins(.14)
    if scene.get('limits'): ax.set_xlim(scene['limits'][:2]);ax.set_ylim(scene['limits'][2:])
    ax.set_title(scene.get('title',''),pad=14)
    return diagnostics

def tetrahedron():
    return np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/(2*np.sqrt(2))

def draw_3d(ax,scene):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    kind=scene['type'];check={};export_mesh=None
    if kind=='dual-edges':
        u,v=scene.get('u',.35),scene.get('v',.5)
        if not 0<u<=.5 or not 0<v<=.5: raise ValueError('u,v must be in (0,1/2]')
        h=np.sqrt(1-u*u-v*v)
        points=np.array([[0,0,-u],[0,0,u],[-v,h,0],[v,h,0],[0,0,0],[0,h,0]])
        for i,j in ((0,2),(0,3),(1,2),(1,3)):
            ax.plot(*points[[i,j]].T,color='#8b9ba3',lw=1,ls='--')
        for i,j in ((0,1),(2,3),(4,5)):
            ax.plot(*points[[i,j]].T,color='#177e89' if i<4 else '#b65b35',lw=2)
        names=['a','b','c','d','O','H']
        for p,name in zip(points,names):ax.text(*p,name,fontsize=12)
        ax.scatter(*points.T,color='#263238',s=18)
        check=dict(u=u,v=v,h=float(h),cross_distance=1.)
    elif kind=='meissner':
        from meissner_mesh import DualPairChoice, build_surface_patches, total_mesh_area, combine_meshes
        points=np.asarray(scene.get('vertices',tetrahedron()),float)
        if points.ndim!=2 or points.shape[1]!=3 or not np.all(np.isfinite(points)):raise ValueError('finite 3D vertices required')
        default=[[[2,3],[0,1]],[[1,3],[0,2]],[[1,2],[0,3]]]
        raw=scene.get('dual_pairs',default)
        if scene.get('smoothing')=='face':raw=[[b,a] for a,b in raw]
        choices=[DualPairChoice(tuple(a),tuple(b)) for a,b in raw]
        res=int(scene.get('resolution',18))
        if res<3:raise ValueError('resolution must be >=3')
        patches,seams=build_surface_patches(points,choices,face_resolution=res,longitudinal_samples=3*res,transverse_samples=res+4)
        colors={'spherical':'#80b4bc','wedge':'#b6d6d1','spindle':'#d88a62'}
        for patch in patches:
            triangles=patch.mesh.points[patch.mesh.triangles]
            collection=Poly3DCollection(triangles,facecolors=colors[patch.kind],linewidth=0,alpha=1,shade=True,lightsource=matplotlib.colors.LightSource(azdeg=125,altdeg=40))
            collection.set_edgecolor('none')
            collection.set_antialiased(False)
            ax.add_collection3d(collection)
        export_mesh=combine_meshes([p.mesh for p in patches])
        points=export_mesh.points
        check=dict(type='meissner',mesh_area=total_mesh_area(patches),triangles=len(export_mesh.triangles),approximation='Parametric patches triangulated for illustration; unwelded seams. Not a certified watertight solid.')
        if 'vertices' not in scene:
            exact=2*np.pi-np.pi*np.sqrt(3)/2*np.arccos(1/3)
            check.update(exact_area=float(exact),area_error=float(check['mesh_area']-exact))
    elif kind=='spherical-triangle':
        from meissner_mesh import slerp
        vertices=np.eye(3);q=np.array(scene.get('helper',[1,1,1]),float);q=q/np.linalg.norm(q)
        if np.any(q<=0):raise ValueError('helper must be inside the positive octant')
        # Faint spherical octant with geodesic edges and auxiliary geodesics.
        phi,theta=np.meshgrid(np.linspace(0,np.pi/2,24),np.linspace(0,np.pi/2,24))
        ax.plot_surface(np.sin(phi)*np.cos(theta),np.sin(phi)*np.sin(theta),np.cos(phi),color='#b6d6d1',alpha=.4,linewidth=0)
        for i in range(3):
            edge=np.array([slerp(vertices[i],vertices[(i+1)%3],t) for t in np.linspace(0,1,70)])
            ax.plot(*edge.T,color='#177e89',lw=2)
            spoke=np.array([slerp(q,vertices[i],t) for t in np.linspace(0,1,70)])
            ax.plot(*spoke.T,color='#b65b35',lw=1.4)
            ax.text(*vertices[i],f'$e_{i+1}$')
        ax.scatter(*q,color='#b65b35');ax.text(*q,' q')
        points=np.vstack([vertices,q,[0,0,0]])
        check=dict(area=float(np.pi/2),helper=q.tolist())
    else:raise ValueError('unknown 3D scene '+kind)
    low=points.min(axis=0);high=points.max(axis=0);center=(low+high)/2;half=max(high-low)*.6
    ax.set_xlim(center[0]-half,center[0]+half);ax.set_ylim(center[1]-half,center[1]+half);ax.set_zlim(center[2]-half,center[2]+half)
    ax.set_box_aspect((1,1,1));ax.view_init(elev=scene.get('elevation',22),azim=scene.get('azimuth',-55));ax.axis('off');ax.set_title(scene.get('title',''))
    return check,export_mesh

def render(scene,output):
    panels=scene.get('panels',[scene]);fig=plt.figure(figsize=scene.get('figsize',[6*len(panels),5]))
    diagnostics=[];meshes=[]
    for i,panel in enumerate(panels):
        is3=panel.get('type') in ('meissner','dual-edges','spherical-triangle')
        ax=fig.add_subplot(1,len(panels),i+1,projection='3d' if is3 else None)
        if is3:
            check,mesh=draw_3d(ax,panel);diagnostics.append(check);meshes.append(mesh)
        else:diagnostics.extend(draw_2d(ax,panel))
    fig.tight_layout(pad=1.2);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=200,bbox_inches='tight');plt.close(fig)
    metadata=dict(scene_title=scene.get('title',''),diagnostics=diagnostics,rendering='Floating-point geometry; samples or triangular facets used only for display.')
    output.with_suffix('.geometry.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return metadata,meshes

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene',type=Path);parser.add_argument('--output','-o',required=True,type=Path)
    parser.add_argument('--obj',type=Path,help='Optional triangle mesh export for a single Meissner scene (unwelded).')
    args=parser.parse_args();scene=json.loads(args.scene.read_text());meta,meshes=render(scene,args.output)
    if args.obj:
        if len(meshes)!=1 or meshes[0] is None:parser.error('--obj requires one Meissner scene')
        mesh=meshes[0];args.obj.parent.mkdir(parents=True,exist_ok=True)
        with args.obj.open('w') as f:
            f.write('# Unwelded illustration mesh, not a certified watertight solid\n')
            for p in mesh.points:f.write('v '+' '.join(f'{x:.12g}' for x in p)+'\n')
            for tri in mesh.triangles:f.write('f '+' '.join(str(int(i)+1) for i in tri)+'\n')
    print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
