#!/usr/bin/env python
import pygame
from pygame.locals import *

class Scanner(pygame.sprite.Sprite):
    
    def __init__(self, surface):
        '''
        Returns a new scanner with the height of the specified surface
        '''
        super(Scanner, self).__init__()
        self.rect = pygame.Rect(0, 0, 1, surface.get_rect().height)
        image = pygame.Surface((1, surface.get_rect().height))
        image.fill((0,255,0))
        self.image = image
        
    def update(self):
        '''
        Updates the scanner by moving it to the left
        '''
        self.rect.left += 1 
        

