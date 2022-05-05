import numpy as np
from constants import dist_matrix, coordinates


class Node:
    def __init__(self, parent=None, position=None):

        """Initializing a node.
        Args:
            parent: Parent of the node.
            position: Index of the node.
        """

        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):

    """Recreates the path from the current node to the starting node.
    Args:
        current_node: The current node under consideration.
    Returns: A list containing the path from the starting node to the current node.
    """

    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    return path


def join_route(route1, route2):

    """Add the contents of the second list to the first list.
    Args:
        route1: List denoting the 1st route.
        route2: List denoting the route to be merged with the 1st route.
    Returns:
        A list with the 2nd route appended to the 1st route.
    """

    for i in route2:
        route1.append(i)
    return route1


def route_distance(route):

    """Calculate the total distance of a route.
    Args:
        route: A list containing the route.
    Returns:
        An integer denoting the total distance of the route.
    """

    distance = 0
    for i in range(1, len(route)):
        distance += dist_matrix[route[i - 1]][route[i]]
    return distance


class Route:

    def __init__(self):

        """Initialize the route object."""

        self.total_nodes = dist_matrix.shape[0]
        self.start = None
        self.end = None
        self.distance = None

    def neighbour(self, node):

        """List of neighbours of a node.
        Args:
            node: The index of the node in consideration.
        Returns:
            List containing the indices of the neighbours of the node.
        """

        nb = np.array([], dtype=np.int8)
        for i in range(self.total_nodes):
            if dist_matrix[node][i] > 0:
                nb = np.append(nb, i)
        return nb

    def astar(self):

        """This function finds the optimal route based on distance."""

        start = self.start
        end = self.end
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        end_node_coordinates = (coordinates[end]['longitude'], coordinates[end]['latitude'])

        # Initialize the open set and closed set
        open_set = []
        closed_set = []

        # Add the start node to the open set
        open_set.append(start_node)

        x = 0
        # Loop till you reach the end node
        while len(open_set) > 0:
            x += 1
            if x > 100000:
                print('Exceeded 100000 loops. Exiting.')
                break
            current_node = open_set.pop(0)
            closed_set.append(current_node)

            # Return the path if end point is reached
            if current_node == end_node:
                path = return_path(current_node)
                return path

            neighbours = self.neighbour(current_node.position)

            for nb in neighbours:

                new_node = Node(current_node, nb)

                # Checking if child is in closed list
                flag = False
                for closed_child in closed_set:
                    if new_node == closed_child:
                        flag = True
                        break

                if flag:
                    continue

                new_node_coordinates = (
                    coordinates[new_node.position]['longitude'], coordinates[new_node.position]['latitude'])
                new_node.g = current_node.g + dist_matrix[nb][current_node.position] / 100
                new_node.h = (new_node_coordinates[0] - end_node_coordinates[0]) ** 2 + (
                        new_node_coordinates[1] - end_node_coordinates[1]) ** 2
                new_node.f = new_node.g + new_node.h

                # Checking if child is already in open list and the new path is larger
                flag = False
                for open_child in open_set:
                    if new_node == open_child and new_node.g > open_child.g:
                        flag = True
                        break

                if flag:
                    continue

                i = 0
                if len(open_set) > 0:
                    while i < len(open_set) and open_set[i].f < new_node.f:
                        i += 1
                open_set.insert(i, new_node)
        return False

    def generate(self, start, end):

        """Generate a new route between the start and end points.
        Args:
            start: The starting position of the route.
            end: The ending position of the route.
        Returns:
            A list containing the generated route.
        """

        self.start = start
        self.end = end
        route = self.astar()
        self.distance = route_distance(route)
        return route
