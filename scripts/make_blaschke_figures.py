#!/usr/bin/env python3
"""Reproduce analytic diagrams for the Blaschke–Lebesgue proof exercises."""
import argparse
import json
import os
import sys
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/cw-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/constant-width-geometry/scripts'))
from cwgeom import regular_reuleaux, irregular_reuleaux, circle_intersections, disk_arcs, boundary, arc_support, arc_area, validate_reuleaux, unit
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':11})
BLUE='#177e89';ORANGE='#b65b35';PURPLE='#735ba5'

def J(x):return np.array([-x[1],x[0]])
def motion(v,i,t):
    n=len(v);k=n//2;j=(i+k)%n;anchor=(i-k)%n;other=(i-1)%n
    w=v.copy();d=v[i]-v[anchor];w[i]=v[anchor]+np.cos(t)*d+np.sin(t)*J(d)
    w[j]=min(circle_intersections(w[i],v[other],1),key=lambda p:np.linalg.norm(p-v[j]))
    return w

def lengths(v):
    k=len(v)//2;u=np.roll(v,-k,axis=0)-v;z=np.roll(v,k,axis=0)-v
    return np.arctan2(u[:,0]*z[:,1]-u[:,1]*z[:,0],np.sum(u*z,axis=1))

def removal(v):
    n=len(v);k=n//2;q=int(np.argmin(lengths(v)));c=(q+k)%n;d=(q-k)%n;a=(q-1)%n;b=(q+1)%n
    p=min(circle_intersections(v[a],v[b],1),key=lambda x:np.linalg.norm(x-(v[c]+v[d])/2))
    w=np.array([v[i] for i in range(n) if i not in [c,d,q]]+[p]);center=w.mean(axis=0)
    w=w[np.argsort(np.arctan2(w[:,1]-center[1],w[:,0]-center[0]))]
    return w,dict(q=v[q],c=v[c],d=v[d],a=v[a],b=v[b],p=p)

def support_polygon(h,theta):
    normals=unit(theta);n=len(h)
    return np.array([np.linalg.solve(np.array([normals[j],normals[(j+1)%n]]),[h[j],h[(j+1)%n]]) for j in range(n)])

def polygon_area(v):return abs(np.sum(v[:,0]*np.roll(v[:,1],-1)-v[:,1]*np.roll(v[:,0],-1)))/2

def outline(ax,v,color=BLUE,alpha=.08,ls='-',lw=2):
    points=boundary(disk_arcs(v),1400);closed=np.vstack([points,points[0]])
    if alpha:ax.fill(*points.T,color=color,alpha=alpha)
    ax.plot(*closed.T,color=color,lw=lw,ls=ls);ax.set_aspect('equal');ax.axis('off')

