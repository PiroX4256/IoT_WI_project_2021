from parse import *
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

anchor_coords = [(0, 0), (0, 10), (5, 0), (10, 0), (5, 10), (10, 10)]


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


def metric_1_distances(nemo_rssi, dataset, debug=False):
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
        all_keys_min_distance = [key for key, value in dataset.items() if
                                 math.fabs(nemo_rssi[anchor] - dataset[key][anchor]) == min_distance]
        closest_points.append(all_keys_min_distance)

    # print(closest_points)

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


'''
Regressione lineare (o qualche grado) per associare RSSI e distanza di ogni antenna
Poi stimare distanza tra ogni antenna e Nemo
Plotta
'''


def metric_2_squared(nemo_rssi, dataset, debug=False):
    data_plot = []
    computed_distances = []

    for anchor in anchor_coords:
        distances = []
        all_rssi = []

        for x, y in dataset.keys():
            d = math.sqrt((anchor[0] - x) ** 2 + (anchor[1] - y) ** 2)
            distances.append(d)
            all_rssi.append(dataset[(x, y)][anchor_coords.index(anchor)])

        # mymodel is the list containing all y values of the regression curve
        mymodel = np.poly1d(np.polyfit(distances, all_rssi, 4))
        # myline is the list containing all x values of the regression curve
        myline = np.linspace(min(distances), max(distances))
        # print(distances)
        data_plot.append({"distances": distances,
                          "rssi": all_rssi,
                          "model": mymodel,
                          "line": myline})

    fig, axs = plt.subplots(2, 3)

    axs[0, 0].scatter(data_plot[0]["distances"], data_plot[0]["rssi"], s=5, c='darkred')
    axs[0, 0].plot(data_plot[0]["line"], data_plot[0]["model"](data_plot[0]["line"]))
    axs[0, 0].axhline(y=nemo_rssi[0], c='green')
    axs[0, 0].set_title('Anchor 1')
    axs[0, 0].set(ylabel='rssi')

    axs[0, 1].scatter(data_plot[1]["distances"], data_plot[1]["rssi"], s=5, c='darkred')
    axs[0, 1].plot(data_plot[1]["line"], data_plot[1]["model"](data_plot[1]["line"]))
    axs[0, 1].axhline(y=nemo_rssi[1], c='green')
    axs[0, 1].set_title('Anchor 2')

    axs[0, 2].scatter(data_plot[2]["distances"], data_plot[2]["rssi"], s=5, c='darkred')
    axs[0, 2].plot(data_plot[2]["line"], data_plot[2]["model"](data_plot[2]["line"]))
    axs[0, 2].axhline(y=nemo_rssi[2], c='green')
    axs[0, 2].set_title('Anchor 3')

    axs[1, 0].scatter(data_plot[3]["distances"], data_plot[3]["rssi"], s=5, c='darkred')
    axs[1, 0].plot(data_plot[3]["line"], data_plot[3]["model"](data_plot[3]["line"]))
    axs[1, 0].axhline(y=nemo_rssi[3], c='green')
    axs[1, 0].set_title('Anchor 4')
    axs[1, 0].set(ylabel='rssi')

    axs[1, 1].scatter(data_plot[4]["distances"], data_plot[4]["rssi"], s=5, c='darkred')
    axs[1, 1].plot(data_plot[4]["line"], data_plot[4]["model"](data_plot[4]["line"]))
    axs[1, 1].axhline(y=nemo_rssi[4], c='green')
    axs[1, 1].set_title('Anchor 5')

    axs[1, 2].scatter(data_plot[5]["distances"], data_plot[5]["rssi"], s=5, c='darkred')
    axs[1, 2].plot(data_plot[5]["line"], data_plot[5]["model"](data_plot[5]["line"]))
    axs[1, 2].axhline(y=nemo_rssi[5], c='green')
    axs[1, 2].set_title('Anchor 6')

    for ax in axs.flat:
        ax.set(xlabel='distance from anchor')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    # for ax in axs.flat:
    # ax.label_outer()

    loc = plticker.MultipleLocator(base=2.0)  # this locator puts ticks at regular intervals
    for ax in axs.flat:
        ax.xaxis.set_major_locator(loc)

    for i in range(0, 6):
        idx = np.argwhere(np.diff(np.sign([nemo_rssi[i]] - data_plot[i]["model"](data_plot[i]["line"])))).flatten()
        computed_distances.append(data_plot[i]["line"][idx])

    # print(computed_distances)

    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.5)
    plt.show()

    return computed_distances


def visual_bubbles(distances):
    x = np.array([0, 5, 10, 0, 5, 10])
    y = np.array([0, 0, 0, 10, 10, 10])
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 11, 1))
    ax.set_yticks(np.arange(0, 11, 1))
    plt.scatter(x, y)
    plt.grid()
    for anchor in anchor_coords:
        circle = plt.Circle(anchor, distances[anchor_coords.index(anchor)], color='b', alpha=0.1)
        plt.gca().add_patch(circle)

    solutions = [(2.24809, 4.68347), (4.1195, 3.1652), (7.37987, 2.26494), (10, 3.46338015), (10, 10 - 4.04061018),
                 (4.30418, 6.15377), (7.39512, 6.91113)]

    for s in solutions:
        plt.scatter(s[0], s[1], c='r')

    centroid = [0, 0]
    for s in solutions:
        centroid[0] += s[0]
        centroid[1] += s[1]

    centroid[0] /= len(solutions)
    centroid[1] /= len(solutions)

    plt.scatter(centroid[0], centroid[1], c='g')
    print("centroid = {}".format(centroid))

    plt.margins(x=0.01, y=0.01)
    plt.show()
    return
