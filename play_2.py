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

#highscore
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

def save_high_score(new_high_score):
    #try:
        # Write the file to disk
    high_score_file = open("high_score.txt", "w")
    high_score_file.write(str(new_high_score))
    high_score_file.close()

def get_score():
    score_levels_file = open("score_levels.txt", "r")
    score = int(score_levels_file.read())
    score_levels_file.close()
    return score

def save_score(inter_score):
    score_levels_file = open("score_levels.txt", "w")
    score_levels_file.write(str(inter_score))
    score_levels_file.close()

def get_lives():
    lives_levels_file = open("lives_levels.txt", "r")
    lives = int(lives_levels_file.read())
    lives_levels_file.close()
    return lives

def save_lives(inter_lives):
    lives_levels_file = open("lives_levels.txt", "w")
    lives_levels_file.write(str(inter_lives))
    lives_levels_file.close()

#center the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

#starting pygame and setting the screen size and the name of the screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hack To The Future")

#loading of soundtrack
pygame.mixer.music.load('sound/lvl2.wav')
pygame.mixer.music.play()   

#beginning of key mapping and introducing some variables for later on
keys = [False,False]
Enemylist = []
count = 0
lives = get_lives()
score = get_score()
explosion_pos = [0,0]  

#some timer stuff I still don't understand
velocity = 1.5
frequency = 40
FPS = 50
fps_time = pygame.time.Clock()
time_passed = fps_time.tick(FPS)

#ImageInfo is a class important for collision detection cuz of the radius and the size
class ImageInfo:

    def __init__(self, size, radius=0):
        self.size = size
        self.radius = radius

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

#loading of images
explosion_img = pygame.image.load("images\player_explosion.png")
car_info = ImageInfo([63, 149], 40)
car_img = pygame.image.load("images\car.png")
enemy2_info = ImageInfo([84, 132], 40)
enemy2_img = pygame.image.load("images\enemy2.png")
myfont = pygame.font.SysFont("monospace", 18, True)


#Implementing classes for the car and the enemies, they actually work
class Background(pygame.sprite.Sprite):

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images\scene2.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Player:

    def __init__(self, position, image, info):
        self.position = position
        self.image = image
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_pos(self):
        return self.position

class Enemy:

    def __init__(self, x, speed, image, info):
        self.x = x
        self.y = 0
        self.speed = velocity * speed
        self.image = image
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def update(self, time_passed):
        self.time_passed = time_passed
        self.y += self.speed*time_passed

    def get_pos(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.radius 

    def collide(self, other_object):
        global lives
        if self.get_pos()[1] + 100 >= other_object.get_pos()[1]:
            if self.get_pos()[0] >= other_object.get_pos()[0] + 15 and self.get_pos()[0] <= other_object.get_pos()[0] + 63:
                explosion_pos [0] = other_object.get_pos()[0] + 45
                explosion_pos [1] = self.get_pos()[1] + 100
                lives -= 1
                return True
            elif self.get_pos()[0] + 84 <= other_object.get_pos()[0] + 63 and self.get_pos()[0] + 84 >= other_object.get_pos()[0] +15:
                explosion_pos [0] = self.get_pos()[0] + 45
                explosion_pos [1] = self.get_pos()[1] + 100
                lives -= 1
                return True
            elif self.get_pos()[0] + 42 <= other_object.get_pos()[0] + 63 and self.get_pos()[0] + 42 >= other_object.get_pos()[0] +15:
                explosion_pos [0] = self.get_pos()[0] + 42
                explosion_pos [1] = self.get_pos()[1] + 100
                lives -= 1
                return True
        else:
            return False


#Create the car
car = Player([WIDTH/2, HEIGHT-149], car_img, car_info)
background = Background("images\scene2.png", [0,0])
x = 0
while True:
    #Background follows
    screen.fill([255, 255, 255])
    screen.blit(background.image,(0,x-2))
    screen.blit(background.image,(0,x-600))                 #<<<<<<<<<<<

    x = x + 1
    if x == 600 or x == 1200:
        x = 0
    #Spawning of enemies
    if count % frequency == 0 and score <= 650:
        Enemylist.append(Enemy(random.randint(66,650),0.1, enemy2_img, enemy2_info))
    if count > 1000:
        count = 0

    #Controlling the speed and the frequency of enemies
    if count % 300 == 0:
        if frequency > 5:
            frequency -= 4
        elif frequency < 5 and frequency > 1:
            frequency -= 4
        elif frequency <=1:
            frequency -=0.01    
        velocity *= 1.15

    #Spawning the car
    screen.blit(car_img, Player.get_pos(car))

    #Calling collision detection in action
    for enemy in Enemylist:
        enemy.update(time_passed)
        screen.blit(enemy2_img, (enemy.x, enemy.y))
        if Enemy.get_pos(enemy)[1] > 600:
            Enemylist.remove(enemy)
            score += 10
            ding = pygame.mixer.Sound('sound/ding.wav').play()

        elif enemy.collide(car) == True:
            boom = pygame.mixer.Sound('sound/blast.wav').play()
            screen.blit(explosion_img, (explosion_pos[0], explosion_pos[1]))
            time.sleep(0.05)
            Enemylist.remove(enemy)

    count += 1

    scoretext = myfont.render("Score {0}".format(score), 4, (255,255,255))
    screen.blit(scoretext, (5, 10))
    lifetext = myfont.render("Lives {0}".format(lives), 4, (255,255,255))
    screen.blit(lifetext, (700, 10))
    highscoretext = myfont.render("Highscore {0}".format(get_high_score()), 4, (255,255,255))    
    screen.blit(highscoretext, (350, 10))

    #Key mappings
    if keys[0]==True and Player.get_pos(car)[0]>80:
        Player.get_pos(car)[0] -= 10
    if keys[1]==True and Player.get_pos(car)[0]<642:
        Player.get_pos(car)[0] += 10
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == pygame.KEYDOWN:
            if event.key==K_LEFT:
                keys[0]=True
            elif event.key==K_RIGHT:
                keys[1]=True
            elif event.key==K_ESCAPE:
                execfile('menu.py')
 
        if event.type == pygame.KEYUP:
            if event.key==K_LEFT:
                keys[0]=False
            elif event.key==K_RIGHT:
                keys[1]=False

    if lives <=0:
        if(score>get_high_score()):
            save_high_score(score)
        save_score(score)    
        execfile('game_over.py')

    if not Enemylist:
        save_score(score)
        save_lives(lives)
        execfile('splash3.py')
    pygame.display.update()       
