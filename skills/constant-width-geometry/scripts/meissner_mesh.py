#!/usr/bin/env python3
"""Parametric surface meshes for small Meissner polyhedra.

The existing ProcessPolyhedra project supplies extremal-set embeddings and
dual-pair combinatorics, but it does not construct the Meissner boundary.
This module fills that gap for an explicitly supplied smoothing choice.

Conventions
-----------
For a dual pair, ``center_edge`` is the circular edge whose points are added
as unit-ball centers.  It remains a wedge.  Its dual ``spindle_edge`` is the
geometrically smoothed edge and carries a spindle surface.

An edge arc is determined by more than its endpoint pair: dangling vertices
can create a spherical digon with two distinct arcs having the same endpoints.
For this reason a smoothing choice stores both endpoint pairs explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy.spatial import ConvexHull


EPSILON = 1.0e-12


def normalized(vector: np.ndarray) -> np.ndarray:
    """Return a normalized copy of a nonzero vector."""
    vector = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(vector))
    if length <= EPSILON:
        raise ValueError("cannot normalize a zero vector")
    return vector / length


def rodrigues(vector: np.ndarray, axis: np.ndarray, angle: float) -> np.ndarray:
    """Rotate ``vector`` around a unit ``axis`` by ``angle`` radians."""
    axis = normalized(axis)
    vector = np.asarray(vector, dtype=float)
    cosine = np.cos(angle)
    sine = np.sin(angle)
    return (
        cosine * vector
        + sine * np.cross(axis, vector)
        + (1.0 - cosine) * np.dot(axis, vector) * axis
    )


def slerp(first: np.ndarray, second: np.ndarray, parameter: float) -> np.ndarray:
    """Shortest spherical interpolation between two unit vectors."""
    first = normalized(first)
    second = normalized(second)
    cosine = float(np.clip(np.dot(first, second), -1.0, 1.0))
    angle = float(np.arccos(cosine))
    if angle <= EPSILON:
        return normalized((1.0 - parameter) * first + parameter * second)
    sine = float(np.sin(angle))
    return (
        np.sin((1.0 - parameter) * angle) / sine * first
        + np.sin(parameter * angle) / sine * second
    )


def signed_rotation_angle(first: np.ndarray, second: np.ndarray, axis: np.ndarray) -> float:
    """Shortest signed angle taking ``first`` to ``second`` around ``axis``."""
    axis = normalized(axis)
    first = first - np.dot(first, axis) * axis
    second = second - np.dot(second, axis) * axis
    first = normalized(first)
    second = normalized(second)
    return float(
        np.arctan2(np.dot(axis, np.cross(first, second)), np.dot(first, second))
    )


@dataclass(frozen=True)
class DualPairChoice:
    """One selected-center edge and the dual edge smoothed by that choice."""

    center_edge: tuple[int, int]
    spindle_edge: tuple[int, int]


@dataclass
class TriangleMesh:
    """A lightweight indexed triangle mesh."""

    points: np.ndarray
    triangles: np.ndarray

    def __post_init__(self) -> None:
        self.points = np.asarray(self.points, dtype=float).reshape((-1, 3))
        self.triangles = np.asarray(self.triangles, dtype=np.int64).reshape((-1, 3))

    @property
    def area(self) -> float:
        if len(self.triangles) == 0:
            return 0.0
        vertices = self.points[self.triangles]
        cross = np.cross(vertices[:, 1] - vertices[:, 0], vertices[:, 2] - vertices[:, 0])
        return float(0.5 * np.linalg.norm(cross, axis=1).sum())


@dataclass
class SurfacePatch:
    """A colored semantic component of the Meissner boundary."""

    kind: str
    mesh: TriangleMesh
    index: int


def mesh_from_grid(grid: np.ndarray, tolerance: float = 1.0e-13) -> TriangleMesh:
    """Triangulate a rectangular point grid, discarding degenerate triangles."""
    grid = np.asarray(grid, dtype=float)
    if grid.ndim != 3 or grid.shape[2] != 3:
        raise ValueError("grid must have shape (rows, columns, 3)")
    rows, columns, _ = grid.shape
    triangles: list[tuple[int, int, int]] = []
    for i in range(rows - 1):
        for j in range(columns - 1):
            lower_left = i * columns + j
            lower_right = lower_left + 1
            upper_left = (i + 1) * columns + j
            upper_right = upper_left + 1
            triangles.append((lower_left, upper_left, lower_right))
            triangles.append((lower_right, upper_left, upper_right))

    points = grid.reshape((-1, 3))
    triangle_array = np.asarray(triangles, dtype=np.int64)
    if len(triangle_array):
        vertices = points[triangle_array]
        areas2 = np.linalg.norm(
            np.cross(vertices[:, 1] - vertices[:, 0], vertices[:, 2] - vertices[:, 0]),
            axis=1,
        )
        triangle_array = triangle_array[areas2 > tolerance]
    return TriangleMesh(points, triangle_array)


def combine_meshes(meshes: Iterable[TriangleMesh]) -> TriangleMesh:
    """Concatenate meshes without welding their boundary vertices."""
    points: list[np.ndarray] = []
    triangles: list[np.ndarray] = []
    offset = 0
    for mesh in meshes:
        if len(mesh.points) == 0:
            continue
        points.append(mesh.points)
        triangles.append(mesh.triangles + offset)
        offset += len(mesh.points)
    if not points:
        return TriangleMesh(np.empty((0, 3)), np.empty((0, 3), dtype=np.int64))
    return TriangleMesh(np.vstack(points), np.vstack(triangles))


def triangular_spherical_mesh(
    center: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
    resolution: int,
) -> TriangleMesh:
    """Mesh the geodesic triangle on the unit sphere about ``center``."""
    if resolution < 1:
        raise ValueError("resolution must be positive")
    directions = [normalized(point - center) for point in (first, second, third)]
    grid_indices: dict[tuple[int, int], int] = {}
    points: list[np.ndarray] = []
    for i in range(resolution + 1):
        for j in range(resolution + 1 - i):
            weights = np.asarray(
                [resolution - i - j, i, j], dtype=float
            ) / resolution
            direction = normalized(
                weights[0] * directions[0]
                + weights[1] * directions[1]
                + weights[2] * directions[2]
            )
            grid_indices[(i, j)] = len(points)
            points.append(center + direction)

    triangles: list[tuple[int, int, int]] = []
    for i in range(resolution):
        for j in range(resolution - i):
            triangles.append(
                (
                    grid_indices[(i, j)],
                    grid_indices[(i + 1, j)],
                    grid_indices[(i, j + 1)],
                )
            )
            if j < resolution - i - 1:
                triangles.append(
                    (
                        grid_indices[(i + 1, j)],
                        grid_indices[(i + 1, j + 1)],
                        grid_indices[(i, j + 1)],
                    )
                )
    return TriangleMesh(np.asarray(points), np.asarray(triangles))


def tangent_basis(normal: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Orthonormal basis of the plane perpendicular to ``normal``."""
    normal = normalized(normal)
    trial = np.array([1.0, 0.0, 0.0])
    if abs(float(np.dot(normal, trial))) > 0.85:
        trial = np.array([0.0, 1.0, 0.0])
    first = normalized(np.cross(normal, trial))
    return first, np.cross(normal, first)


