from pygame import *
from random import randint
import random
import math
import time as pytime # You used time.sleep in countdown
import os
import openai

openai.api_key = 'put it yourself'

font.init()



speeches=[450,510,510,510,270,330]

def draw_back_button(screen):
    back_button_rect = Rect(35, 20, 100, 50)
    mouse_pos = mouse.get_pos()
    is_hovered = back_button_rect.collidepoint(mouse_pos)

    background_color = (255, 255, 240) if is_hovered else (240, 240, 240)
    border_color = (80, 80, 80) if is_hovered else (50, 50, 50)
    if is_hovered:
        glow_rect = back_button_rect.inflate(12, 12)
        s = Surface(glow_rect.size, SRCALPHA)
        draw.ellipse(s, (255, 255, 180, 60), s.get_rect())
        screen.blit(s, glow_rect.topleft)
    draw.rect(screen, background_color, back_button_rect, border_radius=8)
    draw.rect(screen, border_color, back_button_rect, 2, border_radius=8)
    button_font = font.SysFont("georgia", 28, bold=True)
    text_surface = button_font.render("Back", True, (30, 30, 30))
    text_rect = text_surface.get_rect(center=back_button_rect.center)
    screen.blit(text_surface, text_rect)
    return back_button_rect




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
input_active = False
lines = [""]
scroll_offset = 0
inputFont = font.SysFont("Arial", 32)
line_height = inputFont.get_height()
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
    Ttext = font.Font("assets/That Sounds Great.otf", 70)
    Title = Rect(400, 50, 800, 125)
    title=Ttext.render("Debate.io", True, BLACK)
    About = Rect(475, 200, 300, 100)
    Start = Rect(375, 325, 500, 100)
    settings = Rect(475, 450, 300, 100)
    Openinglist = [About, Start, settings]
    openingtext = ["About", "Start", "Settings"] 
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

        screen.blit(title,Title)

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
            return "topGen"
        if mb[0] and settings.collidepoint(mx,my):
            return "settings"
        if mb[0] and About.collidepoint(mx,my):
            return "about"
        
        draw_back_button(screen)

        display.flip()

def get_random_topic(input_text):
    prompt = f"Give me a creative topic for an American Parliamentary style debate. Start it with with an acronym like THBT (this house believes that or THR (this house regrets)or THW (this house would) or BIRT (be it resolves that). The genre that the user has chosen for debate is: {input_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    topic = response['choices'][0]['message']['content'].strip()
    return topic

def get_max_visible_lines():
    global TopicRect
    return TopicRect.height // line_height

def wrap_last_line():
    while True:
        if not lines:
            lines.append("")
        last_line = lines[-1]
        if inputFont.size(last_line)[0] <= TopicRect.width - 20:
            break
        if ' ' in last_line:
            last_space = last_line.rfind(' ')
            new_line = last_line[last_space+1:]
            lines[-1] = last_line[:last_space]
        else:
            new_line = last_line[-1]
            lines[-1] = last_line[:-1]
        lines.append(new_line)

