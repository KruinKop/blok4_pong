import pygame
from pygame.locals import *
from collections import *
import random

pygame.init()
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720, 480))

done = False
white = (255, 255, 255)
purple = (154, 9, 237)
red = (255,0,0)
bg = (127, 127, 127)

font = pygame.font.SysFont("Arial", 36)
txtsurf = font.render("Hello, World", True, white)
txt_width = txtsurf.get_width()
window_surface = pygame.display.get_surface()
window_width, window_height = window_surface.get_size()

time = 5
## for setting the start coordinate in the middle use : window_width // 2 - txt_width // 2

## we kunnen ook named tuples gebruiken om data te gaan groeperen
Point = namedtuple('Point', ['x','y']) ## deze kunnen we dan vereder implementeren binnen de klassen
Rectangle = namedtuple('Rectangle', ['width', 'height'])
vector = namedtuple('vector', ['x', 'y'])

class Ball:
    height = 10
    width = 10
    sprite = "afbeelding_url_hier"
    max_speed = 20

    def __init__(self) -> None:
        self.x_pos = window_width // 2 - self.width // 2
        self.y_pos = window_height // 2 - self.height // 2
        self.dir_x = random.choice([-1,1])
        self.dir_y = random.choice([-1,1])
        self.speed = (window_width - self.width) // (time * FPS)

    def update_pos(self):
        self.x_pos = self.x_pos + (self.dir_x * self.speed)
        self.y_pos = self.y_pos + (self.dir_y * self.speed)

    def draw_rect(self):
        rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        return pygame.draw.rect(screen, red, rect)
    
    def detect_collision(self):
        if self.x_pos <= 0 or self.x_pos + self.width >= window_width:
            # self.dir_x *= -1  Change direction when reaching the window boundaries
            return True
        if self.y_pos <= 0 or self.y_pos + self.height >= window_height:
            self.dir_y *= -1
        return False
    
    def get_rect(self):
        return pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

class Paddle:
    max_speed = 10
    width = 15
    height = 60
    sprite = "afbeelding_url_hier"

    def __init__(self,x_pos) -> None:
        if x_pos == "left":
            self.x_pos = 30
        else:
            self.x_pos = window_width - self.width - 30
        self.y_pos = window_height // 2 - self.height // 2
        self.dir_y = 0
        self.speed = 7
        self.paddle = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

    def draw_paddle(self):
        self.paddle = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        return pygame.draw.rect(screen, purple, self.paddle)
    
    def update_pos_y(self):
        self.y_pos = self.y_pos + (self.dir_y*self.speed)

    def detect_collision(self, ball):
        ball_rect = ball.get_rect()
        collision_rect = self.paddle.clip(ball_rect)

        if collision_rect.width > 0 and collision_rect.height > 0:
            # Determine the side of collision
            if collision_rect.width < collision_rect.height:
                # Vertical collision (left or right side)
                print("vertical collision detected")
                ball.dir_x *= -1 
            else:
                # Horizontal collision (top or bottom side)
                print("horizontal collision detected")
                ball.dir_y *= -1


speelVierkant = Ball()
player1 = Paddle("left")
player2 = Paddle("right")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == KEYDOWN:
            if event.key == K_q:
                done = True
            if event.key == K_KP7:
                player1.dir_y = -1
            if event.key == K_KP1:
                player1.dir_y = 1
            if event.key == K_KP9:
                player2.dir_y = -1
            if event.key == K_KP3:
                player2.dir_y = 1    

        if event.type == KEYUP:
            if event.key in [K_KP1, K_KP7, K_KP9, K_KP3]:
                player1.dir_y = 0
                player2.dir_y = 0

            
    # Clearing the screen once per frame
    screen.fill(bg)  

    # Updating the current state
    done = speelVierkant.detect_collision()
    speelVierkant.update_pos()

    player1.update_pos_y()
    player1.detect_collision(speelVierkant)
    player2.update_pos_y()
    player2.detect_collision(speelVierkant)

    # Drawing the elements
    speelVierkant.draw_rect()
    player1.draw_paddle()
    player2.draw_paddle()

    # Updating the changes
    pygame.display.flip()
    clock.tick(FPS)

    #debugging statements
pygame.quit()
