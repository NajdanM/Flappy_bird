import pygame as pg
import random as rng
pg.init()

background=(137,207,240) 
(width, height) = (600,500)
screen = pg.display.set_mode((width, height))
screen.fill(background)
pg.display.set_caption('Flappy bird')
pg.display.flip()
running = True
pipes = pg.image.load('pipe.png') 
bird = pg.image.load('bird.png')
ground = pg.image.load('ground.png')
e=rng.randint(1,150)
x=400
y=170
vel= 8 
jmp= 15
g= -10  
jmp_pressed=5
jump_finished=0
while running: 
    pg.time.delay(50)
    keys = pg.key.get_pressed()
    if y > 0:
        if keys[pg.K_SPACE] and jump_finished==0:
            jmp_pressed=1   
            jmp=15 
            jump_finished=1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False   
    screen.blit(ground, (0,470))       
    screen.blit(pipes, (x,310+e))
    screen.blit(pipes, (x,-410+e))
    screen.blit(bird, (50,y))
    x-=vel
    if jmp_pressed<5:
        jmp_pressed+=1
        y-=jmp
        jmp-=3
    else:
        y-=g
        if jmp_pressed==5:
            jump_finished=0
    if y>440:
        running = False         
    pg.display.update()  
    screen.fill(background)
          