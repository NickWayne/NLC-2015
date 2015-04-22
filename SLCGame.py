#!/usr/bin/env python

"""Main file for SLC-NLC Project 2015."""

import pygame
import time
pygame.mixer.pre_init(22050,-16, 2, 1024)
pygame.init()

from vector2 import Vector2 as vec2

from World import World
import random
from Menu import Menu
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

def main():
    screen_size = w, h = (1000, 600)
    """screen_size"""

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("SLC Game")
    """Set up display"""

    main_world = World(screen_size)
    """set up the game handler"""

    main_menu = Menu()

    clock = pygame.time.Clock()
    """set up the game clock"""

    target_fps = 120.0

    game_states = ["menu", "game", "help", "win", "lose"]
    current_state = game_states[0]

    sleep_timer = 0

    done = False
    while not done:
        """main game loop"""

        to_debug = False
        time_passed_seconds = clock.tick(target_fps) / 1000.0
        pos = pygame.mouse.get_pos()
        mouse_pos = vec2(pos[0], pos[1])
        """get the time (in seconds) since the last frame.
            Used for movement based on time."""

        for event in pygame.event.get():
            """Get every event that has happened since the
            last frame and loop through it."""
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #done = True
                    current_state = "menu"
                    """This is separate from the pressed keys because
                    this is just a single event rather than every frame
                    the key is pressed down. Good for events you only
                    want happening once."""

                if event.key == pygame.K_F2:
                    """Screenshots"""

                    random_string = ""
                    for i in range(10):
                        random_string += str(random.randint(0, 9))
                        pygame.image.save(screen, random_string + ".png")

                elif event.key == pygame.K_g:
                    to_debug = True

        if current_state == "menu":

            screen.fill((0, 0, 0))

            option = main_menu.handle_mouse_input(mouse_pos, pygame.mouse.get_pressed())
            if option is not None:
                main_world.sound_classes[0].play()
                if option == 1:
                    """start"""
                    current_state = "game"

                elif option == 2:
                    """tutorial"""
                    pass

                elif option == 3:
                    current_state = "help"

                elif option == 4:
                    """credits"""
                    pass

                elif option == 5:
                    done = True

            main_menu.render(screen)
            
            pygame.display.flip()

        elif current_state == "help":
            main_menu.help_screen(screen)
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                current_state = "menu"
            pygame.display.flip()

        elif current_state == "game":
            movement = vec2()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a]:
                movement.x -= 1
            if pressed_keys[pygame.K_d]:
                movement.x += 1

            if pressed_keys[pygame.K_w]:
                movement.y -= 1
            if pressed_keys[pygame.K_s]:
                movement.y += 1

            pressed_buttons = pygame.mouse.get_pressed()
            if pressed_buttons[0]:
                main_world.player.shoot(mouse_pos)

            """Update"""
            main_world.update(mouse_pos, movement, time_passed_seconds)

            """Render"""
            screen.fill((0, 0, 0))
            main_world.render(screen)

            pygame.display.set_caption("[FPS: {:.4}]".format(clock.get_fps()))

            if main_world.game_over:
                current_state = "lose"
                sleep_timer = 3

            if main_world.game_won:
                current_state = "win"
                sleep_timer = 3

            pygame.display.flip()

        elif current_state == "lose":
            screen.fill((0, 0, 0))
            main_font = pygame.font.Font(None, 40)
            screen.blit(main_font.render(("GAME OVER!"),
                True, (0, 0, 204)), (400, 300))

            pygame.display.flip()
            
            sleep_timer -= time_passed_seconds
            if sleep_timer <= 0:
                current_state = "menu"

        elif current_state == "win":
            screen.fill((0, 0, 0))
            main_font = pygame.font.Font(None, 40)
            screen.blit(main_font.render(("YOU WON!"),
                True, (0, 0, 204)), (400, 300))

            pygame.display.flip()
            
            sleep_timer -= time_passed_seconds
            if sleep_timer <= 0:
                current_state = "menu"

    pygame.quit()

if __name__ == "__main__":
    main()
