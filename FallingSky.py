import pygame
import random
import time

# window
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Falling Sky")
clock = pygame.time.Clock()
bg = pygame.image.load('bg.jpg')
#music = pygame.mixer.music.load("music.wav")
#pygame.mixer.music.play(-1)
click_sound=pygame.mixer.Sound('click.wav')
cloud_img=pygame.image.load('cloud.png')
control_img=pygame.image.load('control.jpg')
hit_sound = pygame.mixer.Sound('hitsound.wav')                 
score = 0
high_score = 0
red = (200, 0, 0)
green = (0, 200, 0)
yellow = (200, 200, 0)
bright_yellow = (255, 255, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

# player
class player(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
    def draw(self, win):
        win.blit(cloud_img, (self.x, self.y))

# enemy
class enemy(object):
    def __init__(self, x, y, radius, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), self.radius, 0)

# button
class button(object):
    def __init__(self, msg, x, y, t_width, width, height, color, h_color, action, menu):
        self.msg = msg
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.h_color = h_color
        self.action = action
        self.menu = menu
        self.font_small = pygame.font.SysFont("comicsans", t_width )
        self.text_msg = self.font_small.render(self.msg, 1, (0, 0, 0))

    def draw(self, win):
        # button
        global menu
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global run 
        global click_sound 
        global con_menu  
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(win, self.h_color, ( self.x, self.y, self.width, self.height))
            win.blit(self.text_msg, (self.x + 1, self.y + 3))
            if click[0] == 1:
                click_sound.play()
                if self.action == "play":
                    menu = False
                    run = True
                elif self.action == "quit":
                    click_sound.play()
                    pygame.quit()
                    quit()
                elif self.action == "control":
                    control()
                elif self.action == "back":
                    main_menu()
                    con_menu = False         
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height)) 
            win.blit(self.text_msg, (self.x + 1, self.y + 3))             

cloud = player(225, 400, 90, 90, 10)
ball = enemy(random.randint(0, 450), 0, 25, 8)
def redrawscreen():
    font_score = pygame.font.SysFont("comicsans", 50, True)
    text_score = font_score.render("Score: " + str(score), 1, (0, 0, 0))
    text_high = font_score.render("High score: " + str(high_score), 1, (0, 0, 0))
    win.blit(text_score, (300, 10))
    win.blit(text_high, (0, 10))
    cloud.draw(win)
    ball.draw(win)

# main menu
def main_menu():
    global menu
    global run 
    menu = True
    run = False
    while menu: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
        win.blit(bg, (0, 0))

        # text
        font_menu = pygame.font.SysFont("comicsans", 100)
        text_menu = font_menu.render("Falling Sky", 1, (255, 255, 0))
        win.blit(text_menu, (60, 150))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        elif keys[pygame.K_SPACE]:
            click_sound.play()
            run = True
            menu = False   

        # buttons
        red_button = button("quit", 100, 250, 55, 70, 50,red, bright_red, "quit", menu)
        green_button = button("play", 303, 250, 50, 70, 50,green, bright_green, "play", menu)
        yellow_button = button("control", 175, 320, 50, 123, 50, yellow, bright_yellow, "control", menu)
        yellow_button.draw(win)
        red_button.draw(win)
        green_button.draw(win)
        pygame.display.update()
        clock.tick(15)

# control
def control():
    global main_menu
    global menu
    global con_menu
    con_menu = True
    while con_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
        win.blit(control_img, (0, 0))
        # button
        close_button = button("back", 215, 430, 50, 83, 50, green, bright_green, "back", menu)
        close_button.draw(win)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
             main_menu()
             con_menu = False  
        pygame.display.update()
        clock.tick(15)
main_menu()
# main loop
while run:
    clock.tick(60)
    # movement\events
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run = False 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and cloud.x < 500 - cloud.vel - cloud.width:
        cloud.x += cloud.vel  
    if keys[pygame.K_LEFT] and cloud.x > cloud.vel:
        cloud.x -= cloud.vel
    if keys[pygame.K_ESCAPE]:
        main_menu()    
    # The ball movement
    if ball.y < 600:
        ball.y += ball.vel
    if ball.y >= 600:
        ball.vel += 1
        score += 1
        ball.x = random.randint(30, 450) 
        ball.y = 0 
    if ball.vel == 60:
        ball.vel -= 1
    redrawscreen()     
    # collision
    if cloud.x + cloud.width > ball.x > cloud.x + 2  and cloud.y + cloud.height > ball.y > cloud.y :
        if score > high_score:
            high_score = score 
        hit_sound.play()
        score = 0
        ball.vel = 8
        cloud.x = 225
        ball.y = 0
        ball.x = random.randint(30, 450)
        time.sleep(0.5)
    pygame.display.update() 
    win.blit(bg, (0, 0))       
    

pygame.quit()
quit()