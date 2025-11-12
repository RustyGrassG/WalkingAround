#Handles most utility functions like loading saves, or other assets into the game
import pygame
from OpenGL.GL import  *
from OpenGL.GLU import *
import numpy as np

#Turns a regular pygame surface into an OpenGL texture
def alpha_surf_to_gl(surface: pygame.surface, texID):
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.width, surface.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)

#Refreshes an alpha surface
def alpha_refresh_surf(surfaces):
    for surf in surfaces:
        surf.fill((0,0,0,0))

def surf_to_texture( surface, texID):
        width, height = surface.get_size()
        surface_array = pygame.surfarray.pixels3d(surface)
        surface_array = np.flipud(surface_array)
        #rgb_surface = surface_array.swapaxes(0, 1).astype(np.uint8).tobytes()
        flipped_surf = pygame.transform.flip(surface, False, True)
        texture_data = pygame.image.tobytes(flipped_surf, "RGBA", True)

        glBindTexture(GL_TEXTURE_2D, texID)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)


def check_collisions(col_a, col_b, padding = 1.0):
      #print("Col_a:" + str(col_a) + " - Col_b: " + str(col_b))

      x_overlap = (col_a[0] - padding < col_b[3] + padding) and (col_a[3] + padding > col_b[0] - padding)
      y_overlap = (col_a[1] - padding < col_b[4] + padding) and (col_a[4] + padding > col_b[1] - padding)
      z_overlap = (col_a[2] - padding < col_b[5] + padding) and (col_a[5] + padding > col_b[2] - padding)

      if not x_overlap:
            return False
      if not y_overlap:
            return False
      if not z_overlap:
            return False

      return True

def draw_ui_overlay(size, texID):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, size[0], size[1], 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texID)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Draw a rectangle in screen space
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(size[0], 0)
        glTexCoord2f(1, 1); glVertex2f(size[0], size[1])
        glTexCoord2f(0, 1); glVertex2f(0, size[1])
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