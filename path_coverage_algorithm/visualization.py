import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


def animate_matrix_path(matrix: np.ndarray, all_steps: list) -> None:
    rows, cols = matrix.shape

    # colour map:
    # 0 = unvisited (white)
    # 1 = visited   (blue)
    # 2 = start     (green)
    # 3 = obstacle  (black)
    # 4 = travel    (grey)
    cmap = ListedColormap(['white', 'royalblue', 'forestgreen', 'black', 'lightgrey'])

    # build display matrix
    display = np.zeros_like(matrix, dtype=float)
    display[matrix == -1] = 3      # obstacles → black
    display[0, 0] = 2              # start → green

    fig, ax = plt.subplots(figsize=(6, 6))

    grid_display = ax.imshow(
        display, cmap=cmap, origin='upper', vmin=0, vmax=4
    )

    # grid lines
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1.5)
    ax.set_xticks(np.arange(cols))
    ax.set_yticks(np.arange(rows))
    ax.tick_params(which='major', bottom=False, left=False)

    # robot marker
    path_marker, = ax.plot([], [], 'ro', markersize=12, label="Robot")
    ax.legend(loc="upper right")
    ax.set_title("BCD Path Coverage")

    def init():
        display[matrix != -1] = 0
        display[matrix == -1] = 3
        display[0, 0] = 2
        grid_display.set_data(display)
        path_marker.set_data([], [])
        return grid_display, path_marker

    def update(frame: int):
        r, c, step_type = all_steps[frame]

        if step_type == 'clean':
            if (r, c) == (0, 0):
                display[r, c] = 2       # start stays green
            else:
                display[r, c] = 1       # visited → blue
        else:
            # travel step — only colour if not already visited/obstacle/start
            if display[r, c] == 0:
                display[r, c] = 4       # passing through → grey

        grid_display.set_data(display)
        path_marker.set_data([c], [r])
        ax.set_xlabel(
            f"Step {frame + 1}/{len(all_steps)}: [{r}, {c}] ({step_type})"
        )
        return grid_display, path_marker

    ani = animation.FuncAnimation(
        fig, update,
        frames=len(all_steps),
        init_func=init,
        interval=400,
        blit=False,
        repeat=False,
    )

    plt.show()