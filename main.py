from parse import *
from statistics import mean
from utils import *
from nemo_finder import *

NEMO_RSSI = [-61, -61, -57, -58, -57, -58]

'''
Computes the average signal strength for each entry in the dataset
'''


def compute_avg_signal_strength(dataset):
    signal_dict = {}
    for key in dataset.keys():
        avg_list = []
        for antenna_signals in dataset[key]:
            avg_list.append(mean(antenna_signals))
        signal_dict[key] = avg_list

    return signal_dict


if __name__ == '__main__':
    dataset = get_dataset('dataset.dat')
    print("WHOLE DATASET:")
    print_coords(dataset)
    computed_dataset = compute_avg_signal_strength(dataset)
    print("DATASET WITH AVERAGE RSS FOR EACH ANCHOR:")
    print_coords(computed_dataset)

    # uncomment this line to export the computed average for each entry in the dataset
    export_dataset(compute_avg_signal_strength(dataset), 'computed_dataset.dat')

    print("METRIC 1:")
    distances = metric_1_distances(NEMO_RSSI, computed_dataset)
    print(distances)

    print("METRIC 2:")
    distances_2 = metric_1_distances(NEMO_RSSI, computed_dataset, squared=True)
    print(distances_2)

    print("METRIC 3:")
    distances_3 = metric_2_squared(NEMO_RSSI, computed_dataset)
    visual_bubbles(distances_3)