def spherical_convex_hull(directions: np.ndarray) -> np.ndarray:
    """Cyclic vertices of a spherical convex hull contained in a hemisphere."""
    directions = np.asarray([normalized(v) for v in directions])
    if len(directions) < 3:
        return directions
    pole = normalized(np.sum(directions, axis=0))
    denominators = directions @ pole
    if np.any(denominators <= 1.0e-10):
        raise ValueError("spherical polygon is not contained in the selected hemisphere")
    first, second = tangent_basis(pole)
    projected = directions / denominators[:, None]
    coordinates = np.column_stack((projected @ first, projected @ second))
    hull = ConvexHull(coordinates)
    return directions[hull.vertices]


def spherical_face_polygon(
    center: np.ndarray,
    neighbors: np.ndarray,
    resolution: int,
) -> tuple[TriangleMesh, np.ndarray]:
    """Mesh the central geodesic polygon in one spherical face."""
    directions = spherical_convex_hull(neighbors - center)
    if len(directions) < 3:
        return TriangleMesh(np.empty((0, 3)), np.empty((0, 3), dtype=int)), directions
    interior = center + normalized(np.sum(directions, axis=0))
    pieces = []
    for index in range(len(directions)):
        first = center + directions[index]
        second = center + directions[(index + 1) % len(directions)]
        pieces.append(
            triangular_spherical_mesh(
                center, interior, first, second, resolution=resolution
            )
        )
    return combine_meshes(pieces), directions


def great_circle_arc(
    sphere_center: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    samples: int,
) -> np.ndarray:
    """Shortest geodesic arc on a unit sphere."""
    first_direction = normalized(first - sphere_center)
    second_direction = normalized(second - sphere_center)
    return np.asarray(
        [
            sphere_center + slerp(first_direction, second_direction, parameter)
            for parameter in np.linspace(0.0, 1.0, samples)
        ]
    )


