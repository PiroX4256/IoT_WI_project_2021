from parse import *
import math


def get_computed_dataset(filename):
    dataset_local = {}
    with open(filename) as f:
        for line in f.readlines():
            result = parse('{},{} [{}, {}, {}, {}, {}, {}]', line)

            if result is not None:
                x, y = float(result[0]), float(result[1])
                rssi_str = [[int(n) for n in result[i].strip('\n').split(',')] for i in range(2, 8)]
                dataset_local[(x, y)] = rssi_str
            else:
                print('Parser error: \n' + line)

    return dataset_local

'''
For each antenna, find closest point to Nemo and create a polygon of closest points
    then compute centroid of the polygon.
'''
def get_distances(nemo_rssi, dataset, debug=False):
    out = {}
    # for each antenna, nearest coordinates
    closest_points = []
    for anchor in range(0, 6):
        distances = []
        for i in range(0, 11, 2):
            for j in range(0, 11, 2):
                if (i, j) not in dataset.keys():
                    continue
                distances.append(math.fabs(nemo_rssi[anchor] - dataset[(i, j)][anchor]))

        min_distance = min(distances)
        all_keys_min_distance = [key for key, value in dataset.items() if math.fabs(nemo_rssi[anchor] - dataset[key][anchor]) == min_distance]
        closest_points.append(all_keys_min_distance)

    print(closest_points)


    for i in range(0, 11, 2):
        for j in range(0, 11, 2):
            if (i, j) not in dataset.keys():
                continue
            # now compute the distance for each anchor point
            distance = 0
            for anchor in range(0, 6):
                distance += math.fabs(nemo_rssi[anchor] - dataset[(i, j)][anchor])

            out[(i, j)] = distance

            if debug:
                print('Distance of point ({}, {}) from nemo: {}'.format(i, j, distance))

    # sort by item value (sort by absolute distance)
    out_sorted = dict(sorted(out.items(),
                             key=lambda item: math.fabs(item[1]),
                             reverse=False))

    return out_sorted
