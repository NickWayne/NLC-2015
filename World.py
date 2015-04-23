import pygame

from Virus import Virus
from Spam import Spam
from ImageFuncs import ImageFuncs
from Player import Player
from Shot import Shot
from Boss import Boss
from Rootkit import Rootkit
from Camera import Camera
from WorldMap import WorldMap
from vector2 import Vector2 as vec2
from math import ceil
import random
import glob

class World(object):

    def __init__(self, screen_size):

        self.ss = screen_size

        pygame.mixer.init()
        self.music_files = glob.glob("res/music/*.mp3")
        self.sound_files = glob.glob("res/sounds/*.ogg")

        self.credit_music = glob.glob("res/music/credits/*.mp3")
        self.intro_music = glob.glob("res/music/menu/*.mp3")


        self.sound_classes = [pygame.mixer.Sound(i) for i in self.sound_files]
        for SOUND in self.sound_classes:
            SOUND.set_volume(0.5)
        number = random.randint(0, len(self.music_files)-1)
        
        pygame.mixer.music.load(self.intro_music[0])
        pygame.mixer.music.play(-1)

        self.base_image = pygame.image.load("res/base.png").convert()
        self.image_funcs = ImageFuncs(32, 32, self.base_image)

        self.bullet_list = []
        self.enemy_list = []

        self.player_image = self.image_funcs.get_image(4, 0)
        
        self.game_won = False
        self.game_over = False

        self.main_camera = Camera(self)

        self.main_font = pygame.font.Font(None, 25)
        self.debug_text_on = False

        self.levels = ["tutorial1", "tutorial2", "map", "testingSpawn", "virustest", "scary", "bossfight"]
        self.level_index = 0
        level = self.levels[self.level_index]

        self.set_up_level(level)
        self.back = pygame.image.load("res/back.png").convert()
        self.UI = pygame.image.load("res/UI.png").convert()
        self.UI.set_colorkey((255,0,255))
        self.world_rect = pygame.Rect((0,0),(1000,600))

    def update(self, mouse_pos, movement, tick, to_debug=False):
        """Updates all entities and shots. takes
            arguments for the position of the mouse,
            the player movement vector, and the
            time passed since the last frame."""

        self.world_rect = pygame.Rect((-self.main_camera.offset.x,-self.main_camera.offset.y),(1000,600))

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
                        self.sound_classes[1].play()
                        if enemy.health <= 0:
                            enemy.dead = True
            bullet.update(tick)
            if bullet.dead:
                to_remove.append(bullet)

        for enemy in self.enemy_list:
            enemy.update(tick)
            enemy.update_collisions(self.enemy_list)

            x, y = (int(enemy.pos.x / self.main_map.each_size),
                    int(enemy.pos.y / self.main_map.each_size))

            offset = vec2(enemy.pos.x % self.main_map.each_size,
                        enemy.pos.y % self.main_map.each_size)

            if self.main_map.map_array[x][y].mask.overlap(enemy.mask, vec_to_int(offset)):
                enemy.velocity *= -1
            if enemy.dead:
                to_remove.append(enemy)

        """Update player and then camera"""
        old_pos = self.player.pos.copy()
        self.player.update(mouse_pos, movement, tick)

        x, y = (int(self.player.pos.x / self.main_map.each_size),
                int(self.player.pos.y / self.main_map.each_size))

        offset = vec2(self.player.pos.x % self.main_map.each_size,
                    self.player.pos.y % self.main_map.each_size)

        if to_debug:
            print "x, y:",x,y
            print "player pos:",self.player.pos
            print "each_size:",self.main_map.each_size
            print "offset:",offset
            print "camera pos:",self.main_camera.offset
            print ""

        if self.main_map.map_array[x][y].mask.overlap(self.player.mask, vec_to_int(offset)):
            self.player.velocity *= -1
            #pass

        for i in self.bullet_list:
            if i.bool_enemy == False:
                x, y = (int(i.pos.x // self.main_map.each_size),
                        int(i.pos.y // self.main_map.each_size))

                offset = vec2(i.pos.x % self.main_map.each_size,
                            i.pos.y % self.main_map.each_size)
                i.get_mask()
                if self.main_map.map_array[x][y].mask.overlap(i.mask, vec_to_int(offset)):
                    i.dead = True
                    self.sound_classes[3].play()

        movement = self.player.pos - old_pos
        self.main_camera.update(-movement)

        if self.goal.check():
            self.sound_classes[0].play()
            self.level_index+=1
            self.set_up_level(self.levels[self.level_index])

        if self.player.health <= 0:
            self.game_over = True


        """delete any 'dead' bullets or enemies"""
        for dead_ent in to_remove:
            if dead_ent in self.bullet_list:
                self.bullet_list.remove(dead_ent)

            elif dead_ent in self.enemy_list:
                if dead_ent.__class__.__name__ == "Boss" or (len(self.enemy_list) == 1 and self.goal.pos == vec2(0, 0)):
                    self.goal.pos = dead_ent.pos.copy()
                self.enemy_list.remove(dead_ent)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music_files[random.randint(0, len(self.music_files)-1)])
            pygame.mixer.music.play()

    def phealth_bar(self, screen):
        font = pygame.font.Font(None, 15)
        pos = (20,560)
        w,h = (100,20)
        pygame.draw.rect(screen,(255,0,0),((pos),(w,h)),0)
        pygame.draw.rect(screen,(0,255,0),((pos),(w*(self.player.health/float(self.player.health_max)),h)),0)
        string = "%s/%s" %(self.player.health,self.player.health_max)
        txt = self.main_font.render(str(string), True, (8,59,47))
        txt_rect = txt.get_rect()
        txt_rect.midleft = (20,590)
        screen.blit(txt,txt_rect)

    def render(self, surface):

        surface.blit(self.back,(-500,-500))
        self.main_map.render(surface, self.main_camera)

        for bullet in self.bullet_list:
            bullet.render(surface, self.main_camera)

        for enemy in self.enemy_list:
            # if self.world_rect.colliderect(enemy.rect):
            enemy.render(surface, self.main_camera)

        self.player.render(surface, self.main_camera)

        self.goal.render(surface)

        surface.blit(self.UI,(0,0))
        self.phealth_bar(surface)

    def set_up_level(self, level_name):
        del self.enemy_list[:]
        self.game_over = False
        self.game_won = False
        
        self.map_filename = "maps/"+level_name+".txt"
        self.marching_image = pygame.image.load("maps/MapImage.png").convert()
        self.marching_image.set_colorkey((255, 0, 255))
        self.marching_images = [pygame.image.load("maps/tilemap1.png").convert(),pygame.image.load("maps/tilemap2.png").convert()]
        for i in self.marching_images:
            i.set_colorkey((255, 0, 255))
        self.main_map = WorldMap(self, (32, 32), 256)
        self.main_map.update()

        self.main_camera.offset = vec2(self.ss[0]/2, self.ss[1]/2)
    
        self.player = Player(self, self.player_image, (0, 0))

        self.goal = EndPoint(vec2(0,0), self)

        self.candy_filename = "maps/"+level_name+"-startgoals.txt"
        with open(self.candy_filename) as open_file:
            row_index = 0
            for row in open_file.readlines():
                lst = row.split()
                pos = (float(lst[0]) * 256, float(lst[1]) * 256)
                if row_index == 0:
                    self.main_camera.offset -= pos
                    self.main_camera.offset -= vec2(16, 16)
                    self.player.pos = vec2(*pos)
                elif row_index == 1:
                    self.goal = EndPoint(vec2(*pos), self)

                row_index += 1

        open_file.close()

        enemy_file = open("maps/"+level_name+"-enemymap.txt", "r")
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
            elif e_type == 'v':
                self.enemy_list.append(Virus(self, vec2(*pos)))
        enemy_file.close()

    def instantiate_projectile(self, pos, angle, vel, bool_enemy, bool_player=False):
        self.bullet_list.append(Shot(pos, angle, vel, bool_enemy, bool_player))


class EndPoint(object):
    
    def __init__(self, pos, world):
        self.world = world
        self.pos = pos

    def check(self):
        if self.pos.get_distance_to(self.world.player.pos) < 16:
            return True

        return False

    def render(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), vec_to_int(self.pos + self.world.main_camera.offset), 16, 1)
        pygame.draw.circle(surface, (0, 128, 0), vec_to_int(self.pos + self.world.main_camera.offset), 17, 1)

def vec_to_int(vec):
    return int(vec.x), int(vec.y)
