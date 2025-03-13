import time
import math
import pandas as pd

def main():
    start_time = time.time()


    path = "./Data/point_set.xyz"
    data = None
    with open(path, 'r') as file:
        data = file.readlines()
        print("Data obtained.")
    
    x_values_list = [item.split()[0] for item in data]
    y_values_list = [item.split()[1] for item in data]
    y_min = min(y_values_list)
    y_max = max(y_values_list)
    x_min = min(x_values_list)
    x_max = max(x_values_list)

    cell_size = 10

    grid = create_grid((x_min, x_max), (y_min, y_max), cell_size)
    print(len(grid))

    end_time = time.time()
    time_lapse = end_time - start_time
    print(f"The script ran in: {time_lapse} seconds")


def create_grid(x_range:tuple, y_range:tuple, cell_size:float) -> list:
    origin = (float(x_range[0]), float(y_range[0]))
    x_axis_length = float(x_range[1]) - float(x_range[0])
    y_axis_length = float(y_range[1]) - float(y_range[0])

    x_cells = math.ceil(x_axis_length / cell_size)
    y_cells = math.ceil(y_axis_length / cell_size)

    grid = []

    for i in range(x_cells + 1):
        for j in range(y_cells + 1):
            x = origin[0] + i * cell_size
            y = origin[1] + j * cell_size
            z = 0

            grid.append([x, y, z])
    
    return grid



if __name__ == "__main__":
    main()
