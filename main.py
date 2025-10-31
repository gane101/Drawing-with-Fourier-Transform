import numpy as np
from math import cos,sin,pi,sqrt,atan2
import pygame
from line_profiler import profile
import time
import pandas as pd


terms = 50


pygame.init()

screen = pygame.display.set_mode((800,500))
done = False

# Extracting the data
df = pd.read_csv("Path.csv")
xpoints = df["x"].to_list()
ypoints = df["y"].to_list()

time_step = 1/len(xpoints)

polar_coordinates = []
for i in range(len(xpoints)):
    x = xpoints[i]
    y = ypoints[i]
    r = sqrt(x*x + y*y)
    theta = atan2(y,x)
    polar_coordinates.append([r,theta])

# The coefficient of the nth term is found by an integral
# Which we are doing discretely
def c(n):
    re = 0
    im = 0

    for i in range(int(1/time_step)):
        r,theta = polar_coordinates[i]

        re += r*cos(theta - n*2*pi*i*time_step)
        im += r*sin(theta - n*2*pi*i*time_step)

    return [re,-im]


# The nth term of the function is given by multiplication of c(n) and e^(n*2*pi*i*t)
# Here, we are separating it into real and imaginary parts and then multiplying
def nth_term(n,t):
    a,b = c(n)

    re = a*cos(2*pi*n*t) - b*sin(2*pi*n*t)
    im = a*sin(2*pi*n*t) + b*cos(2*pi*n*t)

    return [re,im]

values = []
for i in range(terms):
    values.append((0,0))

pos = []

# The actual curve is given by adding many terms of the given function. More terms means better result.
# Since the terms can be positive or negative, the function is split into two parts,
# so we are moving forward in positive and negative direction at the same time
def curve(time_passed):

    t = time_passed/100

    if terms==1:
        return nth_term

    # The initial 0th term
    re, im = nth_term(0,t)
    values[0] = (re,im)

    total = 1
    i=1

    while total < terms:

        # The positive term
        re,im = nth_term(i,t)
        values[total] = (re,im)
        total += 1

        if total >= terms:
            break
        else:

            # The negative term
            re,im = nth_term(-i,t)
            values[total] = (re,im)

            total += 1
        i += 1

    return values

t=0
path = []
screen.fill((128,128,128))

fact = 1/1500  # The dampening factor since the values tend to go out of screen

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # screen.fill((128,128,128))

    val = curve(t)
    val = [(0,0)] + val

    t += 0.01
    pos = [0,0]

    for i in range(1,len(val)):
        # You can choose to enable the lines of vectors but make sure to also uncomment line 110
        # pygame.draw.line(screen, (0,0,0) ,(pos[0]*fact+400,-pos[1]*fact+250) , (pos[0]*fact+val[i][0]*fact+400 , -pos[1]*fact-val[i][1]*fact+250))

        pos = [pos[0]+val[i][0],pos[1]+val[i][1]]

    # If you want to see the actual path while watching the lines move in real time, uncomment the code below
    # path.append(pos)
    # for p in path:
        # pygame.draw.circle(screen,(0,0,0),(400+p[0]*fact,250-p[1]*fact),1)
    pygame.draw.circle(screen,(0,0,0),(400+pos[0]*fact,250-pos[1]*fact),2)

    
    if t >= 100:
        t -= 100
        pygame.image.save(screen,f"{terms}.png")
        screen.fill((128,128,128))

    pygame.display.flip()

