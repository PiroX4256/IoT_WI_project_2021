from parse import *


def print_coords(dataset):
    missing = []
    for i in range(0, 10, 2):
        for j in range(0, 10, 2):
            if (i, j) not in dataset.keys():
                missing.append((i, j))
                continue
            print('{}, {}: {}'.format(i, j, dataset[(i, j)]))

    if len(missing) != 0:
        print('Missing values:')
        for item in missing:
            print(item)
    else:
        print('There is no missing value!')


def get_dataset(filename):
    dataset_local = {}
    with open(filename) as f:
        for line in f.readlines():
            result = parse('{},{} {}|{}|{}|{}|{}|{}', line)

            if result is not None:
                x, y = float(result[0]), float(result[1])
                rssi_str = [result[i] for i in range(2, 7)]
                dataset_local[(x, y)] = rssi_str
            else:
                print('Parser error: \n' + line)

    return dataset_local


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dataset = get_dataset('dataset.dat')
    print_coords(dataset)