def intersection_circle_arc(
    first: np.ndarray,
    second: np.ndarray,
    sphere_center_a: np.ndarray,
    sphere_center_b: np.ndarray,
    samples: int,
) -> np.ndarray:
    """Shortest arc from ``first`` to ``second`` in two unit spheres' circle."""
    axis = normalized(sphere_center_b - sphere_center_a)
    circle_center = 0.5 * (sphere_center_a + sphere_center_b)
    first_radial = first - circle_center
    second_radial = second - circle_center
    # Both radial vectors lie in the plane perpendicular to the axis.
    angle = signed_rotation_angle(first_radial, second_radial, axis)
    return np.asarray(
        [
            circle_center
            + rodrigues(first_radial, axis, parameter * angle)
            for parameter in np.linspace(0.0, 1.0, samples)
        ]
    )


def spherical_strip(
    sphere_center: np.ndarray,
    first_curve: np.ndarray,
    second_curve: np.ndarray,
    transverse_samples: int,
) -> TriangleMesh:
    """Fill the short spherical strip between corresponding unit-sphere curves."""
    if len(first_curve) != len(second_curve):
        raise ValueError("strip boundary curves must use the same number of samples")
    grid = np.empty((len(first_curve), transverse_samples, 3), dtype=float)
    for index, (first, second) in enumerate(zip(first_curve, second_curve)):
        first_direction = normalized(first - sphere_center)
        second_direction = normalized(second - sphere_center)
        for column, parameter in enumerate(np.linspace(0.0, 1.0, transverse_samples)):
            grid[index, column] = sphere_center + slerp(
                first_direction, second_direction, parameter
            )
    return mesh_from_grid(grid)


def wedge_mesh(
    points: np.ndarray,
    choice: DualPairChoice,
    longitudinal_samples: int,
    transverse_samples: int,
) -> tuple[TriangleMesh, list[np.ndarray]]:
    """Mesh both spherical halves of the wedge on ``choice.center_edge``."""
    first_index, second_index = choice.center_edge
    support_a_index, support_b_index = choice.spindle_edge
    first = points[first_index]
    second = points[second_index]
    support_a = points[support_a_index]
    support_b = points[support_b_index]
    circular = intersection_circle_arc(
        first, second, support_a, support_b, longitudinal_samples
    )
    geodesic_a = great_circle_arc(support_a, first, second, longitudinal_samples)
    geodesic_b = great_circle_arc(support_b, first, second, longitudinal_samples)
    halves = [
        spherical_strip(support_a, circular, geodesic_a, transverse_samples),
        spherical_strip(support_b, circular, geodesic_b, transverse_samples),
    ]
    return combine_meshes(halves), [circular, geodesic_a, geodesic_b]


def spindle_mesh(
    points: np.ndarray,
    choice: DualPairChoice,
    rotation_samples: int,
    generator_samples: int,
) -> tuple[TriangleMesh, list[np.ndarray]]:
    """Mesh the spindle on ``choice.spindle_edge`` as a surface of revolution."""
    center_a_index, center_b_index = choice.center_edge
    first_index, second_index = choice.spindle_edge
    center_a = points[center_a_index]
    center_b = points[center_b_index]
    first = points[first_index]
    second = points[second_index]

    axis = normalized(second - first)
    axis_point = 0.5 * (first + second)
    angle = signed_rotation_angle(center_a - axis_point, center_b - axis_point, axis)
    generator = great_circle_arc(center_a, first, second, generator_samples)

    grid = np.empty((rotation_samples, generator_samples, 3), dtype=float)
    for row, parameter in enumerate(np.linspace(0.0, 1.0, rotation_samples)):
        rotation = parameter * angle
        grid[row] = np.asarray(
            [axis_point + rodrigues(point - axis_point, axis, rotation) for point in generator]
        )
    final_generator = grid[-1].copy()
    return mesh_from_grid(grid), [generator, final_generator]


def diametric_edges(points: np.ndarray, tolerance: float = 1.0e-8) -> list[tuple[int, int]]:
    """All unordered unit-distance pairs in a diameter-one point set."""
    edges: list[tuple[int, int]] = []
    for first in range(len(points)):
        for second in range(first + 1, len(points)):
            if abs(float(np.linalg.norm(points[first] - points[second])) - 1.0) <= tolerance:
                edges.append((first, second))
    return edges


