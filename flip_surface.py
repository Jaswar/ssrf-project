import numpy as np
import pyvista as pv
from scipy.spatial import KDTree
from tetmesh import Tetmesh
import argparse


def main(args):
    neutral_surface = pv.PolyData(args.neutral_surface_path)
    deformed_surface = pv.PolyData(args.deformed_surface_path)
    contour = pv.PolyData(args.contour_path)
    reflected_contour = pv.PolyData(args.reflected_contour_path)
    old_deformed_surface = deformed_surface.copy()

    kdtree = KDTree(contour.points)
    _, indices_neutral = kdtree.query(neutral_surface.points)

    kdtree = KDTree(neutral_surface.points)
    _, indices = kdtree.query(reflected_contour.points)
    
    midpoint = np.mean(neutral_surface.points[:, 0])
    deformed_surface.points[:, 0] = 2 * midpoint - deformed_surface.points[:, 0]
    contour.points = deformed_surface.points[indices]

    deformed_surface.points = contour.points[indices_neutral]

    plot = pv.Plotter(shape=(1, 2))
    plot.subplot(0, 0)
    plot.add_mesh(old_deformed_surface, color='lightblue')
    plot.subplot(0, 1)
    plot.add_mesh(deformed_surface, color='lightblue')
    plot.link_views()
    plot.show()

    pv.save_meshio(args.deformed_out_path, deformed_surface)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--neutral_surface_path', type=str, required=True)
    parser.add_argument('--deformed_surface_path', type=str, required=True)
    parser.add_argument('--contour_path', type=str, required=True)
    parser.add_argument('--reflected_contour_path', type=str, required=True)
    parser.add_argument('--deformed_out_path', type=str, required=True)

    args = parser.parse_args()
    main(args)