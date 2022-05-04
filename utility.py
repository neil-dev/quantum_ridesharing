import numpy as np
import random
from constants import coordinates
from routes import Route, join_route


def generate_initial_requests(n, center, total_nodes):
    """Generate the initial set of requests.
    Args:
        n: No. of nodes excluding the shuttle stand.
        center: Index of the node considered as the shuttle stand.
        total_nodes: Total number of nodes
    Returns:
        A numpy array of size n containing the initial requests.
    """
    requests = np.zeros(n, dtype=np.int8)
    i = 0
    while i < n:
        val = random.randrange(total_nodes)
        if val != center:
            requests[i] = val
            i += 1
    return requests


def generate_vrp_instance(n, center, requests):
    """Generate a random VRP instance.
    Args:
        n: No. of nodes excluding the shuttle stand.
        center: Index of the node considered as the shuttle stand.
        requests: The initial batch of drop requests.
    Returns:
        A list of (n + 1) x coordinates, a list of (n + 1) y coordinates and an (n + 1) x (n + 1) numpy array as the
        cost matrix.
    """

    # Generate VRP instance
    xs = np.zeros(6)
    ys = np.zeros(6)
    ys[0] = 0
    xs[0] = 0

    for i in range(1, 6):
        ys[i] = (coordinates[requests[i - 1]]['latitude'] - coordinates[center]['latitude']) * 500
        xs[i] = (coordinates[requests[i - 1]]['longitude'] - coordinates[center]['longitude']) * 500

    instance = np.zeros((n + 1, n + 1))
    for ii in range(n + 1):
        for jj in range(ii + 1, n + 1):
            instance[ii, jj] = (xs[ii] - xs[jj]) ** 2 + (ys[ii] - ys[jj]) ** 2
            instance[jj, ii] = instance[ii, jj]

    # Return output
    return instance, xs, ys


def generate_cluster_route(center, requests, cluster):
    """Generate the route for a particular cluster.
    Args:
        center: Index of the node considered as the shuttle stand.
        requests: The initial batch of drop requests.
        cluster: The cluster for which the route is to be generated.
    Returns:
        A path for the cluster, and a list containing the order in which the requests belonging to the cluster are
        serviced.
    """

    path = []
    edge = []
    drop_order = []
    dist = 0
    nodes = [requests[i - 1] for i in cluster]
    closest = nodes[0]
    start = center
    route = Route()
    while len(nodes) > 0:
        closest_distance = 99999999  # Earth's cicumference: 40,075,000 m.
        for node in nodes:
            temp = route.generate(start, node)
            if route.distance < closest_distance:
                closest_distance = route.distance
                closest = node
                edge = temp
        join_route(path, edge[:-1])
        dist = dist + closest_distance
        start = closest
        nodes.remove(closest)
        drop_order.append((center, closest))
    path.append(closest)

    return path, drop_order
