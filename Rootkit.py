import pygame
from vector2 import Vector2 as vec2
from StateMachine import *
from Enemies import *
from math import sin, cos, radians
import ani

class Rootkit(BaseEnemy):

    def __init__(self, world, pos):
        BaseEnemy.__init__(self, world, pos)
        self.ani = ani.Ani(32, 32, world.base_image, .2)
        self.lst = self.ani.get_lst(2,0,2)
        self.max_range = 350
        self.attacking_range = 100
        self.scared_range = 0

        self.dead = False

        """AI Brain variables"""
        self.sneaking_state = Sneaking(self, self.player)
        self.attacking_state = Attacking(self, self.player)
        self.roaming_state = Roaming(self, self.player)
        self.idle_state = Idle(self, self.player)

        self.brain.add_state(self.sneaking_state)
        self.brain.add_state(self.attacking_state)
        self.brain.add_state(self.roaming_state)
        self.brain.add_state(self.idle_state)

        self.brain.set_state("idle")

        self.img = self.world.image_funcs.get_image(0,2)
        self.img.set_colorkey((255,0,255))
        self.image = self.img

        self.rect = self.img.get_rect()


class Sneaking(State):
    """Creeping towards the player invisibly"""

    def __init__(self, enemy, player):
        State.__init__(self, "sneaking")
        self.enemy = enemy
        self.player = player
        
    def do_actions(self, tick):
        self.enemy.velocity += self.enemy.get_vector_to_target() * self.enemy.acceleration * tick

    def entry_actions(self):
        self.enemy.img = self.enemy.lst[0]
        self.enemy.img.set_colorkey((255,0,255))
        self.target = self.player.pos.copy()

    def exit_actions(self):
        pass

    def check_conditions(self):
        if self.enemy.get_dist_to(self.player.pos) < self.enemy.attacking_range:
            return "attacking"


class Attacking(State):
    """Appears and attacks the player"""

    def __init__(self, enemy, player):
        State.__init__(self, "attacking")
        self.enemy = enemy
        self.player = player

    def entry_actions(self):
        self.enemy.img = self.enemy.lst[1]
        self.enemy.img.set_colorkey((255,0,255))
        self.target = self.player.pos.copy()

    def do_actions(self, tick):
        self.enemy.velocity += self.enemy.get_vector_to_target() * self.enemy.acceleration * tick

    def check_conditions(self):
        if self.enemy.get_dist_to(self.player.pos) >= self.enemy.attacking_range:
            return "sneaking"

    def exit_actions(self):
        pass


class Roaming(State):
    """what the enemy does when the player is out of visible range"""

    def __init__(self, enemy, player):
        State.__init__(self, "roaming")
        self.enemy = enemy
        self.player = player

    def entry_actions(self):
        self.enemy.img = self.enemy.lst[0]
        self.enemy.img.set_colorkey((255,0,255))
        while self.enemy.world.main_map.test_collisions_point(self.enemy.target.pos):
            angle = radians(random.randint(0, 359))
            self.enemy.target = RoamPoint(self.enemy.pos + vec2( cos(angle),sin(angle)) * random.randint(25, 150))

    def do_actions(self, tick):
        self.enemy.velocity += self.enemy.get_vector_to_target() * self.enemy.acceleration * tick
        if self.enemy.get_dist_to(self.enemy.target.pos) < 25:
            while self.enemy.world.main_map.test_collisions_point(self.enemy.target.pos):
                angle = radians(random.randint(0, 359))
                self.enemy.target = RoamPoint(self.enemy.pos + vec2(cos(angle), sin(angle)) * random.randint(50, 250))

    def check_conditions(self):
        if self.enemy.can_see(self.player):
            return "sneaking"

        if self.enemy.get_dist_to(self.player.pos) >= 700:
            return "idle"

    def exit_actions(self):
        pass


class Idle(State):
    
    def __init__(self, enemy, player):
        State.__init__(self, "idle")
        self.enemy = enemy
        self.player = player

    def entry_actions(self):
        self.enemy.target = self.enemy

    def do_actions(self, tick):
        pass

    def check_conditions(self):
        if self.enemy.get_dist_to(self.player.pos) < 700:
            return "roaming"
