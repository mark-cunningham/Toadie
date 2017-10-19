# Toadie
# Code Angel

# Classes: MovingObject, Digger, Truck, Car, Turtle, Log, Pavement, Pad, Timer

import pygame

import toadie

# Define constants
BLOCK_SIZE = 32

PAVEMENT_LANE_1 = 13
CAR_LANE_1 = 12
DIGGER_LANE = 11
CAR_LANE_2 = 10
CAR_LANE_3 = 9
TRUCK_LANE = 8
PAVEMENT_LANE_2 = 7
TURTLE_LANE_1 = 6
LOG_LANE_1 = 5
LOG_LANE_2 = 4
TURTLE_LANE_2 = 3
LOG_LANE_3 = 2
HOME_LANE = 1

TOAD_TIME = 45
MILLISECONDS = 1000


# MovingObject class, the base class for all road and river objects
class MovingObject:

    # All moving objects have an image, rectangle and speed
    def __init__(self, speed, location, object_image):
        self.image = toadie.load_media('image', object_image)
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * BLOCK_SIZE
        self.rect.y = location[1] * BLOCK_SIZE
        self.padding_height = (BLOCK_SIZE - self.image.get_height()) / 2

        self.speed = speed

    # All moving objects move using the same principle
    def move(self, game_screen):

        # Add speed on to x coordinate
        self.rect.x = self.rect.x + self.speed

        # If object goes off left of screen start again at right of screen
        if self.rect.right < 0:
            self.rect.x = toadie.SCREEN_WIDTH

        # If object goes off right of screen start again at left of screen
        if self.rect.left > toadie.SCREEN_WIDTH:
            self.rect.x = 0 - self.rect.width

        # Draw the object
        game_screen.blit(self.image, [self.rect.x, self.rect.y + self.padding_height])


# Digger Class takes start_x as parameter, and speed is 2
class Digger(MovingObject):
    def __init__(self, start_x):
        location = [start_x, DIGGER_LANE]
        MovingObject.__init__(self, 2, location, 'digger')


# Digger Class takes start_x as parameter, and speed is -3
class Truck(MovingObject):
    def __init__(self, start_x):
        location = [start_x, TRUCK_LANE]
        MovingObject.__init__(self, -3, location, 'truck')


# RedCar Class takes start_x as parameter, and speed is -2
class RedCar(MovingObject):
    def __init__(self, start_x):
        location = [start_x, CAR_LANE_1]
        MovingObject.__init__(self, -2, location, 'car_red')


# PurpleCar Class takes start_x as parameter, and speed is -3
class PurpleCar(MovingObject):
    def __init__(self, start_x):
        location = [start_x, CAR_LANE_2]
        MovingObject.__init__(self, -3, location, 'car_purple')


# PinkCar Class takes start_x as parameter, and speed is -2
class PinkCar(MovingObject):
    def __init__(self, start_x):
        location = [start_x, CAR_LANE_3]
        MovingObject.__init__(self, -2, location, 'car_pink')


# Turtle Class takes start_x and size as parameter. Size of turtle chain is either 2 or 3
class Turtle(MovingObject):
    def __init__(self, start_x, size):
        if size == 3:
            MovingObject.__init__(self, -3, [start_x, TURTLE_LANE_1], 'turtle3')
        else:
            MovingObject.__init__(self, -3, [start_x, TURTLE_LANE_2], 'turtle2')


# Log Class takes start_x and size as parameter. Size of log chain is either 2, 3 or 4
class Log(MovingObject):
    def __init__(self, start_x, size):
        if size == 1:
            MovingObject.__init__(self, 2, [start_x, LOG_LANE_1], 'log')
        elif size == 2:
            MovingObject.__init__(self, 3, [start_x, LOG_LANE_3], 'log2')
        elif size == 3:
            MovingObject.__init__(self, 4, [start_x, LOG_LANE_2], 'log3')


# Pavement class takes a location as parameter
class Pavement:
    def __init__(self, location):
        self.x = location[0]
        self.y = location[1]
        self.image = toadie.load_media('image', 'pavement')

        self.rect = pygame.Rect(
            self.x * BLOCK_SIZE,
            self.y * BLOCK_SIZE,
            BLOCK_SIZE,
            BLOCK_SIZE
        )

    # The pavement draws itself in the correct location
    def draw(self, game_screen):
        game_screen.blit(self.image, [self.rect.x, self.rect.y])


# Pad Class takes the x coordinate as parameter
class Pad:
    def __init__(self, x_coord):
        self.x = x_coord
        self.image = toadie.load_media('image', 'pad')
        self.occupied_image = toadie.load_media('image', 'occupied_pad')
        self.padding_width = (BLOCK_SIZE - self.image.get_width()) / 2 + self.image.get_width()
        self.padding_height = (BLOCK_SIZE - self.image.get_height()) / 2

        self.rect = pygame.Rect(
            self.x * BLOCK_SIZE + self.padding_width,
            HOME_LANE * BLOCK_SIZE + self.padding_height,
            BLOCK_SIZE,
            BLOCK_SIZE
        )

        self.occupied = False

    # The pad draws itself in the correct location, with the image depicting either occupied or unoccupied pad
    def draw(self, game_screen):
        if self.occupied is False:
            game_screen.blit(self.image, [self.rect.x, self.rect.y])
        else:
            game_screen.blit(self.occupied_image, [self.rect.x, self.rect.y])


# Timer Class
class Timer:

    def __init__(self):

        # The length of time the level runs for
        self.duration = TOAD_TIME * MILLISECONDS

        # The value in ticks that the timer started
        self.start_time = pygame.time.get_ticks()

        # The time left on the timer - starts as duration
        self.time_remaining = self.duration

    # Called from the main game loop, updates the time remaining on the timer
    def update_time(self):
        new_time = pygame.time.get_ticks()
        elapsed_time = new_time - self.start_time
        self.time_remaining = self.duration - elapsed_time
        if self.time_remaining < 0:
            self.time_remaining = 0

    # Tests if the timer is out of time, returnd True if out of time, False if not
    def out_of_time(self):
        if self.time_remaining <= 0:
            no_time_left = True
        else:
            no_time_left = False

        return no_time_left

    # The number of seconds remaining on the timer
    def get_seconds_left(self):
        return int(self.time_remaining / MILLISECONDS)

    # Reset the timer
    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = self.duration


