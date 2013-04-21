#!/usr/bin/env python
import pygame
from pygame.locals import *
from Button import Button
from Scanner import Scanner
import time

from PaintBrush import PaintBrush
                       
class App(object):
    
    def __init__(self):
        '''
        Returns an app object
        '''
        pygame.display.set_caption("SoundScape")
        self.screen = pygame.display.set_mode((800, 600),1)
        self.paintScreen = self.screen.subsurface(pygame.Rect(100, 0, 600, 500))
        self.paletteScreen = self.screen.subsurface(pygame.Rect(0, 0, 100, 300))
        self.screen.fill((183,183,183))
        self.paintScreen.fill((255,255,255))
        self.paletteScreen.blit(pygame.image.load("data/img/palette.png"), (0,0))
        self.paintRect = self.paintScreen.get_rect()
        self.paletteRect = self.paletteScreen.get_rect()
        self.brush = PaintBrush(self.paintScreen)
        self.painting = False
        self.undoCache = []
        pygame.mixer.init(buffer = 256)
        self.playButton = Button("data/img/play_button.png", (350, 500))
        self.playButton.draw(self.screen)
        self.stopButton = Button("data/img/stop_button.png", (460, 515))
        self.stopButton.draw(self.screen)
        self.chordButton = Button("data/img/chord_button.png", (265, 515))
        self.chordButton.draw(self.screen)
        self.demo1Button = Button("data/img/demo_1_button.png", (700, 0))
        self.demo1Button.draw(self.screen)
        self.demo2Button = Button("data/img/demo_2_button.png", (750, 0))
        self.demo2Button.draw(self.screen)
        self.demo3Button = Button("data/img/demo_3_button.png", (700, 50))
        self.demo3Button.draw(self.screen)
        self.demo1 = pygame.image.load('data/img/demo_1.png')
        self.demo2 = pygame.image.load('data/img/demo_2.png')
        self.demo3 = pygame.image.load('data/img/demo_3.png')
        self.help = pygame.image.load('data/img/help.png')
        self.scanGroup = pygame.sprite.Group()
        colorArray = [(254,0,0), (254,63,0), (254,127,0), (254, 214, 0),
                           (254,254,0), (127,254,0), (0,254,0), (13,152,185),
                           (0,0,254),(75,0,130), (143,0,254), (198, 21, 133)]
        # red, red-orange, orange, yellow-orange, yellow, yellow-green, green,
        # blue-green,blue, blue-violet, violet, red-violet
        noteArray = [pygame.mixer.Sound("data/C.ogg"),
                     pygame.mixer.Sound("data/C#.ogg"),
                     pygame.mixer.Sound("data/D.ogg"),
                     pygame.mixer.Sound("data/D#.ogg"),
                     pygame.mixer.Sound("data/E.ogg"),
                     pygame.mixer.Sound("data/F.ogg"),
                     pygame.mixer.Sound("data/F#.ogg"),
                     pygame.mixer.Sound("data/G.ogg"),
                     pygame.mixer.Sound("data/G#.ogg"),
                     pygame.mixer.Sound("data/A.ogg"),
                     pygame.mixer.Sound("data/A#.ogg"),
                     pygame.mixer.Sound("data/B.ogg")]
        #set the volumes at .3 to avoid gain
        for sound in noteArray:
            sound.set_volume(.3)
        #create a dict of notes with each notes corresponding color as its key
        self.noteDict = dict()
        for i in xrange(len(colorArray)):
            self.noteDict[colorArray[i]] = noteArray[i]
        self.playback = False
        self.canvasChordArray = []
        self.brush.set_brush(pygame.image.load("data/img/Brush.png"))
        self.brush.set_follow_angle(True)
        self.color = (254,0,0)
        self.brush.set_color(self.color)
        self.sound = self.noteDict[self.color]
        
    def save_paper(self):
        '''
        Make a copy of the screen and add it to the undoCache
        '''
        self.undoCache.append(self.paintScreen.copy())

    def undo_paper(self):
        '''
        Blits the previous saved state to the screen
        '''
        #Don't undo if there's nothing to undo
        if (len(self.undoCache) >= 1 and len(self.canvasChordArray) >= 1):
            p = self.undoCache.pop()
            self.canvasChordArray.pop()
            self.paintScreen.blit(p,(0,0))
            
    def paint_start(self):
        '''
        Initiates pinting and saves the state of the canvas before
        painting begins
        '''
        self.painting = True
        self.save_paper()
        
    def paint_stop(self):
        '''
        Ends the painting state
        '''
        self.painting = False
     
    def scan_col(self, surface,col):
        '''
        Scan and play the colors in a given column
        '''
        newChordDict = dict()
        #get the color of each pixel in the given row
        for row in xrange(self.paintRect.height):
            x = col
            y = row
            color = self.paintScreen.get_at((x, y))[:3]
            #if the color has a note assigned to it and has not already been
            #seen add it to the newChordDict with the color as the key
            if ((color in self.noteDict) and (color not in newChordDict)):
                newChordDict[color] = (self.noteDict[color])
        for note in self.noteDict.iterkeys():
            #if the note was playing but is no longer present stop playing it
            if ((note in self.chordDict) and (note not in newChordDict)):
                self.noteDict[note].stop()
            #if the note was not playing but is now present, begin playing it.
            if ((note in newChordDict) and (note not in self.chordDict)):
                self.noteDict[note].play()
        self.chordDict = newChordDict
        #sleep for 1 ms to get a more uniform scan speed
        time.sleep(.01)
        
    def mouse_event_handler(self, event):
        '''
        Handles mouse events
        '''
        if event.type == MOUSEBUTTONDOWN:
            self.mouse_button_down_handler(event)
        elif event.type == MOUSEMOTION:
            self.mouse_motion_handler(event)
        elif event.type == MOUSEBUTTONUP:
            self.mouse_button_up_handler(event)
        else: return
    
    def mouse_button_down_handler(self, event):
        '''
        Handles mousebuttondown events
        '''
        if event.button == 1:
            #if the play button is pressed begin scanning
            if (self.playButton.button_pressed(event.pos, 0, 0)):
                if (self.playback == False):
                    self.chordDict = dict()
                    self.scannerLeft = 0
                    self.playback = True
                    self.scanSprite = Scanner(self.paintScreen)
                    self.scanGroup.add(self.scanSprite)
                    self.canvas = self.paintScreen.copy()
            if (self.stopButton.button_pressed(event.pos, 0, 0)):
                if (self.playback == False):
                    return
                else:
                    #clear scanSprites from the screen and stop playing notes
                    self.playback = False
                    self.scanGroup.clear(self.paintScreen, self.canvas)
                    self.scanGroup.empty()
                    for note in self.noteDict.itervalues():
                        note.stop()
            #play all colors currently present on screen
            if (self.chordButton.button_pressed(event.pos, 0, 0)):
                #get all unique elements in canvasChordArray
                canvasChordSet = set(self.canvasChordArray)
                #play all notes in canvasChordSet
                for sound in canvasChordSet:
                    sound.play(0, 1000, 0)
            #load demo1 or demo2 to the screen with their correct respective
            #canvasChordArrays
            if (self.demo1Button.button_pressed(event.pos, 0, 0)):
                self.paintScreen.blit(self.demo1, (0,0))
                self.canvasChordArray = [pygame.mixer.Sound("data/C.ogg"),
                                         pygame.mixer.Sound("data/E.ogg"),
                                         pygame.mixer.Sound("data/D#.ogg"),
                                         pygame.mixer.Sound("data/G.ogg")]
                self.save_paper()
            if (self.demo2Button.button_pressed(event.pos, 0, 0)):
                self.paintScreen.blit(self.demo2, (0,0))
                self.canvasChordArray = [pygame.mixer.Sound("data/E.ogg"),
                                         pygame.mixer.Sound("data/G#.ogg"),
                                         pygame.mixer.Sound("data/B.ogg"),
                                         pygame.mixer.Sound("data/D#.ogg"),
                                         pygame.mixer.Sound("data/F#.ogg"),
                                         pygame.mixer.Sound("data/C#.ogg"),
                                         pygame.mixer.Sound("data/A.ogg")]
            if (self.demo3Button.button_pressed(event.pos, 0, 0)):
                self.paintScreen.blit(self.demo3, (0,0))
                self.canvasChordArray = [pygame.mixer.Sound("data/C.ogg"),
                                         pygame.mixer.Sound("data/E.ogg"),
                                         pygame.mixer.Sound("data/D#.ogg"),
                                         pygame.mixer.Sound("data/G.ogg")]
                self.save_paper()
            #if the user clicks on the palette, set the brush color to the
            #color under the mouse
            if (self.paletteRect.collidepoint(event.pos)):
                self.color = self.paletteScreen.get_at(event.pos)[:3]
                self.sound = self.noteDict[self.color]
                self.sound.play(0, 500, 0)
                self.brush.set_color(self.color)
            #get the position of the mouse with respect to the canvas
            brushPos = (event.pos[0]-self.paintScreen.get_abs_offset()[0],
                        event.pos[1]-self.paintScreen.get_abs_offset()[1])
            #if the mouse is over the canvas begin painting
            if self.paintRect.collidepoint(brushPos):
                self.brush.paint_from(brushPos)
                self.paint_start()
                lineFrom = event.pos
    
    def mouse_motion_handler(self, event):
        '''
        Handles mousemotion events
        '''
        brushPos = (event.pos[0]-self.paintScreen.get_abs_offset()[0],
                    event.pos[1]-self.paintScreen.get_abs_offset()[1])
        #if the mouse is in the canvas and there's no scanning going on
        #continue painting
        if event.buttons[0]:
            if (self.painting and (self.playback == False)):
                if (self.paintRect.collidepoint(brushPos)):
                    self.brush.paint_to(brushPos)
                    #set the volume at .05 to prevent gain
                    #self.sound.set_volume(.05)
                    self.sound.play()
                else:
                    self.sound.stop()
    
    def mouse_button_up_handler(self, event):
        '''
        Handles mousebuttonup events
        '''
        #if there is a mousebuttonup event in the canvas
        #stop painting, stop playing the current note
        #and add the note to the canvasChordArray
        if (event.button == 1 and self.painting and
            self.playback == False):
            self.paint_stop()
            self.sound.stop()
            self.canvasChordArray.append(self.sound)
    
    def main_loop(self):
        clock = pygame.time.Clock()
        lineFrom = None
        lineTo = None
        showHelp = True
        nextUpdate = pygame.time.get_ticks()
        while True:
            if (self.playback == True):
                #clear the screen of scanSprites
                self.scanGroup.clear(self.paintScreen, self.canvas)
                self.scanGroup.update()
                self.scanGroup.draw(self.paintScreen)
                #scan the column at scannerLeft
                self.scan_col(self.paintScreen, self.scannerLeft)
                self.scannerLeft += 1
                #When the scanner reaches the edge of the canvas
                #stop scanning and stop playing all of the notes
                if (self.scannerLeft == self.paintRect.width):
                    self.playback = False
                    for note in self.noteDict.itervalues():
                        note.stop()
            for event in pygame.event.get():
                #if showHelp is true don't handle any event
                if showHelp:
                    if event.type == QUIT:
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return                    
                        else:
                            showHelp = False
                            self.paintScreen.fill((255,255,255))
                else:
                    if event.type == QUIT:
                        pygame.quit()
                        return
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            return                    
                        elif event.key == K_SPACE:
                            #fill the screen with white
                            #and empty the undoCache
                            self.undoCache = []
                            self.paint_start()
                            self.paintScreen.fill((255,255,255))
                            self.canvasChordArray = []
                            self.paint_stop()
                        elif event.key == K_z:
                            self.undo_paper()
                        elif event.key == K_h:
                            showHelp = True 
                    else:
                        self.mouse_event_handler(event)
                    
            if pygame.time.get_ticks() >= nextUpdate:
                nextUpdate+=33
                self.screen = self.screen.copy()
                self.screen.blit(self.paintScreen,self.paintRect.topleft)
                if not showHelp:
                    if lineFrom and lineTo:
                        pygame.draw.line(self.screen,(0,0,0),lineFrom,lineTo)
                #if showHelp is true blit the help screen to the canvas
                if showHelp:
                    self.paintScreen.blit(self.help,(0,0))
                pygame.display.flip()            

def main():

    pygame.init()

    g = App()
    g.main_loop()
 
if __name__ == '__main__': 
    main()



