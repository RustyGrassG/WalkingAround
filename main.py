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

        #Sets up the clock for in-game time management
        self.clock = pygame.time.Clock()

        #Sets display window size and buffering - Allows OpenGL to render properly to the screen
        self.display = (800,600)
        pygame.display.set_mode(self.display, pylocals.DOUBLEBUF | pylocals.OPENGL)
        
        pygame.event.set_grab(True)

        #Sets the screen background (skybox) color, and sets the perspective and position of the camera
        OGL.glClearColor(0.1, 0.1, 0.1, 1)
        OGLU.gluPerspective(90, (self.display[0] / self.display[1]), 0.1, 150.0)
        OGL.glTranslatef(0.0, 0.0, 0.0)

        #Sets up the player stats like speed, jump height, and more!
        self.player_stats = {
            "walk_speed" : 10.0,
            "camera_sensitivity" : 0.01
        }

        #Sets up the player position(x,y,z)
        self.player_height : float = -2.0
        self.player_pos = [0.0,self.player_height,0.0]
        #Use only X and Z to rotate the player
        self.player_yaw = 0.0
        self.player_pitch = 0.0
        self.max_pitch = 89.0
        #self.update_camera(0,0)

        #Stores every object to maintain persistance!
        self.objects = []
        new_cube = drawObject.Cube(color=(1,.5,.5), pos=(0,0,-20))
        self.objects.append(new_cube)
        new_cube2 = drawObject.Cube(color=(.3,.5,.2), pos=(4,0,-15))
        self.objects.append(new_cube2)
        #new_sphere = drawObject.Sphere()
        #self.objects.append(new_sphere)
    
    #intakes the mouse movement per tick and adds it to camera pitch/yaw
    #Takes the current pitch/yaw and adds it to the camera rotation
    #Currently not working... I want this to not use the glu lookat function cause it interferes with my player movement i think
    def update_camera(self, amount_x, amount_y):
        player_pos = self.player_pos.copy()
        print(str(amount_x)+ "," + str(amount_y))
        self.player_yaw += math.radians(amount_x)
        self.player_pitch += math.radians(amount_y)
        self.player_pitch = max(-self.max_pitch, min(self.max_pitch, self.player_pitch))
        forward_x = math.cos(self.player_yaw) * math.cos(self.player_pitch)
        forward_y = math.sin(self.player_pitch)
        forward_z = -math.sin(self.player_yaw) * math.cos(self.player_pitch)
        forward_vector = [forward_x, forward_y, forward_z]
        target = [
            player_pos[0] + forward_vector[0],
            player_pos[1] + forward_vector[1],
            player_pos[2] + forward_vector[2]
        ]
        OGLU.gluLookAt(player_pos[0], player_pos[1], player_pos[2],
                        target[0], target[1], target[2],
                        0,1,0)
        

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
            
            pygame.mouse.set_pos(self.display[0] // 2, self.display[1] // 2)
            dx, dy = pygame.mouse.get_rel()
            dx *= self.player_stats["camera_sensitivity"] * dt
            dy *= self.player_stats["camera_sensitivity"] * dt
            if dx or dy:
                self.update_camera(dx, dy)
            
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player_pos[0] += self.player_stats["walk_speed"] * dt
            if keys[pygame.K_d]:
                self.player_pos[0] -= self.player_stats["walk_speed"] * dt
            if keys[pygame.K_w]:
                self.player_pos[2] += self.player_stats["walk_speed"] * dt
            if keys[pygame.K_s]:
                self.player_pos[2] -= self.player_stats["walk_speed"] * dt
            
            #refreshes the screen each tick
            OGL.glClear(OGL.GL_COLOR_BUFFER_BIT | OGL.GL_DEPTH_BUFFER_BIT)
            for game_object in self.objects:
                game_object.draw(self.player_pos)
            pygame.display.flip()
            




if __name__ == "__main__":
    new_instance = main()
    new_instance.run()
