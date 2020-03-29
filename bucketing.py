# Use the bucketing method to reduce the number of pairs (otherwise N^2)
# then calculate radial and angular distribution

import argparse
import matplotlib.pyplot as plt
import numpy as np
import math

def get_pairs(datafile, D):

    # D defines the average particle number in a box

    D = int(D)

    # get data from datafile
    # get the largest and smallest distance in both directions

    xmax = -1e100
    ymax = -1e100
    xmin = 1e100
    ymin = 1e100
    x = []
    y = []
    type_ = []

    with open(datafile, 'r') as df:
        for idx, line in enumerate(df.readlines()):
            x.append(float(line.split()[0]))
            y.append(float(line.split()[1]))
            type_.append(int(line.split()[2]))
            if x[idx] > xmax:
                xmax = x[idx]
            if x[idx] < xmin:
                xmin = x[idx]
            if y[idx] > ymax:
                ymax = y[idx]
            if y[idx] < ymin:
               ymin = y[idx]
    df.close()

    dim_x = int((xmax - xmin) / D)
    dim_y = int((ymax - ymin) / D)
    x_idxs = [int((i - xmin) // D) for i in x]
    y_idxs = [int((i - ymin) // D) for i in y]

    # create empty buckets filled with None
    buckets = np.empty((dim_x + 1, dim_y + 1), dtype=np.object)

    # modify their value from None to empty list
    for i, j in enumerate(buckets):
        for k, l in enumerate(j):
	    buckets[i][k] = []
    for i, (x_idx, y_idx) in enumerate(zip(x_idxs, y_idxs)):
        buckets[x_idx][y_idx].append(i)

    pairs = []
    for i in range(dim_x):
        for j in range(dim_y):
            for k in buckets[i][j]:
                for ii in range(max(0, i-1), min(dim_x, i+1) + 1):
                    for jj in range(max(0, j-1), min(dim_x, j+1) + 1):
                        for kk in buckets[ii][jj]:
			    pairs.append((k, kk))
    coords = zip(x, y)

    return coords, pairs

def get_distances_and_angles(pairs, coords):
    distances = []
    angles = []
    for i, j in pairs:
        coord_1 = coords[int(i)]
        coord_2 = coords[int(j)]
        x = coord_2[0] - coord_1[0]
        y = coord_2[1] - coord_1[1]
        distance = math.sqrt(x*x + y*y)
        if distance > 1e-5:
            distances.append(distance)
        # if we want double count for the angles, uncomment lines with "angle2"
        # from 0 to 90
        if x > 0 and y > 0:
            angle = math.atan(y/x)/math.pi*180
            #angle2 = math.atan(y/x)/math.pi*180 + 180
        # from 90 to 180
        if x < 0 and y > 0:
            angle = math.atan(y/x)/math.pi*180 + 180
            #angle2 = math.atan(y/x)/math.pi*180 + 360
        # from 180 to 270
        if x < 0 and y < 0:
            angle = math.atan(y/x)/math.pi*180 + 180
            #angle2 = math.atan(y/x)/math.pi*180
        # from 270 to 360
        if x > 0 and y < 0:
            angle = math.atan(y/x)/math.pi*180 + 360
            #angle2 = math.atan(y/x)/math.pi*180 + 180
        angles.append(angle)
        #angles.append(angle2)

    N = len(coords)
    return distances, angles, N

def visualize_result(distances, dr, dtheta, angles, N):
    dtheta = float(dtheta)
    dr = float(dr)

   # get the shortest and the largest distance
    rmax = max(distances)
    rmin = min(distances)

    # get bins
    points = np.arange(rmin, rmax, dr)
    angular_points = np.arange(0, 360, dtheta)

    # prepopulate bins with zeros
    g = [0]*len(points)

    # populate bins with distance occurances in r+dr interval
    for i, r in enumerate(points):
        for dist in distances:
            if (dist >= r) and (dist <= r+dr):
                g[i]+=1

    # prepopulate angular bins with zeros
    h = [0]*len(angular_points)

    # populate angular bins with angle occurances in theta + dtheta interval
    for i, theta in enumerate(angular_points):
        for angle in angles:
            if (angle >= theta) and (angle <= theta + dtheta):
                h[i]+=1
        h[i] = h[i] / 100

    # plot the histogram
    plt.subplot(221)
    plt.title('Radial distribution with d$r = {}$'.format(dr))
    plt.xlabel('Distance')
    plt.plot(points, g, 'r')

    # plot a different histogram to check our graph
    plt.subplot(222)
    plt.title('Radial distribution with d$r = {}$'.format(dr))
    plt.xlabel('Distance')
    plt.hist(distances, bins=points, facecolor='g', normed=1)

    # plot angular distribution as well
    plt.subplot(223)
    plt.title(r'Angular distribution with d$\theta = {}$'.format(dtheta))
    plt.xlabel(r'$\theta$')
    plt.plot(angular_points, h, 'b')

    # plot a different histogram for angular distribution as well
    plt.subplot(224)
    plt.title(r'Angular distribution with d$\theta = {}$'.format(dtheta))
    plt.xlabel(r'$\theta$')
    plt.hist(angles, bins=angular_points, facecolor='g', normed=1)

    plt.tight_layout()
    plt.show()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('d')
    parser.add_argument('dr')
    parser.add_argument('dtheta')
    args = parser.parse_args()

    pairs, coords = get_pairs(args.filename, args.d)
    distances, angles, N = get_distances_and_angles(pairs, coords)
    visualize_result(distances, args.dr, args.dtheta, angles, N)

