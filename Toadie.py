#Toadie

import pygame, sys
from pygame.locals import *


# Define the colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKBLUE = (0, 0, 121)
PURPLE = (201, 128, 255)
YELLOW = (255, 255, 0)
GREEN = (33, 222, 0)


# Define constants
SCREENWIDTH = 448
SCREENHEIGHT = 512

TIMERPADRIGHT = 70
TIMERPADBOTTOM = 16
TIMERHEIGHT = 18
TIMERUNIT = 300


BLOCKSIZE = 32

SCORELANE = 15
LIVESLANE = 14
PAVEMENTLANE1 = 13
CARLANE1 = 12
DIGGERLANE = 11
CARLANE2 = 10
CARLANE3 = 9
TRUCKLANE = 8
PAVEMENTLANE2 = 7
TURTLELANE1 = 6
LOGLANE1 = 5
LOGLANE2 = 4
TURTLELANE2 = 3
LOGLANE3 = 2
HOMELANE = 1

FROGSTARTX = 6
FROGSTARTY = PAVEMENTLANE1
FROGDEATHTIME = 2
FROGTIME = 45


# initialise variables
screen_blocks_wide = int(SCREENWIDTH / BLOCKSIZE)

# Frog class
class Frog(object):
    def __init__(self):
        self.image = pygame.image.load("frog.png")
        self.dead_image = pygame.image.load("dead_frog.png")
        self.rect = self.image.get_rect()
        self.padding_width = (BLOCKSIZE - self.image.get_width()) / 2
        self.padding_height = (BLOCKSIZE - self.image.get_height()) / 2

        self.rect.x = FROGSTARTX * BLOCKSIZE + self.padding_width
        self.rect.y = FROGSTARTY * BLOCKSIZE + self.padding_height

        self.lives = 3
        self.points = 0
        self.home_count = 0
        self.alive = True
        self.death_pause_timer = 0
        self.furthest_forward = self.rect.y




    def draw(self):
        if self.alive is True:
            game_screen.blit(self.image, [self.rect.x, self.rect.y])
        else:
            game_screen.blit(self.dead_image, [self.rect.x, self.rect.y])

    def move(self, direction):
        if self.alive is True:
            if direction == "R":
                if self.rect.x + BLOCKSIZE < SCREENWIDTH:
                    self.rect.x = self.rect.x + BLOCKSIZE

            elif direction == "L":
                if self.rect.x - BLOCKSIZE > 0:
                    self.rect.x = self.rect.x - BLOCKSIZE

            elif direction == "U":
                self.rect.y = self.rect.y - BLOCKSIZE
                if self.rect.y < self.furthest_forward:
                    self.furthest_forward = self.rect.y
                    self.points = self.points + 10


            elif direction == "D":
                if self.rect.y + 3 * BLOCKSIZE < SCREENHEIGHT:
                    self.rect.y = self.rect.y + BLOCKSIZE

    def check_collision(self, vehicle_list):
        for vehicle in vehicle_list:
            if self.rect.colliderect(vehicle.rect):
                self.die()

    def check_water(self, river_list):
        frog_top = self.calc_frog_top()
        if frog_top < PAVEMENTLANE2 * BLOCKSIZE and frog_top > HOMELANE * BLOCKSIZE:
            floating_frog = False
            for river_item in river_list:
                if self.rect.colliderect(river_item):
                    if self.rect.left > river_item.rect.left and self.rect.right < river_item.rect.right:
                        self.rect.x = self.rect.x + river_item.speed
                        floating_frog = True

            if floating_frog is False:
                self.die()

            if floating_frog is True and self.rect.right >= SCREENWIDTH:
                self.die()

            if floating_frog is True and self.rect.left <= 0:
                self.die()

    def check_home(self, home_pads, game_timer):
        frog_top = self.calc_frog_top()
        if frog_top <= HOMELANE * BLOCKSIZE:
            found_home = False
            for pad in home_pads:
                if self.rect.centerx >= pad.rect.left and self.rect.centerx <= pad.rect.right:
                    if pad.occupied is False:
                        found_home = True
                        pad.occupied = True

                        self.points = self.points + 50
                        self.home_count = self.home_count + 1
                        if self.home_count == 5:
                            self.points = self.points + 1000

                        secs_left = game_timer.get_seconds_left()
                        self.points = self.points + 10 * secs_left

                        self.rect.x = FROGSTARTX * BLOCKSIZE + self.padding_width
                        self.rect.y = FROGSTARTY * BLOCKSIZE + self.padding_height

                        self.furthest_forward = self.rect.y
                        game_timer.reset()
                    else:
                        self.die()

            if found_home is False:
                self.die()





    def die(self):
        if self.alive is True:
            self.alive = False
            self.lives -= 1
            if self.lives > 0:
                self.death_pause_timer = pygame.time.get_ticks()

    def check_death_pause(self, game_timer):
        elapsed_time = pygame.time.get_ticks() - self.death_pause_timer
        if elapsed_time > FROGDEATHTIME * 1000:
            self.alive = True
            self.rect.x = FROGSTARTX * BLOCKSIZE + self.padding_width
            self.rect.y = FROGSTARTY * BLOCKSIZE + self.padding_height
            self.furthest_forward = self.rect.y
            game_timer.reset()


    def collect_points(self):
        collected_points = self.points
        self.points = 0

        return collected_points

    def calc_frog_top(self):
        return self.rect.y - self.padding_height







