#!/usr/bin/env python3
"""Reproduce the distance-function and domain-topology plots from analytic data."""
import argparse
import json
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/cw-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
COLORS=['#177e89','#b65b35','#735ba5']
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':11})
SCENES={
 'distance-functions':dict(renderer='scripts/make_topology_figures.py',endpoints=[-1,1],x_limits=[-2.3,2.3],
  caption='The endpoints and the filled interval have the same convex hull and support function, but different distance functions. Their Hausdorff distance is one, attained by the distance-function gap at x=0.',
  alt='Graphs of distance to two endpoints and distance to the interval between them; their maximum vertical difference is one at the origin.',
  problems=['cw-distance-function-basics','cw-hausdorff-distance-functions','cw-hausdorff-support']),
 'grid-domain-topologies':dict(renderer='scripts/make_topology_figures.py',grid_sizes=[4,8,16],
  caption='Filled dots represent G_n; hollow dots are removed from the open interval Ω_n. As n grows, the compact grids fill [0,1], while the domain clearances shrink uniformly to zero. Removed points are shown with enlarged markers, not positive-length holes.',
  alt='Three progressively finer grids, the corresponding punctured intervals, and their triangular clearance graphs decreasing in height.',
  problems=['cw-grid-topology-counterexample','cw-complementary-hausdorff','cw-domain-interior-persistence','cw-convex-boundary-distance'])}


def plot_distance(config):
    a,b=config['endpoints'];x=np.linspace(*config['x_limits'],1601)
    endpoint_distance=np.minimum(abs(x-a),abs(x-b))
    interval_distance=np.maximum(np.maximum(a-x,x-b),0)
    fig,(sets,ax)=plt.subplots(2,1,figsize=(9,6),gridspec_kw={'height_ratios':[1,3]},layout='constrained')
    sets.plot([a,b],[0,0],color=COLORS[1],lw=5)
    sets.scatter([a,b],[.65,.65],color=COLORS[0],s=65)
    sets.text(b+.15,.65,r'$K=\{-1,1\}$',va='center',color=COLORS[0])
    sets.text(b+.15,0,r'$L=[-1,1]$',va='center',color=COLORS[1])
    sets.set_xlim(-2.3,2.7);sets.set_ylim(-.3,1);sets.axis('off')
    ax.plot(x,endpoint_distance,color=COLORS[0],lw=2.4,label=r'$d_K(x)$')
    ax.plot(x,interval_distance,color=COLORS[1],lw=2,ls='--',label=r'$d_L(x)$')
    ax.annotate('',xy=(0,1),xytext=(0,0),arrowprops={'arrowstyle':'<->','color':COLORS[2],'lw':1.7})
    ax.text(.12,1.12,r'$d_H(K,L)=1$',color=COLORS[2])
    ax.set(xlim=config['x_limits'],ylim=(-.06,1.5),xlabel=r'$x$',ylabel='Distance')
    ax.set_xticks([-2,-1,0,1,2]);ax.spines[['top','right']].set_visible(False)
    ax.grid(alpha=.15);ax.legend(loc='upper right',frameon=False)
    fig.suptitle('Distance functions detect the missing interval',fontsize=16)
    return fig


def plot_grid(config):
    sizes=config['grid_sizes'];fig,axes=plt.subplots(len(sizes),2,figsize=(11,6.5),layout='constrained')
    for row,n in enumerate(sizes):
        ax,graph=axes[row];grid=np.arange(n+1)/n
        ax.scatter(grid,np.ones(n+1),color=COLORS[0],s=22,zorder=3)
        ax.plot([0,1],[0,0],color=COLORS[1],lw=3)
        ax.scatter(grid,np.zeros(n+1),facecolors='white',edgecolors=COLORS[1],s=28,zorder=3)
        ax.text(-.055,1,r'$G_{%d}$'%n,ha='right',va='center',color=COLORS[0])
        ax.text(-.055,0,r'$\Omega_{%d}$'%n,ha='right',va='center',color=COLORS[1])
        ax.set(xlim=(-.18,1.06),ylim=(-.55,1.55));ax.axis('off')
        # Endpoints and exact midpoint peaks: this is the exact piecewise-linear graph.
        x=np.arange(2*n+1)/(2*n);y=np.where(np.arange(2*n+1)%2,1/(2*n),0)
        graph.plot(x,y,color=COLORS[1],lw=1.8)
        graph.set(xlim=(0,1),ylim=(0,.17),yticks=[0,1/8],xticks=[0,.5,1])
        graph.text(.98,.151,r'$\max q_{\Omega_n}=1/(2n)$',ha='right',fontsize=10)
        graph.spines[['top','right']].set_visible(False);graph.grid(alpha=.15)
    axes[0,0].set_title('A compact grid and an open punctured interval')
    axes[0,1].set_title('Clearance to the complement')
    axes[-1,1].set_xlabel(r'$x$')
    fig.suptitle('The same grid produces different set limits',fontsize=16)
    return fig


def make_figures(output_dir=None, preview=False):
    folder=Path(output_dir) if output_dir else ROOT/'figures'
    (folder/'scenes').mkdir(parents=True,exist_ok=True);manifest=[]
    for name,config in SCENES.items():
        scene=folder/'scenes'/f'{name}.json';scene.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
        fig=(plot_distance if name=='distance-functions' else plot_grid)(config)
        output=folder/f'{name}.svg';fig.savefig(output)
        if preview:fig.savefig(folder/f'{name}.png',dpi=150)
        plt.close(fig)
        manifest.append(dict(id=name,path='figures/'+output.name,scene='figures/scenes/'+scene.name,
                             caption=config['caption'],alt=config['alt'],problem_ids=config['problems'],role='illustration'))
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'figures')
    parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    make_figures(args.output_dir,args.preview)
    print('Rendered two topology figures in',args.output_dir)
