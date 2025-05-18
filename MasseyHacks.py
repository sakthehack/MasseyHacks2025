from pygame import *
from random import randint
import math
import time as pytime # You used time.sleep in countdown
import os
import openai

openai.api_key = ''
font.init()



speeches=[450,510,510,510,270,330]

def draw_back_button(screen):
    back_button_rect = Rect(40, 30, 60, 40)
    back_button_image = transform.scale(image.load("assets/back.png"), (60, 40))
    screen.blit(back_button_image, back_button_rect.topleft)
    return back_button_rect

endRect=Rect(425,593,400,50)
width,height=1250,650
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
background = Rect(0,0,width,height)
myClock=time.Clock()
running=True
draw.rect(screen,(115,3,16), background)
r,g,b = 116,3,16

class Slider:
    def __init__(self, x, y, color, width=600, height=15, max_value=255):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.max_value = max_value
        self.value = max_value // 2
        self.dragging = False

    def draw(self, surf):
        draw.rect(surf, (180, 180, 180), (self.x, self.y, self.width, self.height))
        knob_x = self.x + (self.value / self.max_value) * self.width
        draw.rect(surf, (0, 0, 0), (knob_x - 6, self.y - 6, 12, self.height + 12))
        draw.rect(surf, self.color, (knob_x - 5, self.y - 5, 10, self.height + 10))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y - 6 <= event.pos[1] <= self.y + self.height + 6:
                self.dragging = True
                self.update_value_from_mouse(event.pos[0])
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            self.update_value_from_mouse(event.pos[0])

    def update_value_from_mouse(self, mouse_x):
        relative_x = min(max(mouse_x - self.x, 0), self.width)
        self.value = int((relative_x / self.width) * self.max_value)

    def get_value(self):
        return self.value

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\n")
        pytime.sleep(1)
        t -= 1
red_slider = Slider(350, 150, (255, 0, 0))
green_slider = Slider(350, 220, (0, 255, 0))
blue_slider = Slider(350, 290, (0, 0, 255))
red_slider.value = 116
green_slider.value = 3
blue_slider.value = 16
volume_slider = Slider(350, 360, (200, 200, 200), max_value=100)
PMR=450
MOP=510
LOC=270
PMC=330
prep=900
def menu(screen):
    global r,g,b
    draw.rect(screen,(r,g,b),background)
    titletext = font.Font("assets/That Sounds Great.otf", 40)
    Title = Rect(325, 50, 600, 125)
    About = Rect(475, 200, 300, 100)
    Start = Rect(375, 325, 500, 100)
    settings = Rect(475, 450, 300, 100)
    Openinglist = [Title, About, Start, settings]
    openingtext = ["Debate.io", "About", "Start", "Settings"] 
    r = red_slider.get_value()
    g = blue_slider.get_value()
    b = green_slider.get_value()
    v = volume_slider.get_value()
    screen.fill((r,g,b))
    running=True
    while running:
        
        result = handle_events()
        if result == "exit":
            return "exit"
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()

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

        if mb[0] and Start.collidepoint(mx,my):
            return "debate"
        if mb[0] and settings.collidepoint(mx,my):
            return "settings"
        if mb[0] and About.collidepoint(mx,my):
            return "about"
        
        draw_back_button(screen)

        display.flip()
def get_random_topic():
    prompt = "Give me a creative topic for an American Parliamentary style debate. Start it with with an acronym like THBT (this house believes that or THR (this house regrets)or THW (this house would) or BIRT (be it resolves that). It can be fun interesting a little serious or whatever you think is apropriate and cool. This is for Highschool debate club practices.)"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    topic = response['choices'][0]['message']['content'].strip()
    return topic
def PrepDebate(screen):
    global topic, total_seconds, speeches
    endRect=Rect(425,593,400,50)
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    newButton=Rect(525,260,200,100)

    # Timer setup
    total_seconds = 10  # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
            
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not timer_ended:
            if not paused:
                remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
            else:
                remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        else:
            remaining_time = 0  # force it to 0 if timer ended

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")
        main_font = font.SysFont("assets/That Sounds Good.otf", 30)
        rendered_text = main_font.render(topic, True, (0, 0, 0))
        screen.blit(rendered_text, (100, 100))
        draw_button(newButton, "New Motion")
        draw_button(endRect, "End Speech")
        if newButton.collidepoint(mx,my):
            draw.rect(screen,WHITE,newButton,5)
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and newButton.collidepoint(mx,my):
            topic = get_random_topic()
            total_seconds = 10
            start_ticks = time.get_ticks()
            pause_accumulated = 0
            paused = False
        if mb[0] and endRect.collidepoint(mx,my):
            timer_ended=True

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "PmDebate"


        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()

topic = get_random_topic()

