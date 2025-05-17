from pygame import *
from random import randint
import math

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
while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
                  
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
      
    myClock.tick(60)
    display.flip()
            
quit()
