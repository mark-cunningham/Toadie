# Toadie
# Code Angel

# Display scoreboard functions

import pygame

import world
import toadie

# Define colours
WHITE = (255, 255, 255)
GREEN = (33, 222, 0)
PURPLE = (201, 128, 255)
YELLOW = (255, 255, 0)

# Define constants
TIMER_PAD_RIGHT = 70
TIMER_PAD_BOTTOM = 16
TIMER_HEIGHT = 18
TIMER_UNIT = 300

SCORE_LANE = 15
LIVES_LANE = 14


# Display the scores at the foot of the screen
def display_scores(game_screen, lives, score, time, toad_lives_image):

    padding = (world.BLOCK_SIZE - toad_lives_image.get_height()) / 2
    width = toad_lives_image.get_width()
    space = 4

    # Display a small toad icon for each life
    for life_number in range(lives):
        game_screen.blit(
            toad_lives_image, [life_number * (width + space) + padding, LIVES_LANE * world.BLOCK_SIZE + padding]
        )

    # Display score
    score_text = 'SCORE   ' + str(score)
    text = toadie.score_font.render(score_text, True, WHITE)
    game_screen.blit(text, [padding, SCORE_LANE * world.BLOCK_SIZE])

    # Display timer
    time_text = 'TIME'
    text = toadie.score_font.render(time_text, True, YELLOW)
    text_rect = text.get_rect()
    game_screen.blit(text, [toadie.SCREEN_WIDTH - text_rect.width - padding, SCORE_LANE * world.BLOCK_SIZE])

    # Convert the time into a rectangle
    timer_width = int(time / TIMER_UNIT)

    if timer_width > 0:
        timer_rect = (
            toadie.SCREEN_WIDTH - TIMER_PAD_RIGHT - timer_width,
            toadie.SCREEN_HEIGHT - TIMER_PAD_BOTTOM - TIMER_HEIGHT,
            timer_width,
            TIMER_HEIGHT
        )

        pygame.draw.rect(game_screen, GREEN, timer_rect)


# Display Game Over screen
def game_over(game_screen, score, hi_score, new_hi_score):

    text_line_1 = toadie.large_font.render('GAME OVER', True, WHITE)
    text_rect_1 = text_line_1.get_rect()

    score_text = 'Score: ' + str(score)
    text_line_2 = toadie.large_font.render(score_text, True, WHITE)
    text_rect_2 = text_line_2.get_rect()

    hi_text = ''
    if new_hi_score > hi_score:
        hi_text = '[New high score]'

    text_line_3 = toadie.score_font.render(hi_text, True, WHITE)
    text_rect_3 = text_line_3.get_rect()

    text_line_4 = toadie.score_font.render('RETURN for new game', True, WHITE)
    text_rect_4 = text_line_4.get_rect()

    msg_bk_left = 0
    msg_bk_top = world.TRUCK_LANE * world.BLOCK_SIZE
    msg_bk_width = toadie.SCREEN_WIDTH
    msg_bk_height = world.BLOCK_SIZE * 5
    msg_bk_rect = (msg_bk_left, msg_bk_top, msg_bk_width, msg_bk_height)
    pygame.draw.rect(game_screen, PURPLE, msg_bk_rect)

    game_screen.blit(
        text_line_1, [(toadie.SCREEN_WIDTH - text_rect_1.width) / 2,
                      msg_bk_top + world.BLOCK_SIZE - world.BLOCK_SIZE / 2]
    )

    game_screen.blit(
        text_line_2, [(toadie.SCREEN_WIDTH - text_rect_2.width) / 2,
                      msg_bk_top + world.BLOCK_SIZE * 2 - world.BLOCK_SIZE / 2]
    )

    game_screen.blit(
        text_line_3, [(toadie.SCREEN_WIDTH - text_rect_3.width) / 2,
                      msg_bk_top + world.BLOCK_SIZE * 3 - world.BLOCK_SIZE / 2]
    )

    game_screen.blit(
        text_line_4, [(toadie.SCREEN_WIDTH - text_rect_4.width) / 2,
                      msg_bk_top + world.BLOCK_SIZE * 4]
    )