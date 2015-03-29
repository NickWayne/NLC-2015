from vector2 import Vector2 as vec2

class Camera(object):

    def __init__(self, world):
        self.world = world
        self.player = self.world.player
        self.offset = -self.player.pos.copy()

    def update(self, movement):
        self.offset += movement