def topGen(screen):
    back_button = draw_back_button(screen)

    input_rect   = Rect(150, 250, 950, 60)
    input_active = False
    input_text   = ""

    input_font   = font.SysFont("Arial", 32)
    button_font  = font.SysFont("Arial", 36)

    prompt_text  = "Enter topic genre:"
    generate_button_rect = Rect(500, 340, 300, 60)
    accept_button_rect   = Rect(550, 500, 200, 60)

    topic = None

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb     = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            elif evt.type == MOUSEBUTTONDOWN:
                if input_rect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False

                if back_button.collidepoint(evt.pos):
                    return "menu"

                if generate_button_rect.collidepoint(evt.pos):
                    topic = get_random_topic(input_text)  # Replace with your topic generator

                if topic and accept_button_rect.collidepoint(evt.pos):
                    return topic

            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif evt.key in (K_RETURN, K_KP_ENTER):
                    input_active = False
                else:
                    input_text += evt.unicode

        # ---- Drawing ----
        screen.fill((r, g, b))  # Define r, g, b elsewhere

        # Input Box
        box_surface = Surface((input_rect.w, input_rect.h), SRCALPHA)
        box_surface.fill((255, 255, 255, 180))
        screen.blit(box_surface, input_rect.topleft)
        draw.rect(screen, BLACK, input_rect, 2)

        # Prompt or Input Text
        if input_text or input_active:
            txt_surface = input_font.render(input_text, True, BLACK)
        else:
            txt_surface = input_font.render(prompt_text, True, (150, 150, 150))
        screen.blit(txt_surface, (input_rect.x + 10, input_rect.y + 14))

        # Generate Button
        gen_color = (200, 200, 255) if generate_button_rect.collidepoint(mx, my) else (180, 180, 220)
        draw.rect(screen, gen_color, generate_button_rect)
        draw.rect(screen, BLACK, generate_button_rect, 2)
        gen_label = button_font.render("Generate Topic", True, BLACK)
        screen.blit(gen_label, gen_label.get_rect(center=generate_button_rect.center))

        if topic:
            words = topic.split()
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + " " + word) <= 50:
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            # Draw up to two lines of topic, ABOVE the input bar
            for i, line in enumerate(lines):
                label = f"Topic: {line}" if i == 0 else line
                topic_surf = input_font.render(label, True, BLACK)
                screen.blit(topic_surf, (input_rect.x + 200, input_rect.y - 150 + i * 35))  # Above input box

            # Accept Button
            accept_color = (180, 255, 180) if accept_button_rect.collidepoint(mx, my) else (160, 230, 160)
            draw.rect(screen, accept_color, accept_button_rect)
            draw.rect(screen, BLACK, accept_button_rect, 2)
            accept_label = button_font.render("Accept", True, BLACK)
            screen.blit(accept_label, accept_label.get_rect(center=accept_button_rect.center))

        # Back Button (draw again each frame)
        back_button = draw_back_button(screen)

        display.flip()



def PrepDebate(screen,input_text):
    global total_seconds, speeches
    topic=input_text
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

    # Timer setup
    total_seconds = 900  # 15 minutes
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

        main_font = font.SysFont("assets/That Sounds Good.otf", 40)

        if topic:
            words = topic.split()
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + " " + word) <= 50:
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            # Draw up to two lines of topic, ABOVE the input bar
            for i, line in enumerate(lines):
                label = f"{line}" if i == 0 else line
                topic_surf = main_font.render(label, True, BLACK)
                screen.blit(topic_surf, (250, 150 + i * 35))  # Above input box

        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
            timer_ended=True

        if mb[0] and continue_button.collidepoint(mx,my) and timer_ended:
            return "PmDebate"


        if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
            
        back_button=draw_back_button(screen)

        display.flip()

