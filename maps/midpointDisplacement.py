import random
import pygame
import VoronoiMapGen as vmg

class terrain:

    def __init__(self, detail, scale):
        self.size = 2**detail + 1
        self.max = self.size -1
        self.map = [[0 for i in range(self.size)] for j in range(self.size)]
        self.scale = scale

    def get(self,x,y):
        if x<0 or x > self.max or y < 0 or y > self.max: return -1
        return self.map[int(x)][int(y)]

    def set(self,x,y,val):
        self.map[int(x)][int(y)] = val

    def average(self,values):
        valid = [v for v in values if v!=-1 ]
        total = sum(valid)
        return total/len(valid)

    def square(self,x,y,size,offset):
        ave = self.average([
            self.get(x-size,y-size),
            self.get(x+size,y-size),
            self.get(x+size,y+size),
            self.get(x-size,y+size)])
        self.set(x,y,ave+offset)

    def diamond(self,x,y,size,offset):
        ave = self.average([
            self.get(x,y-size),
            self.get(x+size,y),
            self.get(x,y+size),
            self.get(x-size,y)])
        self.set(x,y,ave+offset)

    def divide(self, size, roughness):
        x,y,half = size/2.0,size/2.0,size/2.0
        scale = roughness * size
        if half<1:return

        y = half
        while y < self.max:
            x=half
            while x<self.max:
                self.square(x,y,half,random.uniform(0,1)*scale*2-scale)
                x+=size
            y+=size

        y = 0
        while y <= self.max:
            x=(y+half)%size
            while x <= self.max:
                self.diamond(x,y,half,random.uniform(0,1)*scale*2-scale)
                x+=size
            y+=half
                
        self.divide(size/2.0,roughness)  

    def generate(self,roughness):
        self.set(0,0,self.max/2)
        self.set(self.max,0,self.max/2)
        self.set(self.max,self.max,self.max/2)
        self.set(0,self.max, self.max/2)

        self.divide(self.max, roughness)

    def addArrayValues(self, arr1,arr2,fav = None):
        toReturn = [[0 for x in xrange(len(arr2))] for y in xrange(len(arr2))]
        for y in xrange(len(arr2)):
            for x in xrange(len(arr2)):
                if fav == 1:
                    toReturn[x][y] = ((arr1[x][y]*2+arr2[x][y]/2)/2)
                if fav == 2:
                    toReturn[x][y] = ((arr1[x][y]/2+arr2[x][y]*2)/2)
                if fav == None:
                    toReturn[x][y] = ((arr1[x][y]+arr2[x][y])/2)
        return toReturn

    def pertubate(self, arr1, arr2):
        newArray = [[0 for i in range(len(arr1))] for j in range(len(arr1))]
        for i in xrange(len(arr1)):
            for j in xrange(len(arr1)):
                newArray[i][j] = arr1[int(i+arr2[i][j]*self.scale)%(len(arr1))][int(j+arr2[i][j]*self.scale)%(len(arr1))]

        return newArray

