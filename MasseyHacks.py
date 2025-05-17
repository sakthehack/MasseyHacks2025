from pygame import *
from random import randint
import math
import time

font.intit()
Title = rect(475, 100, 300, 100)
beaufort = font.Font("BeaufortforLOL-Medium.ttf", 15)
width,height=1250,650
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()
running=True
background = Rect(0,0,width,height)
draw.rect(screen,(115,3,16), background)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\n")
        time.sleep(1)
        t -= 1

PMR=420
MOP=480
LOC=240
PMC=300

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
                  
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
      
    myClock.tick(60)
    display.flip()
            
quit()
