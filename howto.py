import pygame
from pygame.locals import *
import sys
import time
import os
import math
import random

#Margins for screen
WIDTH = 800
HEIGHT = 600

#center the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

#starting pygame and setting the screen size and the name of the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hack To The Future")

#loading of soundtrack
pygame.mixer.music.load('sound/martymcfly.mp3')
pygame.mixer.music.play()

class Menu_bg(pygame.sprite.Sprite):

	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/how_to_play.png")
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

tutorial = Menu_bg("images/how_to_play.png", [0,0])

while True:
        screen.fill([255, 255, 255])
        screen.blit(tutorial.image, tutorial.rect)
        
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type==pygame.KEYDOWN:
                        if event.key==K_BACKSPACE:
                                execfile('menu.py')
                        elif event.key==K_ESCAPE:
                                pygame.quit()
                                sys.exit()
        pygame.display.update()