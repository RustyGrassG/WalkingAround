import sys
import Scripts
import pygame
import math
from random import uniform
import OpenGL.GL as OGL
import OpenGL.GLU as OGLU
import Scripts.drawObject as drawObject, Scripts.entities as entities
from pygame import locals as pylocals



class main():
    def __init__(self):
        #Initializes the pygame instance and sets the window caption
        pygame.init()
        pygame.display.set_caption("Walking Around")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.mouse.set_relative_mode(True)

        #Sets up the clock for in-game time management
        self.clock = pygame.time.Clock()

        #Sets display window size and buffering - Allows OpenGL to render properly to the screen
        self.display = (800,600)
        pygame.display.set_mode(self.display, pylocals.DOUBLEBUF | pylocals.OPENGL)
        
        OGL.glEnable(OGL.GL_DEPTH_TEST)
        OGL.glEnable(OGL.GL_LIGHTING)
        OGL.glShadeModel(OGL.GL_SMOOTH)
        OGL.glEnable(OGL.GL_COLOR_MATERIAL)
        OGL.glColorMaterial(OGL.GL_FRONT_AND_BACK, OGL.GL_AMBIENT_AND_DIFFUSE)

        OGL.glEnable(OGL.GL_LIGHT0)
        OGL.glLightfv(OGL.GL_LIGHT0, OGL.GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        OGL.glLightfv(OGL.GL_LIGHT0, OGL.GL_AMBIENT, [1.0, 1.0, 1.0, 1])

        self.objects = []

        for i in range(400):
            x = uniform(-100.0, 100.0)
            y = uniform(-100.0, 100.0)
            z = uniform(-100.0, 100.0)
            #Set Cube stats here! Only size, position, and color works
            self.objects.append(drawObject.Cube(pos = (x, y, z), color= (x/(x+y+z), y/(x+y+z), z/(x+y+z)), size = .25))
        

        OGL.glMatrixMode(OGL.GL_PROJECTION)
        OGLU.gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 150.0)

        OGL.glMatrixMode(OGL.GL_MODELVIEW)
        OGLU.gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
        self.viewMatrix = OGL.glGetFloatv(OGL.GL_MODELVIEW_MATRIX)
        OGL.glLoadIdentity()

        #The center of the display window overlay
        self.displayCenter = [self.display[0] // 2, self.display[1] // 2]
        pygame.mouse.set_pos(self.displayCenter)

        #The up down angle used for camera rotation. Needs to be clamped still
        self.up_down_angle = 0.0

        #Set up player object
        self.player = entities.Player()
        

    def run(self):
        while True:
            #Delta time... dont think this is how it works IRL, will probably have to use FPS to make it work
            dt = self.clock.tick(60) / 1000
            print(self.clock.get_fps())
            for event in pygame.event.get():
                if event.type == pylocals.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            
            key_presses = pygame.key.get_pressed()
            dx, dy = pygame.mouse.get_rel()
            
            OGL.glLoadIdentity()

            #if dx or dy:
                #sensitivity = self.player.stats["mouse_sensitivity"]
                #dx *= sensitivity * dt
                #dy *= sensitivity * dt
                
                

            OGL.glLoadIdentity()
            self.player.update_camera(dx, dy, self.displayCenter, dt)

            OGL.glPushMatrix()
            OGL.glLoadIdentity()

            self.player.update_pos(key_presses, dt)

            OGL.glMultMatrixf(self.viewMatrix)
            self.viewMatrix = OGL.glGetFloatv(OGL.GL_MODELVIEW_MATRIX)

            OGL.glPopMatrix()
            OGL.glMultMatrixf(self.viewMatrix)

            OGL.glLightfv(OGL.GL_LIGHT0, OGL.GL_POSITION, [1,-1,1,0])
            
            #refreshes the screen each tick
            OGL.glClear(OGL.GL_COLOR_BUFFER_BIT | OGL.GL_DEPTH_BUFFER_BIT)
            OGL.glBegin(OGL.GL_QUADS)
            for game_object in self.objects:
                game_object.draw(self.player.pos)
            OGL.glEnd()
            pygame.display.flip()
            




if __name__ == "__main__":
    new_instance = main()
    new_instance.run()
