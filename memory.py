# In the memory game the player will try to match two identical images on a rectangular grid, the score of the player is the time taken to complete the game

import pygame,random,time

# User-defined functions
def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Memory Game')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    speed = 0.01
    time.sleep(speed)
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes
class Game:

    def __init__(self, surface):
        # this method will initialize the Game
        # self is the Game to initialize
        # surface is the display window surface object
        
        # the following are objects needed for every game
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.fg_color = pygame.Color('white')
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
       
        # the following are game specific objects
        self.board_size = 4
        self.tiles_clicked = None
        self.tiles_exposed = 0
        self.time = 0
        self.tile_time = 1
        self.board = [ ]
        self.images = [ ]
        self.image_names = ['image1.bmp','image2.bmp','image3.bmp','image4.bmp','image5.bmp','image6.bmp','image7.bmp','image8.bmp']
        self.create_images()
        self.create_board()
        
        
    def create_images(self):
        # creates a list of randomized images
        # self refers to the Game that will be using the created images
        for file in self.image_names:
            image = pygame.image.load(file)
            self.images.append(image)
        self.images = self.images + self.images # concatinating the images list with itself to create a list of 16 images
        random.shuffle(self.images)
        
    def create_board(self):
        # creates a four by four grid 
        # self refers to the Game that will be utilizing the grid
        for row_index in range(self.board_size):
            row = [ ]
            for column_index in range(self.board_size):
                image_index = row_index * self.board_size + column_index 
                image = self.images[image_index]
                width = image.get_width()
                height = image.get_height()
                x = column_index * width
                y = row_index * height
                tile = Tile(x, y, image, self.surface)
                row.append(tile)
            self.board.append(row)    
    
    def play(self):
        # Play the game until the player presses the close box.
        # self is the Game that should be continued or not.
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # handle each user event by changing the game state appropriately.
        # self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_button_up(event.pos)
    
    def tile_position(self, position):
        # will return the tile that has been clicked otherwise it will return none
        # self is the Game whose board will be checked for tile position
        # the parameter position is a set of coordinates and is of class tuple
        for row in self.board:
            for tile in row:
                if tile.cursor_position(position):
                    return tile    
        return None
                                    
    def handle_mouse_button_up(self, position):
        # will handle all the events that relate to a mouse button up event
        # self is the Game whose mouse button up events will be handled
        # the parameter position is a set of coordinates and is of class tuple
        tile = self.tile_position(position)
        
        if tile is not None and tile is not self.tiles_clicked:
            tile.expose_tile()
            if self.tiles_clicked is None: 
                self.tiles_clicked = tile 
           
            elif tile.same_tile(self.tiles_clicked) : # elif the tiles are matching
                self.tiles_clicked = None # reset tiles_clicked so that more tiles can be clicked
                self.tiles_exposed += 1
                tile.draw()
            
            else : # if the tiles do not match
                tile.draw()
                pygame.display.update()
                time.sleep(self.tile_time)
                tile.cover_tile()
                self.tiles_clicked.cover_tile() # the cover_tile method will cover the two mismatching tiles
                self.tiles_clicked = None  
       
                
    def draw_score(self):
        # will the draw score of the game based on how many seconds have elapsed
        # self refers to the Game whose score will be drawn
        font_size = 75
        font = pygame.font.SysFont(None, font_size, True)
        text_surface = font.render(str(self.time), True, self.fg_color, self.bg_color)
        text_width = text_surface.get_width()
        surface_width = self.surface.get_width()
        text_location = (surface_width - text_width, 0)
        self.surface.blit(text_surface, text_location)    

    def draw(self):
        # draw all game objects.
        # self is the Game to draw
        self.surface.fill(self.bg_color)
        for row in self.board:
            for tile in row:
                tile.draw()
        self.draw_score()
        pygame.display.update()
           
    def update(self):
        # update the game objects for the next frame.
        # self is the Game to update
        self.time = pygame.time.get_ticks() // 1000 # divide by 1000 in order to obtain seconds
        
    def decide_continue(self):
        # check the conditions that determine if the game should continue or not
        # self is the Game that needs to be checked
        tile_pairs = self.board_size * 2 
        self.continue_game = self.tiles_exposed != tile_pairs 
        
    
class Tile:
    # An object in this class represents a Tile

    def __init__(self,x,y,image,surface):
        # initialize a Tile.
        # self is the tile to initialize
        # the parameter x refers to the x coordinate and is of type int
        # the parameter y refers to the y coordinate and is of type int
        # the paramter image is the image that will be placed in a specific tile and it is of class pygame.Surface
        # the parameter surface is the surface that the game will be played on and is of class pygame.Surface
        
        self.background_color = pygame.Color('black')
        self.border_width = 4            
        self.location = (x , y)
        self.surface = surface
        self.image = image
        self.exposed_tile = False
        self.cover_image = pygame.image.load('image0.bmp')
    
    def draw(self):
        # draw the tile objects onto the surface
        # self is the tile that we are trying ot draw
        if self.exposed_tile:
            self.surface.blit(self.image, self.location)
        else:
            self.surface.blit(self.cover_image, self.location)
        size = self.image.get_size()
        rectangle = pygame.Rect(self.location, size) 
        pygame.draw.rect(self.surface, self.background_color, rectangle, self.border_width)         
        
    def same_tile(self,twin_tile):
        # will check to see if the two tiles contain the same image
        # the paramater twin tile is the identical tile to a given image and is of class tuple
        if self is None or twin_tile is None:
            return False
        else:
            return (self.image == twin_tile.image)  
    
    def expose_tile(self):
        # will set the state of the tile to be exposed
        # the paramater self is the Tile we are trying to expose
        self.exposed_tile = True
        
    def cover_tile(self):
        # will set the state of the tile to be exposed
        # the paramater self refers to the Tile we are going to cover
        self.exposed_tile = False    
     
    def cursor_position(self, position):
        # will check to the position of the mouse cursor and uses collidepoint to check if a certain tile contains the cursor
        # the paramater self refers to the Tile that we are checking for cursor position 
        # the parameter position is a set of coordinates and is of class tuple
        size = self.image.get_size()
        rectangle = pygame.Rect(self.location, size) 
        if not self.exposed_tile and rectangle.collidepoint(position):
            return True
        else:
            return False

main()