def PmDebate(screen):
    global speeches, lines, scroll_offset, input_active
    
    # Initialize text input variables
    lines = [""]
    scroll_offset = 0
    input_active = False
    inputFont = font.SysFont("Arial", 32)
    line_height = inputFont.get_height()
    
    back_button = draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    poi_button = Rect(1050, 20, 150, 50)

    # Timer setup
    total_seconds = speeches[0]
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0
    timer_ended = False

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15
    poi_count = 0

    def get_max_visible_lines():
        return TopicRect.height // line_height

    def wrap_last_line():
        while True:
            if not lines:
                lines.append("")
            last_line = lines[-1]
            if inputFont.size(last_line)[0] <= TopicRect.width - 20:
                break
            if ' ' in last_line:
                last_space = last_line.rfind(' ')
                new_line = last_line[last_space+1:]
                lines[-1] = last_line[:last_space]
            else:
                new_line = last_line[-1]
                lines[-1] = last_line[:-1]
            lines.append(new_line)

    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen, BLACK, rect, 2)
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
        draw.rect(screen, BLACK, Timerrect, 2)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))
        return remaining

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if TopicRect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False
                    
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
                elif continue_button.collidepoint(mx, my) and remaining_time == 0:
                    return "LopDebate"
                    
            elif evt.type == MOUSEWHEEL:
                max_scroll = max(0, len(lines) - get_max_visible_lines())
                scroll_offset -= evt.y
                scroll_offset = max(0, min(scroll_offset, max_scroll))
                
            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    if lines[-1] == "":
                        if len(lines) > 1:
                            lines.pop()
                    else:
                        lines[-1] = lines[-1][:-1]
                elif evt.key == K_RETURN:
                    lines.append("")
                elif evt.key == K_s and (evt.mod & KMOD_CTRL):
                    with open("Pmnotes.txt", "w", encoding="utf-8") as file:
                        for line in lines:
                            file.write(line + "\n")
                    file.close()
                else:
                    lines[-1] += evt.unicode
                    wrap_last_line()
                scroll_offset = max(0, len(lines) - get_max_visible_lines())

            if mb[0] and back_button.collidepoint(mx, my):
                return "menu"
        
        screen.fill((r, g, b))
        
        # Draw text input box
        topic_surface = Surface((TopicRect.width, TopicRect.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (TopicRect.x, TopicRect.y))
        draw.rect(screen, BLACK, TopicRect, 2)
        
        # Draw wrapped text with scroll
        screen.set_clip(TopicRect)
        y_offset = TopicRect.y + 5
        visible_lines = lines[scroll_offset:scroll_offset + get_max_visible_lines()]
        for line in visible_lines:
            txt_surface = inputFont.render(line, True, BLACK)
            screen.blit(txt_surface, (TopicRect.x + 10, y_offset))
            y_offset += line_height
        screen.set_clip(None)

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        endRect=Rect(425,593,400,50)
        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
                    timer_ended=True
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
                timer_ended = True
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
        back_button = draw_back_button(screen)
        
        display.flip()
def LopDebate(screen):
    global speeches, lines, scroll_offset, input_active

    lines = [""]
    scroll_offset = 0
    input_active = False
    inputFont = font.SysFont("Arial", 32)
    line_height = inputFont.get_height()

    back_button = draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    poi_button = Rect(1050, 20, 150, 50)

    total_seconds = speeches[1]  # use LOP's time
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0
    timer_ended = False

    poi_active = False
    poi_start = 0
    poi_duration = 15
    poi_count = 0

    def get_max_visible_lines():
        return TopicRect.height // line_height

    def wrap_last_line():
        while True:
            if not lines:
                lines.append("")
            last_line = lines[-1]
            if inputFont.size(last_line)[0] <= TopicRect.width - 20:
                break
            if ' ' in last_line:
                last_space = last_line.rfind(' ')
                new_line = last_line[last_space + 1:]
                lines[-1] = last_line[:last_space]
            else:
                new_line = last_line[-1]
                lines[-1] = last_line[:-1]
            lines.append(new_line)

    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen, BLACK, rect, 2)
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
        draw.rect(screen, BLACK, Timerrect, 2)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))
        return remaining

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if TopicRect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False

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
                elif continue_button.collidepoint(mx, my) and remaining_time == 0:
                    return "MgDebate"

            elif evt.type == MOUSEWHEEL:
                max_scroll = max(0, len(lines) - get_max_visible_lines())
                scroll_offset -= evt.y
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    if lines[-1] == "":
                        if len(lines) > 1:
                            lines.pop()
                    else:
                        lines[-1] = lines[-1][:-1]
                elif evt.key == K_RETURN:
                    lines.append("")
                elif evt.key == K_s and (evt.mod & KMOD_CTRL):
                    with open("LOnotes.txt", "w", encoding="utf-8") as file:
                        for line in lines:
                            file.write(line + "\n")
                    file.close()
                    
                else:
                    lines[-1] += evt.unicode
                    wrap_last_line()
                scroll_offset = max(0, len(lines) - get_max_visible_lines())

            if mb[0] and back_button.collidepoint(mx, my):
                return "menu"

        screen.fill((r, g, b))

        topic_surface = Surface((TopicRect.width, TopicRect.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (TopicRect.x, TopicRect.y))
        draw.rect(screen, BLACK, TopicRect, 2)

        screen.set_clip(TopicRect)
        y_offset = TopicRect.y + 5
        visible_lines = lines[scroll_offset:scroll_offset + get_max_visible_lines()]
        for line in visible_lines:
            txt_surface = inputFont.render(line, True, BLACK)
            screen.blit(txt_surface, (TopicRect.x + 10, y_offset))
            y_offset += line_height
        screen.set_clip(None)

        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        endRect=Rect(425,593,400,50)
        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
                    timer_ended=True
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
                timer_ended = True
            draw_button(continue_button, "Continue")

        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x - 150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)
        back_button = draw_back_button(screen)

        display.flip()

