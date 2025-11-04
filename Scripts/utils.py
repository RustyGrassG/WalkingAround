#Handles most utility functions like loading saves, or other assets into the game
import pygame
from OpenGL.GL import  *
from OpenGL.GLU import *
import numpy as np

#Turns a regular pygame surface into an OpenGL texture
def alpha_surf_to_gl(surface):
    glBindTexture(GL_TEXTURE_2D, surface)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.width(), surface.height(), GL_RGBA, GL_UNSIGNED_BYTE, None)