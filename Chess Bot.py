#minimax
import pygame, sys, time
from pygame.locals import *
import time
playtiles = pygame.sprite.Group()
boardString = "" # 1=whitespace 2=blackspace 3=user 4=computer 5=selected
print(boardString)
sizeBase = 600
tileMeasurements = sizeBase/8
if tileMeasurements > sizeBase/8:
    tileMeasurements = sizeBase/8
tileX = 0
tileY = 0
offset = False
pygame.init()
size = (sizeBase,sizeBase)
white = (255,255,255)
computer = (255,0,0)
user = (250,250,250)
black = (0,0,0)
screen = pygame.display.set_mode(size)
screen.fill(white)
pygame.display.set_caption("Checkers Bot")
playing = True

class Tile(pygame.sprite.Sprite):
    def __init__(self, color, name, posY, posX, width, height):
        pygame.draw.rect(screen, (black), pygame.Rect(tileX, tileY, tileMeasurements, tileMeasurements))
def createBoard(screenSizeXY, tileSize):
    global tileX, tileY, offset, boardString, tiles
    print("Creating board in a "+str(int(screenSizeXY/tileSize))+"x"+str(int(screenSizeXY/tileSize))+" grid with each tile being "+str(int(tileSize))+" pixels in length and height ("+str(int(((screenSizeXY/tileSize)*(screenSizeXY/tileSize))/2))+" playable/unplayable tiles)")
    tileX = int(tileMeasurements)
    for i in range(int(((screenSizeXY/tileSize)*(screenSizeXY/tileSize))/2)):
        if tileY <= 2*tileSize:
            newtile = Tile(black, "tileR{}C{}".format(int((i+(screenSizeXY/tileSize))/(screenSizeXY/tileSize)),int(tileX/(screenSizeXY/(screenSizeXY/tileSize))+1)), tileX, tileY, tileSize, tileSize)
            playtiles.add(newtile)
            pygame.draw.circle(screen,computer,[int(tileX+tileSize*0.5), int(tileY+tileSize*0.5)], int(tileSize*0.4), 0)
           # print(tileX, tileY, "cmp")
            if offset:
                boardString = boardString + "4"
                boardString = boardString + "1"
            else:
                boardString = boardString + "1"
                boardString = boardString + "4"
        elif tileY >= ((screenSizeXY/tileSize)-3)*tileSize:
            newtile = Tile(black, "tileR{}C{}".format(int((i+(screenSizeXY/tileSize))/(screenSizeXY/tileSize)),int(tileX/(screenSizeXY/(screenSizeXY/tileSize))+1)), tileX, tileY, tileSize, tileSize)
            playtiles.add(newtile)
            pygame.draw.circle(screen,user,[int(tileX+tileSize*0.5), int(tileY+tileSize*0.5)], int(tileSize*0.4), 0)
         #   print(tileX, tileY, "user")
            if offset:
                boardString = boardString + "3"
                boardString = boardString + "1"
            else:
                boardString = boardString + "1"
                boardString = boardString + "3"
        else:
            newtile = Tile(black, "tileR{}C{}".format(int((i+(screenSizeXY/tileSize))/(screenSizeXY/tileSize)),int(tileX/(screenSizeXY/(screenSizeXY/tileSize))+1)), tileX, tileY, tileSize, tileSize)
            playtiles.add(newtile)
       #     print(tileX, tileY, "tile")
            if offset:
                boardString = boardString + "2"
                boardString = boardString + "1"
            else:
                boardString = boardString + "1"
                boardString = boardString + "2"
        if tileX >= screenSizeXY - (tileMeasurements*2):
            tileY = tileY+tileSize
            if offset:
                offset = False
                tileX = int(tileMeasurements)
            else:
                offset = True
                tileX = 0
            boardString = boardString + "\n"
        else:
            tileX = tileX+(tileSize*2)
createBoard(sizeBase, tileMeasurements)
print(boardString)
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            quit()
    pygame.display.flip()
