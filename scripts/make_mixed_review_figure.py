#!/usr/bin/env python3
"""Reproduce the segment-sweep illustration from analytic disk and segment data."""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/tmp/cw-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCENE = {
    'renderer': 'scripts/make_mixed_review_figure.py',
    'radius': 1.0,
    'segment_length': 0.9,
    'curve_samples': 301,
    'caption': 'Adding a horizontal segment of length ℓ extends every nonempty horizontal slice by ℓ. The shaded curved band therefore has area ℓb, where b is the perpendicular width. For a radius-r disk and its diameter segment, ℓ=b=2r, giving mixed area 2r² despite the segment having zero area. Circle arcs are sampled only for rendering.',
    'alt': 'A disk before and after adding a horizontal segment. In the sum, two horizontal arrows across the added curved band both have length ell; a vertical dimension marks the disk width b.',
    'problems': ['cw-segment-mixed-area', 'cw-valuation-segment-correction'],
}


def make_figures(output_dir=None, preview=False):
    folder = Path(output_dir) if output_dir else ROOT / 'figures'
    (folder / 'scenes').mkdir(parents=True, exist_ok=True)
    name = 'mixed-segment-sweep'
    scene = folder / 'scenes' / f'{name}.json'
    scene.write_text(json.dumps(SCENE, ensure_ascii=False, indent=2) + '\n')
    r = SCENE['radius']
    ell = SCENE['segment_length']
    count = SCENE['curve_samples']
    teal, amber, ink = '#177e89', '#c47a36', '#233548'
    plt.rcParams.update({'svg.fonttype': 'none', 'font.family': 'DejaVu Sans', 'font.size': 12})
    fig, (before, after) = plt.subplots(1, 2, figsize=(11.5, 5.3))
    fig.subplots_adjust(left=.03, right=.99, top=.81, bottom=.23, wspace=.1)
    circle_theta = np.linspace(0, 2*np.pi, count)
    cx, cy = r*np.cos(circle_theta), r*np.sin(circle_theta)
    for ax in (before, after):
        ax.set_aspect('equal')
        ax.set_xlim(-1.65*r, 2.3*r)
        ax.set_ylim(-1.55*r, 1.4*r)
        ax.axis('off')
        ax.fill(cx, cy, facecolor='#d5ecee', edgecolor=teal, linewidth=1.8, zorder=1)
    before.text(-.2*r, .12*r, r'$K=rB$', ha='center', va='center', color=teal, fontsize=17)
    before.plot([-.45*r, -.45*r+ell], [-1.3*r, -1.3*r], color=amber, linewidth=3)
    before.scatter([-.45*r, -.45*r+ell], [-1.3*r, -1.3*r], color=amber, s=20)
    before.text(ell/2-.45*r, -1.5*r, r'$I=[0,\ell]e$', ha='center', color=amber)
    before.set_title('The disk and the zero-area segment', fontsize=13, pad=8)
    before.annotate('', xy=(-1.3*r, r), xytext=(-1.3*r, -r), arrowprops={'arrowstyle':'<->','color':ink})
    before.text(-1.48*r, 0, r'$b=2r$', rotation=90, ha='center', va='center', color=ink)

    theta = np.linspace(-np.pi/2, np.pi/2, count)
    rightx, y = r*np.cos(theta), r*np.sin(theta)
    # The extra band is between the original right semicircle and its translate.
    after.fill(np.r_[rightx, (rightx+ell)[::-1]], np.r_[y, y[::-1]], color='#f1d4b4', zorder=2)
    after.plot(rightx, y, color=teal, linewidth=1.5, linestyle='--', zorder=3)
    after.plot(rightx+ell, y, color=amber, linewidth=2, zorder=3)
    after.plot([0, ell], [r, r], color=amber, linewidth=2, zorder=3)
    after.plot([0, ell], [-r, -r], color=amber, linewidth=2, zorder=3)
    for height in [-.52*r, .52*r]:
        endpoint = np.sqrt(r*r-height*height)
        after.plot([-endpoint, endpoint], [height, height], color=teal, linewidth=1, alpha=.65, zorder=3)
        after.annotate('', xy=(endpoint+ell,height), xytext=(endpoint,height), arrowprops={'arrowstyle':'<->','color':'#75441b','lw':1.4}, zorder=4)
        after.text(endpoint+ell/2, height+.08*r, r'$\ell$', ha='center', va='bottom', color='#75441b', fontsize=13)
    after.text(-.4*r, .03*r, r'$K$', ha='center', va='center', color=teal, fontsize=18)
    after.text((r+ell/2), 0, 'Added\nband', ha='center', va='center', color='#75441b', fontsize=11)
    after.set_title('The sum: each slice gains the same length', fontsize=13, pad=8)
    fig.suptitle('Why a segment contributes to mixed area', fontsize=17, color=ink)
    fig.text(.5, .13, r'$A(K+I)-A(K)=\ell b=2A(K,I)$', ha='center', fontsize=17, color=ink)
    fig.text(.5, .045, r'For a disk and its diameter: $\ell=b=2r$, so $A(rB,I)=2r^2$.', ha='center', fontsize=12, color=ink)
    output = folder / f'{name}.svg'
    fig.savefig(output)
    if preview:
        fig.savefig(folder / f'{name}.png', dpi=150)
    plt.close(fig)
    diagnostic = {
        'geometry': 'Exact disk and horizontal-segment sum; sampled curves only for rendering',
        'radius': r,
        'segment_length': ell,
        'perpendicular_width': 2*r,
        'added_area': 2*r*ell,
        'mixed_area': r*ell,
        'disk_diameter_mixed_area': 2*r*r,
    }
    (folder / f'{name}.geometry.json').write_text(json.dumps(diagnostic, indent=2) + '\n')
    return [dict(id=name, path='figures/'+output.name, scene='figures/scenes/'+scene.name,
                 caption=SCENE['caption'], alt=SCENE['alt'], problem_ids=SCENE['problems'], role='illustration')]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT/'figures')
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    make_figures(args.output_dir, args.preview)
    print('Rendered the mixed-area segment-sweep figure in', args.output_dir)
