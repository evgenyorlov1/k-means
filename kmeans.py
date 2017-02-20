from __future__ import division
import argparse
import random
import math
import pylab as pl
import csv


def k_means(data, clusters):
    # initial centroids
    centroids = list()
    for _ in xrange(clusters):
        index = random.randint(0, len(data)-1)  # can be same index for centroid
        centroids.append(data[index])

    point_dimensions = len(centroids[0])-1

    flag = 50
    while flag > 0:
        # divide data into clusters
        for i, point in enumerate(data):
            closest_centroid = [0, 0]  # distance, class
            for j, centroid in enumerate(centroids):
                dist = euclid_dist(centroid, point)
                if j == 0 or closest_centroid[0] > dist:
                    data[i][-1] = j
                    closest_centroid[0] = dist
                    closest_centroid[1] = j

        # calculate new centroids
        for i in xrange(clusters):
            centroid = [0] * point_dimensions  # 0,0,0,0
            count = 0
            for pnt in data:
                if pnt[-1] == i:
                    count += 1
                    for j in xrange(len(centroid)):
                        centroid[j] += float(pnt[j])
            centroid = [round(el/count, 3) for el in centroid]
            centroids[i] = centroid
            # print 'round {}, cluster {}, centroid {}, count {}'.format(flag, i, centroids[i], count)
        flag -= 1
    return data


def euclid_dist(centroid, point):
    summary = 0
    for i in xrange(len(centroid)-1):
        summary += (float(centroid[i]) - float(point[i]))**2
    return math.sqrt(summary)


def load(data):
    with open(data, 'rb') as file:
        data = csv.reader(file, delimiter=',')
        data = [row for row in data]
        # last element in a row is a cluster
        for i in xrange(len(data)):
            data[i][-1] = 0
        return data


def plot_report(data, clusters):
    for i in xrange(clusters):
        pl.scatter(data[0], data[1], marker='x', color='b', s=500)  # takes list of x, y
        pl.scatter(data[1], data[1], marker='', color='b', s=500)
    pl.title('Dataset with {} clusters'.format(clusters))
    pl.show()


def parse_options():
    optparser = argparse.ArgumentParser(description='K-Means Algorithm.')
    optparser.add_argument(
        '-f', '--input_file',
        dest='filename',
        help='filename containing csv',
        required=True
    )
    optparser.add_argument(
        '-c', '--clusters',
        dest='clusters',
        help='number of clusters',
        default=2,
        type=int
    )
    return optparser.parse_args()


options = parse_options()
data = load(options.filename)
data = k_means(data, options.clusters)
plot_report(data, options.clusters)