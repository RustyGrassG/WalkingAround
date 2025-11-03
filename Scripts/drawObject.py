import OpenGL.GL as GL
import OpenGL.GLU as GLU

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
        
        self.vertices = (
            (size, -size, -size),
            (size, size, -size),
            (-size, size, -size),
            (-size, -size, -size),
            (size, -size, size),
            (size, size, size),
            (-size, -size, size),
            (-size, size, size)
        )
        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )
        self.surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
        )
    
    def draw(self, player_pos: tuple):
        #Quads
        #GL.glBegin(GL.GL_QUADS)
        for surface in self.surfaces:
            x = 0
            for vertex in surface:
                x += 1
                updated_vert_pos = (self.vertices[vertex][0] + self.pos[0] + player_pos[0], self.vertices[vertex][1] + self.pos[1]  + player_pos[1], self.vertices[vertex][2] + self.pos[2]  + player_pos[2])
                GL.glColor3fv(self.color)
                GL.glVertex3fv(updated_vert_pos)
                #print(updated_vert_pos)
        #GL.glEnd()
        #Lines
        if self.show_edges:
            print("debug")
            GL.glBegin(GL.GL_LINES)
            for edge in self.edges:
                x = 0
                for vertice in edge:
                    updated_vert_pos = (vertice + player_pos[x], vertice + player_pos[x], vertice + player_pos[x])
                    GL.glVertex3fv(updated_vert_pos)
                    x += 1
            GL.glEnd()
        

class Sphere(GameObject):
    def __init__(self, size: float = 1.0, pos: tuple = (0,0), color: tuple = (1,1,1), collisions: bool = False, show_edges = False):
        super().__init__(size, pos, color, collisions)

#Updates each OpenGl object each tick
#Draws the object to the screen
def update(object):
    pass