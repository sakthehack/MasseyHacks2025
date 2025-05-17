from pygame import *
from random import *
import math
import time as pytime # You used time.sleep in countdown

font.init()
Title = Rect(475, 100, 300, 100)
titletext = font.Font("That Sounds Great.otf", 40)

width, height = 1250, 650
screen = display.set_mode((width, height))
RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
CRED = (115, 3, 16)

running = True
background = Rect(0, 0, width, height)
myClock = time.Clock()
draw.rect(screen, (115, 3, 16), background)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\n")
        pytime.sleep(1)
        t -= 1

# Boxes for main screen
Title = Rect(325, 50, 600, 125)
About = Rect(475, 200, 300, 100)
Start = Rect(375, 325, 500, 100)
settings = Rect(475, 450, 300, 100)
Openinglist = [Title, About, Start, settings]
openingtext = ["Debate.io", "About", "Start", "Settings"]   

while running:
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    for evt in event.get():
        if evt.type == QUIT:
            running = False

    draw.rect(screen, CRED, background)  # Redraw background each frame

    for i in Openinglist:
        # Draw transparent rectangle
        rect_surface = Surface((i.width, i.height), SRCALPHA)
        rect_surface.fill((225, 3, 16, 60))  # Semi-transparent red
        screen.blit(rect_surface, (i.x, i.y))

        # Render and center the text
        textt = titletext.render(openingtext[Openinglist.index(i)], True, BLACK)
        text_rect = textt.get_rect(center=i.center)
        screen.blit(textt, text_rect)

        # Border hover effect
        if i.collidepoint(mx, my):
            border_color = BLACK if Openinglist.index(i) == 0 else WHITE
        else:
            border_color = BLACK
        draw.rect(screen, border_color, i, 2)

    myClock.tick(60)
    display.flip()

quit()
