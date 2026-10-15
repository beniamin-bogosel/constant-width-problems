#!/usr/bin/env python3
"""Diagrams added during the full mathematical review of the collection."""
import argparse,json,os,sys
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/cw-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/constant-width-geometry/scripts'))
from cwgeom import unit,irregular_reuleaux,disk_arcs,boundary,arc_area,validate_reuleaux
from make_blaschke_figures import removal,outline
plt.rcParams.update({'svg.fonttype':'none','font.family':'DejaVu Sans','font.size':11})
BLUE='#177e89';ORANGE='#b65b35';PURPLE='#735ba5'

def circular_piece(start,end,center,count=160):
    a=np.arctan2(*(start-center)[::-1]);b=np.arctan2(*(end-center)[::-1]);delta=(b-a+np.pi)%(2*np.pi)-np.pi
    points=center+unit(np.linspace(a,a+delta,count))
    diff=end-start;integral=(center[0]*diff[1]-center[1]*diff[0]+delta)/2
    return points,integral

def cap_pieces(pts):
    a,b,c,d,p,q=(pts[k] for k in ['a','b','c','d','p','q'])
    lost=[circular_piece(a,q,c),circular_piece(q,b,d),circular_piece(b,a,p)]
    gained=[circular_piece(c,p,a),circular_piece(p,d,b),circular_piece(d,c,q)]
    return [(np.vstack([piece[0] for piece in cap]),sum(piece[1] for piece in cap)) for cap in [lost,gained]]

def plot_caps(config):
    v=irregular_reuleaux(config['n'],config['perturb']);w,pts=removal(v);(loss,la),(gain,ga)=cap_pieces(pts)
    direct=arc_area(disk_arcs(v))-arc_area(disk_arcs(w))
    assert la>0 and ga>0 and abs(la-ga-direct)<1e-12
    fig,axes=plt.subplots(1,2,figsize=(11.5,5.4),layout='constrained')
    p,q=pts['p'],pts['q'];direction=(q-p)/np.linalg.norm(q-p);pts['s']=p+direction;pts['r']=q-direction
    for ax,cap,color,title in [(axes[0],loss,ORANGE,f'Area removed: {la:.6f}'),(axes[1],gain,PURPLE,f'Area added: {ga:.6f}')]:
        outline(ax,v,BLUE,0,'--',1.3);outline(ax,w,'#737d78',0,'-',1.2)
        ax.fill(*cap.T,color=color,alpha=.65)
        ax.plot(*np.array([p,q]).T,ls=':',color='#777',lw=1)
        for name,point in pts.items():
            ax.scatter(*point,s=12,color='#384a41')
            offsets={'q':(-14,6),'s':(2,8),'r':(2,8),'p':(6,-14),'c':(-10,-16),'d':(6,7),'a':(4,7),'b':(5,-14)}
            ax.annotate('$'+name+'$',point,xytext=offsets[name],textcoords='offset points')
        ax.set_title(title)
    fig.suptitle('Curved caps in shortest-arc removal: removed area exceeds added area',fontsize=15)
    return fig,dict(removed_area=la,added_area=ga,net_difference=direct,cap_identity_error=abs(la-ga-direct),qualification='Exact circular-arc Green integrals; sampled outlines for display.')

def switching_values(theta,n):
    ell=np.pi/n;j=np.floor(theta/ell).astype(int);local=theta-(j+.5)*ell
    z=np.cos(local)/(2*np.cos(ell/2));dz=-np.sin(local)/(2*np.cos(ell/2));upper=j%2==0
    return np.where(upper,z,1-z),np.where(upper,dz,-dz),np.where(upper,0.,1.)

def plot_switching(config):
    n=config['n'];ell=np.pi/n;theta=np.linspace(0,2*np.pi,5001,endpoint=False);h,dh,rho=switching_values(theta,n)
    vertices=unit(ell/2+np.arange(n)*2*ell)/(2*np.cos(ell/2));diag=validate_reuleaux(vertices)
    fig=plt.figure(figsize=(11,5.8),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1.5,1])
    ah=fig.add_subplot(gs[0,0]);ar=fig.add_subplot(gs[1,0]);body=fig.add_subplot(gs[:,1]);points=h[:,None]*unit(theta)+dh[:,None]*unit(theta+np.pi/2)
    ah.plot(theta,h,color=BLUE,lw=2);ah.axhline(.5,color='#727c76',ls='--',lw=1)
    ah.set(title='Support function H',ylabel='H(θ)',xlim=(0,2*np.pi),ylim=(.46,.54),xticks=[0,np.pi,2*np.pi],xticklabels=['0','π','2π'])
    for j in range(2*n):
        color=ORANGE if j%2==0 else BLUE
        ah.axvspan(j*ell,(j+1)*ell,alpha=.055,color=color)
    # Exact step intervals, with vertical connectors serving only as a display convention.
    breaks=np.arange(2*n+1)*ell;values=(np.arange(2*n+1)%2).astype(float)
    ar.step(breaks,values,where='post',color=BLUE,lw=2)
    ar.set(title='Curvature radius ρ = H″ + H',xlabel='Normal angle θ',ylabel='ρ(θ)',xlim=(0,2*np.pi),ylim=(-.12,1.2),yticks=[0,1],xticks=[0,np.pi,2*np.pi],xticklabels=['0','π','2π'])
    ar.annotate('',xy=(ell,-.05),xytext=(0,-.05),arrowprops=dict(arrowstyle='<->',color=ORANGE));ar.text(ell/2,.12,'ℓ',ha='center',color=ORANGE)
    for ax in [ah,ar]:ax.spines[['top','right']].set_visible(False);ax.grid(alpha=.12)
    body.plot(*np.vstack([points,points[0]]).T,color=BLUE,lw=2);body.fill(*points.T,color=BLUE,alpha=.06);body.scatter(*vertices.T,color=ORANGE,s=30,zorder=3)
    body.plot([],[],color=BLUE,lw=2,label='ρ = 1: unit-circle arcs');body.scatter([],[],color=ORANGE,s=30,label='ρ = 0: vertices')
    body.set_aspect('equal');body.set_ylim(-.77,.62);body.axis('off');body.legend(loc='lower center',bbox_to_anchor=(.5,0),frameon=False,fontsize=10);body.set_title('The resulting regular Reuleaux pentagon')
    fig.suptitle('Equal switching intervals become equal circular arcs',fontsize=16)
    return fig,dict(**diag,interval_length=ell,endpoint_slope=.5*np.tan(ell/2),qualification='Piecewise analytic support and curvature; jump values of curvature are irrelevant a.e.')