def MgDebate(screen):
    global speeches, lines, scroll_offset, input_active

    lines = [""]
    scroll_offset = 0
    input_active = False
    inputFont = font.SysFont("Arial", 32)
    line_height = inputFont.get_height()

    back_button = draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    poi_button = Rect(1050, 20, 150, 50)

    total_seconds = speeches[2]  # use MG's time
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0
    timer_ended = False

    poi_active = False
    poi_start = 0
    poi_duration = 15
    poi_count = 0

    def get_max_visible_lines():
        return TopicRect.height // line_height

    def wrap_last_line():
        while True:
            if not lines:
                lines.append("")
            last_line = lines[-1]
            if inputFont.size(last_line)[0] <= TopicRect.width - 20:
                break
            if ' ' in last_line:
                last_space = last_line.rfind(' ')
                new_line = last_line[last_space + 1:]
                lines[-1] = last_line[:last_space]
            else:
                new_line = last_line[-1]
                lines[-1] = last_line[:-1]
            lines.append(new_line)

    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen, BLACK, rect, 2)
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
        draw.rect(screen, BLACK, Timerrect, 2)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))
        return remaining

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if TopicRect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False

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
                elif continue_button.collidepoint(mx, my) and remaining_time == 0:
                    return "MoDebate"

            elif evt.type == MOUSEWHEEL:
                max_scroll = max(0, len(lines) - get_max_visible_lines())
                scroll_offset -= evt.y
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    if lines[-1] == "":
                        if len(lines) > 1:
                            lines.pop()
                    else:
                        lines[-1] = lines[-1][:-1]
                elif evt.key == K_RETURN:
                    lines.append("")
                elif evt.key == K_s and (evt.mod & KMOD_CTRL):
                    with open("mgnotes.txt", "w", encoding="utf-8") as file:
                        for line in lines:
                            file.write(line + "\n")
                    file.close()
                else:
                    lines[-1] += evt.unicode
                    wrap_last_line()
                scroll_offset = max(0, len(lines) - get_max_visible_lines())

            if mb[0] and back_button.collidepoint(mx, my):
                return "menu"

        screen.fill((r, g, b))

        topic_surface = Surface((TopicRect.width, TopicRect.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (TopicRect.x, TopicRect.y))
        draw.rect(screen, BLACK, TopicRect, 2)

        screen.set_clip(TopicRect)
        y_offset = TopicRect.y + 5
        visible_lines = lines[scroll_offset:scroll_offset + get_max_visible_lines()]
        for line in visible_lines:
            txt_surface = inputFont.render(line, True, BLACK)
            screen.blit(txt_surface, (TopicRect.x + 10, y_offset))
            y_offset += line_height
        screen.set_clip(None)

        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        endRect=Rect(425,593,400,50)
        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
                    timer_ended=True
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
                timer_ended = True
            draw_button(continue_button, "Continue")

        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x - 150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)
        back_button = draw_back_button(screen)

        display.flip()

