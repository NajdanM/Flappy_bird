import pygame as pg 
import numpy as np
import random as rng
import neat
import os

pg.init()


""" Bird class """


class Bird():
    def __init__(self,bird_x,bird_y):
        self.y = bird_y
        self.x = bird_x
        self.vel = 20
        self.jump_finish = 1
        self.image = pg.image.load("drakula.png")

    def jump(self):
        if self.jump_finish == 1:
            self.vel = -20
            self.jump_finish = 0

    def update(self):    
        self.y += self.vel
        if self.vel < 20 :
            self.vel += 5
        if self.vel == -5:
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


""" Screen implementation """


background=(137,207,240) 
(width, height) = (600,500)
screen = pg.display.set_mode((width, height))
screen.fill(background)
pg.display.set_caption('Flappy bird')
pg.display.flip()
font = pg.font.Font(None, 40)
ground = pg.image.load("ground.png")

pipes = []
gen = 0


""" Game """


def eval_genomes(genomes, config):
    global gen
    gen +=1
    nets = []
    ge = []
    birds = []

    e = rng.randint(-150,150)
    pipes = [pipe_down(480,310+e,8,120),pipe_up(480,-410+e,8,120)]

    for x, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(40,160))
        ge.append(genome)

    pipe_number = 0
    score = 0
    speed = 45

    running = True
    while running and len(birds) > 0: 
        pg.time.delay(speed)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False
                pg.quit()
                quit()
                break    

        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and speed != 0:
            speed -= 1
        if keys[pg.K_DOWN]:
            speed +=1    
        
        for x, bird in enumerate(birds):
            bird.update()
            ge[x].fitness += 0.1
            output = nets[x].activate((bird.y, abs(bird.y - (pipes[1].y + 600)), abs(bird.y - pipes[0].y)))

            if output[0] > 0.5:
                bird.jump()

        """ Adding pipes """
        
        if(pipes[pipe_number].x <= 400):
            e = rng.randint(-150,150)
            pipes.append(pipe_down(800,310+e,8,120))
            pipes.append(pipe_up(800,-410+e,8,120))
            pipe_number += 2

        """ Deleting pipes """
        
        if(pipes[0].x < -100):
            del pipes[0]
            del pipes[0]
            pipe_number -=2
            score +=1
            for g in ge:
                g.fitness += 5

        """ Drawing """

        for pipe in pipes:
            pipe.update()
        for pipe in pipes:
            pipe.draw(screen)
        for bird in birds:
            bird.draw(screen)
        screen.blit(ground, (0, 470))
        text = font.render(''+str(score), 1, (255,255,255))
        screen.blit(text, (270,100)) 
        text2 = font.render('Generacija: '+str(gen), 1, (255,255,255))
        screen.blit(text2, (0,0))
        pg.display.update() 
        screen.fill(background)

        """ Pipe collision """
        
        if pipes[0].x <= 80 and pipes[0].x > -60:
            for x, bird in enumerate(birds):
                if bird.pipe_collision(pipes[0].y):  
                    ge[x].fitness -= 1
                    nets.pop(x)
                    ge.pop(x)
                    birds.pop(x)

        """ Ground collision"""

        for x, bird in enumerate(birds):
            if bird.ground_collision() or bird.y < -50:
                nets.pop(x)
                ge.pop(x)
                birds.pop(x)


""" Adding text document with information for genetic algorithm """


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

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