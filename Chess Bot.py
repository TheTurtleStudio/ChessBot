#minimax
import pygame, sys, time
from pygame.locals import *
import time

boardString = "" # 1=whitespace 2=blackspace 3=user 4=computer 5=selected


sizeBase = 600
rowcount = 10 # Adjust this to set the size of the board, must be divisible by 2
tileMeasurements = sizeBase/rowcount
if tileMeasurements > sizeBase/rowcount:
    tileMeasurements = sizeBase/rowcount


active_player = 'user' # Set who goes first here. This is changed by switch_player() after every turn.
game_score = {'user':0, 'computer':0} # The scorecard

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
black_square = pygame.Surface((tileMeasurements, tileMeasurements))
pygame.draw.rect(black_square, black, (0,0,tileMeasurements,tileMeasurements),0)
black_circle = pygame.Surface((tileMeasurements,tileMeasurements), pygame.SRCALPHA, 32)
black_circle.convert_alpha()
x = black_circle.get_rect()
pygame.draw.circle(black_circle,black,x.center,15)
#pygame.draw.circle(black_circle,black,(x.centerx+tileMeasurements,x.centery/2),15)
playing = True


playtiles = pygame.sprite.Group()
gamepiece_group = pygame.sprite.Group()

class Board():
    def __init__(self):
        pass

    def get_board(self):
        pass
  
class Tile(pygame.sprite.Sprite):
    def __init__(self, color, name, posX, posY, width, height, occupied=False, owner=None, tile_location={}):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tileMeasurements,tileMeasurements))
        pygame.draw.rect(self.image, black,(0,0,width,height),0)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.name = name
        self.occupied = occupied
        self.owner = owner
        self.tile_location = tile_location
        tileSize = tileMeasurements


class gamePiece(pygame.sprite.Sprite):
    def __init__(self, color, tile_location, name, posX, posY, radius):
        pygame.sprite.Sprite.__init__(self)
        self.originalimage = pygame.Surface((tileMeasurements,tileMeasurements), pygame.SRCALPHA, 32)
        self.originalimage.convert_alpha()
        pygame.draw.circle(self.originalimage, color, (self.originalimage.get_width()/2,self.originalimage.get_height()/2), radius, 0)
        self.rect = self.originalimage.get_rect()
        self.image = self.originalimage
        self.rect.x = posX
        self.rect.y = posY
        self.name = name
        self.tile_location = tile_location
        self.selected = False

                
def createBoard(screenSizeXY, tileSize):
    global tileX, tileY, offset, boardString, tiles
    print("Creating board in a "+str(int(screenSizeXY/tileSize))+"x"+str(int(screenSizeXY/tileSize))+" grid with each tile being "+str(int(tileSize))+" pixels in length and height ("+str(int(((screenSizeXY/tileSize)*(screenSizeXY/tileSize))/2))+" playable/unplayable tiles)")
    tileX = int(tileMeasurements)
    
    for i in range(int(((screenSizeXY/tileSize)*(screenSizeXY/tileSize))/2)):
        if tileY <= 2*tileSize:
            tile_location = {'row': int(tileY/(screenSizeXY/(screenSizeXY/tileSize))+1), 'col': int(tileX/(screenSizeXY/(screenSizeXY/tileSize))+1)}
            playtiles.add(Tile(black, "Tile", tileX, tileY, tileSize, tileSize, occupied=True, owner='computer', tile_location=tile_location))
            gamepiece_group.add(gamePiece(computer, tile_location, 'computer', tileX, tileY, int(tileSize*0.4)))
            
            if offset:
                boardString = boardString + "41"
            else:
                boardString = boardString + "14"
                
        elif tileY >= ((screenSizeXY/tileSize)-3)*tileSize:
            tile_location = {'row': int(tileY/(screenSizeXY/(screenSizeXY/tileSize))+1), 'col': int(tileX/(screenSizeXY/(screenSizeXY/tileSize))+1)}
            playtiles.add(Tile(black, "Tile", tileX, tileY, tileSize, tileSize, occupied=True, owner='user', tile_location=tile_location))
            gamepiece_group.add(gamePiece(user, tile_location, 'user', tileX, tileY, int(tileSize*0.4)))
         
            if offset:
                boardString = boardString + "31"
            else:
                boardString = boardString + "13"
        else:
            tile_location = {'row': int(tileY/(screenSizeXY/(screenSizeXY/tileSize))+1), 'col': int(tileX/(screenSizeXY/(screenSizeXY/tileSize))+1)}
            newtile = Tile(black, "Tile", tileX, tileY, tileSize, tileSize, occupied=False, tile_location=tile_location)
            playtiles.add(newtile)
            if offset:
                boardString = boardString + "21"
            else:
                boardString = boardString + "12"
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