def MoDebate(screen):
    global speeches, lines, scroll_offset, input_active

    # Initialize text input variables
    lines = [""]
    scroll_offset = 0
    input_active = False
    inputFont = font.SysFont("Arial", 32)
    line_height = inputFont.get_height()

    back_button = draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    poi_button = Rect(1050, 20, 150, 50)

    # Timer setup
    total_seconds = speeches[3]
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0
    timer_ended = False

    # POI variables
    poi_active = False
    poi_start = 0
    poi_duration = 15
    poi_count = 0

    def get_max_visible_lines():
        return TopicRect.height // line_height

    def wrap_last_line():
        while True:
            if not lines:
                lines.append("")
            last_line = lines[-1]
            if inputFont.size(last_line)[0] <= TopicRect.width - 20:
                break
            if ' ' in last_line:
                last_space = last_line.rfind(' ')
                new_line = last_line[last_space+1:]
                lines[-1] = last_line[:last_space]
            else:
                new_line = last_line[-1]
                lines[-1] = last_line[:-1]
            lines.append(new_line)

    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen, BLACK, rect, 2)
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
        draw.rect(screen, BLACK, Timerrect, 2)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))
        return remaining

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if TopicRect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False

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
                elif continue_button.collidepoint(mx, my) and remaining_time == 0:
                    return "LocDebate"

            elif evt.type == MOUSEWHEEL:
                max_scroll = max(0, len(lines) - get_max_visible_lines())
                scroll_offset -= evt.y
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    if lines[-1] == "":
                        if len(lines) > 1:
                            lines.pop()
                    else:
                        lines[-1] = lines[-1][:-1]
                elif evt.key == K_RETURN:
                    lines.append("")
                elif evt.key == K_s and (evt.mod & KMOD_CTRL):
                    with open("Monotes.txt", "w", encoding="utf-8") as file:
                        for line in lines:
                            file.write(line + "\n")
                    file.close()
                else:
                    lines[-1] += evt.unicode
                    wrap_last_line()
                scroll_offset = max(0, len(lines) - get_max_visible_lines())

            if mb[0] and back_button.collidepoint(mx, my):
                return "menu"

        screen.fill((r, g, b))

        # Draw text input box
        topic_surface = Surface((TopicRect.width, TopicRect.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (TopicRect.x, TopicRect.y))
        draw.rect(screen, BLACK, TopicRect, 2)

        # Draw wrapped text with scroll
        screen.set_clip(TopicRect)
        y_offset = TopicRect.y + 5
        visible_lines = lines[scroll_offset:scroll_offset + get_max_visible_lines()]
        for line in visible_lines:
            txt_surface = inputFont.render(line, True, BLACK)
            screen.blit(txt_surface, (TopicRect.x + 10, y_offset))
            y_offset += line_height
        screen.set_clip(None)

        # Draw timer and buttons
        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        endRect=Rect(425,593,400,50)
        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
                    timer_ended=True
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
                timer_ended = True
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
        back_button = draw_back_button(screen)

        display.flip()

def LocDebate(screen):
    global speeches, lines, scroll_offset, input_active

    lines = [""]
    scroll_offset = 0
    input_active = False
    inputFont = font.SysFont("Arial", 32)
    line_height = inputFont.get_height()

    back_button = draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    poi_button = Rect(1050, 20, 150, 50)

    total_seconds = speeches[4]  # use LOP's time
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0
    timer_ended = False

    poi_active = False
    poi_start = 0
    poi_duration = 15
    poi_count = 0

    def get_max_visible_lines():
        return TopicRect.height // line_height

    def wrap_last_line():
        while True:
            if not lines:
                lines.append("")
            last_line = lines[-1]
            if inputFont.size(last_line)[0] <= TopicRect.width - 20:
                break
            if ' ' in last_line:
                last_space = last_line.rfind(' ')
                new_line = last_line[last_space + 1:]
                lines[-1] = last_line[:last_space]
            else:
                new_line = last_line[-1]
                lines[-1] = last_line[:-1]
            lines.append(new_line)

    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen, BLACK, rect, 2)
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
        draw.rect(screen, BLACK, Timerrect, 2)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))
        return remaining

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if TopicRect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False

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
                elif continue_button.collidepoint(mx, my) and remaining_time == 0:
                    return "PmcDebate"

            elif evt.type == MOUSEWHEEL:
                max_scroll = max(0, len(lines) - get_max_visible_lines())
                scroll_offset -= evt.y
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    if lines[-1] == "":
                        if len(lines) > 1:
                            lines.pop()
                    else:
                        lines[-1] = lines[-1][:-1]
                elif evt.key == K_RETURN:
                    lines.append("")
                elif evt.key == K_s and (evt.mod & KMOD_CTRL):
                    with open("locnotes.txt", "w", encoding="utf-8") as file:
                        for line in lines:
                            file.write(line + "\n")
                    file.close()
                else:
                    lines[-1] += evt.unicode
                    wrap_last_line()
                scroll_offset = max(0, len(lines) - get_max_visible_lines())

            if mb[0] and back_button.collidepoint(mx, my):
                return "menu"

        screen.fill((r, g, b))

        topic_surface = Surface((TopicRect.width, TopicRect.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (TopicRect.x, TopicRect.y))
        draw.rect(screen, BLACK, TopicRect, 2)

        screen.set_clip(TopicRect)
        y_offset = TopicRect.y + 5
        visible_lines = lines[scroll_offset:scroll_offset + get_max_visible_lines()]
        for line in visible_lines:
            txt_surface = inputFont.render(line, True, BLACK)
            screen.blit(txt_surface, (TopicRect.x + 10, y_offset))
            y_offset += line_height
        screen.set_clip(None)

        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        endRect=Rect(425,593,400,50)
        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
                    timer_ended=True
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
                timer_ended = True
            draw_button(continue_button, "Continue")

        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x - 150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)
        back_button = draw_back_button(screen)

        display.flip()