def validate_extremal(points: np.ndarray, tolerance: float = 1.0e-8) -> list[tuple[int, int]]:
    """Validate diameter one and the extremal count ``2m-2``."""
    points = np.asarray(points, dtype=float)
    pair_distances = [
        float(np.linalg.norm(points[i] - points[j]))
        for i in range(len(points))
        for j in range(i + 1, len(points))
    ]
    diameter = max(pair_distances)
    if abs(diameter - 1.0) > tolerance:
        raise ValueError(f"point set diameter is {diameter:.16g}, not one")
    edges = diametric_edges(points, tolerance=tolerance)
    expected = 2 * len(points) - 2
    if len(edges) != expected:
        raise ValueError(f"found {len(edges)} diameters; extremality requires {expected}")
    return edges


def validate_choices(
    points: np.ndarray,
    choices: Sequence[DualPairChoice],
    tolerance: float = 1.0e-8,
) -> None:
    """Check completeness and the metric conditions for supplied dual pairs."""
    if len(choices) != len(points) - 1:
        raise ValueError(
            f"found {len(choices)} dual choices; an extremal {len(points)}-point "
            f"set requires {len(points) - 1}"
        )

    pair_keys: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for number, choice in enumerate(choices):
        center_edge = tuple(sorted(choice.center_edge))
        spindle_edge = tuple(sorted(choice.spindle_edge))
        if any(index < 0 or index >= len(points) for index in center_edge + spindle_edge):
            raise ValueError(f"choice {number} contains an out-of-range vertex index")
        if center_edge[0] == center_edge[1] or spindle_edge[0] == spindle_edge[1]:
            raise ValueError(f"choice {number} contains a degenerate edge")
        if center_edge == spindle_edge:
            raise ValueError(f"choice {number} uses the same edge on both sides")
        pair_key = tuple(sorted((center_edge, spindle_edge)))
        if pair_key in pair_keys:
            raise ValueError(f"choice {number} duplicates a supplied dual pair")
        pair_keys.add(pair_key)

        for first in choice.center_edge:
            for second in choice.spindle_edge:
                distance = float(np.linalg.norm(points[first] - points[second]))
                if abs(distance - 1.0) > tolerance:
                    raise ValueError(
                        f"choice {number} is not dual: distance {first}-{second}={distance}"
                    )


def build_surface_patches(
    points: np.ndarray,
    choices: Sequence[DualPairChoice],
    face_resolution: int = 18,
    longitudinal_samples: int = 54,
    transverse_samples: int = 22,
) -> tuple[list[SurfacePatch], list[np.ndarray]]:
    """Construct spherical polygons, wedges, spindles, and their seam curves."""
    points = np.asarray(points, dtype=float)
    diameter_graph = validate_extremal(points)
    validate_choices(points, choices)

    neighbors: list[list[int]] = [[] for _ in points]
    for first, second in diameter_graph:
        neighbors[first].append(second)
        neighbors[second].append(first)

    patches: list[SurfacePatch] = []
    seam_curves: list[np.ndarray] = []
    for center_index, neighbor_indices in enumerate(neighbors):
        if len(neighbor_indices) < 3:
            continue
        mesh, boundary_directions = spherical_face_polygon(
            points[center_index], points[neighbor_indices], resolution=face_resolution
        )
        patches.append(SurfacePatch("spherical", mesh, center_index))
        for index in range(len(boundary_directions)):
            first = points[center_index] + boundary_directions[index]
            second = points[center_index] + boundary_directions[
                (index + 1) % len(boundary_directions)
            ]
            seam_curves.append(
                great_circle_arc(
                    points[center_index], first, second, longitudinal_samples
                )
            )

    for index, choice in enumerate(choices):
        wedge, wedge_curves = wedge_mesh(
            points,
            choice,
            longitudinal_samples=longitudinal_samples,
            transverse_samples=transverse_samples,
        )
        spindle, spindle_curves = spindle_mesh(
            points,
            choice,
            rotation_samples=longitudinal_samples,
            generator_samples=transverse_samples,
        )
        patches.append(SurfacePatch("wedge", wedge, index))
        patches.append(SurfacePatch("spindle", spindle, index))
        # The non-smooth circular center edge should remain visually explicit.
        seam_curves.append(wedge_curves[0])
        # Generator curves delimit a spindle from neighboring spherical patches.
        seam_curves.extend(spindle_curves)

    return patches, seam_curves


def total_mesh_area(patches: Sequence[SurfacePatch]) -> float:
    """Sum the areas of all semantic boundary patches."""
    return float(sum(patch.mesh.area for patch in patches))
