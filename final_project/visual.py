from constants import image_coordinates

from PIL import Image, ImageDraw, ImageFont


class Visual:
    # Color constants used for drawing routes.
    start_color = (255, 255, 255)
    branch_color = [(0, 255, 0), (0, 255, 255)]
    current_route_color = [(173, 255, 47), (30, 144, 255)]
    old_route_color = [(8, 105, 114), (135, 206, 250)]
    drop_node_color = [(0, 100, 0), (180, 0, 180)]
    current_position_color = [(0, 250, 154), (123, 104, 238)]
    denied_request_color = [(255, 0, 0), (255, 0, 255)]

    def __init__(self, center, node_size=5, folder=None):

        """Initialize the Map Drawer.
        Args:
            center: Index of the hub.
            node_size: Size of the node to be drawn.
            folder: The name of the folder where the images are to be saved.
        """

        if folder is None:
            folder = 'random'
        self.center = center
        self.node_size = node_size
        self.folder = folder
        self.im = None
        self.draw = None
        self.initialize()

    def draw_denied_request(self, request):

        """Draw the nodes for a denied request.
        Args:
            request: A tuple containing the pickup and drop location.
        """

        node_size = 10
        for i in range(2):
            self.draw.ellipse((
                image_coordinates[request[i]][0] - node_size, image_coordinates[request[i]][1] - node_size,
                image_coordinates[request[i]][0] + node_size,
                image_coordinates[request[i]][1] + node_size), fill=self.denied_request_color[i],
                outline=(0, 0, 0))

    def draw_initial_requests(self, requests):

        """Draw the nodes for the initial requests.
        Args:
            requests: The initial batch of drop requests.
        """

        for req in requests:
            self.draw.ellipse(
                (image_coordinates[req][0] - self.node_size, image_coordinates[req][1] - self.node_size,
                 image_coordinates[req][0] + self.node_size, image_coordinates[req][1] + self.node_size),
                fill=(255, 0, 0), outline=(0, 0, 0))
        self.draw.ellipse(
            (image_coordinates[self.center][0] - self.node_size, image_coordinates[self.center][1] - self.node_size,
             image_coordinates[self.center][0] + self.node_size, image_coordinates[self.center][1] + self.node_size),
            fill=(255, 255, 255), outline=(0, 0, 0))

    def draw_nodes(self, shuttles):

        """Draw the nodes for a particular state of the shuttle.
        Args:
            shuttles: A list of objects containing the current shuttle objects.
        """

        for i in range(len(shuttles)):
            for req in shuttles[i].drop_order:
                self.draw.ellipse(
                    (image_coordinates[req[1]][0] - self.node_size, image_coordinates[req[1]][1] - self.node_size,
                     image_coordinates[req[1]][0] + self.node_size, image_coordinates[req[1]][1] + self.node_size),
                    fill=self.drop_node_color[i], outline=(0, 0, 0))
            self.draw.ellipse((image_coordinates[shuttles[i].current_position][0] - self.node_size,
                               image_coordinates[shuttles[i].current_position][1] - self.node_size,
                               image_coordinates[shuttles[i].current_position][0] + self.node_size,
                               image_coordinates[shuttles[i].current_position][1] + self.node_size),
                              fill=self.current_position_color[i], outline=(0, 0, 0))

            if shuttles[i].pickup:
                self.draw.ellipse((image_coordinates[shuttles[i].pickup[0]][0] - self.node_size,
                                   image_coordinates[shuttles[i].pickup[0]][1] - self.node_size,
                                   image_coordinates[shuttles[i].pickup[0]][0] + self.node_size,
                                   image_coordinates[shuttles[i].pickup[0]][1] + self.node_size),
                                  fill=self.branch_color[i], outline=(0, 0, 0))

        self.draw.ellipse(
            (image_coordinates[self.center][0] - self.node_size, image_coordinates[self.center][1] - self.node_size,
             image_coordinates[self.center][0] + self.node_size, image_coordinates[self.center][1] + self.node_size),
            fill=(255, 255, 255), outline=(0, 0, 0))

    def draw_request_text(self, request):

        """Draw the current request text.
        Args:
            request: A tuple containing the pickup and drop location.
        """

        self.draw.text((30, 20), 'Request: ({}, {})'.format(request[0]+1, request[1]+1),
                       font=ImageFont.truetype("arial.ttf", 12), fill=(0, 0, 0, 255))

    def draw_route(self, route, color):

        """Draw a route on the map.
        Args:
            route: A list containing the route.
            color: Color of the route.
        """

        for i in range(1, len(route)):
            self.draw.line((image_coordinates[route[i - 1]][0], image_coordinates[route[i - 1]][1],
                            image_coordinates[route[i]][0], image_coordinates[route[i]][1]), color, width=5)

    def draw_state(self, shuttles):

        """Draw the nodes for a particular state of the shuttle along with the current routes of the shuttles.
        Args:
            shuttles: A list of objects containing the current shuttle objects.
        """

        for i in range(len(shuttles)):
            for j in range(1, len(shuttles[i].route)):
                self.draw.line((image_coordinates[shuttles[i].route[j - 1]][0],
                                image_coordinates[shuttles[i].route[j - 1]][1],
                                image_coordinates[shuttles[i].route[j]][0],
                                image_coordinates[shuttles[i].route[j]][1]), self.current_route_color[i], width=5)
            for req in shuttles[i].drop_order:
                self.draw.ellipse(
                    (image_coordinates[req[1]][0] - self.node_size, image_coordinates[req[1]][1] - self.node_size,
                     image_coordinates[req[1]][0] + self.node_size, image_coordinates[req[1]][1] + self.node_size),
                    fill=self.drop_node_color[i], outline=(0, 0, 0))
            self.draw.ellipse((image_coordinates[shuttles[i].current_position][0] - self.node_size,
                               image_coordinates[shuttles[i].current_position][1] - self.node_size,
                               image_coordinates[shuttles[i].current_position][0] + self.node_size,
                               image_coordinates[shuttles[i].current_position][1] + self.node_size),
                              fill=self.current_position_color[i], outline=(0, 0, 0))

            if shuttles[i].pickup:
                self.draw.ellipse((image_coordinates[shuttles[i].pickup[0]][0] - self.node_size,
                                   image_coordinates[shuttles[i].pickup[0]][1] - self.node_size,
                                   image_coordinates[shuttles[i].pickup[0]][0] + self.node_size,
                                   image_coordinates[shuttles[i].pickup[0]][1] + self.node_size),
                                  fill=self.branch_color[i], outline=(0, 0, 0))

        self.draw.ellipse(
            (image_coordinates[self.center][0] - self.node_size, image_coordinates[self.center][1] - self.node_size,
             image_coordinates[self.center][0] + self.node_size, image_coordinates[self.center][1] + self.node_size),
            fill=(255, 255, 255), outline=(0, 0, 0))

    def initialize(self):

        """Load the image and create the draw object."""

        self.im = Image.open("test-img.png")
        self.draw = ImageDraw.Draw(self.im)

    def save(self, title):

        """Save the image in a folder.
        Args:
            title: Name of the saved file.
        """

        self.im.save('{}/{}.png'.format(self.folder, title))

    def show(self):

        """Create a temporary image file and show the image."""

        self.im.show()
