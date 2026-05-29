# BCD_algorithm.py
import numpy as np
from heapq import heappush, heappop


def find_cells(matrix: np.ndarray) -> list:
    transposed = matrix.T
    row_diffs = transposed[:-1] == transposed[1:]
    identical = np.all(row_diffs, axis=1)
    slices = np.where(~identical)[0]
    boundaries = [0] + list(slices + 1) + [len(transposed)]
    cells = []
    for i in range(len(boundaries) - 1):
        col_start = boundaries[i]
        col_end   = boundaries[i + 1] - 1
        sample_col = transposed[col_start]
        free_rows = list(np.where(sample_col != -1)[0])
        cells.append({
            'col_start': col_start,
            'col_end':   col_end,
            'free_rows': free_rows
        })
    return cells


def get_path(matrix: np.ndarray, start: tuple, end: tuple) -> list:
    rows, cols = matrix.shape
    if start == end:
        return []
    counter = 0
    heap = [(0, 0, counter, start, [start])]
    seen = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while heap:
        cost, _, _, (r, c), path = heappop(heap)
        if (r, c) in seen:
            continue
        seen.add((r, c))
        if (r, c) == end:
            return [(pos[0], pos[1], 'travel') for pos in path[1:-1]]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                if matrix[nr][nc] != -1:
                    if matrix[nr][nc] in (1, 2):
                        step_cost = 0
                    else:
                        step_cost = 3
                    new_cost = cost + step_cost
                    heuristic = abs(nr - end[0]) + abs(nc - end[1])
                    counter += 1
                    heappush(heap, (new_cost, heuristic, counter, (nr, nc), path + [(nr, nc)]))
    return []


def sweep_cell(matrix: np.ndarray, cell: dict, entry_col: int = None, reverse: bool = False) -> list:
    """Sweep a BCD cell in boustrophedon order.
    reverse=True: start from the last free row and sweep upward,
    so the robot enters from the bottom when snaking between cells."""
    steps = []
    col_start = cell['col_start']
    col_end   = cell['col_end']
    free_rows = cell['free_rows']

    # Reverse row order if entering from the bottom
    rows_to_sweep = list(reversed(free_rows)) if reverse else free_rows

    for i, row in enumerate(rows_to_sweep):
        if i % 2 == 0:
            # Left to right
            start_col = entry_col if (i == 0 and entry_col is not None) else col_start
            for col in range(start_col, col_end + 1):
                if matrix[row][col] == 0 or matrix[row][col] == 2:
                    matrix[row][col] = 1
                    steps.append((row, col, 'clean'))
            current_col = col_end
        else:
            # Right to left
            start_col = entry_col if (i == 0 and entry_col is not None) else col_end
            for col in range(start_col, col_start - 1, -1):
                if matrix[row][col] == 0 or matrix[row][col] == 2:
                    matrix[row][col] = 1
                    steps.append((row, col, 'clean'))
            current_col = col_start

        if i + 1 < len(rows_to_sweep):
            next_row = rows_to_sweep[i + 1]
            if abs(next_row - row) != 1:
                travel = get_path(matrix, (row, current_col), (next_row, current_col))
                steps.extend(travel)

    return steps