import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import math

pygame.init()
width, height = 840, 1080
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
angle = 90
keydown = False
posx, posy = 390, 585
posx1, posy1 = 390, 410
posx2, posy2 = 390, 490
posx3, posy3 = 335, 490
posx4, posy4 = 445, 490


class MySprite(pygame.sprite.Sprite):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        super(MySprite, self).__init__()
        self.images = [
                       pygame.image.load('resources/images/pacman0.png'),
                       pygame.image.load('resources/images/pacman1.png'),
                       pygame.image.load('resources/images/pacman2.png')
                       ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x, y, 20, 20)

    def update(self):
        self.index += 0.5
        self.image = self.images[int(self.index) % 3]

    def next_image(self):
        for img in self.images:
            yield img
            yield img


class blinky1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super(blinky1, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('resources/images/BlinkyRight.png'))
        self.images.append(pygame.image.load('resources/images/BlinkyLeft.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x, y, 20, 20)

    def turn(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class pinky1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super(pinky1, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('resources/images/PinkyRight.png'))
        self.images.append(pygame.image.load('resources/images/PinkyLeft.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x, y, 20, 20)

    def turn(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class inky1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super(inky1, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('resources/images/InkyRight.png'))
        self.images.append(pygame.image.load('resources/images/InkyLeft.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x, y, 20, 20)

    def turn(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class clyde1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super(clyde1, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('resources/images/ClydeRight.png'))
        self.images.append(pygame.image.load('resources/images/ClydeLeft.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x, y, 20, 20)

    def turn(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


sprite = MySprite(posx, posy)

blinky = blinky1(posx1, posy1)
pinky = pinky1(posx2, posy2)
inky = inky1(posx3, posy3)
clyde = clyde1(posx4, posy4)

clock = pygame.time.Clock()

# player = pygame.image.load("resources/images/pacman0.png")
backdrop = pygame.image.load("resources/images/backdrop.png")
movemap = pygame.image.load("resources/images/movemap.png")

while 1:

    sprite.update()
    screen.fill(0)
    screen.blit(movemap, (0, 0))

    screen.blit(backdrop, (0, 0))

    playerrot = pygame.transform.rotate(sprite.image, angle)
    playerpos1 = (posx, posy)
    playerpos2 = (
        posx + pygame.Surface.get_size(sprite.image)[0] // 2, posy + pygame.Surface.get_size(sprite.image)[1] // 2)
    # playerpos1 = (playerpos[0]-playerrot.get_rect().width//2, playerpos[1]-playerrot.get_rect().height//2)
    screen.blit(playerrot, playerpos1)

    blinkypos = (posx1, posy1)
    screen.blit(blinky.image, blinkypos)

    pinkypos = (posx2, posy2)
    screen.blit(pinky.image, pinkypos)

    inkypos = (posx3, posy3)
    screen.blit(inky.image, inkypos)

    clydepos = (posx4, posy4)
    screen.blit(clyde.image, clydepos)
<<<<<<< HEAD
    
    #pygame.Surface.set_at(backdrop, (playerpos2), Color('yellow'))
    colorgetRIGHT = pygame.Surface.get_at(movemap, ((playerpos2[0] + 30, playerpos2[1])))
    colorgetTOP = pygame.Surface.get_at(movemap, ((playerpos2[0], playerpos2[1] - 30)))
    colorgetLEFT = pygame.Surface.get_at(movemap, ((playerpos2[0] - 30, playerpos2[1])))
    colorgetBOTTOM = pygame.Surface.get_at(movemap, ((playerpos2[0], playerpos2[1] + 30)))
    
    colorgetTOPRIGHT = pygame.Surface.get_at(movemap, ((playerpos2[0] + 25, playerpos2[1] - 25)))
    colorgetTOPLEFT = pygame.Surface.get_at(movemap, ((playerpos2[0] - 25, playerpos2[1] - 25)))
    colorgetBOTTOMLEFT = pygame.Surface.get_at(movemap, ((playerpos2[0] - 25, playerpos2[1] + 25)))
    colorgetBOTTOMRIGHT = pygame.Surface.get_at(movemap, ((playerpos2[0] + 25, playerpos2[1] + 25)))
    
=======

    pygame.Surface.set_at(backdrop, playerpos2, Color('yellow'))

>>>>>>> 3e21e299eaff12708d3048fba35dd5c845296365
    pygame.display.update()

    for event in pygame.event.get():

<<<<<<< HEAD
        if event.type==pygame.QUIT:
            pygame.quit() 
            exit(0) 
            
#----------------
#change section to brain wave patterns
            
    #change the event type/event key to brain signal
        if event.type == pygame.KEYDOWN and not keydown:
            if event.key==K_w:
                #keep keys array
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        #same thing        
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
                
#------------------
                
=======
        if event.type == pygame.QUIT:
            pygame.quit()
            print(f"{sprite.index*2} frames")
            exit(0)

        if event.type == pygame.KEYDOWN and not keydown:
            # keydown = True
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
            # else:
            # keydown = False

        if event.type == pygame.KEYUP:
            # keydown =False
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False

>>>>>>> 3e21e299eaff12708d3048fba35dd5c845296365
    if angle == 270:
        if(colorgetTOP == (0, 0, 0, 255)):
            if(colorgetTOPRIGHT == (0, 0, 0, 255)):
                if(colorgetTOPLEFT == (0, 0, 0, 255)):
                    posy -= 6
    if angle == 0:
        if(colorgetLEFT == (0, 0, 0, 255)):
            if(colorgetTOPLEFT == (0, 0, 0, 255)):
                if(colorgetBOTTOMLEFT == (0, 0, 0, 255)):
                    posx -= 6
    if angle == 180:
        if(colorgetRIGHT == (0, 0, 0, 255)):
            if(colorgetTOPRIGHT == (0, 0, 0, 255)):
                if(colorgetBOTTOMRIGHT == (0, 0, 0, 255)):
                    posx += 6
    if angle == 90:
<<<<<<< HEAD
        if(colorgetBOTTOM == (0, 0, 0, 255)):
            if(colorgetBOTTOMRIGHT == (0, 0, 0, 255)):
                if(colorgetBOTTOMLEFT == (0, 0, 0, 255)):
                    posy += 6
    
    
    if keys[0]:
        if(colorgetTOP == (0, 0, 0, 255)):
            if(colorgetTOPRIGHT == (0, 0, 0, 255)):
                if(colorgetTOPLEFT == (0, 0, 0, 255)):
                    angle = 270
    elif keys[2]:
        if(colorgetBOTTOM == (0, 0, 0, 255)):
            if(colorgetBOTTOMRIGHT == (0, 0, 0, 255)):
                if(colorgetBOTTOMLEFT == (0, 0, 0, 255)):
                    angle = 90                              
    if keys[1]:
        if(colorgetLEFT == (0, 0, 0, 255)):
            if(colorgetTOPLEFT == (0, 0, 0, 255)):
                if(colorgetBOTTOMLEFT == (0, 0, 0, 255)):
                    angle = 0                                
    elif keys[3]:
        if(colorgetRIGHT == (0, 0, 0, 255)):
            if(colorgetTOPRIGHT == (0, 0, 0, 255)):
                if(colorgetBOTTOMRIGHT == (0, 0, 0, 255)):
                    angle = 180                                
    clock.tick(60)
=======
        posy += 6

    if keys[0]:
        angle = 270
        # posy -= 8
    elif keys[2]:
        angle = 90
        # posy +=8
    if keys[1]:
        angle = 0
        # posx-=8
    elif keys[3]:
        angle = 180
        # posx+=8
    clock.tick(60)
>>>>>>> 3e21e299eaff12708d3048fba35dd5c845296365
