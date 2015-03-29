import pygame
from pygame.locals import *
from random import randint,uniform, seed

class point:
    
    def __init__(self, pos,color=False):
        #Basic point, this will be used for the "feature points"
        #these will hold their position, as well as a seperate x and y
        #variable for easy use. Also a distance variable will be assigned
        #for when calculating the voronoi diagram

        self.pos = pos
        self.x=pos[0]
        self.y=pos[1]
        self.distance = 0
        self.color = None
        #if color: self.color = randint(0,255)

    def get_distance(self, p2):
        #Basic distance formula. I don't square root everything
        #in order to speed up the process
        try:
            distance = float((p2.x-self.x)**2)+((p2.y-self.y)**2)
        except DivideByZeroError:
            distance = 0
        self.distance = distance
        return distance

    def addColor(self):
        self.color = uniform(0,1)


class mapGen:

    def lerp(self, c1, c2, a):
        return c1+(c2-c1)*a

    def whole_new(self, num_R, size=(256, 256), c1=0, c2=0, c3=0):
        #Creates 1 image of the Voronoi diagram. I only listed the first 3
        #coefficients because that's all I will really need, but feel free
        #to add more
        
        w, h = size  #Very easy to use w and h instead of size[0] and size[1]
        
        toReturn = [[0 for i in xrange(size[0])] for j in xrange(size[1])]

        point_list = [point((randint(0, w), randint(0, h))) for i in range(num_R)]        #Creates the random "interest" points,

        max_brightness = 0

        for y in xrange(h):     #Do row-by-row instead of
            for x in xrange(w): #collumn-by-collumn
                currentPoint = point((x,y))
                new_pointlist = sorted(point_list, key=lambda point: point.get_distance(currentPoint))  #sort the points in a new list by their distance from the current point

                currentPoint.brightness = int(c1*new_pointlist[0].distance+c2*new_pointlist[1].distance+c3*new_pointlist[2].distance)/(num_R*(size[0]/((512.0/size[0])*256)))
                #this uses the coefficients and the new list to find the brightness of the wanted pixel
                #the math at the end is something I came to after about a half hour of fiddling around
                #with values. This will keep the value at a constant and good level, and not flatten anything.

                max_brightness = max(max_brightness, currentPoint.brightness)
                toReturn[x][y] = currentPoint.brightness

        for y in xrange(h):
            for x in xrange(w):
                toReturn[x][y] = (toReturn[x][y] / float(max_brightness)) * 255

        return toReturn

    def flat(self, num_R, size=(256,256)):
        #Creates 1 image of the voronoi diagram. I only listed the first 3
        #coefficients because that's all I will really need, but feel free
        #to add more
        w,h = size  #Very easy to use w and h instead of size[0] and size[1]
        
        toReturn = [[0 for i in xrange(size[0])] for j in xrange(size[1])]

        point_list = [point((randint(0,w), randint(0,h)),True) for i in range(num_R)]        #Creates the random "interest" points,
        for POINT in point_list:
            POINT.addColor()

        for y in xrange(h):     #Do row-by-row instead of
            for x in xrange(w): #collumn-by-collumn
                currentPoint = point((x,y))
                new_pointlist = sorted(point_list, key=lambda point: point.get_distance(currentPoint))  #sort the points in a new list by their distance from the current point

                currentPoint.brightness = new_pointlist[0].color

                toReturn[x][y] = currentPoint.brightness

        return toReturn

    def lerp_two_images(self, pic1, pic2, a):
        w,h= pic1.get_size()
        surface = pygame.Surface((w,h))

        for y in xrange(h):
            for x in xrange(w):
                clr1 = pic1.get_at((x,y))
                clr2 = pic2.get_at((x,y))
                clrR = (clr1[0]*(1-a)+clr2[0]*a)
                clrG = (clr1[1]*(1-a)+clr2[1]*a)
                clrB = (clr1[2]*(1-a)+clr2[2]*a)
                try:
                    surface.set_at((x,y), (clrR, clrG, clrB))
                except TypeError, e:
                    print clr
                    raise e

        return surface

    def combine_images(self, *pics):
        #Takes a list of images and combines them (grayscale).
        #All picture sizes must be of equal or less length than the first
        #but it is reccomended to have the exact same size for each

        num_pics = len(pics)
        w,h = len(pics[0]),len(pics[0]) #Again, this is very nice for keeping things quick
        print "W/H",w,h

        total_map = [[0 for i in xrange(h)] for i in xrange(w)] #Create a 2D array to hold all the values
        for PIC in pics:    #Loops through each of the given pictures
            for y in xrange(h):         #Row-by-Row
                for x in xrange(w):
                    try:
                        total_map[x][y]+=PIC[x][y]   #Adds the current value at the map to the corresponding cell on the array
                    except IndexError:
                        print x,y
                        print len(total_map), len(total_map[0])
                        raise IndexError

        for y in xrange(h):     #Loop through again, row-by-row
            for x in xrange(w):
                total_map[x][y]/=num_pics   #average out each cell

        return total_map

    def threshold(self, surface, lower=100, upper=128):
        #returns a thresholded surface of the image provided

        w,h = surface.get_size()
        new_surface = pygame.Surface((w,h))     #Create a surface with an identical size as the provided image
        new_surface.fill((0,0,0))   #fill with black, we will be setting the white values
        for y in xrange(h):     #Row-by-Row
            for x in xrange(w):
                if lower <= surface.get_at((x,y))[0] <= upper: #Checks to see if the value is in the threshold
                    new_surface.set_at((x,y), (255,255,255))    #Sets the pixel at that position to white if it is

        return new_surface

    def negative(self, array):
        #Just returns the negative of an image (grayscale only)
        #this is usefull because the function favors darker colors
        #in the middle of the image
        
        w, h = len(array[0]), len(array)
        for y in xrange(h):
            for x in xrange(w):
                array[x][y] = abs(array[x][y]-255)

        return array

    def negativeArray(self, ARRAY):
        w = h = len(ARRAY)
        toReturn = [[0 for x in xrange(w)]for y in xrange(h)]
        for y in xrange(h):
            for x in xrange(w):
                toReturn[x][y] = 255-ARRAY[x][y]

        return toReturn

    def multiplyArray(self, rhs, toMul):
        w = h = len(toMul)
        toReturn = [[0 for x in xrange(w)] for y in xrange(h)]
        for y in xrange(h):
            for x in xrange(w):
                toReturn[x][y] = toMul[x][y]*rhs[x][y]
        return toReturn


    def reallyCoolFull(self, total_size=(256,256), num_p=25, RandomSeed=None):
        #Uses 4 (or as many as you make, but I have found this to look cool)
        #calls to "whole_new()" and averages them out to create one cool image
        #that can be used in map generation! :D

        if RandomSeed!=None:
            seed(RandomSeed)

        #WARNING: THIS CAN TAKE A VERY LONG TIME
        #32x32: 0.4s, 64x64: 0.8s, 128x128:2.5s 
        #256x256: 9.8s, 512x512: 37.1s!

        pic1 = self.whole_new(num_p, total_size, c1=-1)
        pic2 = self.whole_new(num_p, total_size, c2=1)
        pic3 = self.whole_new(num_p, total_size, c3=1)
        pic4 = self.whole_new(num_p, total_size, c1=-1, c2=1)

        return self.combine_images(pic1,pic2,pic3,pic4)