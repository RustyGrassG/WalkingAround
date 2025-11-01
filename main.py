import drawObject
import pygame
from pygame import locals as pylocals
import OpenGL.GL as OGL
import OpenGL.GLU as OGLU
import math

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

        cube_1 = drawObject.Cube(pos=(3, 10, -5), color=(.5,.3,.5))
        cube_2 = drawObject.Cube(pos=(0, -2, -5), color=(.1,.7,.0))
        cube_3 = drawObject.Cube(pos=(3, 4, -5), color=(.2,.3,.5))
        cube_4 = drawObject.Cube(pos=(-10.0, 0, -5.0), color=(.3,.2,.3))
        self.objects = [
            cube_1,
            cube_2,
            cube_3,
            cube_4
        ]

        OGL.glMatrixMode(OGL.GL_PROJECTION)
        OGLU.gluPerspective(45, (self.display[0]/self.display[1]), 0.1, 50.0)

        OGL.glMatrixMode(OGL.GL_MODELVIEW)
        OGLU.gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
        self.viewMatrix = OGL.glGetFloatv(OGL.GL_MODELVIEW_MATRIX)
        OGL.glLoadIdentity()

        self.displayCenter = [self.display[0] // 2, self.display[1] // 2]
        self.mouseMove = [0,0]
        pygame.mouse.set_pos(self.displayCenter)

        self.up_down_angle = 0.0

        self.player_pos = [0.0, 0.0, 0.0]
        self.player_stats = {
            "walk_speed" : 10.0,
            "camera_sensitivity" : 2.0
        }
        

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
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

            if dx or dy:
                dx *= self.player_stats["camera_sensitivity"] * dt
                dy *= self.player_stats["camera_sensitivity"] * dt
                pygame.mouse.set_pos(self.displayCenter)

            OGL.glLoadIdentity()

            self.up_down_angle += dy
            OGL.glRotatef(self.up_down_angle, 1.0, 0.0, 0.0)

            OGL.glPushMatrix()
            OGL.glLoadIdentity()

            if key_presses[pygame.K_a]:
                self.player_pos[0] += self.player_stats["walk_speed"] * dt
            if key_presses[pygame.K_d]:
                self.player_pos[0] -= self.player_stats["walk_speed"] * dt
            if key_presses[pygame.K_w]:
                self.player_pos[1] -= self.player_stats["walk_speed"] * dt
            if key_presses[pygame.K_s]:
                self.player_pos[1] += self.player_stats["walk_speed"] * dt

            OGL.glRotatef(dx, 0.0, 1.0, 0.0)

            OGL.glMultMatrixf(self.viewMatrix)
            self.viewMatrix = OGL.glGetFloatv(OGL.GL_MODELVIEW_MATRIX)

            OGL.glPopMatrix()
            OGL.glMultMatrixf(self.viewMatrix)

            OGL.glLightfv(OGL.GL_LIGHT0, OGL.GL_POSITION, [1,-1,1,0])
            
            #refreshes the screen each tick
            OGL.glClear(OGL.GL_COLOR_BUFFER_BIT | OGL.GL_DEPTH_BUFFER_BIT)
            for game_object in self.objects:
                game_object.draw(self.player_pos)
            pygame.display.flip()
            




if __name__ == "__main__":
    new_instance = main()
    new_instance.run()
