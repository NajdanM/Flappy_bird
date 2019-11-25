import pygame as pg 
import numpy as np
import random as rng
import os
import neat

pg.init()


""" Bird class """


class Bird():
    def __init__(self,bird_x,bird_y):
        self.y = bird_y
        self.x = bird_x
        self.vel = 20
        self.jump_finish = 1
        self.image = pg.image.load("bird.png")

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
        if self.y + 40 >= pipe_y or self.y <= pipe_y - 120:
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


def new_pipe (pipes):
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


def first_pipes(pipes):
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

gen = 0
birds = []
pipe_number = 0

""" Drawing """
    
def drawing (pipes,birds,screen):
    for pipe in pipes:
        pipe.draw(screen)
    for bird in birds:
        bird.draw(screen)
    screen.blit(ground, (0, 470))
    pg.display.update()
    screen.fill(background)


""" Screen implementation """


background=(137,207,240) 
(width, height) = (600,500)
screen = pg.display.set_mode((width, height))
screen.fill(background)
pg.display.set_caption('Flappy bird')
pg.display.flip()
ground = pg.image.load("ground.png")
pipes = []
first_pipes(pipes)
gen = 0

""" Game """

def eval_genomes(genomes, config):
    global  gen
    gen += 1
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(40,170))
        ge.append(genome)
    score = 0
    pipe_number = 0
    clock = pg.time.Clock() 
    running = True
    while running:
        pg.time.delay(45)
        clock.tick(45)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False

        """ Moving """
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.update()

        output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[0].y), abs(bird.y - pipes[0].y - 120)))

        if output[0] > 0.5:  
            bird.jump()

        for pipe in pipes:
            pipe.update()


        """ Adding pipes """
        
        if(pipes[pipe_number].x <= 400):
            new_pipe(pipes)
            pipe_number += 2
            score +=1

        """ Deleting pipes """
        
        if(pipes[0].x < -100):
            del pipes[0]
            del pipes[0]
            pipe_number -=2

        """ Pipe collision """
        """ lower_pipe_y = pipes[0].y"""
        
        if pipes[0].x <= 80 and pipes[0].x > -60:
            for bird in birds:
                if bird.pipe_collision(pipes[0].y):  
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

        """ Ground collision"""

        for bird in birds:
            if bird.ground_collision():
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
        
        drawing(pipes, birds, screen)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)