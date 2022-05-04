import random


class Passenger:
    def __init__(self, request, shuttle_number):
        self.id = None
        self.request = request
        self.shuttle_number = shuttle_number
        self.generate_passenger_id()

    def details(self):
        print('ID: {}\tRequest Info: {}\t Shuttle Number: {}'.format(self.id, self.request, self.shuttle_number))

    def generate_passenger_id(self):
        """ This function generates a random passenger id."""
        pid = 'P'
        for i in range(3):
            pid += str(random.randrange(10))
        for i in range(2):
            pid += chr(random.randrange(65, 91))
        for i in range(4):
            pid += str(random.randrange(10))
        self.id = pid
