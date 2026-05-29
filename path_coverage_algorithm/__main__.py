# main.py
from .matrix import Matrix
from .BCD_algorithm import find_cells, sweep_cell, get_path
from .visualization import animate_matrix_path


if __name__ == "__main__":
    n = Matrix()
    print("\n--- Original Matrix ---")
    n.print_Matrix()

    cells = find_cells(n.matrix)
    # Filter empty cells, then sort strictly left to right by col_start
    ordered_cells = sorted(
        [c for c in cells if c['free_rows']],
        key=lambda c: c['col_start']
    )

    all_steps   = []
    current_pos = (0, 0)
    going_right = True  # snake direction: first cell sweeps top-down, alternate

    for cell in ordered_cells:
        # Choose entry point based on sweep direction to minimise travel
        if going_right:
            entry_row = cell['free_rows'][0]
        else:
            entry_row = cell['free_rows'][-1]
        entry_col = cell['col_start']
        target = (entry_row, entry_col)

        if current_pos != target:
            travel = get_path(n.matrix, current_pos, target)
            all_steps.extend(travel)
            current_pos = target

        cell_steps = sweep_cell(n.matrix, cell, entry_col=current_pos[1], reverse=not going_right)
        all_steps.extend(cell_steps)

        if cell_steps:
            current_pos = (cell_steps[-1][0], cell_steps[-1][1])

        going_right = not going_right  # flip for next cell

    travel_count = sum(1 for _, _, t in all_steps if t == 'travel')
    clean_count  = sum(1 for _, _, t in all_steps if t == 'clean')
    print(f"\n--- Step Breakdown ---")
    print(f"Clean steps:  {clean_count}")
    print(f"Travel steps: {travel_count}")
    print(f"Total steps:  {len(all_steps)}")
    if all_steps:
        print(f"Travel %:     {travel_count / len(all_steps) * 100:.1f}%")

    print("\n--- Launching Animation ---")
    animate_matrix_path(n.matrix, all_steps)