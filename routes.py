import numpy as np


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class Route:

    def __init__(self, dist_matrix, coordinates):
        self.dist_matrix = dist_matrix
        self.coordinates = coordinates
        self.total_nodes = dist_matrix.shape[0]
        self.start = None
        self.end = None

    def return_path(self, current_node):
        """
            Recreates the path from the current node to the starting node.
        """

        path = []
        current = current_node
        while current is not None:
            path.append(current.position)
            current = current.parent
        path = path[::-1]
        return path

    def neighbour(self, node):
        """
            This function returns the list of neighbours of a node.
        """
        nb = np.array([], dtype=np.int8)
        for i in range(self.total_nodes):
            if self.dist_matrix[node][i] > 0:
                nb = np.append(nb, i)
        return nb

    def astar(self):
        """
        This function finds the optimal route based on distance.
        """
        start = self.start
        end = self.end
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        end_node_coordinates = (self.coordinates[end]['longitude'], self.coordinates[end]['latitude'])

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
                path = self.return_path(current_node)
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
                    self.coordinates[new_node.position]['longitude'], self.coordinates[new_node.position]['latitude'])
                new_node.g = current_node.g + self.dist_matrix[nb][current_node.position] / 100
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
        self.start = start
        self.end = end
        return self.astar()