from pygame import *
from random import randint
import math
import time as pytime # You used time.sleep in countdown
import os


font.init()

def draw_back_button(screen):
    back_button_rect = Rect(40, 50, 60, 40)
    back_button_image = transform.scale(image.load("assets/back.png"), (60, 40))
    screen.blit(back_button_image, back_button_rect.topleft)
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
volume_slider = Slider(350, 360, (200, 200, 200), max_value=100)
PMR=420
MOP=480
LOC=240
PMC=300
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
def PrepDebate(screen):
    back_button=draw_back_button(screen)
    running=True
    while running:

        display.flip()

def settings(screen):
    font.init()
    main_font = font.SysFont("That Sounds Good.otf", 40)
    small_font = font.SysFont("That Sounds Good.otf", 30)
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
    elif page == "settings":
        page = settings(screen)
    elif page == "about":
        page = about(screen)
 
quit()
