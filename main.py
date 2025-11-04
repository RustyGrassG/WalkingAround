import sys
import Scripts
import pygame
import math
from random import uniform
from OpenGL.GL import  *
from OpenGL.GLU import *
import Scripts.drawObject as drawObject, Scripts.entities as entities
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
        self.font = pygame.font.Font(pygame.font.get_default_font(), 50)
        self.text = "None"
        self.text = self.font.render("Cubes: " , False, (255, 255, 255))

        #Sets display window size and buffering - Allows OpenGL to render properly to the screen
        self.display = (800,600)
        self.screen = pygame.display.set_mode(self.display, pylocals.DOUBLEBUF | pylocals.OPENGL)
        self.ui_layer = pygame.Surface(self.display, pygame.SRCALPHA)
        self.ui_layer.fill((0,0,0, 0))
        self.ui_layer.blit(self.text, (10,10))
        self.ui_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.ui_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.display[0], self.display[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        

        #Setting the pygame font for writting things on screen
        #print(pygame.font.get_fonts())
        
        
        
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [1.0, 1.0, 1.0, 1])

        self.objects = []

        if self.debug:
            self.avg_fps = 0
            self.fps_tick = 0

        for i in range(0):
            x = uniform(-100.0, 100.0)
            y = uniform(-100.0, 100.0)
            z = uniform(-100.0, 100.0)
            #Set Cube stats here! Only size, position, and color works
            self.objects.append(drawObject.Cube(pos = (x, y, z), color= (x/(x+y+z), y/(x+y+z), z/(x+y+z)), size = uniform(0.25, 2.5)))
        self.update_cube_count()

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 150.0)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()

        #The center of the display window overlay
        self.displayCenter = [self.display[0] // 2, self.display[1] // 2]
        pygame.mouse.set_pos(self.displayCenter)

        #The up down angle used for camera rotation. Needs to be clamped still
        self.up_down_angle = 0.0

        #Set up player object
        self.player = entities.Player()
        

    def update_cube_count(self):
        self.ui_layer.fill((0,0,0,0))
        self.text = self.font.render("Cubes: " + str(len(self.objects)), True, (255, 255, 255))
        self.ui_layer.blit(self.text, (10,10))
        #self.text_data = pygame.image.tobytes(self.text, "RGBA", True)
        
    def surf_to_texture(self, surface, texID):
        width, height = surface.get_size()
        surface_array = pygame.surfarray.pixels3d(surface)
        surface_array = np.flipud(surface_array)
        rgb_surface = surface_array.swapaxes(0, 1).astype(np.uint8).tobytes()
        flipped_surf = pygame.transform.flip(surface, False, True)
        texture_data = pygame.image.tobytes(flipped_surf, "RGBA", True)

        glBindTexture(GL_TEXTURE_2D, texID)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glBindTexture(GL_TEXTURE_2D, 0)

    def draw_ui_overlay(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.display[0], self.display[1], 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.ui_texture)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Draw a rectangle in screen space
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(self.display[0], 0)
        glTexCoord2f(1, 1); glVertex2f(self.display[0], self.display[1])
        glTexCoord2f(0, 1); glVertex2f(0, self.display[1])
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # restore projection + modelview
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def run(self):
        while True:
            #Delta time... dont think this is how it works IRL, will probably have to use FPS to make it work
            dt = self.clock.tick(60) / 1000
            if self.debug:
                self.avg_fps += self.clock.get_fps()
                self.fps_tick += 1
                avg_fps = self.avg_fps / self.fps_tick
                print("Average FPS: " + str(avg_fps))
                if self.fps_tick >= 60:
                    self.avg_fps = avg_fps
                    self.fps_tick = 1
                    
                
            for event in pygame.event.get():
                if event.type == pylocals.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == pygame.K_SPACE:
                        x = uniform(-100.0, 100.0)
                        y = uniform(-100.0, 100.0)
                        z = uniform(-100.0, 100.0)
                        #Set Cube stats here! Only size, position, and color works
                        self.objects.append(drawObject.Cube(pos = (x, y, z), color= (x/(x+y+z), y/(x+y+z), z/(x+y+z)), size = uniform(0.25, 2.5)))
                        self.update_cube_count()

            key_presses = pygame.key.get_pressed()
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
            self.surf_to_texture(self.ui_layer, self.ui_texture)
            glBegin(GL_QUADS)
            for game_object in self.objects:
                game_object.draw(self.player.pos)
            glEnd()
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 1)
            #pygame.display.get_surface().blit(self.text, self.displayCenter)
            #self.screen.blit(self.text, self.displayCenter)
            self.draw_ui_overlay()
            pygame.display.flip()
            




if __name__ == "__main__":
    new_instance = main()
    new_instance.run()
