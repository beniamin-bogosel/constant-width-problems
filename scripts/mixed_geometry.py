"""Polygon helpers for the mixed-area exercises and reproducible figures."""
from pathlib import Path
import sys
import numpy as np
from scipy.spatial import ConvexHull

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/constant-width-geometry/scripts'))
from cwgeom import disk_arcs, unit


def hull(points):
    points = np.asarray(points)
    return points[ConvexHull(points).vertices]


def area(vertices):
    vertices = np.asarray(vertices)
    following = np.roll(vertices, -1, axis=0)
    # Planar determinants also work with NumPy versions requiring 3D np.cross inputs.
    determinants = vertices[:, 0] * following[:, 1] - vertices[:, 1] * following[:, 0]
    return abs(np.sum(determinants)) / 2


def mixed_area(first, second):
    """Exact polygon edge formula, evaluated in floating point."""
    first, second = hull(first), hull(second)
    edges = np.roll(second, -1, axis=0) - second
    lengths = np.linalg.norm(edges, axis=1)
    normals = np.column_stack((edges[:, 1], -edges[:, 0])) / lengths[:, None]
    return np.sum(lengths * np.max(first @ normals.T, axis=0)) / 2


def tangent_polygon(vertices, width=1.):
    """Intersect endpoint tangent half-planes of a valid Reuleaux polygon."""
    vertices = np.asarray(vertices)
    angles = sorted((a % (2*np.pi)) for arc in disk_arcs(vertices, width)
                    for a in (arc.start, arc.start + arc.sweep))
    unique = []
    for a in angles:
        if not unique or a - unique[-1] > 1e-9:
            unique.append(a)
    if len(unique) > 1 and unique[0] + 2*np.pi - unique[-1] < 1e-9:
        unique.pop()
    normals = unit(np.array(unique))
    supports = np.max(vertices @ normals.T, axis=0)
    corners = []
    for i in range(len(normals)):
        j = (i+1) % len(normals)
        corners.append(np.linalg.solve(normals[[i,j]], supports[[i,j]]))
    corners = hull(corners)
    assert np.max(corners @ normals.T - supports) < 1e-8
    return corners
