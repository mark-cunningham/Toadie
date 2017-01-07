#Toadie

import pygame, sys
from pygame.locals import *


# Define the colours
BLACK = (0, 0, 0)


# Define constants
SCREENWIDTH = 448
SCREENHEIGHT = 512

BLOCKSIZE = 32
FROGSTARTX = 6
FROGSTARTY = 13

PAVEMENTLANE1 = 13
CARLANE1 = 12
DIGGERLANE = 11
CARLANE2 = 10
CARLANE3 = 9
TRUCKLANE = 8
PAVEMENTLANE2 = 7


# initialise variables
screen_blocks_wide = int(SCREENWIDTH / BLOCKSIZE)

# Frog class
class Frog(object):

    def __init__(self):
        self.image = pygame.image.load("frog.png")
        self.x = FROGSTARTX
        self.y = FROGSTARTY



    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCKSIZE, self.y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
        game_screen.blit(self.image, [self.rect.x, self.rect.y])

    def move(self, direction):
        if direction == "R":
            self.x = self.x + 1
            if self.x > SCREENWIDTH / BLOCKSIZE - 1:
                self.x = SCREENWIDTH / BLOCKSIZE - 1
        elif direction == "L":
            self.x = self.x - 1
            if self.x < 0:
                self.x = 0
        elif direction == "U":
            self.y = self.y - 1

        elif direction == "D":
            self.y = self.y + 1
            if self.y > SCREENHEIGHT / BLOCKSIZE - 2:
                self.y = SCREENHEIGHT / BLOCKSIZE - 2



class MovingObject(object):

    def __init__(self, speed, location, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * BLOCKSIZE
        self.rect.y = location[1] * BLOCKSIZE

        self.speed = speed




    def move(self):
        self.rect.x = self.rect.x + self.speed
        if self.rect.right < 0:
            self.rect.x = SCREENWIDTH
        if self.rect.left > SCREENWIDTH:
            self.rect.x = 0

        game_screen.blit(self.image, [self.rect.x, self.rect.y])

class Pavement(object):
    def __init__(self, location):
        self.x = location[0]
        self.y = location[1]
        self.image = pygame.image.load("pavement.png")

    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCKSIZE, self.y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
        game_screen.blit(self.image, [self.rect.x, self.rect.y])









def main():



    # Initialise objects
    frog = Frog()

    pavement_blocks = []
    for counter in range(screen_blocks_wide):
        pavement_block = Pavement([counter, PAVEMENTLANE1])
        pavement_blocks.append(pavement_block)
        pavement_block = Pavement([counter, PAVEMENTLANE2])
        pavement_blocks.append(pavement_block)


    car_a1 = MovingObject(-4, [4, CARLANE1], "car_a.png")
    car_a2 = MovingObject(-4, [9, CARLANE1], "car_a.png")
    car_a3 = MovingObject(-4, [14, CARLANE1], "car_a.png")

    digger_1 = MovingObject(4, [6, DIGGERLANE], "digger.png")
    digger_2 = MovingObject(4, [11, DIGGERLANE], "digger.png")
    digger_3 = MovingObject(4, [16, DIGGERLANE], "digger.png")

    car_b1 = MovingObject(-6, [2, CARLANE2], "car_b.png")
    car_b2 = MovingObject(-6, [7, CARLANE2], "car_b.png")
    car_b3 = MovingObject(-6, [12, CARLANE2], "car_b.png")

    car_c1 = MovingObject(4, [3, CARLANE3], "car_c.png")
    car_c2 = MovingObject(4, [8, CARLANE3], "car_c.png")
    car_c3 = MovingObject(4, [13, CARLANE3], "car_c.png")

    truck_1 = MovingObject(-4, [3, TRUCKLANE], "truck.png")
    truck_2 = MovingObject(-4, [9, TRUCKLANE], "truck.png")





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
        for pavement in pavement_blocks:
            pavement.draw()

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
        clock.tick(30)




if __name__ == '__main__':
    pygame.init()
    game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Toadie")
    pygame.key.set_repeat(500, 200)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Helvetica", 16)
    main()