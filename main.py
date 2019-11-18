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
e1=rng.randint(-150,150)
e2=rng.randint(-150,150)
e3=rng.randint(-150,150)
x_pipe1=400
x_pipe2=800
x_pipe3=1200
y_bird=170
vel= 8 
jmp= 20
g= -20  
jmp_pressed=5
jump_finished=0
jump_fall=5
while running: 
    pg.time.delay(50)
    keys = pg.key.get_pressed()
    if y_bird > 0:
        if keys[pg.K_SPACE] and jump_finished==0:
            jmp_pressed=1   
            jmp=20 
            g=0
            jump_finished=1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False   
    screen.blit(ground, (0,470))       
    screen.blit(pipes, (x_pipe1,310+e1))
    screen.blit(pipes, (x_pipe1,-410+e1))
    screen.blit(pipes, (x_pipe2,310+e2))
    screen.blit(pipes, (x_pipe2,-410+e2))
    screen.blit(pipes, (x_pipe3,310+e3))
    screen.blit(pipes, (x_pipe3,-410+e3))
    screen.blit(bird, (40,y_bird))
    x_pipe1-=vel
    x_pipe2-=vel
    x_pipe3-=vel
    if x_pipe1==-120:
        x_pipe1=1080
        e1=rng.randint(-150,150)
    if x_pipe2==-120:
        x_pipe2=1080
        e2=rng.randint(-150,150)
    if x_pipe3==-120:
        x_pipe3=1080
        e3=rng.randint(-150,150)
    if jmp_pressed<5:
        jmp_pressed+=1
        y_bird-=jmp
        jmp-=5
        jump_fall=1
    else:
        if jump_fall<5:
            jump_fall+=1
            y_bird-=g
            g-=5
        else:
            y_bird-=g
        if jmp_pressed==5:
            jump_finished=0
    if x_pipe1<40 and x_pipe1>-60:
        if y_bird>270+e1 or y_bird<190+e1:
            running=False
    if x_pipe2<40 and x_pipe2>-60:
        if y_bird>270+e2 or y_bird<190+e2:
            running=False
    if x_pipe3<40 and x_pipe3>-60:
        if y_bird>270+e3 or y_bird<190+e3:
            running=False    
    if y_bird>440:
        running = False         
    pg.display.update()  
    screen.fill(background) 