import pygame, sys
from pygame.locals import *
import os


class TimeStamp():
    def __init__(self, time=0):
        self.time = time

class Line():
    start = (0,0)
    end = (0,0)

    def __init__(self, start, end):
        self.start = start
        self.end =end

class Player():
    def __init__(self, color, rect, name):
        self.color = color
        self.rect = rect
        self.name = name
        self.drag = False
        self.lines = []

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
        if QUIT == event.type:
            pygame.quit()
            sys.exit()
        elif MOUSEMOTION == event.type:
            for player in list_of_players:
                if player.drag:
                    player.rect.center = event.pos
                    player.lines[-1][currentTime.time][-1].end = player.rect.center
        elif MOUSEBUTTONDOWN == event.type:

            #check to see if player is clicked
            for player in list_of_players:
                if player.rect.collidepoint(event.pos):
                    player.drag = True

                    if player.lines:
                        if player.lines[-1].has_key(currentTime.time):
                            #set lines here
                            player.lines[-1][currentTime.time].append(Line(player.rect.center, player.rect.center))
                        else:
                            #create the dict and list
                            player.lines[-1][currentTime.time] = [Line(player.rect.center, player.rect.center)]
                    else:
                        player.lines.append( {currentTime.time : [Line(player.rect.center, player.rect.center)] } )
        elif MOUSEBUTTONUP == event.type:
            for player in list_of_players:
                if player.drag:
                    player.drag = False

        #KEYBOARD INPUT
        # + : Advance curTime
        # - : Revert curTime
        elif KEYDOWN == event.type:
            if event.unicode == u'+':
                currentTime.time = currentTime.time + 1
            elif event.unicode == u'-':
                currentTime.time = currentTime.time - 1
                if currentTime.time < 0:
                    currentTime.time = 0
            elif event.unicode == u'm':
                if mode == 0:
                    mode = 1
                else:
                    mode = 0
            print currentTime.time




        screen.blit(map, (0,0))
        if mode == 0:
            for player in list_of_players:
                pygame.draw.rect( screen, player.color, player.rect)

                for lineDict in player.lines:
                    for lineList in lineDict.itervalues():
                        for line in lineList:
                                pygame.draw.line(screen, player.color, line.start, line.end)
        elif mode == 1:
            for player in list_of_players:
                for lineDict in player.lines:
                    times = range(0, currentTime.time+1)
                    print times
                    for time in times:
                        if lineDict.has_key(time):
                            print lineDict
                            for line in lineDict[time]: 
                                pygame.draw.line(screen, player.color, line.start, line.end)
                            pygame.draw.rect( screen, player.color, Rect(line.end, (10,10)))
        pygame.display.update()
