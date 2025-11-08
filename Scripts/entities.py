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
        self.stats = {
            "walk_speed" : 10.0,
            "height" : -1.8,
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
        #Takes the horizontal(yaw) camera angle, in degrees, and converts it to radians
        rot_radians = math.radians(self.left_right_angle)

        #Gets the forward and right vector movements
        forward = [-math.sin(rot_radians), math.cos(rot_radians)]
        right = [math.cos(rot_radians), math.sin(rot_radians)]

        #gets the player walk speed from dic
        speed = self.stats["walk_speed"]
        move_dir = [0, 0]
        if keys[pygame.K_w]:
            move_dir[0] += forward[0]
            move_dir[1] += forward[1]
        if keys[pygame.K_s]:
            move_dir[0] -= forward[0]
            move_dir[1] -= forward[1]
        if keys[pygame.K_d]:
            move_dir[0] -= right[0]
            move_dir[1] -= right[1]
        if keys[pygame.K_a]:
            move_dir[0] += right[0]
            move_dir[1] += right[1]
        
        #Normalizes the walk speed (makes a 0-1 value)
        move_norm = math.hypot(move_dir[0], move_dir[1])
        if move_norm:
            move_dir[0] /= move_norm
            move_dir[1] /= move_norm

        OGL.glTranslatef(move_dir[0] * speed * dt,0, move_dir[1] * speed * dt)