import sys
import Scripts
import pygame
import math
from random import uniform
from OpenGL.GL import  *
from OpenGL.GLU import *
import Scripts.drawObject as drawObject, Scripts.entities as entities, Scripts.utils as utils
from pygame import locals as pylocals
import numpy as np



class main():
    def __init__(self):
        self.debug = True
        #Initializes the pygame instance and sets the window caption
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Walking Around")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.mouse.set_relative_mode(True)

        #Sets up the clock for in-game time management
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.cube_count_text = self.font.render("Cubes: " , False, (255, 255, 255))
        self.fps_count_text = self.font.render("FPS: " , False, (255, 255, 255))
        self.space_to_summon_cube = self.font.render("PRESS SPACE TO SUMMON CUBE",  False, (255,255,255))

        #Sets display window size and buffering - Allows OpenGL to render properly to the screen
        self.display = (800,600)
        self.screen = pygame.display.set_mode(self.display, pylocals.DOUBLEBUF | pylocals.OPENGL)

        #The UI layer overlay for the screen
        self.ui_layer = pygame.Surface(self.display, pygame.SRCALPHA)
        self.ui_layer.fill((0,0,0, 0))
        self.ui_layer.blit(self.cube_count_text, (10,10))
        self.ui_texture = glGenTextures(1)
        utils.alpha_surf_to_gl(self.ui_layer, self.ui_texture)
    
        self.avg_fps = 0
        
        #Set up player object
        self.player = entities.Player()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [1.0, 1.0, 1.0, 1])

        #Holds all the objects in the world
        self.objects = []

        for i in range(1,5):
            x = uniform(-100.0, 100.0)
            y = uniform(-100.0, 100.0)
            z = uniform(-100.0, 100.0)
            pos_i = (math.pi * 2) / 4 * i
            x_pos = math.cos(pos_i)
            y_pos = math.sin(pos_i)
            #Set Cube stats here! Only size, position, and color works
            #self.objects.append(drawObject.Cube(pos = (x, y, z), color= (x/(x+y+z), y/(x+y+z), z/(x+y+z)), size = uniform(0.25, 2.5)))
            self.objects.append(drawObject.Cube(pos = (x_pos * 10, y_pos * 10, 0), color= (x/(x+y+z), y/(x+y+z), z/(x+y+z)), size = uniform(0.75, 1.0)))
        

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 280.0)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, .01, 0, 0, 0, 0, 0, 0, .01)
        glTranslatef(0, 0, self.player.stats["height"])
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        
        glLoadIdentity()
        #The center of the display window overlay
        self.displayCenter = [self.display[0] // 2, self.display[1] // 2]
        pygame.mouse.set_pos(self.displayCenter)

        #The up down angle used for camera rotation. Needs to be clamped still
        self.up_down_angle = 0.0

        
        
        self.a_surf_refresh_list = []
        self.update_UI()

    #Testing Function will probably get deleted
    def update_UI(self):
        self.ui_layer.fill((0,0,0,0))

        #Adds the current cube count to the screen UI
        self.cube_count_text = self.font.render("Cubes: " + str(len(self.objects)), True, (255, 255, 255))
        self.ui_layer.blit(self.cube_count_text, (10,10))

        #Adds the current FPS to the screen UI
        self.fps_count_text = self.font.render(f"FPS: {round(self.avg_fps)}" , False, (255, 255, 255))
        self.ui_layer.blit(self.fps_count_text, (10, 50))
        
        self.space_to_summon_cube = self.font.render("PRESS SPACE TO SUMMON CUBE",  False, (255,255,255))
        self.ui_layer.blit(self.space_to_summon_cube, (50, self.displayCenter[1] * 2 - 50))
        utils.surf_to_texture(self.ui_layer, self.ui_texture)
        
    

    

    def run(self):
        fps_tick = 0
        avg_fps = 0
        while True:
            #Used to refresh surfaces other than OGL surfaces
            #utils.alpha_refresh_surf(self.a_surf_refresh_list)

            #Delta time... dont think this is how it works IRL, will probably have to use FPS to make it work
            dt = self.clock.tick(60) / 1000
            if self.debug:
                avg_fps += self.clock.get_fps()
                fps_tick += 1
                collective_avg_fps = avg_fps / fps_tick
                if fps_tick >= 60:
                    avg_fps = collective_avg_fps
                    self.avg_fps = collective_avg_fps
                    fps_tick = 1
                    self.update_UI()
                    
                
            for event in pygame.event.get():
                if event.type == pylocals.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                        

            key_presses = pygame.key.get_pressed()
            #Debug will be removed
            if key_presses[pygame.K_SPACE]:
                x = uniform(-100.0, 100.0)
                y = uniform(-100.0, 100.0)
                z = uniform(-100.0, 100.0)
                #Set Cube stats here! Only size, position, and color works
                self.objects.append(drawObject.Cube(pos = (x, y, z), color= (x/(x+y+z), y/(x+y+z), z/(x+y+z)), size = uniform(0.25, 2.5)))
                self.update_UI()
            dx, dy = pygame.mouse.get_rel()
            
            glLoadIdentity()

            #if dx or dy:
                #sensitivity = self.player.stats["mouse_sensitivity"]
                #dx *= sensitivity * dt
                #dy *= sensitivity * dt
                
                

            glLoadIdentity()
            self.player.update_camera(dx, dy, self.displayCenter, dt)

            glPushMatrix()
            glLoadIdentity()
            

            self.player.update_pos(key_presses, dt)

            glMultMatrixf(self.viewMatrix)
            self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            glPopMatrix()
            glMultMatrixf(self.viewMatrix)

            glLightfv(GL_LIGHT0, GL_POSITION, [1,-1,1,0])
            
            
            #refreshes the screen each tick
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            for game_object in self.objects:
                game_object.draw()
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 1)
            #pygame.display.get_surface().blit(self.text, self.displayCenter)
            #self.screen.blit(self.text, self.displayCenter)
            utils.draw_ui_overlay(self.display, self.ui_texture)
            pygame.display.flip()
            




if __name__ == "__main__":
    new_instance = main()
    new_instance.run()