class MovingObject(object):

    def __init__(self, speed, location, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * BLOCKSIZE
        self.rect.y = location[1] * BLOCKSIZE
        self.padding_height = (BLOCKSIZE - self.image.get_height()) / 2

        self.speed = speed

    def move(self):
        self.rect.x = self.rect.x + self.speed
        if self.rect.right < 0:
            self.rect.x = SCREENWIDTH
        if self.rect.left > SCREENWIDTH:
            self.rect.x = 0 - self.rect.width

        game_screen.blit(self.image, [self.rect.x, self.rect.y  + self.padding_height])

class Digger(MovingObject):
    def __init__(self, start_x):
        location = [start_x, DIGGERLANE]
        MovingObject.__init__(self, 2, location, "digger.png")

class Truck(MovingObject):
    def __init__(self, start_x):
        location = [start_x, TRUCKLANE]
        MovingObject.__init__(self, -3, location, "truck.png")

class Car(MovingObject):
    def __init__(self, start_x, car_type):
        if car_type == "Red":
            MovingObject.__init__(self, -2, [start_x, CARLANE1], "car_a.png")
        elif car_type == "Purple":
            MovingObject.__init__(self, -3, [start_x, CARLANE2], "car_b.png")
        else:
            MovingObject.__init__(self, -2, [start_x, CARLANE3], "car_c.png")


class Turtle(MovingObject):
    def __init__(self, start_x, size, sinking_turtle):
        self.sinking_turtle = sinking_turtle
        if size == 3:
            MovingObject.__init__(self, -3, [start_x, TURTLELANE1], "turtle3.png")
        else:
            MovingObject.__init__(self, -3, [start_x, TURTLELANE2], "turtle2.png")

class Log(MovingObject):
    def __init__(self, start_x, size):
        if size == 1:
            MovingObject.__init__(self, 2, [start_x, LOGLANE1], "log.png")
        elif size == 2:
            MovingObject.__init__(self, 3, [start_x, LOGLANE3], "log2.png")
        elif size == 3:
            MovingObject.__init__(self, 4, [start_x, LOGLANE2], "log3.png")


class Pavement(object):
    def __init__(self, location):
        self.x = location[0]
        self.y = location[1]
        self.image = pygame.image.load("pavement.png")

    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCKSIZE, self.y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE)
        game_screen.blit(self.image, [self.rect.x, self.rect.y])


