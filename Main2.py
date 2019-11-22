import pygame as pg 
import numpy as np

pg.init()


""" Bird class """


class bird(pg.sprite.Sprite):
    def __init__(self,bird_y,bird_x):
        self.y = bird_y
        self.x = bird_x
        self.vel = 20
        self.image = pg.image.load("bird.png")
    def jump(self):
        self.vel = -10
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


""" Upper pipe class """


class pipe_up(pg.sprite.Sprite):
    def __init__(self,pipe_x,pipe_y,pipe_vel,pipe_gap):
        self.vel = pipe_vel
        self.x = pipe_x
        self.y = pipe_y
        self.gap = pipe_gap
        self.image = pg.image.load("pipe.png")
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y + self.gap/2))


""" Lower pipe class """


class pipe_down(pg.sprite.Sprite):
    def __init__(self,pipe_x,pipe_y,pipe_vel,pipe_gap):
        self.vel = pipe_vel
        self.x = pipe_x
        self.y = pipe_y
        self.gap = pipe_gap
        self.image = pg.image.load("pipe.png")
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y + self.gap/2))


""" Function for pipe making  """


def Pipe_maker(pipe_gap):
    pipe_x = 400
    pipe_vel = -8
    pipe_y = 250 + pipe_gap/2
    pipe_down(pipe_x, pipe_y, pipe_vel,pipe_gap)
    pipe_y = -350- pipe_gap/2
    pipe_up(pipe_x, pipe_y, pipe_vel,pipe_gap)


""" Screen implementation """


background=(137,207,240) 
(width, height) = (600,500)
screen = pg.display.set_mode((width, height))
screen.fill(background)
pg.display.set_caption('Flappy bird')
pg.display.flip()
running = True


""" variables 
x_pipe
y_pipe
y_bird
x_bird
pipe_gap
pipe_vel
bird_vel=gravity

"""


""" Game """
while running: 
    pg.time.delay(45)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        pass
     