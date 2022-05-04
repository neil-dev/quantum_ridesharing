import random


class Shuttle:
    def __init__(self, route, drop_order=None):
        if drop_order is None:
            drop_order = []
        self.number = None
        self.passengers = None
        self.current_position = route[0]
        self.index = 0
        self.route = route
        self.drop_order = drop_order
        self.occupancy = 0
        self.service = False
        self.pickup = None
        self.generate_shuttle_number()

    def set_passengers(self, passengers):
        self.passengers = passengers
        self.occupancy = len(passengers)

    def passenger_details(self):
        for passenger in self.passengers:
            passenger.details()

    def details(self):
        print('Number: {}\tNumber of Passengers: {}\t\tCurrent Position: {}\t Route : {} \tDrop order: {}'.format(
            self.number, self.occupancy, self.current_position, self.route, self.drop_order))

    def generate_shuttle_number(self):
        """
            This function randomly generates a car number.
        """
        number = 'WB'
        for i in range(2):
            number += str(random.randrange(10))
        number += chr(random.randrange(65, 91))
        for i in range(4):
            number += str(random.randrange(10))
        self.number = number
