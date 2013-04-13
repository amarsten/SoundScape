import pygame
import sys, os
from pygame.sprite import Sprite
from pygame.rect import Rect
from DataPanel import DataPanel, DataVariable

class ControlPanel(object):
    def __init__(self, appScreen, left, top, width, height):
        self.controlPanelSurface = appScreen.subsurface(pygame.Rect((left, top),
                                                             (width, height)))
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.herbivoreButton = Button('Herbivore_Button.png', (0, 0))
        hbWidth = self.herbivoreButton.rect.width
        hbHeight = self.herbivoreButton.rect.height
        self.predatorButton = Button('Predator_Button.png', (hbWidth, 0))
        self.omnivoreButton = Button('Omnivore_Button.png', (hbWidth * 2, 0))
        self.resetButton = Button('Reset_Button.png', (hbWidth * 5, 0))
        self.quitButton = Button('Quit_Button.png', (hbWidth * 6, 0))
        self.rect = Rect(left, top, width, height)
        
    def draw(self):
        self.herbivoreButton.draw(self.controlPanelSurface)
        self.predatorButton.draw(self.controlPanelSurface)
        self.omnivoreButton.draw(self.controlPanelSurface)
        self.resetButton.draw(self.controlPanelSurface)
        self.quitButton.draw(self.controlPanelSurface)
               
class Button(Sprite):
    def __init__(self, buttonImage, (top, left)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(buttonImage).convert_alpha()
        self.rect = self.image.get_bounding_rect()
        self.rect.topleft = (top, left)
        colorkey = self.image.get_at((0,0))
        self.image.set_colorkey(colorkey)

    def buttonPressed(self, mouse, x, y):
        left = x + self.rect.left
        top = y + self.rect.top
        width = self.rect.width
        height = self.rect.height
        self.newRect = Rect(left, top, width, height)
        if (self.newRect.collidepoint(mouse) == True):
            return True
        else:
            return False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)