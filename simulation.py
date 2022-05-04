from shuttle import Shuttle
from passenger import Passenger
from utility import generate_cluster_route
from visual import Visual
from routes import Route, join_route

import random


class Simulation:
    def __init__(self, m, n, center, total_nodes, clusters, requests, folder=None):
        if folder is None:
            folder = 'random'
        self.m = m
        self.n = n
        self.center = center
        self.total_nodes = total_nodes
        self.clusters = clusters
        self.requests = requests
        self.folder = folder
        self.shuttles = []
        self.shuttle_index = {}
        self.initialization()

    def initialization(self):
        """
        Generating the initial state.
        In the initial state, the initial passengers are assigned to the shuttles available and the corresponding routes
        are generated.
        Then a simulation is run for fifty iterations, in which the car is consider to move to the next node in its route in every iteration.
        There is only one request generated per iteration, which is handled accordingly.
        """
        for i in range(self.m):
            # Initial shuttle and passenger initiation
            current_passengers = []
            path, drop_order = generate_cluster_route(self.center, self.requests, self.clusters[i])
            shuttle = Shuttle(path, drop_order)
            for drop_request in drop_order:
                current_passengers.append(Passenger(drop_request, shuttle.number))
            shuttle.set_passengers(current_passengers)
            self.shuttle_index[shuttle.number] = i
            self.shuttles.append(shuttle)
            shuttle.details()
            for passenger in current_passengers:
                passenger.details()

        # Displaying the initial state on map
        initial_state = Visual(self.center, self.folder)
        initial_state.draw_state(self.shuttles)
        initial_state.show()

    def simulate(self):
        print('\n\t###Simulation Starting###\n')
        for i in range(30):
            print('\nIteration ', i + 1)
            for shuttle in self.shuttles:
                if shuttle.route != [] and shuttle.index < len(shuttle.route) - 1:
                    shuttle.index += 1
                    shuttle.current_position = shuttle.route[shuttle.index]
                for drop_request in shuttle.drop_order:
                    if drop_request == shuttle.pickup:
                        continue
                    if drop_request[1] == shuttle.current_position:
                        shuttle.drop_order.remove(drop_request)
                        shuttle.passengers.pop(0)
                        shuttle.occupancy -= 1
                        print('Passenger dropped up at {} by car {}'.format(shuttle.current_position, shuttle.number))
                if not shuttle.drop_order:
                    shuttle.route = []
                    shuttle.index = -1
                if shuttle.service is True and shuttle.current_position == shuttle.pickup[0]:
                    shuttle.passenger_details()
                    shuttle.passengers.insert(shuttle.drop_order.index(shuttle.pickup),
                                              Passenger(shuttle.pickup, shuttle.number))
                    shuttle.occupancy += 1
                    print('Passenger picked up at {} by car {}'.format(shuttle.pickup[0], shuttle.number))
                    shuttle.service = False
                    shuttle.pickup = None
            request = self.request_generator()
            self.request_handler(request, i)
            print('\n')
            for shuttle in self.shuttles:
                print(
                    'Number: {}\tNumber of Passengers: {}\t\tCurrent Position: {}\tRoute : {}\tDrop order: {}\t'
                    'Service: {}\tPickup: {}'.format(
                        shuttle.number, shuttle.occupancy, shuttle.current_position, shuttle.route, shuttle.drop_order,
                        shuttle.service, shuttle.pickup))

    def request_generator(self):

        """Generate a random request."""

        src = random.randrange(self.total_nodes)
        dest = random.randrange(self.total_nodes)
        while src == dest:
            dest = random.randrange(self.total_nodes)
        return src, dest

    def request_handler(self, request, iteration):

        """This function handles a generated request and services it accordingly.
        """
        iteration_state = Visual(self.center, self.folder)
        iteration_state.draw_state(self.shuttles)
        print('Request generated: ', request)
        iteration_state.draw_request_text(request)

        suitable_shuttles = []
        route = Route()
        for shuttle in self.shuttles:
            occupancy = shuttle.occupancy
            src_pt = -1
            dest_pt = -1
            detour = 0
            pos = 0
            # Checking whether occupancy is not full and if the shuttle is already servicing another passenger.
            if shuttle.occupancy < 4 and shuttle.service is False:
                if shuttle.occupancy != 0:
                    pos = shuttle.route.index(shuttle.current_position)
                    shortest_distance = 999999
                    for i in range(pos, pos + 3):
                        if i >= len(shuttle.route):
                            break
                        point = shuttle.route[i]
                        route.generate(point, request[0])
                        print('{}\t{}\t{}\t{}'.format(i, point, request[0], route.distance))
                        if route.distance < 1000:
                            if route.distance > shortest_distance:
                                continue
                            src_pt = i
                            shortest_distance = route.distance
                    detour += shortest_distance

                    # Remove print statement
                    print('Source Point: {}'.format(src_pt))

                    if src_pt != -1:
                        shortest_distance = 999999
                        for j in range(pos, len(shuttle.route)):
                            route.generate(shuttle.route[j], request[1])
                            if route.distance < 1000:
                                if route.distance > shortest_distance:
                                    continue
                                shortest_distance = route.distance
                                dest_pt = j
                        detour += shortest_distance

                    # Remove print statement
                    print('Destination Point: {}'.format(dest_pt))

                    if src_pt != -1 and dest_pt != -1 and detour < 2000:
                        suitable_shuttles.append((shuttle, (src_pt, dest_pt)))
                else:
                    route.generate(shuttle.current_position, request[0])
                    if route.distance <= 3000:
                        suitable_shuttles.append((shuttle, (0, 1)))
        if len(suitable_shuttles) == 0:
            print('\nNo suitable shuttles')
            iteration_state.draw_denied_request(request)
            iteration_state.show()
            # iteration_state.save('Iteration_{}.png'.format(iteration + 1))
            return
        print('\nSuitable Shuttles: ')
        for shuttle in suitable_shuttles:
            route.generate(shuttle[0].current_position, request[0])
            print(
                'Distance: {}\t Number: {}\tNumber of Passengers: {}\t\tCurrent Position: {}\t Route : {} '
                '\tDrop order: {}'.format(
                    route.distance, shuttle[0].number, shuttle[0].occupancy, shuttle[0].current_position,
                    shuttle[0].route, shuttle[0].drop_order))
        route.generate(suitable_shuttles[0][0].current_position, request[0])
        closest_dist = route.distance
        closest = 0
        # selecting the closest shuttle from the list of suitable shuttles.
        for i in range(1, len(suitable_shuttles)):
            route.generate(suitable_shuttles[i][0].current_position, request[0])
            if route.distance < closest_dist:
                closest_dist = route.distance
                closest = i
        selected_shuttle = suitable_shuttles[closest]
        print('Selected Shuttle: ', suitable_shuttles[closest][0].number)
        if len(selected_shuttle[0].passengers) == 0:
            # Use spanning tree algo
            selected_shuttle[0].drop_order.append(request)
            temp = (route.generate(selected_shuttle[0].current_position, request[0]), route.generate(*request))
            selected_shuttle[0].route = join_route(temp[0][:-1], temp[1])
            selected_shuttle[0].index = 0
            if selected_shuttle[0].current_position == request[0]:
                selected_shuttle[0].passengers.append(
                    Passenger(request, selected_shuttle[0].number))
                selected_shuttle[0].occupancy += 1
                print('Passenger picked up at {} by shuttle {}'.format(request[0], selected_shuttle[0].number))

                # draw new route
                iteration_state.draw_route(temp[1],
                                           iteration_state.current_route_color[self.shuttle_index[
                                               selected_shuttle[0].number]])
            else:
                selected_shuttle[0].pickup = request
                selected_shuttle[0].service = True
                iteration_state.draw_route(temp[0],
                                           iteration_state.branch_color[self.shuttle_index[selected_shuttle[0].number]])
                iteration_state.draw_route(temp[1],
                                           iteration_state.current_route_color[self.shuttle_index[
                                               selected_shuttle[0].number]])
        else:
            src_pt = selected_shuttle[1][0]
            dest_pt = selected_shuttle[1][1]
            drop_list = [node for node in selected_shuttle[0].drop_order]
            flag = False
            insert_index = 0
            for i in range(len(drop_list)):
                if dest_pt < selected_shuttle[0].route.index(drop_list[i][1]):
                    drop_list.insert(i, request)
                    insert_index = i
                    flag = True
                    break
            if not flag:
                insert_index = len(drop_list)
                drop_list.append(request)
            selected_shuttle[0].drop_order = [order for order in drop_list]
            new_route = selected_shuttle[0].route[:src_pt]

            # draw old route
            iteration_state.draw_route(selected_shuttle[0].route,
                                       iteration_state.old_route_color[self.shuttle_index[selected_shuttle[0].number]])

            branch_route = route.generate(selected_shuttle[0].route[src_pt], request[0])
            new_route = join_route(new_route, branch_route[:-1])

            drop_first = False
            for i in range(insert_index):
                if selected_shuttle[0].route.index(drop_list[i][1]) > src_pt:
                    drop_first = True
                    break
            drop_list = drop_list[i if drop_first else insert_index:]
            join_index = len(new_route)
            new_route = join_route(new_route, route.generate(request[0], drop_list[0][1])[:-1])
            for i in range(1, len(drop_list)):
                new_route = join_route(new_route, route.generate(drop_list[i - 1][1], drop_list[i][1])[:-1])
            new_route.append(drop_list[-1][1])
            selected_shuttle[0].route = new_route
            # draw new route
            iteration_state.draw_route(new_route[join_index:],
                                       iteration_state.current_route_color[self.shuttle_index[
                                           selected_shuttle[0].number]])

            if selected_shuttle[0].current_position == request[0]:
                selected_shuttle[0].passengers.insert(insert_index, Passenger(request,
                                                                              selected_shuttle[0].number))
                selected_shuttle[0].occupancy += 1
                print('Passenger picked up at {} by shuttle {}'.format(request[0], selected_shuttle[0].number))
            else:
                selected_shuttle[0].pickup = request
                selected_shuttle[0].service = True

                # draw branch route
                iteration_state.draw_route(branch_route,
                                           iteration_state.branch_color[self.shuttle_index[selected_shuttle[0].number]])
        iteration_state.show()
        # iteration_state.save('Iteration_{}.png'.format(iteration + 1))