def PmDebate(screen):
    global speeches,endRect
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)

    # Timer setup
    total_seconds = speeches[0]   # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False
    poi_button = Rect(1050, 20, 150, 50)

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15  # seconds
    poi_count = 0

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if poi_button.collidepoint(evt.pos):
                    if poi_active:
                        poi_active = False
                        poi_count += 1
                    else:
                        poi_active = True
                        poi_start = time.get_ticks()
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")



        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x-150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "LopDebate"

        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()
def LopDebate(screen):
    global speeches,endRect
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)

    # Timer setup
    total_seconds = speeches[1]   # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False
    poi_button = Rect(1050, 20, 150, 50)

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15  # seconds
    poi_count = 0

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if poi_button.collidepoint(evt.pos):
                    if poi_active:
                        poi_active = False
                        poi_count += 1
                    else:
                        poi_active = True
                        poi_start = time.get_ticks()
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")



        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x-150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "MgDebate"

        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()
def MgDebate(screen):
    global speeches,endRect
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)

    # Timer setup
    total_seconds = speeches[2]   # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False
    poi_button = Rect(1050, 20, 150, 50)

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15  # seconds
    poi_count = 0

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if poi_button.collidepoint(evt.pos):
                    if poi_active:
                        poi_active = False
                        poi_count += 1
                    else:
                        poi_active = True
                        poi_start = time.get_ticks()
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")



        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x-150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "MoDebate"

        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()
def MoDebate(screen):
    global speeches,endRect
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)

    # Timer setup
    total_seconds = speeches[3]   # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False
    poi_button = Rect(1050, 20, 150, 50)

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15  # seconds
    poi_count = 0

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if poi_button.collidepoint(evt.pos):
                    if poi_active:
                        poi_active = False
                        poi_count += 1
                    else:
                        poi_active = True
                        poi_start = time.get_ticks()
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")



        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x-150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "LocDebate"

        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()
def LocDebate(screen):
    global speeches,endRect
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)

    # Timer setup
    total_seconds = speeches[4]   # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False
    poi_button = Rect(1050, 20, 150, 50)

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15  # seconds
    poi_count = 0

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if poi_button.collidepoint(evt.pos):
                    if poi_active:
                        poi_active = False
                        poi_count += 1
                    else:
                        poi_active = True
                        poi_start = time.get_ticks()
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")



        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x-150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "PmcDebate"

        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()
def PmcDebate(screen):
    global speeches,endRect
    back_button=draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    inputFont = font.SysFont("Arial", 32)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    # Buttons left and right of the timer
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    # Timer setup
    total_seconds = speeches[5]   # 15 minutes
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0

    # Input text field
    input_active = False
    input_text = ""
    input_box = TopicRect
    running=True
    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen,BLACK,rect,2)
        label = buttonFont.render(text, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_timer(start_ticks, total_seconds, pause_accumulated):
        current_ticks = time.get_ticks()
        seconds_passed = (current_ticks - start_ticks - pause_accumulated) // 1000
        remaining = max(0, total_seconds - seconds_passed)
        mins, secs = divmod(remaining, 60)
        timer_str = '{:02d}:{:02d}'.format(mins, secs)

        draw.rect(screen, RED, Timerrect)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))

        return remaining
    timer_ended = False
    poi_button = Rect(1050, 20, 150, 50)

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15  # seconds
    poi_count = 0

    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if poi_button.collidepoint(evt.pos):
                    if poi_active:
                        poi_active = False
                        poi_count += 1
                    else:
                        poi_active = True
                        poi_start = time.get_ticks()
                if pause_button.collidepoint(evt.pos) and not paused:
                    paused = True
                    pause_start = time.get_ticks()
                elif resume_button.collidepoint(evt.pos) and paused:
                    paused = False
                    pause_end = time.get_ticks()
                    pause_accumulated += pause_end - pause_start
                elif continue_button.collidepoint(mx,my) and remaining_time == 0:
                    print("sigma")
                    #would go to next thing.
                
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key == K_RETURN:
                    input_active = False
                else:
                    input_text += evt.unicode

            if mb[0] and back_button.collidepoint(mx,my):
                return "menu"
            back_button=draw_back_button(screen)
        
        screen.fill((r,g,b))

        # Draw input box with transparency and border
        topic_surface = Surface((input_box.width, input_box.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (input_box.x, input_box.y))
        draw.rect(screen, BLACK, input_box, 2)

        # Draw topic text
        text_surf = inputFont.render(input_text, True, BLACK)
        screen.blit(text_surf, (input_box.x + 10, input_box.y + 10))

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

        draw_button(pause_button, "Pause", not paused)
        draw_button(resume_button, "Resume", paused)

        if remaining_time == 0:
            if not timer_ended:
                if not paused:
                    remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
                else:
                    draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))

                draw_button(pause_button, "Pause", not paused)
                draw_button(resume_button, "Resume", paused)

                if remaining_time == 0:
                    timer_ended = True
            else:
                # Show the continue button instead of timer
                draw.rect(screen, RED, Timerrect)
                draw_button(continue_button, "Continue")



        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x-150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)

        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()