def remove_highlight():
    screen.blit(black_square, (origin_tile.rect.x, origin_tile.rect.y))

def add_highlight():
    screen.blit(black_circle, (selected_piece.rect.x, selected_piece.rect.y))

def switch_player():
    global active_player
    if active_player == 'user':
        active_player = 'computer'
    else:
        active_player = 'user'

def check_game_score():
    global playing
    
    user = game_score['user']
    computer = game_score['computer']
    winner = None
    print('\nUser score: {}\nComputer score: {}'.format(user,computer))
    print('Must reach {} to win the game'.format(winning_score))

    if user == winning_score:
        playing = False
        winner = 'User'
    elif computer == winning_score:
        playing = False
        winner = 'Computer'
    if winner:
        print('\n\n\n{} HAS WON THE GAME!!'.format(winner))
        
def check_if_piece_clicked(mouse):
    global selected_piece, move_pending
    
    for piece in gamepiece_group:
        if piece.rect.collidepoint(mouse): # Find the game piece that is being clicked
            if piece.name == active_player and not move_pending: # Only select a piece if it belongs to the active player and move is not pending
                piece.selected = True
                selected_piece = piece
                add_highlight()

def check_if_tile_clicked(mouse):
    global destination_tile
    
    for tile in playtiles:
        if tile.rect.collidepoint(mouse):
            if selected_piece and not tile.occupied: # Only move if a piece is selected and destination is not occupied
                destination_tile = tile
                return True

def make_move():
    # POSSIBLY DO SOME AI STUFF HERE WHEN DETERMINING
    # all possible moves for the computer player.
    
    if check_for_valid_move(): # If this returns true then proceed with the move.
        _move()

        
