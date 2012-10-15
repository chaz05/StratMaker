import pygame, sys
from pygame.locals import *
import os


class TimeStamp():
    def __init__(self, time=0):
        self.time = time

class Line():
    start = (0,0)
    end = (0,0)

    def __init__(self, start, end, color):
        self.start = start
        self.end =end
        self.color = color

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start, self.end)

class Mode():
    edit = 0
    playback = 1

class Player():
    def __init__(self, color, rect, name):
        self.color = color
        self.rect = rect
        self.size = self.rect.size
        self.name = name
        self.drag = False
        self.lines = []
    
    def draw(self, screen, timeStamp=TimeStamp(-1),mode=Mode.edit):
        # if Editting, only draw the last rect
        if Mode.edit == mode:
            pygame.draw.rect( screen, self.color, self.rect)

        #for either draw the lines, but if playback play to the current time
        for lineDict in self.lines:
            for time,lines in lineDict.iteritems():
                if Mode.playback == mode and  time <= timeStamp.time or Mode.edit == mode:
                    for line in lines:
                        line.draw(screen)
                    if Mode.playback == mode:
                        pygame.draw.rect(screen, self.color, Rect(line.end, player.size))

    def addLine(self, timeStamp, start, end):
        # check to make sure we have a list of lines first, if not init it
        if self.lines:
            # if the dictionary has the current time else add it ( may need to create our own object for this)
            if self.lines[-1].has_key(timeStamp.time):
                # Add the line
                self.lines[-1][timeStamp.time].append(Line(start, end, self.color))
            else:
                # Create the list of lines and add the Line
                self.lines[-1][timeStamp.time] = [Line(start, end, self.color)]
        else:
            self.lines.append( {timeStamp.time : [ Line(start, end, self.color) ] } )


pygame.init()

size = (600,400)
currentTime = TimeStamp(1)
#screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hello World!')

#load map
map = pygame.image.load(os.path.abspath("Maps/de_inferno.jpg"))
size = map.get_size()
screen = pygame.display.set_mode(size)
map.convert()
screen.blit(map, (0,0))

list_of_players = [ Player(pygame.Color(255,0,0,0), pygame.Rect(40,90,10,10), "Red"),
                    Player(pygame.Color(0,255,0,0), pygame.Rect(100,90,10,10), "Green")]


mode = 0 # Editing, Viewing

while True:


    for event in pygame.event.get():
	print event
        if QUIT == event.type:
            pygame.quit()
            sys.exit()
        elif MOUSEMOTION == event.type:
            for player in list_of_players:
                if player.drag:
                    player.rect.center = event.pos
                    # should probably do this cleaner !TODO
                    player.lines[-1][currentTime.time][-1].end = player.rect.center
        elif MOUSEBUTTONDOWN == event.type:

            #check to see if player is clicked
            for player in list_of_players:
                if player.rect.collidepoint(event.pos):
                    player.drag = True

                    # Add the line to the Player
                    player.addLine(currentTime, player.rect.center, player.rect.center)
                    break
        elif MOUSEBUTTONUP == event.type:
            for player in list_of_players:
                if player.drag:
                    player.drag = False

        #KEYBOARD INPUT
        # + : Advance curTime
        # - : Revert curTime
        # m : switch mode
        elif KEYDOWN == event.type:
            # Adj. Time
            if event.unicode == u'+':
                currentTime.time = currentTime.time + 1
            elif event.unicode == u'-':
                currentTime.time = currentTime.time - 1
                if currentTime.time < 0:
                    currentTime.time = 0
            # Set Mode
            elif event.unicode == u'm':
                if mode == Mode.edit:
                    mode = Mode.playback
                else:
                    mode = Mode.edit
            print currentTime.time




        screen.blit(map, (0,0))
        for player in list_of_players:
            player.draw(screen, currentTime, mode)

        pygame.display.flip() 
