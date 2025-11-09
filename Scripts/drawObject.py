from OpenGL.GL import *
import numpy as np
from OpenGL.arrays import vbo

class GameObject():
    def __init__(self, size: float, pos: tuple = (0,0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        self.size = size
        self.pos = pos
        self.color = color
        self.collisions = collisions
        self.debug = True
        self.show_edges = show_edges

class Cube(GameObject):
    def __init__(self, size: float = 1.0, pos: tuple = (0,0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        super().__init__(size, pos, color, collisions)
        s = self.size

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

        self.vertex_count = len(vertices)
        self.vbo = vbo.VBO(vertices)
    
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glColor3fv(self.color)

        self.vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vbo)

        glDrawArrays(GL_QUADS, 0, self.vertex_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        self.vbo.unbind()
        glPopMatrix()
        

class Sphere(GameObject):
    def __init__(self, size: float = 1.0, pos: tuple = (0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        super().__init__(size, pos, color, collisions)

#Updates each OpenGl object each tick
#Draws the object to the screen
def update(object):
    pass