def plot_motion(config):
    v=regular_reuleaux(config['n']);i=config['index'];j=(i+len(v)//2)%len(v);w=motion(v,i,config['parameter'])
    diag=validate_reuleaux(w);fig,(ax,graph)=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    outline(ax,v,BLUE);outline(ax,w,ORANGE,.08)
    for z in range(len(v)):
        ax.scatter(*v[z],color=BLUE,s=18);ax.annotate(f'$p_{z}$',v[z],xytext=(8,5),textcoords='offset points')
    for z in (i,j):
        ax.scatter(*w[z],color=ORANGE,s=20);ax.annotate('',xy=w[z],xytext=v[z],arrowprops=dict(arrowstyle='->',color=ORANGE,lw=2))
    ax.set_title('Two moving vertices; all widths stay one')
    ts=np.linspace(-.1,.1,81);areas=[arc_area(disk_arcs(motion(v,i,t))) for t in ts]
    graph.plot(ts,areas,color=ORANGE,lw=2);graph.scatter([0],[arc_area(disk_arcs(v))],color=BLUE,zorder=3)
    graph.set(xlabel='Rotation parameter t (radians)',ylabel='Area',title='The regular pentagon is a local maximum\nalong this motion')
    graph.grid(alpha=.15);graph.spines[['top','right']].set_visible(False)
    fig.suptitle('A Blaschke deformation',fontsize=16)
    return fig,diag

def plot_removal(config):
    v=irregular_reuleaux(config['n'],config['perturb']);w,pts=removal(v);diag=validate_reuleaux(w)
    fig,axes=plt.subplots(1,2,figsize=(10.5,5.4),layout='constrained')
    outline(axes[0],v);outline(axes[1],v,BLUE,0,'--',1);outline(axes[1],w,ORANGE)
    q=pts['q'];arcs=disk_arcs(v);short=min(arcs,key=lambda a:np.linalg.norm(a.center-q));axes[0].plot(*short.points(100).T,color=PURPLE,lw=4)
    for ax in axes:
        for name,p in pts.items():
            ax.scatter(*p,color=ORANGE if name=='p' else BLUE,s=15)
            offset=(7,5) if name not in ['c','p'] else (-12,-16)
            ax.annotate('$'+name+'$',p,xytext=offset,textcoords='offset points')
        for name in ['a','b']:
            ax.plot(*np.array([pts[name],pts['p']]).T,ls=':',lw=1,color='#919c95')
    oldarea=arc_area(disk_arcs(v));axes[0].set_title(f'Before: {len(v)} arcs, area {oldarea:.6f}')
    axes[1].set_title(f'After: {len(w)} arcs, area {diag["area"]:.6f}')
    fig.suptitle('Removing a smallest arc',fontsize=16)
    diag['original_area']=oldarea;diag['area_decrease']=oldarea-diag['area']
    return fig,diag

def plot_equiangular(config):
    v=regular_reuleaux(3);arcs=disk_arcs(v);fig,axes=plt.subplots(1,3,figsize=(12,4.2),layout='constrained');rows=[]
    for ax,n in zip(axes,config['normal_counts']):
        theta=config['orientation']+np.arange(n)*2*np.pi/n;h=arc_support(arcs,theta);p=support_polygon(h,theta)
        outline(ax,v);closed=np.vstack([p,p[0]]);ax.plot(*closed.T,color=ORANGE,lw=1.6)
        ax.set_title(f'{n} equally spaced support normals');ax.set_xlim(-.8,.8);ax.set_ylim(-.7,.8)
        rows.append(dict(normal_count=n,area=polygon_area(p),perimeter=float(np.linalg.norm(np.roll(p,-1,axis=0)-p,axis=1).sum())))
    fig.suptitle('Circumscribed equiangular polygons approach the body',fontsize=16)
    return fig,dict(samples=rows,qualification='Exact support-line intersections; zero-length sides may occur at corners.')

def plot_strips(config):
    fig,axes=plt.subplots(1,3,figsize=(12,4.4),layout='constrained');theta=np.arange(6)*np.pi/3;rows=[]
    for ax,t in zip(axes,config['parameters']):
        h=.5+(-1.)**np.arange(6)*t;p=support_polygon(h,theta);closed=np.vstack([p,p[0]])
        ax.fill(*p.T,color=BLUE,alpha=.09);ax.plot(*closed.T,color=BLUE,lw=2)
        ax.set_aspect('equal');ax.axis('off');ax.set_xlim(-.8,.8);ax.set_ylim(-.8,.8)
        area=np.sqrt(3)/2-6*np.sqrt(3)*t*t;ax.set_title(f't = {t:.4f}\nArea = {area:.6f}')
        rows.append(dict(t=t,area=area,shoelace_area=polygon_area(p)))
    fig.suptitle('Three unit-width strips: regular hexagon to triangle',fontsize=16)
    return fig,dict(samples=rows)

SCENES={
 'blaschke-two-vertex':dict(n=5,index=0,parameter=.09,caption='An exact two-vertex Blaschke motion of the regular width-one pentagon. Blue is the initial body, orange the perturbed body. Areas are computed by circular-arc integration; the plot illustrates, rather than proves, the negative second variation.',alt='Initial and deformed Reuleaux pentagons beside a graph of area with a strict local maximum at the undeformed pentagon.',problems=['cw-arc-normal-integral','cw-blaschke-two-vertex-motion','cw-blaschke-negative-second-variation','cw-reuleaux-finite-compactness']),
 'smallest-arc-removal':dict(n=7,perturb=[.035,-.02,.015,-.01],caption='A shortest arc cd (purple) and opposite corner q are replaced using the unit-circle intersection p. The new body has five arcs; c and d become smooth points. Dashed blue is the previous boundary. Both bodies are constructed and checked as width-one Reuleaux polygons.',alt='An irregular seven-arc Reuleaux polygon and its five-arc replacement, with the shortest arc and points a, b, c, d, p, q labeled.',problems=['cw-shortest-arc-chord-lemma','cw-smallest-arc-removal','cw-polygon-descent-limit']),
 'equiangular-supports':dict(normal_counts=[6,12,24],orientation=.13,caption='The same Reuleaux triangle inside intersections of 6, 12 and 24 equally spaced supporting half-planes. At a corner several successive support lines can meet at one point, producing zero-length sides in the indexed polygon.',alt='Three increasingly fine circumscribed equiangular supporting polygons around one Reuleaux triangle.',problems=['cw-equiangular-support-perimeter','cw-equiangular-area-quadratic','cw-equiangular-mesh-error','cw-reuleaux-approximation-support-splice']),
 'hexagon-strip-sliding':dict(parameters=[0,.09,1/6],caption='Opposite supports remain one unit apart while the three strips slide. At the endpoint three sides vanish and an equilateral triangle remains. These straight-sided polygons are not constant-width bodies.',alt='A regular hexagon, an alternating-side hexagon, and a limiting equilateral triangle obtained by sliding three strips.',problems=['cw-hexagon-strip-sliding','cw-pal-hexagon'])}
PLOTTERS=[plot_motion,plot_removal,plot_equiangular,plot_strips]

def make_figures(output_dir=None,preview=False):
    folder=Path(output_dir) if output_dir else ROOT/'figures';(folder/'scenes').mkdir(parents=True,exist_ok=True);manifest=[]
    for (name,config),plot in zip(SCENES.items(),PLOTTERS):
        scene=dict(renderer='scripts/make_blaschke_figures.py',**config)
        (folder/'scenes'/f'{name}.json').write_text(json.dumps(scene,indent=2)+'\n')
        fig,diag=plot(config);fig.savefig(folder/f'{name}.svg')
        if preview:fig.savefig(folder/f'{name}.png',dpi=140)
        plt.close(fig);(folder/f'{name}.geometry.json').write_text(json.dumps(diag,indent=2)+'\n')
        manifest.append(dict(id=name,path=f'figures/{name}.svg',scene=f'figures/scenes/{name}.json',caption=config['caption'],alt=config['alt'],problem_ids=config['problems'],role='illustration'))
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,default=ROOT/'figures');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    make_figures(args.output_dir,args.preview);print('Rendered four Blaschke–Lebesgue figures in',args.output_dir)
