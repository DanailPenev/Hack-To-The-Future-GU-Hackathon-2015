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
pygame.mixer.music.load('sound/win.mp3')
pygame.mixer.music.play()

def get_score():
    score_levels_file = open("score_levels.txt", "r")
    score = int(score_levels_file.read())
    score_levels_file.close()
    return score

class Splash(pygame.sprite.Sprite):

	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/congrats.png")
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

congrats_splash = Splash("images/congrats.png", [0,0])
myfont = pygame.font.SysFont("monospace", 28, True)

while True:
        screen.fill([255, 255, 255])
        screen.blit(congrats_splash.image, congrats_splash.rect)
        scoretext = myfont.render("Score {0}".format(get_score()), 4, (255,255,255))
        screen.blit(scoretext, (300, 420))
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type==pygame.KEYDOWN:
                        if event.key==K_SPACE:
                                execfile('play_4.py')
                        elif event.key==K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                        elif event.key==K_BACKSPACE:
                                execfile('menu.py')
        pygame.display.update()