def plot_aliasing(config):
    n=config['grid_size'];k=2*n+3;theta=np.linspace(0,2*np.pi,8001);rho=.5+np.sin(k*theta)-np.sin(3*theta);grid=np.arange(n)*2*np.pi/n
    witness=3*np.pi/(2*k);value=.5+np.sin(k*witness)-np.sin(3*witness)
    assert value<0 and np.max(abs(.5+np.sin(k*grid)-np.sin(3*grid)-.5))<1e-12
    fig,ax=plt.subplots(figsize=(11,4.5),layout='constrained');ax.plot(theta,rho,color=BLUE,lw=1.5,label=r'$\rho(\theta)=1/2+\sin(19\theta)-\sin(3\theta)$')
    ax.fill_between(theta,rho,0,where=rho<0,color=ORANGE,alpha=.28,interpolate=True);ax.axhline(0,color='#747e78',lw=1)
    ax.scatter(grid,np.full(n,.5),s=40,color=PURPLE,zorder=4,label='8 grid samples: all equal to 1/2')
    ax.scatter([witness],[value],color=ORANGE,zorder=4,s=25);ax.annotate('Negative between grid points',xy=(witness,value),xytext=(.65,-1.5),arrowprops=dict(arrowstyle='->',color=ORANGE),color=ORANGE)
    ax.set(xlim=(0,2*np.pi),ylim=(-1.8,3.2),xlabel='Normal angle θ',ylabel='Candidate curvature radius ρ',xticks=np.arange(5)*np.pi/2,xticklabels=['0','π/2','π','3π/2','2π'])
    ax.spines[['top','right']].set_visible(False);ax.legend(loc='upper right',frameon=False,fontsize=10);ax.grid(alpha=.13)
    fig.suptitle('Positive samples do not certify convexity',fontsize=16)
    return fig,dict(grid_size=n,frequency=k,witness_angle=witness,witness_curvature=value,max_sample_error=float(np.max(abs(np.sin(k*grid)-np.sin(3*grid)))),qualification='Analytic aliasing identity; dense samples used only to draw the graph.')

SCENES={
 'shortest-arc-caps':dict(n=7,perturb=[.035,-.02,.015,-.01],caption='The orange region is removed near q and the purple region is added near p. The line pq splits them into the paired curvilinear pieces used in the comparison lemma. Their boundaries include circular arcs, so straight-triangle areas would give the wrong subtraction. Dashes show the original boundary; the solid gray curve is the replacement.',alt='Two views of the same shortest-arc replacement, with the removed curved cap shaded orange and the added curved cap shaded purple; points p, q, r, s, a, b, c, d are marked.',problems=['cw-smallest-arc-removal']),
 'switching-support-curvature':dict(n=5,caption='A piecewise analytic support function for a width-one regular Reuleaux pentagon. Equal intervals alternate between curvature radius zero and one: zero intervals map to single vertices, while unit intervals trace unit-circle arcs. Curvature values at the finitely many jumps are immaterial.',alt='Support and stepwise curvature-radius graphs with equal switching intervals beside the corresponding Reuleaux pentagon, whose vertices are orange and arcs blue.',problems=['cw-curvature-bang-bang','cw-variational-switching-rule','cw-switching-ode-regularity','cw-blaschke-lebesgue-variational']),
 'curvature-aliasing':dict(grid_size=8,caption='For N=8 and k=2N+3=19, the two sine modes agree at every grid direction, so all sampled curvature values are 1/2. Between them the candidate curvature is negative on open intervals. This function cannot be the curvature radius of a convex support function despite passing the sampled inequalities.',alt='An oscillating curvature candidate crossing below zero between eight positive sample points; negative regions are shaded.',problems=['cw-grid-failure','cw-convexity-certificate'])}

def make_figures(output_dir=None,preview=False):
    folder=Path(output_dir) if output_dir else ROOT/'figures';(folder/'scenes').mkdir(parents=True,exist_ok=True);manifest=[]
    for (name,config),plot in zip(SCENES.items(),[plot_caps,plot_switching,plot_aliasing]):
        scene=dict(renderer='scripts/make_review_figures.py',**config);(folder/'scenes'/f'{name}.json').write_text(json.dumps(scene,indent=2)+'\n')
        fig,diag=plot(config);fig.savefig(folder/f'{name}.svg')
        if preview:fig.savefig(folder/f'{name}.png',dpi=140)
        plt.close(fig);(folder/f'{name}.geometry.json').write_text(json.dumps(diag,indent=2)+'\n')
        manifest.append(dict(id=name,path=f'figures/{name}.svg',scene=f'figures/scenes/{name}.json',caption=config['caption'],alt=config['alt'],problem_ids=config['problems'],role='illustration'))
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,default=ROOT/'figures');parser.add_argument('--preview',action='store_true');args=parser.parse_args();make_figures(args.output_dir,args.preview)
    print('Rendered three review diagrams in',args.output_dir)
