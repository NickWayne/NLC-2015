# import pygame
from ImageFuncs import *

# class test(object):
#
#     def __init__(self,img,x,y):
#         self.ani = ani(32,32,img,.2)
#         self.lst = self.ani.get_lst(6,0,3)
#         self.img = self.lst[0]
#         self.x = x
#         self.y = y
#
#     def animate(self,tick):
#          self.img = self.lst[self.ani.get_frame(tick)]
#          self.img.set_colorkey((255,0,255))
#
#     def render(self):
#         screen.blit(self.img,(self.x,self.y))
class Ani(object):
    """
    Creates an animation given the cell width, height, and the image and it returns the image needed at the time passed
    in seconds
    """

    def __init__(self, w_cell, h_cell, img, speed):
        """
        :param w_cell: width of a cell
        :param h_cell: height of a cell
        :param img: the image going to be used
        :param speed: speed at which the animation proceeds at in seconds
        :return: None
        """
        self.speed_max = speed
        self.speed = speed
        self.base_img = img
        self.img_funcs =ImageFuncs(w_cell, h_cell, img)
        self.finished = False

    def get_lst(self,num,x,y):
        """
        :param num: number of cells needed
        :param x: x location to start at
        :param y: y location to start at
        :return: List of images
        """
        self.ani_num = 0
        self.ani_num_max = num
        return self.img_funcs.get_images(num,x,y)

    def reset(self):
        """
        :return: None
        """
        self.speed = self.speed_max
        self.ani_num = 0

    def get_frame(self,tick):
        """
        :param tick: Time passed in seconds
        :return: The number of the list the picture needs to be
        """
        self.speed -= tick
        if self.speed <= 0:
            self.speed = self.speed_max
            self.ani_num += 1
            if self.ani_num == self.ani_num_max:
                self.ani_num = 0
                self.finished = True
                return self.ani_num
            else:
                return self.ani_num
        return self.ani_num

