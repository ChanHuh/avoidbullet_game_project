import random
import pygame
import colorsys

class Bullet:
    def __init__(self, x, y, radius, damage, to_x, to_y):
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = radius
        self.damage = damage
        self.color = [190,0,0] # red
        self.color_hsv = [random.random(),1,1]
        

    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.color_hsv[0] = (self.color_hsv[0] + 0.0001*dt) % 1
        self.color = tuple(map(lambda x: int(255*x), colorsys.hsv_to_rgb(*self.color_hsv)))
        self.pos[0] = (self.pos[0] + dt*self.to[0]) % width
        self.pos[1] = (self.pos[1] + dt*self.to[1]) % height
        pos_int = (int(self.pos[0]), int(self.pos[1]))
        pygame.draw.circle(screen, self.color, pos_int, self.radius)
    