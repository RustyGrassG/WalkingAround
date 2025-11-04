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