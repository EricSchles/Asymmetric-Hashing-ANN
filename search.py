import numpy as np
import scipy as scp
import heapq


def approximate_search(query, data, centroids, hash, R= 100):
    if R < len(data): R = len(data)
    num_chunks = centroids.shape[0]
    # Google uses 256
    num_centroids = centroids.shape[1]

    # build lookup table --
    # lookup[i, j] == squared euclidean distance between the jth centroid of
    # the ith chunk and the query point
    lookup = np.empty(tuple([num_chunks] + [num_centroids]))

    for i, chunk in enumerate(centroids):
        for j, centroid in enumerate(chunk):
            lookup[i, j] = scp.spatial.distance.sqeuclidean(query, centroid)

    # calculate approximate distance
    approx_dists = [(float("inf"), -1)]*R
    for index, h_i in hash:
        approx_dist = 0
        for i, j in enumerate(h_i):
            approx_dist += lookup[i, j]
        if approx_dist < approx_dists[0]:
            heapq._heapreplace_max(approx_dists, (approx_dist, index))
    return approx_dists