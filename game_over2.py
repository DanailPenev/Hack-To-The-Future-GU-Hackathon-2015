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
pygame.mixer.music.load('sound/death.wav')
pygame.mixer.music.play()

def get_high_score():
    # Default high score
    
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        
    except IOError:
        high_score = 0
    except ValueError:
        high_score = 0
    return high_score

def get_score():
    score_levels_file = open("score_levels.txt", "r")
    score = int(score_levels_file.read())
    score_levels_file.close()
    return score

class Menu_bg(pygame.sprite.Sprite):

	def __init__(self, image_file, location):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/game_over.png")
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location

gameover = Menu_bg("images/game_over.png", [0,0])
myfont = pygame.font.SysFont("monospace", 30, True)
yourfont = pygame.font.SysFont("monospace", 50, True, True)

while True:
        screen.fill([255, 255, 255])
        screen.blit(gameover.image, gameover.rect)
        achievmenttext = myfont.render("You scored", 4, (255, 255, 255))
        scoretext = myfont.render("{0}".format(get_score()), 4, (255, 255, 255))
        screen.blit(achievmenttext, (280, 310))
        screen.blit(scoretext, (470, 310))
        highscoretext = yourfont.render("NEW HIGHSCORE!", 4, (255, 255, 255))
        if get_score() >= get_high_score():
                screen.blit(highscoretext, (200, 350))
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type==pygame.KEYDOWN:
                        if event.key==K_SPACE:
                                execfile('play_inf.py')
                        elif event.key==K_BACKSPACE:
                                execfile('menu.py')
                        elif event.key==K_ESCAPE:
                                pygame.quit()
                                sys.exit()
        pygame.display.update()
