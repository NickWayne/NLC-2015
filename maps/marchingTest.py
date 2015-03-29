import pygame
from pygame.locals import *
pygame.init()

import VoronoiMapGen as vmg
from midpointDisplacement import *

w = h = 512
screen = pygame.display.set_mode((w, h))

marchingImg = pygame.image.load("testing.png").convert()

grandSize = 32

pygame.font.init()
font1 = pygame.font.Font(None, 25)


class tile:

    def __init__(self, pos):
        self.tl = 8
        self.tr = 4
        self.br = 2
        self.bl = 1
        self.on = False
        self.pos = pos

    def update(self, data_map):
        total = 0
        size = grandSize
        x,y = self.pos
        if data_map[x][y].on:
            total += self.tl
        if data_map[(x+1) % len(data_map)][y].on:
            total += self.tr
        if data_map[(x+1) % len(data_map)][(y+1) % len(data_map[0])].on:
            total += self.br
        if data_map[x][(y+1) % len(data_map[0])].on:
            total += self.bl
        newY = total//4
        newX = total%4

        self.image = marchingImg.subsurface(newX*32, newY*32, 32, 32)
        self.img = pygame.transform.scale(self.image, (size, size))

    def render(self, surface):
        surface.blit(self.img, (self.pos[0]*grandSize,self.pos[1]*grandSize))


class Enemy_text(object):

    def __init__(self, letter, pos):
        self.letter = letter
        self.pos = pos

    def render(self, surface):
        self.img = font1.render(self.letter, True, (255, 0, 0))
        surface.blit(self.img, (self.pos[0] * grandSize, self.pos[1] * grandSize))

    def to_text(self):
        return self.letter + " " + str(self.pos[0]) + " " + str(self.pos[1])


class CandyText(object):

    def __init__(self, pos):
        self.pos = pos

    def render(self, surface):
        pygame.draw.circle(surface, (255, 156, 0), (int(self.pos[0]*grandSize), int(self.pos[1]*grandSize)), 10)

    def to_text(self):
        return str(self.pos[0]) + " " + str(self.pos[1])

tileMap = [[tile((x,y)) for y in range(512/grandSize)] for x in range(512/grandSize)]

for y in range(len(tileMap)):
    for x in range(len(tileMap[0])):
        tileMap[x][y].on = True

bool_enemy = False

options = ["map", "enemies", "candies"]
option_index = 0

current_state = options[option_index]

candy_lst = []
enemy_lst = []
lst = []
done = False
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            
            if event.key == K_F2:
                pygame.image.save(screen, "SCREENSHOT.png")

            if event.key == K_F3:
                for y in range(len(tileMap)):
                    lst.append([])
                    for x in range(len(tileMap[y])):
                        if tileMap[x][y].on == True:
                            lst[y].append(1)
                        else:
                            lst[y].append(0)
                    lst[y].append(1)
                
                with open("map.txt", "w") as f :
                    for i in lst:
                        for g in i:
                            g = str(g)
                            a = g.replace("[","")
                            b = a.replace("]","")
                            c = b.replace(",","")
                            f.write(str(c))
                        f.write("\n")

                f.close()

                with open("enemymap.txt", "w") as f:
                    for e in enemy_lst:
                        f.write(e.to_text() + "\n")
                f.close()

                with open("candymap.txt", "w") as f:
                    for c in candy_lst:
                        f.write(c.to_text() + "\n")
                f.close()

            if event.key == K_SPACE:
                option_index += 1
                option_index %= len(options)
                current_state = options[option_index]

        if event.type == MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            if current_state == "enemies":
                posX, posY = pygame.mouse.get_pos()
                posX2 = posX / float(grandSize)
                posY2 = posY / float(grandSize)
                
                pressed_keys = pygame.key.get_pressed()
                for k in range(len(pressed_keys)):
                    if pressed_keys[k]:
                        enemy_char = pygame.key.name(k)
                        break

                if event.button == 1:
                    character = enemy_char

                enemy_lst.append(Enemy_text(character, (posX2, posY2)))

            elif current_state == "candies":
                posX, posY = pygame.mouse.get_pos()
                posX2 = posX / float(grandSize)
                posY2 = posY / float(grandSize)
                candy_lst.append(CandyText((posX2, posY2)))

            
    pressed = pygame.mouse.get_pressed()

    if current_state == "map":
        if pressed[0]:
            posX, posY = pygame.mouse.get_pos()
            tileMap[posX//grandSize][posY//grandSize].on = 1
        elif pressed[2]:
            posX, posY = pygame.mouse.get_pos()
            tileMap[posX//grandSize][posY//grandSize].on = 0
            
    screen.fill((255,255,255))
    for y in range(512/grandSize):
        for x in range(512/grandSize):
            TILE = tileMap[x][y]
            TILE.update(tileMap)
            TILE.render(screen)

    for CHARACTER in enemy_lst:
        CHARACTER.render(screen)
            
    
    for c in candy_lst:
        c.render(screen)
    
    pygame.display.update()
    pygame.display.set_caption(current_state)
    
pygame.quit()
    
