import pygame
from pygame.locals import *

w, h = screen_size = (640, 480)

screen = pygame.display.set_mode(screen_size)
pygame.mouse.set_visible(False)

""" A simple mask-collision example I wrote, tests to see if two images
    (In this case with a lot of transparency) collide, with pixel-perfect
    results. I did notice that in this with these two images there was
    a few imperfections, but it is much less than if you were to use
    circle or rectangle-based collision."""

"""Two basic and crudely drawn images with a lot of clear space"""
image_1 = pygame.image.load("maskTestImage1.png").convert()
image_1.set_colorkey((255, 0, 255))

image_2 = pygame.image.load("maskTestImage2.png").convert()
image_2.set_colorkey((255, 0, 255))


class Entity(object):
    """Basic entity uses class in case many entities were to be tested at the same time"""

    def __init__(self, pos, pic):
        self.pos = pos
        self.pic = pic
        """The mask is easily created from this simple command"""
        self.mask = pygame.mask.from_surface(self.pic)

    def check_collision(self, other_entity):
        """ Because masks don't have a position property an offset must be supplied
            to see if the masks overlap in game"""
        offset = (self.pos[0] - other_entity.pos[0],
                  self.pos[1] - other_entity.pos[1])
        if self.mask.overlap(other_entity.mask, offset) is not None:
            return True
        else:
            return False

    def render(self, surface):
        """I personally don't like always drawing to screen here so I just make it an argument"""
        surface.blit(self.pic, self.pos)

"""Instantiate the two entities that will be tested"""
ent1 = Entity((20, h/2), image_1)
ent2 = Entity((w/2, h/2), image_2)

"""I use while not done to avoid any errors. Makes it clean and nice to look at"""
done = False
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            done = True

    mouse_pos = pygame.mouse.get_pos()
    ent2.pos = mouse_pos
    """ Just set the position of one of the entities to your mouse (or some form of input)
        to test the collision"""

    if ent2.check_collision(ent1):
        pygame.display.set_caption("Collided")
    else:
        pygame.display.set_caption("Not Collided")

    screen.fill((0, 0, 0))
    ent1.render(screen)
    ent2.render(screen)
    """Render and update like a boss"""

    pygame.display.update()
pygame.quit()