import random


class Passenger:
    def __init__(self, request, shuttle_number):
        """Initializes a passenger
        Args:
            request: A tuple containing the pickup location and drop location.
        """
        self.id = None
        self.request = request
        self.shuttle_number = shuttle_number
        self.generate_passenger_id()

    def details(self):
        """Display the details of the passenger"""
        print('ID: {}\tRequest Info: {}\t Shuttle Number: {}'.format(self.id, self.request, self.shuttle_number))

    def generate_passenger_id(self):
        """Generate a random passenger id.
        Returns:
            A string id of length 10.
        """
        pid = 'P'
        for i in range(3):
            pid += str(random.randrange(10))
        for i in range(2):
            pid += chr(random.randrange(65, 91))
        for i in range(4):
            pid += str(random.randrange(10))
        self.id = pid