def check_for_valid_move(): # Check if the move is valid and return True if it is. Otherwise returns implicitly as None.
    global selected_piece, gamepiece, origin_tile, user_score, computer_score, middle_tile

    for tile in playtiles:
        if tile.rect.x == selected_piece.rect.x and tile.rect.y == selected_piece.rect.y:
            origin_tile = tile # This is the tile where the moving piece came from
            
    if active_player == 'user': # Need to modify to allow a value of 'both' for King pieces
        direction = 'up'
    else:
        direction = 'down'

    origin_row = origin_tile.tile_location['row']
    origin_column = origin_tile.tile_location['col']
    destination_row = destination_tile.tile_location['row']
    destination_column = destination_tile.tile_location['col']


    if destination_row == origin_row + 1: # Piece is trying to move down 1 row
        if direction == 'down' or direction == 'both':
            if active_player == 'computer':
                if destination_column == origin_column + 1 or destination_column == origin_column - 1: # Piece is trying to move 1 tile to the left or right
                    if not destination_tile.occupied: # Only allow if destination is not occupied
                        return True


                    
    elif destination_row == origin_row - 1: # Piece is trying to move up 1 row
        if direction == 'up' or direction == 'both':
            if active_player == 'user':
                if destination_column == origin_column + 1 or destination_column == origin_column - 1:
                    if not destination_tile.occupied:
                        return True



    elif destination_row == origin_row + 2: # Piece is trying to move down 2 rows, possible jump
        if direction == 'down' or direction == 'both':
            if active_player == 'computer':
                if destination_column == origin_column + 2 or destination_column == origin_column - 2: # Piece is trying to move 2 tiles to the left or right
                    if destination_column == origin_column + 2: # jumping right
                        for tile in playtiles:
                            if tile.tile_location['row'] == origin_row + 1 and tile.tile_location['col'] == origin_column + 1:
                                if tile.owner and not tile.owner == active_player:
                                    if not destination_tile.occupied:
                                        game_score[active_player] += 1
                                        middle_tile = tile
                                        tile.owner = None
                                        tile.occupied = False
                                        return True
                    elif destination_column == origin_column - 2: # jumping to left
                        for tile in playtiles: # Looping the tiles to find the tile that's being jumped.
                            if tile.tile_location['row'] == origin_row + 1 and tile.tile_location['col'] == origin_column - 1: # This is the tile being jumped
                                if tile.owner and not tile.owner == active_player: # Make sure the owner of the tile is the opponent so you don't jump your own piece
                                    if not destination_tile.occupied:
                                        game_score[active_player] += 1
                                        middle_tile = tile 
                                        tile.owner = None # Remove the owner of the tile that was just jumped
                                        tile.occupied = False # Mark the tile as unoccupied
                                        return True



                                    
    elif destination_row == origin_row - 2: # Piece is trying to move up 2 rows, possible jump
        if direction == 'up' or direction == 'both':
            if active_player == 'user':
                move_type = 'jumping'
                if destination_column == origin_column + 2 or destination_column == origin_column - 2:
                    if destination_column == origin_column + 2: # jumping to right
                        for tile in playtiles:
                            if tile.tile_location['row'] == origin_row - 1 and tile.tile_location['col'] == origin_column + 1:
                                if tile.owner and not tile.owner == active_player:
                                    if not destination_tile.occupied:
                                        game_score[active_player] += 1
                                        middle_tile = tile
                                        tile.owner = None
                                        tile.occupied = False
                                        return True
                    elif destination_column == origin_column - 2: # jumping to left
                        for tile in playtiles:
                            if tile.tile_location['row'] == origin_row - 1 and tile.tile_location['col'] == origin_column - 1:
                                if tile.owner and not tile.owner == active_player:
                                    if not destination_tile.occupied:
                                        game_score[active_player] += 1
                                        middle_tile = tile
                                        tile.owner = None
                                        tile.occupied = False
                                        return True
    

        
def _move(): # This should really only be called by make_move()
    global selected_piece, gamepiece, origin_tile, middle_tile, jumped_piece

    destination_tile.occupied = True # Sets the destination tile as being occupied
    destination_tile.owner = active_player # Set the destination tile's owner as the active player


    origin_tile.occupied = False
    origin_tile.owner = None
    screen.blit(black_square, (origin_tile.rect.x, origin_tile.rect.y))                               
    selected_piece.rect.x = destination_tile.rect.x
    selected_piece.rect.y = destination_tile.rect.y
    gamepiece_group.draw(screen)
    selected_piece = None
    if middle_tile:
        for piece in gamepiece_group:
            if piece.rect.x == middle_tile.rect.x and piece.rect.y == middle_tile.rect.y:
                jumped_piece = piece
                break
        jumped_piece.kill()
        screen.blit(black_square,(middle_tile.rect.x, middle_tile.rect.y))
        middle_tile = None
        jumped_piece = None
        check_game_score() # Check the game score and end the game if there is a winner
    switch_player() # Move is done, switch player.
    


        
createBoard(sizeBase, tileMeasurements)
playtiles.draw(screen)
gamepiece_group.draw(screen)

selected_piece = None # A variable to hold the selected piece that is trying to move.
destination_tile = None # A variable to hold the destination tile that is being moved to.
middle_tile = None # A variable to hold the tile that is between a jumping piece and it's destination
origin_tile = None # A variable to hold the tile where the moving piece originated from
jumped_piece = None # A variable to hold the game piece that was jumped
move_pending = False # A variable to hold whether or not a multi-move is pending. Not curently implemented
winning_score = len(gamepiece_group) / 2 # The score required to win the game.

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            check_if_piece_clicked(mouse) # Check if a game piece was clicked
            if check_if_tile_clicked(mouse): # Check if a tile was clicked                                                          
                make_move() # Attempt the move
                        
            
    pygame.display.flip()
