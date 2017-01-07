#Toadie

import pygame, sys
from pygame.locals import *


# Define the colours
BLACK = (0, 0, 0)


# Define constants
SCREENWIDTH = 448
SCREENHEIGHT = 512


BLOCKSIZE = 14
FROGSTARTX = 12
FROGSTARTY = 34

CARAY = 380
DIGGERY = 350
CARBY = 320
CARCY = 290
TRUCKY = 255


# Define globals

# Frog class
class Frog(object):

    def __init__(self):
        self.frog_image = pygame.image.load("frog.png")
        self.frog_x = FROGSTARTX
        self.frog_y = FROGSTARTY



    def draw(self):
        self.rect = pygame.Rect(self.frog_x * BLOCKSIZE, self.frog_y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
        game_screen.blit(self.frog_image, [self.rect.x, self.rect.y])

    def move(self, direction):
        if direction == "R":
            self.frog_x = self.frog_x + 1
            if self.frog_x > SCREENWIDTH / BLOCKSIZE - 1:
                self.frog_x = SCREENWIDTH / BLOCKSIZE - 1
        elif direction == "L":
            self.frog_x = self.frog_x - 1
            if self.frog_x < 0:
                self.frog_x = 0
        elif direction == "U":
            self.frog_y = self.frog_y - 1

        elif direction == "D":
            self.frog_y = self.frog_y + 1
            if self.frog_y > SCREENHEIGHT / BLOCKSIZE - 2:
                self.frog_y = SCREENHEIGHT / BLOCKSIZE - 2



class MovingObject(object):

    def __init__(self, speed, location, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]

        self.speed = speed




    def move(self):
        self.rect.x = self.rect.x + self.speed
        if self.rect.right < 0:
            self.rect.x = SCREENWIDTH
        if self.rect.left > SCREENWIDTH:
            self.rect.x = 0

        game_screen.blit(self.image, [self.rect.x, self.rect.y])




"""class Car(MovingObject):

    def __init__(self, speed, location, image):
        MovingObject.__init__(self, speed, location, image)
        self.car_image = pygame.image.load("car_1.png")

    def draw(self):
        game_screen.blit(self.car_image, [self.x, self.y])"""









def main():



    # Initialise objects
    frog = Frog()
    car_a1 = MovingObject(-4, [110, CARAY], "car_a.png")
    car_a2 = MovingObject(-4, [250, CARAY], "car_a.png")
    car_a3 = MovingObject(-4, [390, CARAY], "car_a.png")

    digger_1 = MovingObject(4, [180, DIGGERY], "digger.png")
    digger_2 = MovingObject(4, [320, DIGGERY], "digger.png")
    digger_3 = MovingObject(4, [460, DIGGERY], "digger.png")

    car_b1 = MovingObject(-6, [80, CARBY], "car_b.png")
    car_b2 = MovingObject(-6, [220, CARBY], "car_b.png")
    car_b3 = MovingObject(-6, [360, CARBY], "car_b.png")

    car_c1 = MovingObject(4, [110, CARCY], "car_c.png")
    car_c2 = MovingObject(4, [250, CARCY], "car_c.png")
    car_c3 = MovingObject(4, [390, CARCY], "car_c.png")

    truck_1 = MovingObject(-4, [100, TRUCKY], "truck.png")
    truck_2 = MovingObject(-4, [280, TRUCKY], "truck.png")



    while True:  # main game loop
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_LEFT]:
            frog.move("L")
        elif key_pressed[pygame.K_RIGHT]:
            frog.move("R")
        elif key_pressed[pygame.K_UP]:
            frog.move("U")
        elif key_pressed[pygame.K_DOWN]:
            frog.move("D")


        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        game_screen.fill(BLACK)
        frog.draw()
        car_a1.move()
        car_a2.move()
        car_a3.move()

        digger_1.move()
        digger_2.move()
        digger_3.move()

        car_b1.move()
        car_b2.move()
        car_b3.move()

        car_c1.move()
        car_c2.move()
        car_c3.move()

        truck_1.move()
        truck_2.move()

        pygame.display.update()
        clock.tick(20)




if __name__ == '__main__':
    pygame.init()
    game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Frogger")
    pygame.key.set_repeat(10, 20)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 16)
    main()