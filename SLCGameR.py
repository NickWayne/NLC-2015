#!/usr/bin/env python

"""Main file for SLC-NLC Project 2015."""

import pygame
import time
pygame.init()

from vector2 import Vector2 as vec2

from World import World
import random

"""
PROMPT:

You are a computer virus tracker.
You live inside a computer and travel the network looking
for viruses and malware. When some are detected, you have
to travel to the infection site and launch anti-virus software
discs at the malware minions.
Escalate the adventure from basic network bugs to a Web Bot boss.
Take note in design to include computer networking structure and devices.
"""

SCREEN_SIZE = W, H = (1000, 600)
"""screen_size"""

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("SLC Game")
"""Set up display"""

MAIN_WORLD = World(SCREEN_SIZE)
"""set up the game handler"""

CLOCK = pygame.time.Clock()
"""set up the game clock"""

TARGET_FPS = 120.0

DONE = False
while not DONE:
    """main game loop"""

    TIME_PASSED_SECONDS = CLOCK.tick(TARGET_FPS) / 1000.0
    POS = pygame.mouse.get_pos()
    MOUSE_POS = vec2(POS[0], POS[1])
    """get the time (in seconds) since the last frame.
        Used for movement based on time."""

    for EVENT in pygame.event.get():
        """Get every event that has happened since the
        last frame and loop through it."""
        if EVENT.type == pygame.QUIT:
            DONE = True

        if EVENT.type == pygame.KEYDOWN:
            if EVENT.key == pygame.K_ESCAPE:
                DONE = True
                """This is separate from the pressed keys because
                this is just a single event rather than every frame
                the key is pressed down. Good for events you only
                want happening once."""

            if EVENT.key == pygame.K_F2:
                """Screenshots"""

                RANDOM_STRING = ""
                for i in range(10):
                    RANDOM_STRING += str(random.randint(0, 9))
                    pygame.image.save(SCREEN, RANDOM_STRING + ".png")

    MOVEMENT = vec2()
    PRESSED_KEYS = pygame.key.get_pressed()
    if PRESSED_KEYS[pygame.K_a]:
        MOVEMENT.x -= 1
    if PRESSED_KEYS[pygame.K_d]:
        MOVEMENT.x += 1

    if PRESSED_KEYS[pygame.K_w]:
        MOVEMENT.y -= 1
    if PRESSED_KEYS[pygame.K_s]:
        MOVEMENT.y += 1

    PRESSED_BUTTONS = pygame.mouse.get_pressed()
    if PRESSED_BUTTONS[0]:
        MAIN_WORLD.player.shoot(MOUSE_POS)

    """Update"""
    MAIN_WORLD.update(MOUSE_POS, MOVEMENT, TIME_PASSED_SECONDS)

    """Render"""
    SCREEN.fill((0, 0, 0))

    MAIN_WORLD.render(SCREEN)

    pygame.display.set_caption("[FPS: {:.4}]".format(CLOCK.get_fps()))

    if MAIN_WORLD.game_over:
        SCREEN.fill((0, 0, 0))
        MAIN_FONT = pygame.font.Font(None, 40)
        SCREEN.blit(MAIN_FONT.render(("GAME OVER!"),
                    True, (0, 0, 204)), (400, 300))

        pygame.display.flip()
        time.sleep(3)
        DONE = True

    if MAIN_WORLD.game_won:
        SCREEN.fill((0, 0, 0))
        MAIN_FONT = pygame.font.Font(None, 40)
        SCREEN.blit(MAIN_FONT.render(("YOU WON!"),
                    True, (0, 0, 204)), (400, 300))

        pygame.display.flip()
        time.sleep(3)
        DONE = True

    pygame.display.flip()

pygame.quit()
