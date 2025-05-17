from pygame import *
from random import randint
import math
import time

font.intit()
Title = rect(475, 100, 300, 100)
beaufort = font.Font("That Sounds Great.otf", 40)
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
Title = Rect(325, 50, 600, 125)
About = Rect(475, 200, 300, 100)
Start = Rect(375, 325, 500, 100)
settings = Rect(475, 450, 300, 100)
Openinglist = [Title, About, Start, settings]
openingtext = ["Debate.io", "About", "Start", "Settings"]
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
prep=900

while running:
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    for evt in event.get():
        if evt.type==QUIT:
            running=False
     for i in Openinglist:
        draw.rect(screen, (225,3,16), i)
        textt = titletext.render(openingtext[Openinglist.index(i)],True, BLACK)
        text_rect = textt.get_rect(center = i.center)
        screen.blit(textt,text_rect)
        if i.collidepoint(mx,my):
            if Openinglist.index(i) != 0:
                draw.rect(screen, WHITE, i, 2)
            else:
                draw.rect(screen,BLACK,i,2)
        else:
            draw.rect(screen,BLACK,i,2)              
      
    myClock.tick(60)
    display.flip()
            
quit()
