import time
import random


def main() -> None:
    start_time = time.time()
    file_path = "./Data/point_set.xyz"
    amount_of_data = 2_000_000

    data_list = create_points((20_000, 40_000), (20_000, 40_000), (400, 500), amount_of_data)

    with open(file_path, 'w') as file:
        for line in data_list:
            file.write(line)
        print("File Created.")

    end_time = time.time()
    time_lapse = end_time - start_time
    print(f"The script ran in: {time_lapse} seconds")


def create_points(x_range:tuple, y_range:tuple, z_range:tuple, amount:int) -> list[str]:
    result = []
    for x in range(amount):
        x_value = random.randint(x_range[0], x_range[1])
        y_value = random.randint(y_range[0], y_range[1])
        z_value = random.randint(z_range[0], z_range[1])

        result.append(f"{x_value} {y_value} {z_value}\n")
    
    return result



if __name__ == "__main__":
    main()