class Pad(object):
    def __init__(self, x_coord):
        self.x = x_coord
        self.image = pygame.image.load("pad.png")
        self.occupied_image = pygame.image.load("occupied_pad.png")
        self.padding_width = (BLOCKSIZE - self.image.get_width()) / 2 + self.image.get_width()
        self.padding_height = (BLOCKSIZE - self.image.get_height()) / 2
        self.rect = pygame.Rect(self.x * BLOCKSIZE + self.padding_width, HOMELANE * BLOCKSIZE + self.padding_height,
                                BLOCKSIZE, BLOCKSIZE)
        self.occupied = False

    def draw(self):
        if self.occupied is False:
            game_screen.blit(self.image, [self.rect.x, self.rect.y])
        else:
            game_screen.blit(self.occupied_image, [self.rect.x, self.rect.y])




class Timer(object):
    def __init__(self, time_in_secs):
        self.duration = time_in_secs * 1000
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = self.duration

    def update_time(self):
        new_time = pygame.time.get_ticks()
        elapsed_time = new_time - self.start_time
        self.time_remaining = self.duration - elapsed_time
        if self.time_remaining < 0:
            self.time_remaining = 0

    def out_of_time(self):
        if self.time_remaining <= 0:
            no_time_left = True
        else:
            no_time_left = False

        return no_time_left

    def get_seconds_left(self):
        return int(self.time_remaining / 1000)

    def reset(self):
        self.start_time = pygame.time.get_ticks()
        self.time_remaining = self.duration




def main():

    # Initialise objects
    frog = Frog()
    score = 0
    game_timer = Timer(FROGTIME)

    pavement_blocks = []
    for counter in range(screen_blocks_wide):
        pavement_block = Pavement([counter, PAVEMENTLANE1])
        pavement_blocks.append(pavement_block)
        pavement_block = Pavement([counter, PAVEMENTLANE2])
        pavement_blocks.append(pavement_block)

    landing_pads = []
    for counter in range(5):
        landing_pad = Pad(counter * 3)
        landing_pads.append(landing_pad)


    traffic = []
    river = []

    car_a1 = Car(4, "Red")
    car_a2 = Car(9, "Red")
    car_a3 = Car(14, "Red")
    traffic.extend((car_a1, car_a2, car_a3))

    digger_1 = Digger(6)
    digger_2 = Digger(11)
    digger_3 = Digger(16)
    traffic.extend((digger_1, digger_2, digger_3))

    car_b1 = Car(2, "Purple")
    car_b2 = Car(7, "Purple")
    car_b3 = Car(12, "Purple")
    traffic.extend((car_b1, car_b2, car_b3))

    car_c1 = Car(3, "Pink")
    car_c2 = Car(8, "Pink")
    car_c3 = Car(13, "Pink")
    traffic.extend((car_c1, car_c2, car_c3))

    truck_1 = Truck(3)
    truck_2 = Truck(3)
    traffic.extend((truck_1, truck_2))

    turtle_a1 = Turtle(1, 3, False)
    turtle_a2 = Turtle(5, 3, False)
    turtle_a3 = Turtle(9, 3, False)
    turtle_a4 = Turtle(13, 3, True)
    river.extend((turtle_a1, turtle_a2, turtle_a3, turtle_a4))

    turtle_b1 = Turtle(2, 2, True)
    turtle_b2 = Turtle(6, 2, False)
    turtle_b3 = Turtle(10, 2, False)
    turtle_b4 = Turtle(14, 2, False)
    river.extend((turtle_b1, turtle_b2, turtle_b3, turtle_b4))

    log_a1 = Log(1, 1)
    log_a2 = Log(6, 1)
    log_a3 = Log(11, 1)
    river.extend((log_a1, log_a2, log_a3))

    log_b1 = Log(5, 3)
    log_b2 = Log(13, 3)
    river.extend((log_b1, log_b2))

    log_c1 = Log(3, 2)
    log_c2 = Log(9, 2)
    log_c3 = Log(15, 2)
    river.extend((log_c1, log_c2, log_c3))


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



        game_screen.fill(DARKBLUE)

        pygame.draw.rect(game_screen, BLACK, (0, SCREENHEIGHT / 2, SCREENWIDTH, SCREENHEIGHT))

        # Load home
        home_image = pygame.image.load("home.png").convert()
        game_screen.blit(home_image, [0, 0])

        for pavement in pavement_blocks:
            pavement.draw()

        for pad in landing_pads:
            pad.draw()

        turtle_a1.move()
        turtle_a2.move()
        turtle_a3.move()
        turtle_a4.move()

        turtle_b1.move()
        turtle_b2.move()
        turtle_b3.move()
        turtle_b4.move()

        log_a1.move()
        log_a2.move()
        log_a3.move()

        log_b1.move()
        log_b2.move()

        log_c1.move()
        log_c2.move()
        log_c3.move()

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

        frog.check_collision(traffic)
        frog.check_water(river)
        frog.check_home(landing_pads, game_timer)

        game_timer.update_time()
        display_scores(frog.lives, score, game_timer.time_remaining)

        if game_timer.out_of_time() is True:
            frog.die()

        if frog.alive is False and frog.lives > 0:
            frog.check_death_pause(game_timer)

        if frog.lives == 0:
            game_over()

        if frog.home_count == 5:
            game_over()

        score = score + frog.collect_points()



        pygame.display.update()
        clock.tick(30)


