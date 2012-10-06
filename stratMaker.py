import pygame, sys
from pygame.locals import *
import os

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

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hello World!')

#load map
map = pygame.image.load(os.path.abspath("Maps/de_inferno.jpg"))
map.convert()
size = map.get_size()
screen = pygame.display.set_mode(size)
screen.blit(map, (0,0))

list_of_players = [ Player(pygame.Color(255,0,0,0), pygame.Rect(40,90,10,10), "Red"),
                    Player(pygame.Color(0,255,0,0), pygame.Rect(100,90,10,10), "Green")]


while True:
    
  
    for event in pygame.event.get():
        if QUIT == event.type:
            pygame.quit()
            sys.exit()
        elif MOUSEMOTION == event.type:
            for player in list_of_players:
                if player.drag:
                    player.rect.center = event.pos
                    player.lines[-1].end = player.rect.center
        elif MOUSEBUTTONDOWN == event.type:

            #check to see if player is clicked
            for player in list_of_players:
                if player.rect.collidepoint(event.pos):
                    player.drag = True
                    player.lines.append(Line(player.rect.center, player.rect.center))
        elif MOUSEBUTTONUP == event.type:
            for player in list_of_players:
                if player.drag:
                    player.drag = False
                    
        screen.blit(map, (0,0))
        for player in list_of_players:
            pygame.draw.rect( screen, player.color, player.rect)

            for line in player.lines:
                pygame.draw.line(screen, player.color, line.start, line.end)
        pygame.display.update()
        
