import pygame as pg 
import numpy as np
import random as rng

pg.init()


""" Bird class """


class Bird():
    def __init__(self,bird_x,bird_y):
        self.y = bird_y
        self.x = bird_x
        self.vel = 20
        self.jump_finish = 1
        self.image = pg.image.load("bird.png")
        self.score = 0

    def jump(self):
        if self.jump_finish == 1:
            self.vel = -20
            self.jump_finish = 0

    def update(self):    
        self.y += self.vel
        if self.vel < 20 :
            self.vel += 4
        if self.vel == 0:
            self.jump_finish = 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def pipe_collision (self, pipe_y):
        if self.y + 34 >= pipe_y or self.y <= pipe_y - 130:
            return True
        return False
    
    def ground_collision (self):
        if self.y >= 430:
            return True
        return False


""" Upper pipe class """


class pipe_up():
    def __init__(self,pipe_x,pipe_y,pipe_vel,pipe_gap):
        self.vel = pipe_vel
        self.x = pipe_x
        self.y = pipe_y
        self.gap = pipe_gap
        self.image = pg.image.load("pipe.png")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        self.x -= self.vel


""" Lower pipe class """


class pipe_down():
    def __init__(self,pipe_x,pipe_y,pipe_vel,pipe_gap):
        self.vel = pipe_vel
        self.x = pipe_x
        self.y = pipe_y
        self.gap = pipe_gap
        self.image = pg.image.load("pipe.png")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x -= self.vel


""" Pipe maker """


def new_pipe ():
    pipe_x = 800
    pipe_y = 310
    pipe_gap = 160 
    pipe_vel = 8
    e = rng.randint(-150,150)
    lower = pipe_down(pipe_x, pipe_y + e, pipe_vel, pipe_gap)
    pipe_y = -410
    upper = pipe_up(pipe_x, pipe_y + e, pipe_vel, pipe_gap)
    pipes.append(lower)
    pipes.append(upper)


""" First pipes """


def first_pipes():
    pipe_x = 480
    pipe_y = 310
    pipe_gap = 120 
    pipe_vel = 8
    e = rng.randint(-150,150)
    lower = pipe_down(pipe_x, pipe_y + e, pipe_vel, pipe_gap)
    pipe_y = -410
    upper = pipe_up(pipe_x, pipe_y + e, pipe_vel, pipe_gap)
    pipes.append(lower)
    pipes.append(upper)


""" Bird initialization """


birds = []
bird_y = 160
bird_x = 40
bird = Bird(bird_x,bird_y)
birds.append(bird)
score = 0


""" Pipe initialization """


pipes = []
pipe_number = 0
first_pipes()


""" Screen implementation """


background=(137,207,240) 
(width, height) = (600,500)
screen = pg.display.set_mode((width, height))
screen.fill(background)
pg.display.set_caption('Flappy bird')
pg.display.flip()
running = True
clock = pg.time.Clock()
font = pg.font.Font(None, 40)
ground = pg.image.load("ground.png")


""" Game """


while running: 
    pg.time.delay(45)
    clock.tick()
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False

    """ Jump """
    
    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        bird.jump()

    """ Adding pipes """
    
    if(pipes[pipe_number].x <= 400):
        new_pipe()
        pipe_number += 2

    """ Deleting pipes """
    
    if(pipes[0].x < -100):
        del pipes[0]
        del pipes[0]
        pipe_number -=2
        score +=1

    """ Drawing """

    for pipe in pipes:
        pipe.update()
    for pipe in pipes:
        pipe.draw(screen)
    for bird in birds:
        bird.update()
    for bird in birds:
        bird.draw(screen)
    screen.blit(ground, (0, 470))
    text = font.render('Score '+str(score), 1, (255,255,255))   
    screen.blit(text, (0,0)) 
    pg.display.update() 
    screen.fill(background)

    """ Pipe collision """
    """ lower_pipe_y = pipes[0].y"""
    
    if pipes[0].x <= 73 and pipes[0].x > -57:
        for bird in birds:
            if bird.pipe_collision(pipes[0].y):  
                running = False

    """ Ground collision"""

    for bird in birds:
        if bird.ground_collision():
            running = False