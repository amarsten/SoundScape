import pygame
from pygame.locals import *

from lib.v2d import v2d
        
class PaintBrush(object):
    def __init__(self,surface):
        """
        Creates a new PaintBrush object to paint on the specified surface. 
        """
        self.lastPos = None
        self.dest = surface
        self.drawAngle = None
        self.rest = 0.0
        
        self.orgBrush = None
        self.brush = None
        self.brushRect = None

        self.space = 1.0
        self.followAngle = False
        self.imageBrush = False
        
        self.color = None
                        
    def _blit(self,pos):
        if (self.brush is None):
            return
        
        #change the direction/angle of the brush image based on the direction of the brush movement
        if (self.followAngle and self.drawAngle is not None):
            bimg = pygame.transform.rotozoom(self.brush,-self.drawAngle.get_angle(),1.0) 
            brect = bimg.get_rect()
        else:
            bimg = self.brush
            brect = self.brushRect
                    
        brect.center = pos.ipos
        self.dest.blit(bimg,brect.topleft)

    def _blit_line(self,fromPos,toPos):
        """
        Draws a line between two points as a 2d vector
        """
                
        drawVect = toPos-fromPos
        
        if (self.drawAngle is None):
            self.drawAngle = v2d(drawVect)
            self.drawAngle.length = 20.0
        else:
            self.drawAngle+=drawVect
            self.drawAngle.length = 20.0
           
        len = drawVect.length      
        
        if (len < self.rest):
            self.rest-=len
            return
        
        if (self.rest>0.0):
            drawVect.length = self.rest
            curPos = fromPos+drawVect
        else:
            curPos = v2d(fromPos)
        
        len-=self.rest
        self.rest = 0.0
        self._blit(curPos)
        
        drawVect.length = self.space
        while len > self.space:
            curPos += drawVect
            self._blit(curPos)
            len-=self.space
            
        self.rest = self.space-len
        
    def set_brush(self,brush,imageBrush=False):
        """
        Sets the surface to be used as a brush. 
        If imageBrush is True the brush will not be affected by color changes.
        """
        self.orgBrush = brush.copy()
        self.brush = brush.copy()
        self.brushRect = brush.get_rect()
        self.space = 1.0
        self.followAngle = False
                
        self.imageBrush = imageBrush

    def set_follow_angle(self,followAngle):
        """
        If followAngle is True then the brush will rotate along with the
        drawing angle.
        """
        self.followAngle = followAngle
        
    def set_color(self,(r,g,b)):
        """
        Sets the color of all pixels in the brush. Will not affect the per
        pixel alpha values. This will have no effect if the brush is set as an
        image brush.
        """
        color = pygame.Color(r,g,b)
        if (not self.brush or self.imageBrush):
            return
        self.color = color
        #go through each pixel in the brush and set its color
        #to the specified color but with the alpha of the brush
        for x in range(self.brushRect.width):
            for y in range(self.brushRect.height):
                c = self.brush.get_at((x, y))
                color.a = c.a
                self.brush.set_at((x,y),color)
        
    def set_alpha(self,alpha):
        """
        Modify the current per pixel alpha values.
        Alpha value can be 0.0 to 1.0
        """
        if (not self.brush):
            return
        #get the color value of each pixel
        for x in range(self.brushRect.width):
            for y in range(self.brushRect.height):
                c = self.orgBrush.get_at((x, y))
                if (self.color is not None and not self.imageBrush):
                    c.r = self.color.r
                    c.g = self.color.g
                    c.b = self.color.b
                #change the alpha to the nearest int
                c.a = int(round(float(c.a)*alpha))
                self.brush.set_at((x,y),c)        
        
    def paint_line(self,fromPos,toPos):
        """
        Paints a line.
        Ex: paint_line((30,40),(210,113))
        """
        if (not self.brush):
            return
        self.paint_from(fromPos)
        self.paint_to(toPos)    
        
    def paint_from(self,pos):
        """
        Starts to paint at the given position.
        Ex: paint_from((30,40))
        """
        if (not self.brush):
            return        
        self.rest = 0.0
        self.lastPos = v2d(pos)
        if (not self.followAngle):            
            self._blit_line(self.lastPos,v2d(pos))
        else:
            self.drawAngle = None 

    def paint_to(self,pos):
        """
        Paint from the last position to the given one.
        Ex: paint_to((210,113))
        """
        if (not self.brush):
            return        
        if (pos and self.lastPos):
            pos = v2d(pos)
            self._blit_line(self.lastPos,pos)
            self.lastPos = pos
