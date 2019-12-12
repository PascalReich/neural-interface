import pygame
from pygame.locals import *
from pygame import Color

pygame.init()
width, height = 480, 640
screen=pygame.display.set_mode((width,height))

backdrop = pygame.image.load("resources/images/backdrop.png")
pygame.Surface.set_at(backdrop, (0,1010), Color('yellow'))
screen.fill(0)
screen.blit(backdrop, (0,0))
pygame.display.update()
test = pygame.Surface.get_at(backdrop,((0,100)))
test1 = pygame.Surface.get_size(backdrop)[1] // 2
print(test)

#if test == (255, 255, 0, 255):
    #print("y")
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)