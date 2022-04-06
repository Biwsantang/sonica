from crazyslam.mapping import *

def update_grid_map(grid, ranges, angles, state, params):
    """Update the grid map given a new set on sensor data

    Args:
        grid: Grid map to be updated
        ranges: Set of range inputs from the sensor
        angles: Angles at which the range points are captured
        state: State estimate (x, y, yaw)
        params: Parameters dictionary

    Returns:
        Updated occupancy grid map
    """
    LOG_ODD_MAX = 100 #100
    LOG_ODD_MIN = -50 #-50
    LOG_ODD_OCCU = 1 #1
    LOG_ODD_FREE = 0.3 #0.3

    # compute the measured position
    targets = target_cell(state, ranges, angles)
    targets = discretize(targets, params)

    # find the affected cells
    position = discretize(state[:2], params)
    cells = bresenham_line(position.reshape(2), targets)

    # update log odds
    grid[tuple(np.array(cells).T)] -= LOG_ODD_FREE
    grid[targets[0], targets[1]] += LOG_ODD_OCCU
    grid[position[0], position[1]] = LOG_ODD_MIN #LOG_ODD_FREE

    return np.clip(grid, a_max=LOG_ODD_MAX, a_min=LOG_ODD_MIN)