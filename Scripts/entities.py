#A script that holds all of the entities in the main project. 
#This script will cover entity movement, and collisions, ai logic, and more

#This script will also be the main script used for the main player entitiy
#that includes player movement, camera movement, and any other sort of even for the main player
import pygame
import math
import OpenGL.GL as OGL
import OpenGL.GLU as OGLU

class Player():
    def __init__(self, pos : list = [0.0, 0.0, 0.0]):
        self.pos = pos
        self.stats = {
            "walk_speed" : 10.0,
            "mouse_sensitivity": 8.0
        }
        self.up_down_angle = 0.0
        self.left_right_angle = 0.0
        self.viewMatrix = OGL.glGetFloatv(OGL.GL_MODELVIEW_MATRIX)
    
    def update_camera(self, dx, dy, center, dt):
        sensitivity = self.stats["mouse_sensitivity"]
        dx *= sensitivity * dt
        dy *= sensitivity * dt
        self.up_down_angle += dy
        self.up_down_angle = max(-89, min(89, self.up_down_angle))
        self.left_right_angle += dx
        OGL.glRotatef(self.up_down_angle, 1.0, 0.0, 0.0)
        OGL.glRotatef(self.left_right_angle, 0.0, 1.0, 0.0)
    
    def update_pos(self, keys, dt):
        speed = self.stats["walk_speed"]
        if keys[pygame.K_a]:
            self.pos[0] += speed * dt
        if keys[pygame.K_d]:
            self.pos[0] -= speed * dt
        if keys[pygame.K_w]:
            self.pos[1] -= speed * dt
        if keys[pygame.K_s]:
            self.pos[1] += speed * dt