def settings(screen):
    font.init()
    main_font = font.SysFont("assets/That Sounds Good.otf", 40)
    small_font = font.SysFont("assets/That Sounds Good.otf", 30)
    back_button=draw_back_button(screen)

    
        
    

    sliders = [
        (red_slider, "Red"),
        (green_slider, "Green"),
        (blue_slider, "Blue"),
        (volume_slider, "Volume"),]
    
    running=True

    while running:
        result = handle_events()
        if result == "exit":
            return "exit"
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
    

        r = red_slider.get_value()
        g = blue_slider.get_value()
        b = green_slider.get_value()
        v = volume_slider.get_value()
        screen.fill((r,g,b))

        # Title
        title = main_font.render("Settings", True, WHITE)
        screen.blit(title, (width // 2 - title.get_width() // 2, 40))

        for slider, label in sliders:
            slider.draw(screen)
            label_text = small_font.render(f"{label}: {slider.get_value()}", True, WHITE)
            screen.blit(label_text, (slider.x - 130, slider.y - 5))

        for e in event.get():
            if e.type == QUIT:
                running = False
            for slider, _ in sliders:
                slider.handle_event(e)
        
        if mb[0] and back_button.collidepoint(mx, my):
            return "menu"
        
        back_button=draw_back_button(screen)

        display.flip()
    

def about(screen):
    title_font = font.SysFont("That Sounds Good.otf", 50)
    text_font = font.SysFont("That Sounds Good.otf", 28)
    back_button=draw_back_button(screen)
    odette=transform.scale(image.load("assets/odette.jpg"),(700,350))


    # Dummy slide data (replace with image filenames and captions if needed)
    about_slides = [
        {"image": "about1.png", "caption": "Welcome to Debate.io – your debate companion."},
        {"image": "about2.png", "caption": "Change the color palet of the app!"},
        {"image": "about3.png", "caption": "Used by trusted debaters all through Massey!"}
    ]

    # Load or mock image (if you don't have images, just use Rects)
    def load_slide_image(name):
        path = os.path.join("assets", name)
        if os.path.exists(path):
            return image.load(path).convert()
        else:
            # Draw placeholder surface with text
            surface = Surface((700, 350))
            # text = text_font.render("Missing Image", True, RED)
            # surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, 150))
            return surface

    # Load slide images
    for slide in about_slides:
        slide["surface"] = load_slide_image(slide["image"])

    current_slide = 0

    # Arrows
    left_arrow = Rect(150, height // 2 - 50, 60, 100)
    right_arrow = Rect(width - 210, height // 2 - 50, 60, 100)
    running = True
    while running:
        result = handle_events()
        if result == "exit":
            return "exit"
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        
        screen.fill((116,3,16))
        if mb[0] and back_button.collidepoint(mx,my):
            return "menu"
        
        back_button=draw_back_button(screen)

        # Title
        title = title_font.render("About Us", True, WHITE)
        screen.blit(title, (width // 2 - title.get_width() // 2, 30))

        # Draw current image
        image_box = about_slides[current_slide]["surface"]
        screen.blit(image_box, (width // 2 - image_box.get_width() // 2, 120))


        odette_x, odette_y = 275, 120
        screen.blit(odette, (odette_x, odette_y))

        # Draw caption directly below Odette image
        caption_text = text_font.render(about_slides[current_slide]["caption"], True, WHITE)
        caption_x = width // 2 - caption_text.get_width() // 2
        caption_y = odette_y + odette.get_height() + 20  # 20px gap below image
        screen.blit(caption_text, (caption_x, caption_y))

        # Arrows
        draw.polygon(screen, WHITE, [(left_arrow.right, left_arrow.top), (left_arrow.left, left_arrow.centery), (left_arrow.right, left_arrow.bottom)])
        draw.polygon(screen, WHITE, [(right_arrow.left, right_arrow.top), (right_arrow.right, right_arrow.centery), (right_arrow.left, right_arrow.bottom)])

        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if left_arrow.collidepoint(e.pos):
                    current_slide = (current_slide - 1) % len(about_slides)
                elif right_arrow.collidepoint(e.pos):
                    current_slide = (current_slide + 1) % len(about_slides)
        


        display.flip()
def handle_events():
    for evt in event.get():
        if evt.type ==QUIT:
            return "exit"

page = "menu"
while page != "exit":
    if page == "menu":
        page = menu(screen)
    elif page == "debate":
        page = PrepDebate(screen)
    elif page == "PmDebate":
        page = PmDebate(screen)
    elif page == "LopDebate":
        page = LopDebate(screen)
    elif page == "MgDebate":
        page = MgDebate(screen)
    elif page == "MoDebate":
        page = MoDebate(screen)
    elif page == "LocDebate":
        page = LocDebate(screen)
    elif page == "PmcDebate":
        page = PmcDebate(screen)
    elif page == "settings":
        page = settings(screen)
    elif page == "about":
        page = about(screen)
 
quit()