def display_scores(lives, score, time):
    padding = (BLOCKSIZE - frog_lives_image.get_height()) / 2
    width = frog_lives_image.get_width()
    space = 4
    for life_number in range(lives):
        game_screen.blit(frog_lives_image, [life_number * (width + space) + padding, LIVESLANE * BLOCKSIZE + padding])

    score_text = "SCORE   " + str(score)
    text = score_font.render(score_text, True, (WHITE))
    game_screen.blit(text, [padding, SCORELANE * BLOCKSIZE])

    time_text = "TIME"
    text = score_font.render(time_text, True, (YELLOW))
    text_rect = text.get_rect()
    game_screen.blit(text, [SCREENWIDTH - text_rect.width - padding, SCORELANE * BLOCKSIZE])

    timer_width = int(time / TIMERUNIT)

    if (timer_width > 0):
        timer_rect = (SCREENWIDTH - TIMERPADRIGHT - timer_width, SCREENHEIGHT - TIMERPADBOTTOM - TIMERHEIGHT, timer_width,
        TIMERHEIGHT)
        pygame.draw.rect(game_screen, GREEN, timer_rect)



def game_over():
    text_line_1 = large_font.render("GAME OVER", True, (WHITE))
    text_rect_1 = text_line_1.get_rect()

    text_line_2 = large_font.render("RETURN for new game", True, (WHITE))
    text_rect_2 = text_line_2.get_rect()

    msg_bk_left = BLOCKSIZE * 2
    msg_bk_top = BLOCKSIZE * 6
    msg_bk_width = SCREENWIDTH - msg_bk_left * 2
    msg_bk_height = SCREENHEIGHT - msg_bk_top * 2
    msg_bk_rect = (msg_bk_left, msg_bk_top, msg_bk_width, msg_bk_height)
    pygame.draw.rect(game_screen, PURPLE, msg_bk_rect)

    game_screen.blit(text_line_1, [(SCREENWIDTH - text_rect_1.width) / 2, msg_bk_top + BLOCKSIZE])
    game_screen.blit(text_line_2, [(SCREENWIDTH - text_rect_2.width) / 2, msg_bk_top + msg_bk_height - 2 * BLOCKSIZE])



if __name__ == '__main__':
    pygame.init()
    game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Toadie")
    pygame.key.set_repeat(500, 200)

    clock = pygame.time.Clock()
    large_font = pygame.font.SysFont("Helvetica", 24)
    score_font = pygame.font.SysFont("Helvetica Bold", 24)

    # Load images
    frog_lives_image = pygame.image.load("frog_lives.png")

    main()