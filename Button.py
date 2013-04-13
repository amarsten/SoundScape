import pygame
import sys, os
from pygame.sprite import Sprite
from pygame.rect import Rect
               
class Button(Sprite):
    def __init__(self, buttonImage, (x, y)):
        '''
        Returns a button object
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(buttonImage).convert_alpha()
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = (x, y)

    def button_pressed(self, mouse, x, y):
        '''
        Returns true if the button has been pressed
        '''
        #create a rect with the size of the button,
        #but offset by x and y if the button is in a surface other
        #than the main screen
        pressed = False
        left = x + self.rect.left
        top = y + self.rect.top
        width = self.rect.width
        height = self.rect.height
        self.buttonRect = Rect(left, top, width, height)
        #check if the mouse is over that rect
        if (self.buttonRect.collidepoint(mouse) == True):
            pressed = True
        return pressed
    
    def draw(self, surface):
        '''
        Draws button to the specified surface
        '''
        surface.blit(self.image, self.rect.topleft)