file_names = ["Pmnotes.txt", "LOnotes.txt", "mgnotes.txt", "Monotes.txt", "locnotes.txt", "PMCnotes.txt"]

all_texts=  []


def generate_feedback(combined_text):
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a debate coach providing detailed, constructive feedback. If you dont get enough feedback, give general tips to improve. This is AP debate format. The format of the feedback, will be based of a judges perspective, it will mainly hightlight the points discussed and POI taken and all of the sorts. At the end of the feedback, you are to decide whether side opp won or side gov won the debate. Have the winner printed on its own line either gov or opp. A winner MUST be decided no matter how little information there is."}, {"role": "user", "content": f"Here are the debater's notes from six speeches:\n{combined_text}\nPlease give feedback on clarity, logic, rebuttals, style, and POI use. Give your own input on what you think you would have done if the debaters didnt do good enough."}])
        return response["choices"][0]["message"]["content"]

        feedback = ""

def PmcDebate(screen):
    global speeches, lines, scroll_offset, input_active

    lines = [""]
    scroll_offset = 0
    input_active = False
    inputFont = font.SysFont("Arial", 32)
    line_height = inputFont.get_height()

    back_button = draw_back_button(screen)
    font.init()
    timertxtFont = font.Font("assets/That Sounds Great.otf", 150)
    buttonFont = font.SysFont("Arial", 40)
    TopicRect = Rect(75, 75, 1100, 300)
    Timerrect = Rect(350, 432, 550, 150)
    continue_button = Rect(350, 432, 550, 150)
    pause_button = Rect(Timerrect.left - 160, Timerrect.centery - 30, 150, 60)
    resume_button = Rect(Timerrect.right + 10, Timerrect.centery - 30, 150, 60)
    poi_button = Rect(1050, 20, 150, 50)

    total_seconds = speeches[5]  # use LOP's time
    start_ticks = time.get_ticks()
    paused = False
    pause_start = 0
    pause_accumulated = 0
    timer_ended = False

    poi_active = False
    poi_start = 0
    poi_duration = 15
    poi_count = 0

    def get_max_visible_lines():
        return TopicRect.height // line_height

    def wrap_last_line():
        while True:
            if not lines:
                lines.append("")
            last_line = lines[-1]
            if inputFont.size(last_line)[0] <= TopicRect.width - 20:
                break
            if ' ' in last_line:
                last_space = last_line.rfind(' ')
                new_line = last_line[last_space + 1:]
                lines[-1] = last_line[:last_space]
            else:
                new_line = last_line[-1]
                lines[-1] = last_line[:-1]
            lines.append(new_line)

    def draw_button(rect, text, active=True):
        color = GREY if active else (100, 100, 100)
        rect_color = Surface((rect.width, rect.height), SRCALPHA)
        rect_color.fill((*color, 255))
        screen.blit(rect_color, (rect.x, rect.y))
        draw.rect(screen, BLACK, rect, 2)
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
        draw.rect(screen, BLACK, Timerrect, 2)
        timetext = timertxtFont.render(timer_str, True, BLACK)
        screen.blit(timetext, (Timerrect.x + 17, Timerrect.y - 15))
        return remaining

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                running = False
            elif evt.type == MOUSEBUTTONDOWN:
                if TopicRect.collidepoint(evt.pos):
                    input_active = True
                else:
                    input_active = False

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
                elif continue_button.collidepoint(mx, my) and remaining_time == 0:
                    for file in file_names:
                            with open(file, "r", encoding="utf-8") as f:
                                text = f.read()
                                all_texts.append(f"--- {file} ---\n{text}\n")
                    combined_text = "\n".join(all_texts)
                    final_feedback = generate_feedback(combined_text)

                    with open("debate_feedback.txt", "w", encoding="utf-8") as f:
                        f.write(final_feedback)
                    f.close()
                    return "Judging"

            elif evt.type == MOUSEWHEEL:
                max_scroll = max(0, len(lines) - get_max_visible_lines())
                scroll_offset -= evt.y
                scroll_offset = max(0, min(scroll_offset, max_scroll))

            elif evt.type == KEYDOWN and input_active:
                if evt.key == K_BACKSPACE:
                    if lines[-1] == "":
                        if len(lines) > 1:
                            lines.pop()
                    else:
                        lines[-1] = lines[-1][:-1]
                elif evt.key == K_RETURN:
                    lines.append("")
                elif evt.key == K_s and (evt.mod & KMOD_CTRL):
                    with open("PMCnotes.txt", "w", encoding="utf-8") as file:
                        for line in lines:
                            file.write(line + "\n")
                    file.close()
                    
                else:
                    lines[-1] += evt.unicode
                    wrap_last_line()
                scroll_offset = max(0, len(lines) - get_max_visible_lines())

            if mb[0] and back_button.collidepoint(mx, my):
                return "menu"

        screen.fill((r, g, b))

        topic_surface = Surface((TopicRect.width, TopicRect.height), SRCALPHA)
        topic_surface.fill((255, 255, 255, 180))
        screen.blit(topic_surface, (TopicRect.x, TopicRect.y))
        draw.rect(screen, BLACK, TopicRect, 2)

        screen.set_clip(TopicRect)
        y_offset = TopicRect.y + 5
        visible_lines = lines[scroll_offset:scroll_offset + get_max_visible_lines()]
        for line in visible_lines:
            txt_surface = inputFont.render(line, True, BLACK)
            screen.blit(txt_surface, (TopicRect.x + 10, y_offset))
            y_offset += line_height
        screen.set_clip(None)

        if not paused:
            remaining_time = draw_timer(start_ticks, total_seconds, pause_accumulated)
        else:
            draw_timer(start_ticks, total_seconds, pause_accumulated + (time.get_ticks() - pause_start))
        endRect=Rect(425,593,400,50)
        draw_button(endRect, "End Speech")
        if endRect.collidepoint(mx,my):
            draw.rect(screen,WHITE,endRect,5)
        if mb[0] and endRect.collidepoint(mx,my):
                    timer_ended=True
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
                timer_ended = True
            draw_button(continue_button, "Continue")

        if poi_active:
            poi_elapsed = (time.get_ticks() - poi_start) // 1000
            poi_remaining = max(0, poi_duration - poi_elapsed)
            poi_label = buttonFont.render(f"POI: {poi_remaining}s", True, WHITE)
            screen.blit(poi_label, (poi_button.x - 150, poi_button.y))
            if poi_remaining == 0:
                poi_count += 1
                poi_active = False

        draw_button(poi_button, f"POI: {poi_count}", not poi_active)
        back_button = draw_back_button(screen)

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
    odette=transform.scale(image.load("assets/odette.jpg"),(700,400))
    #little ai help
    about_slides = [
        {"image": "about1.png", "caption": "Welcome to Debate.io – your debate companion."},
        {"image": "about2.png", "caption": "Used and beloved by all Massey Debaters."},
        {"image": "about2.png", "caption": "Generate fun topics of your interest..."},
        {"image": "about3.png", "caption": "Have properly structured debates with built in debate timers..."},
        {"image": "about4.png", "caption": "And get consistent AI reviewed feedback based off your judge's notes"},
        {"image": "about5.png", "caption": "Start Debating Now with Debate.io!!!"}

    ]

    # Little AI usage to load images
    def load_slide_image(name):
        path = os.path.join("assets", name)
        if os.path.exists(path):
            return image.load(path).convert()
        else:
            surface = Surface((700, 350))
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
def judging(screen):
    import os
    font.init()
    title_font = font.SysFont("Arial", 80)
    button_font = font.SysFont("Arial", 50)
    result_font = font.SysFont("Arial", 60)


    results_button = Rect(460, 350, 310, 100)
    back_button = Rect(20, 20, 150, 60)

    winner_revealed = False
    winner = "Unknown"

    # Try to read the winner from the file
    winner_file_path = "debate_feedback.txt"
    if os.path.exists(winner_file_path):
        with open(winner_file_path, "r") as f:
            lines = f.readlines()
    winner = lines[-1]

    running = True
    while running:
        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()

        for evt in event.get():
            if evt.type == QUIT:
                return "exit"
            elif evt.type == MOUSEBUTTONDOWN:
                if results_button.collidepoint(evt.pos):
                    winner_revealed = True
                if back_button.collidepoint(evt.pos):
                    return "menu"

        screen.fill((116,3,15))

        # Title
        title_surface = title_font.render("Judging", True, BLACK)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 100))

        # Show Results button
        draw.rect(screen, (255,3,16) , results_button)
        draw.rect(screen, BLACK, results_button, 3)
        button_text = button_font.render("Show Results", True, WHITE)
        screen.blit(button_text, (results_button.centerx - button_text.get_width() // 2,
                                  results_button.centery - button_text.get_height() // 2))

        # Back button
        draw.rect(screen, GREY, back_button)
        draw.rect(screen, BLACK, back_button, 2)
        back_text = button_font.render("Back", True, BLACK)
        screen.blit(back_text, (back_button.x + 10, back_button.y))

        # Show winner if revealed
        if winner_revealed:
            result_text = result_font.render(f"{winner} Wins!", True, BLACK)
            screen.blit(result_text, (screen.get_width() // 2 - result_text.get_width() // 2, 500))

        display.flip()

        display.flip()
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu(screen)
    elif page=="topGen":
        page = topGen(screen)
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
    elif page == "Judging":
        judging(screen)
    else:
        page = PrepDebate(screen,page)
 
quit()
