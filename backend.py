from dwave.system import LeapHybridSampler


class Backend:
    """Class containing all backend solvers that may be used to solve the Vehicle Routing Problem."""

    def __init__(self, vrp):
        """Initializes required variables and stores the supplied instance of the VehicleRouter object."""

        # Store relevant data
        self.vrp = vrp

        # Initialize necessary variables
        self.result_dict = None

    def solve(self):
        """Takes the solver as input and redirects control to the corresponding solver."""

        # Call Leap Solver
        self.solve_leap()

    def solve_leap(self):
        """Solve using Leap Hybrid Sampler."""

        # Solve
        sampler = LeapHybridSampler()
        self.vrp.result = sampler.sample(self.vrp.bqm)

        # Extract solution
        self.vrp.timing.update(self.vrp.result.info)
        self.result_dict = self.vrp.result.first.sample
        self.vrp.extract_solution(self.result_dict)
