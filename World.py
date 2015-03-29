import pygame

from Enemies import BaseEnemy
from Virus import Virus
from Spam import Spam
from ImageFuncs import *
from Player import *
from Shot import *
from Boss import *
from Rootkit import *
from Camera import *
from WorldMap import WorldMap
import random


class World(object):

    def __init__(self, screen_size):

        self.ss = screen_size
        self.counter = 0

        self.base_image = pygame.image.load("res/base.png").convert()
        self.image_funcs = ImageFuncs(32, 32, self.base_image)

        self.bullet_list = []
        self.enemy_list = []

        self.player_image = self.image_funcs.get_image(0, 0)
        self.player = Player(self, self.player_image, (512, 512))
        
        self.render_boss = False
        self.game_won = False
        self.game_over = False

        self.main_camera = Camera(self)
        self.main_camera.offset += vec2(self.ss[0]/2, self.ss[1]/2)

        self.main_font = pygame.font.Font(None, 25)
        self.debug_text_on = False

        self.map_filename = "maps/map.txt"
        self.marching_image = pygame.image.load("maps/testing.png").convert()
        self.marching_image.set_colorkey((255, 0, 255))
        self.main_map = WorldMap(self, (32,32), 256)
        self.main_map.update()

        self.set_up_demo()
        self.back = pygame.image.load("res/back.png").convert()
        self.back2= pygame.image.load("res/back2.png").convert()

        self.candy_filename = "maps/candymap.txt"
        self.candy_list = []
        with open(self.candy_filename) as f:
            for row in f.readlines():
                lst = row.split()
                pos = (float(lst[0]), float(lst[1]))
                self.candy_list.append(pos)

        f.close()

    def update(self, mouse_pos, movement, tick):
        """Updates all entities and shots. takes
            arguments for the position of the mouse,
            the player movement vector, and the
            time passed since the last frame."""

        to_remove = []

        for bullet in self.bullet_list:
            if bullet.bool_enemy:
                if bullet.rect.colliderect(self.player.rect):
                    bullet.dead = True
                    self.player.health -= 5
            else:
                for enemy in self.enemy_list:
                    if bullet.rect.colliderect(enemy.rect):
                        bullet.dead = True
                        enemy.health -= 10
                        enemy.hit_this_frame = True
                        if enemy.health <= 0:
                            enemy.dead = True
            bullet.update(tick)
            if bullet.dead:
                to_remove.append(bullet)

        for enemy in self.enemy_list:
            enemy.update(tick)
            enemy.update_collisions(self.enemy_list)
            if enemy.dead:
                to_remove.append(enemy)

        """Update player and then camera"""
        old_pos = self.player.pos.copy()
        self.player.update(mouse_pos, movement, tick)
        if self.main_map.test_collisions(self.player.mask, self.player.pos.copy()):
            self.player.velocity *= -1
        movement = self.player.pos - old_pos
        self.main_camera.update(-movement)

        if self.player.health <= 0:
            self.game_over = True


        """delete any 'dead' bullets or enemies"""
        for dead_ent in to_remove:
            if dead_ent in self.bullet_list:
                self.bullet_list.remove(dead_ent)

            elif dead_ent in self.enemy_list:
                self.enemy_list.remove(dead_ent)

    def background(self,surface):
        surface.blit(self.back,(vec2(-500,-500)))
        if self.main_camera.offset.x >= 0 and self.main_camera.offset.y >= 0:
            surface.blit(self.back2,(self.main_camera.offset.x,self.main_camera.offset.y))
        elif self.main_camera.offset.x >= 0 :
            surface.blit(self.back2,(self.main_camera.offset.x,0))
        elif self.main_camera.offset.y >= 0:
            surface.blit(self.back2,(0,self.main_camera.offset.y))
        else:
            surface.blit(self.back,(-500,-500))
            surface.blit(self.back2,(0,0))

    def render(self, surface):

        #self.background(surface)
        self.main_map.render(surface, self.main_camera)

        for bullet in self.bullet_list:
            bullet.render(surface, self.main_camera)

        for enemy in self.enemy_list:
            enemy.render(surface, self.main_camera)

        self.player.render(surface, self.main_camera)
            
        if self.debug_text_on:
            pass

        surface.blit(self.main_font.render(("Player Health:" + str(self.player.health)),True, (0,204,0)),(100,500))


    def set_up_demo(self):
        num_virus = 0
        num_spam = 0
        for i in xrange(num_virus):
            self.enemy_list.append(Virus(self, vec2(random.randint(0, self.ss[0]),
                                                    random.randint(0, self.ss[1]))))
        for i in xrange(num_spam):
            self.enemy_list.append(Spam(self, vec2(random.randint(0, self.ss[0]),
                                                   random.randint(0, self.ss[1]))))
        
        enemy_file = open("maps/enemymap.txt", "r")
        for line in enemy_file.readlines():
            everything = line.split(" ")
            if len(everything) > 3:
                if everything[3] == "x\n":
                    continue
            e_type = everything[0]
            pos = float(everything[1]) * 256, float(everything[2]) * 256
            if e_type == 's':
                self.enemy_list.append(Spam(self, vec2(*pos)))
            elif e_type == 'k':
                self.enemy_list.append(Boss(self, vec2(*pos)))
            elif e_type == 'r':
                self.enemy_list.append(Rootkit(self, vec2(*pos)))
            else:
                self.enemy_list.append(Virus(self, vec2(*pos)))
        enemy_file.close()

    def instantiate_projectile(self, pos, angle, vel, bool_enemy, bool_player = False):
        self.bullet_list.append(Shot.Shot(pos, angle, vel, bool_enemy, bool_player))

    def test(self):
        """THIS COMMENT IS FOR A COMMIT. IMAGINE
            HOW FUCKING COOL WE ARE WHEN USING GIT"""
        print "dur da dur"

def vec_to_int(vec):
    return int(vec.x), int(vec.y)
