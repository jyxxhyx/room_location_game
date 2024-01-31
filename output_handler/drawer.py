import functools

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def draw_solution(file_name, grids, coords, flags):
    width = 10
    grid_nodes = [[[i, j], [i + 1, j], [i + 1, j + 1], [i, j + 1], [i, j]]
                  for i in range(grids[0]) for j in range(grids[1])]

    feasible_nodes = list()
    infeasible_nodes = list()
    all_nodes = list()
    for flag, coord in zip(flags, coords):
        i = coord[0]
        j = coord[1]
        block = [[i, j], [i + 1, j], [i + 1, j + 1], [i, j + 1], [i, j]]
        all_nodes.append(block)
        if flag:
            feasible_nodes.append(block)
        else:
            infeasible_nodes.append(block)
    fig, ax = plt.subplots()
    all_nodes = sorted(all_nodes, key=functools.cmp_to_key(compare))

    _draw_blocks(grid_nodes, width, ax, 2, 'w')
    _draw_blocks(feasible_nodes, width, ax, 2, 'b')
    _draw_blocks(infeasible_nodes, width, ax, 2, 'g')
    _draw_block_numbers(all_nodes, width, fig, 2, 'black')

    ax.set_xlim([0, grids[0] * width])
    ax.set_ylim([0, grids[1] * width])
    ax.axis('equal')
    ax.set_axis_off()
    plt.margins(0, 0)
    plt.savefig('{}.jpg'.format(file_name), bbox_inches='tight', pad_inches=0)
    plt.savefig('{}.pdf'.format(file_name), bbox_inches='tight', pad_inches=0)

    return


def _draw_blocks(blocks, width, ax, line_width, face_color):
    polygons = list()
    for block in blocks:
        polygon = [(x * width, y * width) for (x, y) in block]
        polygons.append(polygon)
    patches = [Polygon(polygon) for polygon in polygons]
    p = PatchCollection(patches,
                        facecolors=face_color,
                        edgecolors='k',
                        linewidths=line_width,
                        alpha=0.6)
    ax.add_collection(p)
    return


def _draw_block_numbers(blocks, grid_width, fig, line_width, face_color):
    for idx, rec in enumerate(blocks):
        x = (min(node[0]
                 for node in rec) + max(node[0]
                                        for node in rec)) / 2 * grid_width
        y = (min(node[1]
                 for node in rec) + max(node[1]
                                        for node in rec)) / 2 * grid_width
        size = grid_width
        plt.text(x,
                 y,
                 str(idx),
                 fontsize=size,
                 figure=fig,
                 fontweight='extra bold',
                 fontfamily='monospace',
                 va='center',
                 ha='center',
                 c=face_color)
    return


def compare(block1, block2):
    max_col_1 = max(item[1] for item in block1)
    max_col_2 = max(item[1] for item in block2)
    if max_col_1 != max_col_2:
        return -max_col_1 + max_col_2
    else:
        return max(item[0] for item in block1) - max(item[0]
                                                     for item in block2)
