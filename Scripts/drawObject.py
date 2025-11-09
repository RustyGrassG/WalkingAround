from OpenGL.GL import *
import numpy as np
from OpenGL.arrays import vbo


def create_cube_vbo(size=1.0):
    s = size
    vertices = np.array([
        # Front
        [ s,  s, -s], [-s,  s, -s], [-s, -s, -s], [ s, -s, -s],
        # Back
        [ s,  s,  s], [ s, -s,  s], [-s, -s,  s], [-s,  s,  s],
        # Top
        [ s,  s,  s], [-s,  s,  s], [-s,  s, -s], [ s,  s, -s],
        # Bottom
        [ s, -s,  s], [ s, -s, -s], [-s, -s, -s], [-s, -s,  s],
        # Left
        [-s,  s,  s], [-s, -s,  s], [-s, -s, -s], [-s,  s, -s],
        # Right
        [ s,  s,  s], [ s,  s, -s], [ s, -s, -s], [ s, -s,  s],
    ], dtype=np.float32)
    return vbo.VBO(vertices), len(vertices)


class GameObject():
    def __init__(self, size: float, pos: tuple = (0,0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        self.size = size
        self.pos = np.array(pos, dtype=np.float32)
        self.color = color
        self.collisions = collisions
        self.debug = True
        self.show_edges = show_edges

class Cube(GameObject):
    shared_vbo = None
    vertex_count = 0

    def __init__(self, size: float = 1.0, pos: tuple = (0,0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        super().__init__(size, pos, color, collisions)
        if Cube.shared_vbo is None:
            Cube.shared_vbo, Cube.vertex_count = create_cube_vbo(size)
        
    
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glColor3fv(self.color)
        glDrawArrays(GL_QUADS, 0, Cube.vertex_count)
        glPopMatrix()
        

class Sphere(GameObject):
    def __init__(self, size: float = 1.0, pos: tuple = (0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        super().__init__(size, pos, color, collisions)

#Updates each OpenGl object each tick
#Draws the object to the screen
def update(object):
    pass