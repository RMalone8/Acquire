import math
import pygame
import sys
import random
from os.path import exists
from ast import literal_eval

'''
Constants
'''

HEIGHT, WIDTH = 900, 1500
ROWS = 9
COLS = 12
SQUARE_SIZE = HEIGHT//ROWS
PIECE_SIZE = SQUARE_SIZE - 10
BUTTON_HEIGHT = 70
BUTTON_WIDTH = 90
MENU_BUTTON_HEIGHT = 140
MENU_BUTTON_WIDTH = 300

PINK = (255,193,204)
RED = (255,0,0)
LIGHTISH_RED = (255,90,90)
WHITE = (255,255,255)
BLUE = (30,30,255)
LIGHTISH_BLUE = (90,90,255)
GREEN = (60,200,60)
LIGHTISH_GREEN = (120,200,120)
BLACK = (0,0,0)
GREY = (111,111,111)
LIGHT_GREY = (200,200,200)
LIGHTISH_GREY = (131,131,131)
LIGHT_BROWN = (213, 196, 161)
LIGHTISH_YELLOW = (255,243,109)
YELLOW = (254,221,0)
ORANGE = (255, 140,51)
LIGHTISH_ORANGE = (255,160,51)
LIGHTISH_PURPLE = (225, 70,255)
PURPLE = (197, 30,227)
TEAL = (0,191,230)
LIGHTISH_TEAL = (51,221,255)
ANTIQUE_WHITE = (250,235,215)

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#let users pick the names of the companies! Or allow them to just select the default names

class Menu_Button:
    def __init__(self,x,y,text_input,font,color,l_color,width,height):
        self.x = x
        self.y = y
        self.text_input = text_input
        self.font = font
        self.color = color
        self.l_color = l_color
        self.hover_color = l_color
        self.text_input = text_input
        self.text = font.render(self.text_input,True,self.hover_color)
        self.hovering = False
        self.width = width
        self.height = height
        self.text_rect = self.text.get_rect(center=(self.x+(self.width//2),self.y+(self.height//2)))

    def draw_menu_button(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width, self.height))
        pygame.draw.rect(win, self.l_color, (self.x+5,self.y+5,self.width-10, self.height-10))
        win.blit(self.text,self.text_rect)

    def update_menu_button(self, win, x, y):
        if x >= self.x and x <= (self.x+self.width) and y >= self.y and y <= (self.y+self.height):
            self.hover_color = self.color
            self.hovering = True
        else:
            self.hover_color = WHITE
            self.hovering = False

        self.text = self.font.render(self.text_input,True,self.hover_color)
        self.text_rect = self.text.get_rect(center=(self.x+(self.width//2),self.y+(self.height//2)))
        win.blit(self.text,self.text_rect)

    def check_for_click(self):
        if self.hovering:
            return True
        return False

class Toggle_Button(Menu_Button):
    def update_t_button(self, win, x,y,toggle):
        self.update_menu_button(win,x,y)
        if toggle:
            pygame.draw.rect(win, tuple(map(lambda t: t - 50 if t > 50 else t,self.l_color)), (self.x,self.y,self.width, self.height))
            pygame.draw.rect(win, tuple(map(lambda t: t - 50 if t > 50 else t,self.color)), (self.x+5,self.y+5,self.width-10, self.height-10))
            self.text_rect = self.text.get_rect(center=(self.x+(self.width//2),self.y+(self.height//2)))
            win.blit(self.text,self.text_rect)
        else:
            self.draw_menu_button(win)

class Board:
    def __init__(self, game):
        self.blue_button = Button(BLUE, LIGHTISH_BLUE, 1305, 1, game)
        self.red_button = Button(RED, LIGHTISH_RED, 1205, 1, game)
        self.green_button = Button(GREEN, LIGHTISH_GREEN, 1405, 1, game)
        self.yellow_button = Button(YELLOW, LIGHTISH_YELLOW, 1205, 73, game)
        self.teal_button = Button(TEAL, LIGHTISH_TEAL, 1305, 73, game)
        self.purple_button = Button(PURPLE, LIGHTISH_PURPLE, 1405, 73, game)
        self.orange_button = Button(ORANGE, LIGHTISH_ORANGE, 1305, 145, game)
        self.game = game

    def draw_squares(self,win):
        win.fill(ANTIQUE_WHITE)

        for row in range(COLS):
            for col in range(ROWS):
                pygame.draw.rect(win, LIGHT_BROWN, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(COLS+1):
            pygame.draw.line(win, GREY, (row*100,0),(row*100,900),4)
        for col in range(ROWS+1):
            pygame.draw.line(win, GREY, (0,col*100),(1200,col*100),4)

        pygame.draw.line(win, GREY, (1200,219),(1500,219),4)

    def updating_buttons(self, win):
        self.red_button.button_update(win,self.game.available_companies[0])
        self.blue_button.button_update(win,self.game.available_companies[1])
        self.green_button.button_update(win,self.game.available_companies[2])
        self.yellow_button.button_update(win,self.game.available_companies[3])
        self.teal_button.button_update(win,self.game.available_companies[4])
        self.purple_button.button_update(win,self.game.available_companies[5])
        self.orange_button.button_update(win,self.game.available_companies[6])

    def draw_for_merge(self, win):
        if 3 in self.game.tied_companies:
            self.red_button.button_update(win,1)
        else:
            self.red_button.button_update(win,0)
        if 4 in self.game.tied_companies:
            self.blue_button.button_update(win,1)
        else:
            self.blue_button.button_update(win,0)
        if 5 in self.game.tied_companies:
            self.green_button.button_update(win,1)
        else:
            self.green_button.button_update(win,0)
        if 6 in self.game.tied_companies:
            self.yellow_button.button_update(win,1)
        else:
            self.yellow_button.button_update(win,0)
        if 7 in self.game.tied_companies:
            self.teal_button.button_update(win,1)
        else:
            self.teal_button.button_update(win,0)
        if 8 in self.game.tied_companies:
            self.purple_button.button_update(win,1)
        else:
            self.purple_button.button_update(win,0)
        if 9 in self.game.tied_companies:
            self.orange_button.button_update(win,1)
        else:
            self.orange_button.button_update(win,0)
        

class Button:
    def __init__(self, color, l_color, x, y, game):
        self.color = color
        self.light_color = l_color
        self.left_corner_x = x
        self.left_corner_y = y
        self.game = game
        self.used = False

    def draw_button(self, win):
        pygame.draw.rect(win, self.color, (self.left_corner_x+2,self.left_corner_y+2, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(win, self.light_color, (self.left_corner_x+6,self.left_corner_y+6, BUTTON_WIDTH-8, BUTTON_HEIGHT-8))

    def check_for_click(self, mouse_x, mouse_y):
        if mouse_x >= self.left_corner_x and mouse_x <= self.left_corner_x + BUTTON_WIDTH and mouse_y >= self.left_corner_y and mouse_y <= self.left_corner_y + BUTTON_HEIGHT and self.used == False: 
            return True
        return False

    def button_update(self, win, available):
        if available:
            pygame.draw.rect(win, self.color, (self.left_corner_x+2,self.left_corner_y+2, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(win, self.light_color, (self.left_corner_x+6,self.left_corner_y+6, BUTTON_WIDTH-8, BUTTON_HEIGHT-8))
            self.used = False
        else:
            pygame.draw.rect(win, GREY, (self.left_corner_x+2,self.left_corner_y+2, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(win, LIGHTISH_GREY, (self.left_corner_x+6,self.left_corner_y+6, BUTTON_WIDTH-8, BUTTON_HEIGHT-8))
            self.used = True

      
class Game:
    def __init__(self, player_names, available_pieces, initial_moves):
        self.turn = 0
        self.round = 1
        self.available_companies = [3,4,5,6,7,8,9]
        self.company_not_chosen = True
        self.skip = False
        self.skip_two = False
        self.biggest_company = 0
        self.merging_values = []
        self.companies_temp = []
        self.tied_companies = []
        self.direction_x = []
        self.direction_y = []
        self.adding = False
        self.create = False
        self.piece_placed = False
        self.piece_drawn = False
        self.piece_discarded = False
        self.number_of_tiles = [0,0,0,0,0,0,0]
        self.initial_moves = initial_moves
        self.available_pieces = available_pieces
        self.player_moves = [[] for i in player_names]
        self.discarded_pieces = []
        self.player_names = player_names
        self.balances = [6000 for i in player_names]
        self.total_stocks = [25,25,25,25,25,25,25]
        self.owned_stocks = [[0 for i in range(7)] for j in player_names]
        self.stock_prices = [0,0,0,0,0,0,0]
        self.first_bonus = [0,0,0,0,0,0,0]
        self.second_bonus = [0,0,0,0,0,0,0]
        self.board = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1]]


    def draw_labels(self, win, piece_labels):
        for i in range(1,10):
            for j in range(1,13):
                win.blit(MENU_FONT_S.render(str(piece_labels[i][j]),True,BLACK),MENU_FONT_S.render(str(piece_labels[i][j]),True,BLACK).get_rect(center=(j*100-50.2,i*100-50.2)))
                win.blit(MENU_FONT_S.render(str(piece_labels[i][j]),True,WHITE),MENU_FONT_S.render(str(piece_labels[i][j]),True,WHITE).get_rect(center=(j*100-50,i*100-50)))

    def draw_possible_moves(self, win, game, top_color, bottom_color, piece_labels):
        for i in range(1,10):
            for j in range(1,13):
                if [i,j] in game.player_moves[game.turn]:
                    win.blit(MENU_FONT_S.render(str(piece_labels[i][j]),True,bottom_color),MENU_FONT_S.render(str(piece_labels[i][j]),True,bottom_color).get_rect(center=(j*100-50.1,i*100-50.1)))
                    win.blit(MENU_FONT_S.render(str(piece_labels[i][j]),True,top_color),MENU_FONT_S.render(str(piece_labels[i][j]),True,top_color).get_rect(center=(j*100-50,i*100-50)))
                    

    def collect_tiles(self, turn, initializing: bool):
        if initializing:
            for i in range(6):
                xpos = random.randrange(1,10)
                ypos = random.randrange(1,13)
                while self.available_pieces[xpos][ypos] == 0:
                    xpos = random.randrange(1,10)
                    ypos = random.randrange(1,13)
                self.player_moves[turn].append([xpos,ypos])
                self.available_pieces[xpos][ypos] = 0
        else:
            xpos = random.randrange(1,10)
            ypos = random.randrange(1,13)
            while self.available_pieces[xpos][ypos] == 0:
                xpos = random.randrange(1,10)
                ypos = random.randrange(1,13)
            self.player_moves[turn].append([xpos,ypos])
            self.available_pieces[xpos][ypos] = 0

    def place_tile(self, win, x, y):
        #when a spot is clicked and all of the companies have been placed, the move is taken away from the player even though it should stay with the player when they try to place a piece next to another unclaimed piece
        if self.available_companies[0] == 0 and self.available_companies[1] == 0 and self.available_companies[2] == 0 and self.available_companies[3] == 0 and self.available_companies[4] == 0 and self.available_companies[5] == 0 and self.available_companies[6] == 0:
            if x >= 0 and x < 1200:
                if self.board[(y//100)+1][(x//100)+1] == 0 and self.board[(y//100)][(x//100)+1] == 2 and self.board[(y//100)+2][(x//100)+1] <= 2 and self.board[(y//100)+1][(x//100)] <= 2 and self.board[(y//100)+1][(x//100)+2] <= 2:
                    self.create = True
                    self.skip_two = True
                if self.board[(y//100)+1][(x//100)+1] == 0 and self.board[(y//100)+2][(x//100)+1] == 2 and self.board[(y//100)][(x//100)+1] <= 2 and self.board[(y//100)+1][(x//100)] <= 2 and self.board[(y//100)+1][(x//100)+2] <= 2:
                    self.create = True
                    self.skip_two = True
                if self.board[(y//100)+1][(x//100)+1] == 0 and self.board[(y//100)+1][(x//100)] == 2 and self.board[(y//100)][(x//100)+1] <= 2 and self.board[(y//100)+2][(x//100)+1] <= 2 and self.board[(y//100)+1][(x//100)+2] <= 2:
                    self.create = True
                    self.skip_two = True
                if self.board[(y//100)+1][(x//100)+1] == 0 and self.board[(y//100)+1][(x//100)+2] == 2 and  self.board[(y//100)+2][(x//100)+1] <= 2 and self.board[(y//100)+1][(x//100)] <= 2 and self.board[(y//100)][(x//100)+1] <= 2:
                    self.create = True
                    self.skip_two = True
        if x >= 0 and x < 1200 and self.board[(y//100)+1][(x//100)+1] == 0 and self.create == False:
            #used to have 'or self.skip'
            self.board[(y//100)+1][(x//100)+1] = 2
            pygame.draw.rect(win, GREY, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
            pygame.draw.rect(win, LIGHTISH_GREY, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            self.create = False
        else:
            self.skip = True
        self.create = False
        self.direction_x = []
        self.direction_y = []

    def check_if_tile_forms_company(self, x, y):
        if x >= 0 and x < 1200:
            self.skip = False
            if self.board[(y//100)+1][(x//100)+1] == self.board[(y//100)][(x//100)+1] and self.board[(y//100)][(x//100)+1] == 2:
                self.create = True
                self.direction_x.append(0)
                self.direction_y.append(-1)
                pygame.display.update()
            if self.board[(y//100)+1][(x//100)+1] == self.board[(y//100)+2][(x//100)+1] and self.board[(y//100)+2][(x//100)+1] == 2:
                self.create = True
                self.direction_x.append(0)
                self.direction_y.append(1)
                pygame.display.update()
            if self.board[(y//100)+1][(x//100)+1] == self.board[(y//100)+1][(x//100)] and self.board[(y//100)+1][(x//100)] == 2:
                self.create = True
                self.direction_x.append(-1)
                self.direction_y.append(0)
                pygame.display.update()
            if self.board[(y//100)+1][(x//100)+1] == self.board[(y//100)+1][(x//100)+2] and self.board[(y//100)+1][(x//100)+2] == 2:
                self.create = True
                self.direction_x.append(1)
                self.direction_y.append(0)
                pygame.display.update()
            self.skip = False
        

    def choose_company(self, g_button, r_button, b_button, y_button, p_button, t_button, o_button):
        if g_button:
            return 5
        if b_button:
            return 4
        if r_button:
            return 3
        if y_button:
            return 6
        if t_button:
            return 7
        if o_button:
            return 9
        if p_button:
            return 8
        return "error"
        
    def create_company(self, win, x, y, color):
        if x >= 0 and x < 1200:
            #prompt user for their company choice
            
            '''self.skip = False
            for i in range(len(self.direction_x)):
                for j in range(len(self.initial_moves)):
                    if [(y//100)+self.direction_y[i]+1,(x//100)+self.direction_x[i]+1] == self.initial_moves[j][0:2] and self.initial_moves[j][2] != 0:
                        for z in range(len(self.initial_moves)):
                            if self.initial_moves[z][2] == self.initial_moves[j][2]:
                                print(x//100,self.initial_moves[z][1],(x//100)+1-self.initial_moves[z][1])
                                print(y//100,self.initial_moves[z][0],(y//100)+1-self.initial_moves[z][0])
                                for row in range(ROWS+2):
                                        print(self.board[row])
                                self.direction_x.append((x//100)-self.initial_moves[z][1])
                                self.direction_y.append((y//100)-self.initial_moves[z][0])
                        self.skip = True
                    if self.skip:
                        break
                if self.skip:
                    break
            self.skip = False'''
            


            if color == 3:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 3
                pygame.draw.rect(win, RED, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_RED, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 3
                    pygame.draw.rect(win, RED, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_RED, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[0] = 0
                if self.total_stocks[0] != 0:
                    self.owned_stocks[self.turn][0] += 1
                    self.total_stocks[0] -= 1

            if color == 4:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 4
                pygame.draw.rect(win, BLUE, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 4
                    pygame.draw.rect(win, BLUE, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[1] = 0
                if self.total_stocks[1] != 0:
                    self.owned_stocks[self.turn][1] += 1
                    self.total_stocks[1] -= 1

            if color == 5:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 5
                pygame.draw.rect(win, GREEN, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 5
                    pygame.draw.rect(win, GREEN, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[2] = 0
                if self.total_stocks[2] != 0:
                    self.owned_stocks[self.turn][2] += 1
                    self.total_stocks[2] -= 1

            if color == 6:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 6
                pygame.draw.rect(win, YELLOW, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 6
                    pygame.draw.rect(win, YELLOW, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[3] = 0
                if self.total_stocks[3] != 0:
                    self.owned_stocks[self.turn][3] += 1
                    self.total_stocks[3] -= 1

            if color == 7:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 7
                pygame.draw.rect(win, TEAL, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 7
                    pygame.draw.rect(win, TEAL, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[4] = 0
                if self.total_stocks[4] != 0:
                    self.owned_stocks[self.turn][4] += 1
                    self.total_stocks[4] -= 1

            if color == 8:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 8
                pygame.draw.rect(win, PURPLE, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 8
                    pygame.draw.rect(win, PURPLE, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[5] = 0
                if self.total_stocks[5] != 0:
                    self.owned_stocks[self.turn][5] += 1
                    self.total_stocks[5] -= 1

            if color == 9:
                #first piece
                self.board[(y//100)+1][(x//100)+1] = 9
                pygame.draw.rect(win, ORANGE, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                #other pieces
                for i in range(len(self.direction_x)):
                    self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] = 9
                    pygame.draw.rect(win, ORANGE, ((x+6+(self.direction_x[i]*100)),(y+6+(self.direction_y[i]*100)),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11+(self.direction_x[i]*100)),(y+11+(self.direction_y[i]*100)),PIECE_SIZE-10,PIECE_SIZE-10))
                self.available_companies[6] = 0
                if self.total_stocks[6] != 0:
                    self.owned_stocks[self.turn][6] += 1
                    self.total_stocks[6] -= 1

            self.direction_x, self.direction_y = [], []
            self.create = False
            self.company_not_chosen = True

    def check_if_tile_adds_to_company(self, x, y):
        if x >= 0 and x < 1200 and self.board[(y//100)+1][(x//100)+1] == 2:
             if self.board[(y//100)][(x//100)+1] > 2:
                self.adding = True
                self.direction_x.append(0)
                self.direction_y.append(-1)
             if self.board[(y//100)+2][(x//100)+1] > 2:
                self.adding = True
                self.direction_x.append(0)
                self.direction_y.append(1)
             if self.board[(y//100)+1][(x//100)] > 2:
                self.adding = True
                self.direction_x.append(-1)
                self.direction_y.append(0)
             if self.board[(y//100)+1][(x//100)+2] > 2:
                self.adding = True
                self.direction_x.append(1)
                self.direction_y.append(0)


    def add_tile_to_company(self, win, x, y):
        self.skip = True
        for i in range(len(self.direction_x)):
            self.board[(y//100)+1][(x//100)+1] = self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1]
            #If it's red
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 3:
                pygame.draw.rect(win, RED, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_RED, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            #If it's blue
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 4:
                pygame.draw.rect(win, BLUE, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            #If it's green
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 5:
                pygame.draw.rect(win, GREEN, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 6:
                pygame.draw.rect(win, YELLOW, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 7:
                pygame.draw.rect(win, TEAL, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 8:
                pygame.draw.rect(win, PURPLE, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+self.direction_y[i]+1][(x//100)+self.direction_x[i]+1] == 9:
                pygame.draw.rect(win, ORANGE, ((x+6),(y+6),PIECE_SIZE,PIECE_SIZE))
                pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            #If there is an unchained tile next to the tile about to be added
            if self.board[(y//100)][(x//100)+1] == 2:
                self.board[(y//100)][(x//100)+1] = self.board[(y//100)+1][(x//100)+1]
                if self.board[(y//100)+1][(x//100)+1] == 3:
                    pygame.draw.rect(win, RED, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_RED, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 4:
                    pygame.draw.rect(win, BLUE, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 5:
                    pygame.draw.rect(win, GREEN, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 6:
                    pygame.draw.rect(win, YELLOW, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 7:
                    pygame.draw.rect(win, TEAL, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 8:
                    pygame.draw.rect(win, PURPLE, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 9:
                    pygame.draw.rect(win, ORANGE, ((x+6),(y+6-100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11),(y+11-100),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+2][(x//100)+1] == 2:
                self.board[(y//100)+2][(x//100)+1] = self.board[(y//100)+1][(x//100)+1]
                if self.board[(y//100)+1][(x//100)+1] == 3:
                    pygame.draw.rect(win, RED, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_RED, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 4:
                    pygame.draw.rect(win, BLUE, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 5:
                    pygame.draw.rect(win, GREEN, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 6:
                    pygame.draw.rect(win, YELLOW, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 7:
                    pygame.draw.rect(win, TEAL, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 8:
                    pygame.draw.rect(win, PURPLE, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 9:
                    pygame.draw.rect(win, ORANGE, ((x+6),(y+6+100),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11),(y+11+100),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+1][(x//100)] == 2:
                self.board[(y//100)+1][(x//100)] = self.board[(y//100)+1][(x//100)+1]
                if self.board[(y//100)+1][(x//100)+1] == 3:
                    pygame.draw.rect(win, RED, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_RED, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 4:
                    pygame.draw.rect(win, BLUE, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 5:
                    pygame.draw.rect(win, GREEN, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 6:
                    pygame.draw.rect(win, YELLOW, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 7:
                    pygame.draw.rect(win, TEAL, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 8:
                    pygame.draw.rect(win, PURPLE, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 9:
                    pygame.draw.rect(win, ORANGE, ((x+6-100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11-100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            if self.board[(y//100)+1][(x//100)+2] == 2:
                self.board[(y//100)+1][(x//100)+2] = self.board[(y//100)+1][(x//100)+1]
                if self.board[(y//100)+1][(x//100)+1] == 3:
                    pygame.draw.rect(win, RED, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_RED, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 4:
                    pygame.draw.rect(win, BLUE, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_BLUE, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 5:
                    pygame.draw.rect(win, GREEN, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_GREEN, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 6:
                    pygame.draw.rect(win, YELLOW, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_YELLOW, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 7:
                    pygame.draw.rect(win, TEAL, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_TEAL, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 8:
                    pygame.draw.rect(win, PURPLE, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_PURPLE, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
                if self.board[(y//100)+1][(x//100)+1] == 9:
                    pygame.draw.rect(win, ORANGE, ((x+6+100),(y+6),PIECE_SIZE,PIECE_SIZE))
                    pygame.draw.rect(win, LIGHTISH_ORANGE, ((x+11+100),(y+11),PIECE_SIZE-10,PIECE_SIZE-10))
            
        self.adding = False
        self.direction_x, self.direction_y = [], []
        self.skip = False
        
    def check_if_tile_merges_chains(self, x, y):
        if x > 0 and x < 1200:
            if self.board[(y//100)+1][(x//100)+1] < self.board[(y//100)+1][(x//100)+2]:
                self.direction_x.append(1)
                self.direction_y.append(0)
                if self.board[(y//100)+1][(x//100)+2] != self.board[(y//100)+1][(x//100)] and self.board[(y//100)+1][(x//100)] > 2:
                    self.direction_x.append(-1)
                    self.direction_y.append(0)
                if self.board[(y//100)+1][(x//100)+2] != self.board[(y//100)][(x//100+1)] and self.board[(y//100)][(x//100+1)] > 2:
                    self.direction_x.append(0)
                    self.direction_y.append(-1)
                if self.board[(y//100)+1][(x//100)+2] != self.board[(y//100)+2][(x//100+1)] and self.board[(y//100)+2][(x//100+1)] > 2:
                    self.direction_x.append(0)
                    self.direction_y.append(1)
                if len(self.direction_x) > 1:
                    return True
                return False
            if self.board[(y//100)+1][(x//100)+1] < self.board[(y//100)+1][(x//100)]:
                self.direction_x.append(-1)
                self.direction_y.append(0)
                if self.board[(y//100)+1][(x//100)] != self.board[(y//100)][(x//100)+1] and self.board[(y//100)][(x//100)+1] > 2:
                    self.direction_x.append(0)
                    self.direction_y.append(-1)
                if self.board[(y//100)+1][(x//100)] != self.board[(y//100+2)][(x//100)+1] and self.board[(y//100)+2][(x//100)+1] > 2:
                    self.direction_x.append(0)
                    self.direction_y.append(1)
                if len(self.direction_x) > 1:
                    return True
                return False
            if self.board[(y//100)+1][(x//100)+1] < self.board[(y//100)][(x//100)+1]:
                self.direction_x.append(0)
                self.direction_y.append(-1)
                if self.board[(y//100)][(x//100)+1] != self.board[(y//100+2)][(x//100)+1] and self.board[(y//100)+2][(x//100)+1] > 2:
                    self.direction_x.append(0)
                    self.direction_y.append(1)
                if len(self.direction_x) > 1:
                        return True
                return False

    def count_tiles(self):
        self.number_of_tiles = [0,0,0,0,0,0,0]
        for row in range(ROWS+2):
            for col in range(COLS+2):
                if self.board[row][col] == 3:
                    self.number_of_tiles[0] += 1
                if self.board[row][col] == 4:
                    self.number_of_tiles[1] += 1
                if self.board[row][col] == 5:
                    self.number_of_tiles[2] += 1
                if self.board[row][col] == 6:
                    self.number_of_tiles[3] += 1
                if self.board[row][col] == 7:
                    self.number_of_tiles[4] += 1
                if self.board[row][col] == 8:
                    self.number_of_tiles[5] += 1
                if self.board[row][col] == 9:
                    self.number_of_tiles[6] += 1
        #Also, updating prices
        for i in range(2):
            if self.number_of_tiles[i] == 0:
                self.stock_prices[i] = 0
                self.first_bonus[i] = 0
            if self.number_of_tiles[i] == 2:
                self.stock_prices[i] = 200
                self.first_bonus[i] = 2000
            if self.number_of_tiles[i] == 3:
                self.stock_prices[i] = 300
                self.first_bonus[i] = 3000
            if self.number_of_tiles[i] == 4:
                self.stock_prices[i] = 400
                self.first_bonus[i] = 4000
            if self.number_of_tiles[i] == 5:
                self.stock_prices[i] = 500
                self.first_bonus[i] = 5000
            if self.number_of_tiles[i] >= 6 and self.number_of_tiles[i] <= 10:
                self.stock_prices[i] = 600
                self.first_bonus[i] = 6000
            if self.number_of_tiles[i] >= 11 and self.number_of_tiles[i] <= 20:
                self.stock_prices[i] = 700
                self.first_bonus[i] = 7000
            if self.number_of_tiles[i] >= 21 and self.number_of_tiles[i] <= 30:
                self.stock_prices[i] = 800
                self.first_bonus[i] = 8000
            if self.number_of_tiles[i] >= 31 and self.number_of_tiles[i] <= 40:
                self.stock_prices[i] = 900
                self.first_bonus[i] = 9000
            if self.number_of_tiles[i] >= 41:
                self.stock_prices[i] = 1000
                self.first_bonus[i] = 10000
            self.second_bonus[i] = self.first_bonus[i]//2
        for i in range(2,5):
            if self.number_of_tiles[i] == 0:
                self.stock_prices[i] = 0
                self.first_bonus[i] = 0
            if self.number_of_tiles[i] == 2:
                self.stock_prices[i] = 300
                self.first_bonus[i] = 3000
            if self.number_of_tiles[i] == 3:
                self.stock_prices[i] = 400
                self.first_bonus[i] = 4000
            if self.number_of_tiles[i] == 4:
                self.stock_prices[i] = 500
                self.first_bonus[i] = 5000
            if self.number_of_tiles[i] == 5:
                self.stock_prices[i] = 600
                self.first_bonus[i] = 6000
            if self.number_of_tiles[i] >= 6 and self.number_of_tiles[i] <= 10:
                self.stock_prices[i] = 700
                self.first_bonus[i] = 7000
            if self.number_of_tiles[i] >= 11 and self.number_of_tiles[i] <= 20:
                self.stock_prices[i] = 800
                self.first_bonus[i] = 8000
            if self.number_of_tiles[i] >= 21 and self.number_of_tiles[i] <= 30:
                self.stock_prices[i] = 900
                self.first_bonus[i] = 9000
            if self.number_of_tiles[i] >= 31 and self.number_of_tiles[i] <= 40:
                self.stock_prices[i] = 1000
                self.first_bonus[i] = 10000
            if self.number_of_tiles[i] >= 41:
                self.stock_prices[i] = 1100
                self.first_bonus[i] = 11000
            self.second_bonus[i] = self.first_bonus[i]//2
        for i in range(5,7):
            if self.number_of_tiles[i] == 0:
                self.stock_prices[i] = 0
                self.first_bonus[i] = 0
            if self.number_of_tiles[i] == 2:
                self.stock_prices[i] = 400
                self.first_bonus[i] = 4000
            if self.number_of_tiles[i] == 3:
                self.stock_prices[i] = 500
                self.first_bonus[i] = 5000
            if self.number_of_tiles[i] == 4:
                self.stock_prices[i] = 600
                self.first_bonus[i] = 6000
            if self.number_of_tiles[i] == 5:
                self.stock_prices[i] = 700
                self.first_bonus[i] = 7000
            if self.number_of_tiles[i] >= 6 and self.number_of_tiles[i] <= 10:
                self.stock_prices[i] = 800
                self.first_bonus[i] = 8000
            if self.number_of_tiles[i] >= 11 and self.number_of_tiles[i] <= 20:
                self.stock_prices[i] = 900
                self.first_bonus[i] = 9000
            if self.number_of_tiles[i] >= 21 and self.number_of_tiles[i] <= 30:
                self.stock_prices[i] = 1000
                self.first_bonus[i] = 10000
            if self.number_of_tiles[i] >= 31 and self.number_of_tiles[i] <= 40:
                self.stock_prices[i] = 1100
                self.first_bonus[i] = 11000
            if self.number_of_tiles[i] >= 41:
                self.stock_prices[i] = 1200
                self.first_bonus[i] = 12000
            self.second_bonus[i] = self.first_bonus[i]//2

    def check_for_tied_tiles(self, merging_tiles, win, board):
        self.tied_companies = []
        for i in range(len(merging_tiles)):
            if merging_tiles[i] == self.number_of_tiles[self.biggest_company-3]:
                self.tied_companies.append(i+3)
        if len(self.tied_companies) > 1:
            board.draw_for_merge(WIN)
            self.skip = True
            self.companies_temp = self.available_companies
            self.available_companies = [0,0,0,0,0,0,0]
            for z in range(len(self.tied_companies)):
                for i in range(len(self.available_companies)):
                    if self.tied_companies[z] == (i+3):
                        self.available_companies[i] = self.tied_companies[z]                    
            self.company_not_chosen = True
            return True
        return False
        
    def preparing_merge(self,x,y,win,board):
        safe = 0
        self.merging_values = []
        merging_company_tiles = [0,0,0,0,0,0,0]
        self.biggest_company = 0
        for i in range(len(self.direction_x)):
            self.merging_values.append(self.board[(y//100)+1+self.direction_y[i]][(x//100)+1+self.direction_x[i]])
        self.merging_values = list(set(self.merging_values))
        self.count_tiles()
        for i in range(len(merging_company_tiles)):
            if (i+3) in self.merging_values:
                merging_company_tiles[i] = self.number_of_tiles[i]
                if merging_company_tiles[i] > 10:
                    safe += 1
        if safe > 1:
            self.board[(y//100)+1][(x//100)+1] = 0
            pygame.draw.rect(win, LIGHT_BROWN, (((x//100)*100+6),((y//100)*100+6),PIECE_SIZE,PIECE_SIZE))
            self.player_moves[self.turn].append([(y//100)+1,(x//100)+1])
            self.skip_two = True
            return False
        self.biggest_company = merging_company_tiles.index(max(merging_company_tiles))
        self.biggest_company += 3
        return self.check_for_tied_tiles(merging_company_tiles,win,board)

    def merge_chains(self, win):
        self.merging_values.remove(self.biggest_company)
        if self.skip:
            self.available_companies = self.companies_temp
            self.skip = False
        handle_merge(win,self)
        for i in range(len(self.merging_values)):
            self.available_companies[self.merging_values[i]-3] = self.merging_values[i]
            for row in range(ROWS+2):
                for col in range(COLS+2):
                    if self.board[row][col] == self.merging_values[i]:
                        self.board[row][col] = self.biggest_company
                        if self.biggest_company == 3:
                            pygame.draw.rect(win, RED, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_RED, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))
                        if self.biggest_company == 4:
                            pygame.draw.rect(win, BLUE, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_BLUE, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))
                        if self.biggest_company == 5:
                            pygame.draw.rect(win, GREEN, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_GREEN, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))
                        if self.biggest_company == 6:
                            pygame.draw.rect(win, YELLOW, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_YELLOW, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))
                        if self.biggest_company == 7:
                            pygame.draw.rect(win, TEAL, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_TEAL, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))
                        if self.biggest_company == 8:
                            pygame.draw.rect(win, PURPLE, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_PURPLE, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))
                        if self.biggest_company == 9:
                            pygame.draw.rect(win, ORANGE, (((col-1)*100+6),((row-1)*100+6),PIECE_SIZE,PIECE_SIZE))
                            pygame.draw.rect(win, LIGHTISH_ORANGE, (((col-1)*100+11),((row-1)*100+11),PIECE_SIZE-10,PIECE_SIZE-10))


        self.direction_y, self.direction_x = [], []
        self.count_tiles()
   
pygame.init()
MENU_FONT = pygame.font.SysFont('imprintshadow', 100)
MENU_FONT_S = pygame.font.SysFont('imprintshadow', 50)
MENU_FONT_M = pygame.font.SysFont('imprintshadow', 75)
MENU_FONT_lilS = pygame.font.SysFont('imprintshadow', 40)
MENU_FONT_XlilS = pygame.font.SysFont('imprintshadow',25)
MENU_FONT_XS = pygame.font.SysFont('imprintshadow', 30)
MENU_FONT_XXS = pygame.font.SysFont('imprintshadow', 20)

def main(win, player_names, available_pieces, moves, piece_labels, saved_game: bool):
    NEXT = Menu_Button(1200,820,"NEXT TURN", MENU_FONT_XS, GREY, LIGHTISH_GREY,300,80)
    VIEW_PIECES = Menu_Button(1250,500,"PIECES", MENU_FONT_XS, GREY, LIGHTISH_GREY,200,80)
    GAME_OVER = Menu_Button(1250,600, "END GAME", MENU_FONT_XS, GREY, LIGHTISH_GREY, 200,80)
    MY_INFO = Menu_Button(1250,400,"MY INFO", MENU_FONT_XS, GREY, LIGHTISH_GREY, 200,80)
    PURCHASE = Menu_Button(1250,300,"PURCHASE", MENU_FONT_XS, GREY, LIGHTISH_GREY,200,80)
    SAVE_GAME = Menu_Button(1417.5,155,"SAVE", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 70,50)
    game = Game(player_names, available_pieces, moves)
    board = Board(game)
    board.draw_squares(win)
    board.updating_buttons(win)
    pygame.display.set_caption('Acquire')
    if saved_game:
        with open("saved_game_acquire.txt","r") as saved:
            lines = saved.readlines()
            reminding = literal_eval(lines[16].partition(":")[-1])
            total_purchases = literal_eval(lines[15].partition(":")[-1])
            game.round = literal_eval(lines[17].partition(":")[-1])
            game.discarded_pieces = literal_eval(lines[12].partition(":")[-1])
            game.piece_discarded = literal_eval(lines[11].partition(":")[-1])
            game.piece_drawn = literal_eval(lines[10].partition(":")[-1])
            game.piece_placed = literal_eval(lines[9].partition(":")[-1])
            game.player_moves = literal_eval(lines[8].partition(":")[-1])
            game.available_companies = literal_eval(lines[6].partition(":")[-1])
            game.total_stocks = literal_eval(lines[5].partition(":")[-1])
            game.owned_stocks = literal_eval(lines[4].partition(":")[-1])
            game.balances = literal_eval(lines[3].partition(":")[-1])
            game.board = literal_eval(lines[2].partition(":")[-1])
            game.turn = literal_eval(lines[1].partition(":")[-1])
        load_board(win,game,piece_labels)
    else:
        reminding = False
        total_purchases = 0
        for i in range(len(moves)):
            game.skip = True
            game.place_tile(win,(moves[i][1]-1)*100, (moves[i][0]-1)*100)
            game.skip = False

        for i in range(len(player_names)):
            game.collect_tiles(i,True)

    game.draw_labels(win,piece_labels)
    run = True
    clock = pygame.time.Clock()
    turn_round = MENU_FONT_XS.render("Round " + str(game.round),True,BLACK)
    turn_round_rect = turn_round.get_rect(center=(1350,775))
    whose_turn = MENU_FONT_XS.render(player_names[game.turn],True,BLACK)
    whose_turn_rect = whose_turn.get_rect(center=(1350,250))
    win.blit(whose_turn,whose_turn_rect)
    win.blit(turn_round,turn_round_rect)
    while run:
        MY_INFO.draw_menu_button(win)
        GAME_OVER.draw_menu_button(win)
        NEXT.draw_menu_button(win)
        VIEW_PIECES.draw_menu_button(win)
        PURCHASE.draw_menu_button(win)
        SAVE_GAME.draw_menu_button(win)
        x,y = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEXT.check_for_click():
                    if game.piece_placed:
                        if len(game.player_moves[game.turn]) == 6:
                            total_purchases = 0
                            whose_turn.fill(ANTIQUE_WHITE)
                            if game.turn == len(player_names)-1:
                                game.turn = 0
                                game.round += 1
                                turn_round.fill(ANTIQUE_WHITE)
                                win.blit(turn_round,turn_round_rect)
                                turn_round = MENU_FONT_XS.render("Round " + str(game.round),True,BLACK)
                                turn_round_rect = turn_round.get_rect(center=(1350,775))
                                win.blit(turn_round,turn_round_rect)
                            else:
                                game.turn += 1
                            whose_turn.fill(ANTIQUE_WHITE)
                            win.blit(whose_turn,whose_turn_rect)
                            #big names leak onto the board, make font smaller for big names
                            whose_turn = MENU_FONT_XS.render(player_names[game.turn],True,BLACK)
                            whose_turn_rect = whose_turn.get_rect(center=(1350,250))
                            win.blit(whose_turn,whose_turn_rect)
                            game.piece_placed = False
                            game.piece_drawn = False
                            game.piece_discarded = False
                            if reminding:
                                reminder.fill(ANTIQUE_WHITE)
                                reminder_rect = reminder.get_rect(center=(1350,800))
                                win.blit(reminder, reminder_rect)
                                reminding = False
                        else:
                            reminder = MENU_FONT_XXS.render("Don't forget to draw...",True,LIGHTISH_RED)
                            reminder_rect = reminder.get_rect(center=(1350,800))
                            win.blit(reminder, reminder_rect)
                            reminding = True
                    else:
                        reminder = MENU_FONT_XXS.render("Remember to place a piece",True,LIGHTISH_RED)
                        reminder_rect = reminder.get_rect(center=(1350,800))
                        win.blit(reminder, reminder_rect)
                        reminding = True
                if VIEW_PIECES.check_for_click():
                    view_pieces(win,game,piece_labels)
                    win.blit(turn_round,turn_round_rect)
                if GAME_OVER.check_for_click():
                    game.count_tiles()
                    if max(game.number_of_tiles) > 40:
                        game_over(win,game)
                        run = False
                if MY_INFO.check_for_click():
                    view_my_info(win,game)
                    win.blit(turn_round,turn_round_rect)
                if PURCHASE.check_for_click():
                    total_purchases = purchase_stocks(win,game,total_purchases)
                    win.blit(turn_round,turn_round_rect)
                if SAVE_GAME.check_for_click():
                    with open("saved_game_acquire.txt","w") as save:
                        save.write(f"Player Names:{player_names}\n")
                        save.write(f"The turn:{game.turn}\n")
                        save.write(f"The board:{game.board}\n")
                        save.write(f"The balances:{game.balances}\n")
                        save.write(f"Stocks owned:{game.owned_stocks}\n")
                        save.write(f"Stocks remaining:{game.total_stocks}\n")
                        save.write(f"Companies Available:{game.available_companies}\n")
                        save.write(f"Available Pieces:{game.available_pieces}\n")
                        save.write(f"Player's moves:{game.player_moves}\n")
                        save.write(f"Tile Placed?:{game.piece_placed}\n")
                        save.write(f"Tile Drawn?:{game.piece_drawn}\n")
                        save.write(f"Piece Discarded?:{game.piece_discarded}\n")
                        save.write(f"Discared Pieces:{game.discarded_pieces}\n")
                        save.write(f"Initial Moves:{game.initial_moves}\n")
                        save.write(f"Piece Labels:{piece_labels}\n")
                        save.write(f"Total Purchases:{total_purchases}\n")
                        save.write(f"Reminding?:{reminding}\n")
                        save.write(f"The round:{game.round}\n")

                    #save game!
                    #with open("saved_game_acquire.txt","r") as save:
                        #print(save.read())
                if [(y//100)+1,(x//100)+1] in game.player_moves[game.turn] and not game.piece_placed:
                    game.place_tile(win, (x//100)*100, (y//100*100))
                    if not game.skip_two:
                        game.skip_two = False
                        game.player_moves[game.turn].remove([(y//100)+1,(x//100)+1])
                        game.piece_placed = True
                        game.draw_labels(win, piece_labels)
                        if game.check_if_tile_merges_chains(x,y):
                            if game.preparing_merge(x,y, win, board):
                                while game.company_not_chosen:
                                    pygame.display.update()
                                    board.updating_buttons(win)
                                    for event in pygame.event.get():
                                        board.draw_for_merge(win)
                                        if event.type == pygame.QUIT:
                                            run = False
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            choice_x,choice_y = pygame.mouse.get_pos()
                                            b_button = board.blue_button.check_for_click(choice_x,choice_y)
                                            g_button = board.green_button.check_for_click(choice_x,choice_y)
                                            r_button = board.red_button.check_for_click(choice_x,choice_y)
                                            y_button = board.yellow_button.check_for_click(choice_x,choice_y)
                                            t_button = board.teal_button.check_for_click(choice_x,choice_y)
                                            o_button = board.orange_button.check_for_click(choice_x,choice_y)
                                            p_button = board.purple_button.check_for_click(choice_x,choice_y)
                                            if r_button == True or b_button == True or g_button == True or y_button == True or t_button == True or p_button == True or o_button == True:
                                                game.company_not_chosen = False
                                game.biggest_company = game.choose_company(g_button, r_button, b_button, y_button, p_button, t_button, o_button)
                                game.draw_labels(win, piece_labels)
                            if not game.skip_two:
                                game.merge_chains(win)
                            game.skip_two = False
                            game.draw_labels(win, piece_labels)
                            game.company_not_chosen = True
                        game.check_if_tile_adds_to_company(x,y)
                        if game.adding and game.skip == False:
                            game.add_tile_to_company(win, (x//100)*100, (y//100)*100)
                            game.draw_labels(win, piece_labels)
                        game.check_if_tile_forms_company(x,y)
                        if game.create and game.adding == False and game.skip == False:
                            while game.company_not_chosen:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        run = False
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        choice_x,choice_y = pygame.mouse.get_pos()
                                        b_button = board.blue_button.check_for_click(choice_x,choice_y)
                                        g_button = board.green_button.check_for_click(choice_x,choice_y)
                                        r_button = board.red_button.check_for_click(choice_x,choice_y)
                                        y_button = board.yellow_button.check_for_click(choice_x,choice_y)
                                        t_button = board.teal_button.check_for_click(choice_x,choice_y)
                                        o_button = board.orange_button.check_for_click(choice_x,choice_y)
                                        p_button = board.purple_button.check_for_click(choice_x,choice_y)
                                        if r_button == True or b_button == True or g_button == True or y_button == True or t_button == True or p_button == True or o_button == True:
                                            game.company_not_chosen = False
                            choice = game.choose_company(g_button, r_button, b_button, y_button, p_button, t_button, o_button)
                            game.create_company(win,(x//100)*100,(y//100*100), choice)
                            game.draw_labels(win, piece_labels)
                            game.count_tiles()
                    
        game.skip_two = False           
        GAME_OVER.update_menu_button(win,x,y)
        NEXT.update_menu_button(win,x,y)
        VIEW_PIECES.update_menu_button(win,x,y)
        MY_INFO.update_menu_button(win,x,y)
        PURCHASE.update_menu_button(win,x,y)
        SAVE_GAME.update_menu_button(win,x,y)
        game.skip = False
        pygame.display.update()
        board.updating_buttons(win)


    pygame.quit()
    sys.exit()


def main_menu(win):
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption('Main Menu')
    PLAY = Menu_Button(525,375,"PLAY",MENU_FONT,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH*1.5,MENU_BUTTON_HEIGHT-30)
    LOAD = Menu_Button(525,500,"LOAD", MENU_FONT,GREY,LIGHTISH_GREY, MENU_BUTTON_WIDTH*1.5, MENU_BUTTON_HEIGHT-30)
    RULES = Menu_Button(525,625,"RULES",MENU_FONT,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH*1.5,MENU_BUTTON_HEIGHT-30)
    QUIT = Menu_Button(525,750,"QUIT",MENU_FONT,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH*1.5,MENU_BUTTON_HEIGHT-30)
    #LOGO = pygame.image.load("Acquire-logo-3.jpg").convert()
    while run:

        win.fill(ANTIQUE_WHITE)
        pygame.draw.rect(win,BLACK,(350,10,800,880),10)
        pygame.draw.rect(win,GREY,(400,121,700,213))
        #win.blit(LOGO,(404,125))
        RULES.draw_menu_button(win)
        PLAY.draw_menu_button(win)
        QUIT.draw_menu_button(win)
        LOAD.draw_menu_button(win)
        x,y = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT.check_for_click():
                    pygame.quit()
                    sys.exit()
                if PLAY.check_for_click():
                    setup(win)
                if RULES.check_for_click():
                    pass
                if LOAD.check_for_click() and exists("saved_game_acquire.txt"):
                    with open("saved_game_acquire.txt","r") as saved:
                        lines = saved.readlines()
                        turn_order = literal_eval(lines[0].partition(":")[-1])
                        available_pieces = literal_eval(lines[7].partition(":")[-1])
                        moves = literal_eval(lines[13].partition(":")[-1])
                        piece_labels = literal_eval(lines[14].partition(":")[-1])
                        main(win, turn_order, available_pieces, moves, piece_labels, True)

        
        RULES.update_menu_button(win,x,y)
        QUIT.update_menu_button(win,x,y)
        PLAY.update_menu_button(win,x,y)
        LOAD.update_menu_button(win,x,y)

        pygame.display.update()

def setup(win):
    pygame.display.set_caption('Setup')
    running = True
    clock = pygame.time.Clock()
    BACK = Menu_Button(0,0,"BACK",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-40,MENU_BUTTON_HEIGHT-40)
    LETSGO = Menu_Button(600,570,"GO",MENU_FONT,GREY,LIGHTISH_GREEN,MENU_BUTTON_WIDTH,MENU_BUTTON_HEIGHT)
    CUSTOM_COMPS = Menu_Button(300,400,"CUSTOMIZE COMPANY NAMES",MENU_FONT_S,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH*3,MENU_BUTTON_HEIGHT)
    PICK_NAMES = Menu_Button(575,260,"PICK NAMES",MENU_FONT_S,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH+50,MENU_BUTTON_HEIGHT-30)
    TWO = Toggle_Button(500,150,"2",MENU_FONT,BLUE,LIGHTISH_BLUE,100,100)
    THREE = Toggle_Button(600,150,"3",MENU_FONT,BLUE,LIGHTISH_BLUE,100,100)
    FOUR = Toggle_Button(700,150,"4",MENU_FONT,BLUE,LIGHTISH_BLUE,100,100)
    FIVE = Toggle_Button(800,150,"5",MENU_FONT,BLUE,LIGHTISH_BLUE,100,100)
    SIX = Toggle_Button(900,150,"6",MENU_FONT,BLUE,LIGHTISH_BLUE,100,100)
    player_selection = [0,0,0,0,0]
    c_names = ["","","","","","",""]
    win.fill(ANTIQUE_WHITE)
    player_names = []
    while running:
        win.blit(MENU_FONT_M.render("Number of Players",True,BLACK),MENU_FONT_M.render("Number of Players",True,BLACK).get_rect(center=(750,100)))
        CUSTOM_COMPS.draw_menu_button(win)
        PICK_NAMES.draw_menu_button(win)
        BACK.draw_menu_button(win)
        LETSGO.draw_menu_button(win)
        TWO.draw_menu_button(win)
        THREE.draw_menu_button(win)
        FOUR.draw_menu_button(win)
        FIVE.draw_menu_button(win)
        SIX.draw_menu_button(win)
        x,y = pygame.mouse.get_pos()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CUSTOM_COMPS.check_for_click():
                    c_names = [i.rstrip(" ") for i in custom_names(win,c_names)]
                    win.fill(ANTIQUE_WHITE)
                if LETSGO.check_for_click():
                    if "" in player_names or player_names == []:
                        win.blit(MENU_FONT_S.render("Please finish entering all of the player names",True,RED),MENU_FONT_S.render("Please finish entering all of the player names",True,RED).get_rect(center=(750,750)))
                    else:
                        pick_order(win,player_names)
                if BACK.check_for_click():
                    main_menu(win)
                    win.fill(ANTIQUE_WHITE)
                if TWO.check_for_click():
                    player_selection = [0,0,0,0,0]
                    player_selection[0] = 1
                    player_names = []
                if THREE.check_for_click():
                    player_selection = [0,0,0,0,0]
                    player_selection[1] = 1
                    player_names = []
                if FOUR.check_for_click():
                    player_selection = [0,0,0,0,0]
                    player_selection[2] = 1
                    player_names = []
                if FIVE.check_for_click():
                    player_selection = [0,0,0,0,0]
                    player_selection[3] = 1
                    player_names = []
                if SIX.check_for_click():
                    player_selection = [0,0,0,0,0]
                    player_selection[4] = 1
                    player_names = []
                if PICK_NAMES.check_for_click():
                    if max(player_selection) != 0:
                        if player_names == []:
                            player_names = ["" for i in range(player_selection.index(max(player_selection)) + 2)]
                        player_names = name_selection(win,(player_selection.index(max(player_selection)) + 2), player_names)
                        win.fill(ANTIQUE_WHITE)


        TWO.update_t_button(win,x,y,player_selection[0])
        THREE.update_t_button(win,x,y,player_selection[1])
        FOUR.update_t_button(win,x,y,player_selection[2])
        FIVE.update_t_button(win,x,y,player_selection[3])
        SIX.update_t_button(win,x,y,player_selection[4])
        PICK_NAMES.update_menu_button(win,x,y)
        BACK.update_menu_button(win,x,y)
        LETSGO.update_menu_button(win,x,y)
        CUSTOM_COMPS.update_menu_button(win,x,y)
        pygame.display.update()


def custom_names(win, c_names):
    pygame.display.set_caption('Custom Company Names')
    running = True
    clock = pygame.time.Clock()
    BACK = Menu_Button(0,0,"BACK",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-40,MENU_BUTTON_HEIGHT-40)
    SAVE = Menu_Button(1200,760,"SAVE",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-40,MENU_BUTTON_HEIGHT-40)
    RESET = Menu_Button(40,760,"RESET",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-25,MENU_BUTTON_HEIGHT-40)
    BLUE_CO = Toggle_Button(525,200,"BLUE",MENU_FONT_M,BLUE,LIGHTISH_BLUE, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    RED_CO = Toggle_Button(25,200,"RED",MENU_FONT_M,RED,LIGHTISH_RED, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    GREEN_CO = Toggle_Button(1025,200,"GREEN",MENU_FONT_M,GREEN,LIGHTISH_GREEN, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    YELLOW_CO = Toggle_Button(25,400,"YELLOW",MENU_FONT_M,YELLOW,LIGHTISH_YELLOW, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    PURPLE_CO = Toggle_Button(1025,400,"PURPLE",MENU_FONT_M,PURPLE,LIGHTISH_PURPLE, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    ORANGE_CO = Toggle_Button(525,600,"ORANGE",MENU_FONT_M,ORANGE,LIGHTISH_ORANGE, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    TEAL_CO = Toggle_Button(525,400,"TEAL",MENU_FONT_M,TEAL,LIGHTISH_TEAL, BUTTON_WIDTH*5, BUTTON_HEIGHT*2)
    chosen_comp = [0,0,0,0,0,0,0]
    names = c_names
    if len([i for i in names if i != ""]) > 0:
        for q in range(7):
            if names[q] != "":
                if len(names[q]) < 9:
                    if q == 0:
                        RED_CO.text_input = names[q]
                        RED_CO.font = MENU_FONT_S
                    if q == 1:
                        BLUE_CO.text_input = names[q]
                        BLUE_CO.font = MENU_FONT_S
                    if q == 2:
                        GREEN_CO.text_input = names[q]
                        GREEN_CO.font = MENU_FONT_S 
                    if q == 3:
                        YELLOW_CO.text_input = names[q]
                        YELLOW_CO.font = MENU_FONT_S
                    if q == 4:
                        TEAL_CO.text_input = names[q]
                        TEAL_CO.font = MENU_FONT_S
                    if q == 5:
                        PURPLE_CO.text_input = names[q]
                        PURPLE_CO.font = MENU_FONT_S
                    if q == 6:
                        ORANGE_CO.text_input = names[q]
                        ORANGE_CO.font = MENU_FONT_S
                else:
                    if q == 0:
                        RED_CO.text_input = names[q]
                        RED_CO.font = MENU_FONT_XS
                    if q == 1:
                        BLUE_CO.text_input = names[q]
                        BLUE_CO.font = MENU_FONT_XS
                    if q == 2:
                        GREEN_CO.text_input = names[q]
                        GREEN_CO.font = MENU_FONT_XS 
                    if q == 3:
                        YELLOW_CO.text_input = names[q]
                        YELLOW_CO.font = MENU_FONT_XS
                    if q == 4:
                        TEAL_CO.text_input = names[q]
                        TEAL_CO.font = MENU_FONT_XS
                    if q == 5:
                        PURPLE_CO.text_input = names[q]
                        PURPLE_CO.font = MENU_FONT_XS
                    if q == 6:
                        ORANGE_CO.text_input = names[q]
                        ORANGE_CO.font = MENU_FONT_XS



    name = ""
    while running:
        win.fill(ANTIQUE_WHITE)
        BACK.draw_menu_button(win)
        BLUE_CO.draw_menu_button(win)
        RED_CO.draw_menu_button(win)
        GREEN_CO.draw_menu_button(win)
        YELLOW_CO.draw_menu_button(win)
        PURPLE_CO.draw_menu_button(win)
        TEAL_CO.draw_menu_button(win)
        ORANGE_CO.draw_menu_button(win)
        SAVE.draw_menu_button(win)
        RESET.draw_menu_button(win)

        clock.tick(FPS)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                if event.key == pygame.K_TAB:
                        if 1 in chosen_comp:
                            name = ""
                            if chosen_comp[-1] == 1:
                                chosen_comp[-1] = 0
                                chosen_comp[0] = 1
                            else:
                                spot = chosen_comp.index(max(chosen_comp))
                                chosen_comp[spot] = 0
                                chosen_comp[spot + 1] = 1
                if len(name) < 14:
                    if event.key == pygame.K_q:
                        name += "Q"
                    if event.key == pygame.K_w:
                        name += "W"
                    if event.key == pygame.K_e:
                        name += "E"
                    if event.key == pygame.K_r:
                        name += "R"
                    if event.key == pygame.K_t:
                        name += "T"
                    if event.key == pygame.K_y:
                        name += "Y"
                    if event.key == pygame.K_u:
                        name += "U"
                    if event.key == pygame.K_i:
                        name += "I"
                    if event.key == pygame.K_o:
                        name += "O"
                    if event.key == pygame.K_p:
                        name += "P"
                    if event.key == pygame.K_a:
                        name += "A"
                    if event.key == pygame.K_s:
                        name += "S"
                    if event.key == pygame.K_d:
                        name += "D"
                    if event.key == pygame.K_f:
                        name += "F"
                    if event.key == pygame.K_g:
                        name += "G"
                    if event.key == pygame.K_h:
                        name += "H"
                    if event.key == pygame.K_j:
                        name += "J"
                    if event.key == pygame.K_k:
                        name += "K"
                    if event.key == pygame.K_l:
                        name += "L"
                    if event.key == pygame.K_z:
                        name += "Z"
                    if event.key == pygame.K_x:
                        name += "X"
                    if event.key == pygame.K_c:
                        name += "C"
                    if event.key == pygame.K_v:
                        name += "V"
                    if event.key == pygame.K_b:
                        name += "B"
                    if event.key == pygame.K_n:
                        name += "N"
                    if event.key == pygame.K_m:
                        name += "M"
                    if event.key == pygame.K_SPACE:
                        name += " "
                    if event.key == pygame.K_MINUS:
                        name += "-"
                    if event.key == pygame.K_QUOTE:
                        name += "'"
                    
            if chosen_comp[0]:
                names[0] = name.lstrip(" ")
                if names[0] == "":
                    RED_CO.text_input = "RED"
                    RED_CO.font = MENU_FONT_M
                elif len(names[0]) < 9:
                    RED_CO.font = MENU_FONT_S
                    RED_CO.text_input = names[0]
                elif len(names[0]) >= 9:
                    RED_CO.font = MENU_FONT_XS
                    RED_CO.text_input = names[0]

            if chosen_comp[1]:
                names[1] = name.lstrip(" ")
                if names[1] == "":
                    BLUE_CO.text_input = "BLUE"
                    BLUE_CO.font = MENU_FONT_M
                elif len(names[1]) < 9:
                    BLUE_CO.font = MENU_FONT_S
                    BLUE_CO.text_input = names[1]
                elif len(names[1]) >= 9:
                    BLUE_CO.text_input = names[1]
                    BLUE_CO.font = MENU_FONT_XS

            if chosen_comp[2]:
                names[2] = name.lstrip(" ")
                if names[2] == "":
                    GREEN_CO.text_input = "GREEN"
                    GREEN_CO.font = MENU_FONT_M
                elif len(names[2]) < 9:
                    GREEN_CO.font = MENU_FONT_S
                    GREEN_CO.text_input = names[2]
                elif len(names[2]) >= 9:
                    GREEN_CO.text_input = names[2]
                    GREEN_CO.font = MENU_FONT_XS

            if chosen_comp[3]:
                names[3] = name.lstrip(" ")
                if names[3] == "":
                    YELLOW_CO.text_input = "YELLOW"
                    YELLOW_CO.font = MENU_FONT_M
                elif len(names[3]) < 9:
                    YELLOW_CO.font = MENU_FONT_S
                    YELLOW_CO.text_input = names[3]
                elif len(names[3]) >= 9:
                    YELLOW_CO.text_input = names[3]
                    YELLOW_CO.font = MENU_FONT_XS

            if chosen_comp[4]:
                names[4] = name.lstrip(" ")
                if names[4] == "":
                    TEAL_CO.text_input = "TEAL"
                    TEAL_CO.font = MENU_FONT_M
                elif len(names[4]) < 9:
                    TEAL_CO.font = MENU_FONT_S
                    TEAL_CO.text_input = names[4]
                elif len(names[4]) >= 9:
                    TEAL_CO.text_input = names[4]
                    TEAL_CO.font = MENU_FONT_XS

            if chosen_comp[5]:
                names[5] = name.lstrip(" ")
                if names[5] == "":
                    PURPLE_CO.text_input = "PURPLE"
                    PURPLE_CO.font = MENU_FONT_M
                elif len(names[5]) < 9:
                    PURPLE_CO.font = MENU_FONT_S
                    PURPLE_CO.text_input = names[5]
                elif len(names[5]) >= 9:
                    PURPLE_CO.text_input = names[5]
                    PURPLE_CO.font = MENU_FONT_XS

            if chosen_comp[6]:
                names[6] = name.lstrip(" ")
                if names[6] == "":
                    ORANGE_CO.text_input = "ORANGE"
                    ORANGE_CO.font = MENU_FONT_M
                elif len(names[6]) < 9:
                    ORANGE_CO.font = MENU_FONT_S
                    ORANGE_CO.text_input = names[6]
                elif len(names[6]) >= 9:
                    ORANGE_CO.text_input = names[6]
                    ORANGE_CO.font = MENU_FONT_XS
                        

            if event.type == pygame.MOUSEBUTTONDOWN:
                chosen_comp = [0,0,0,0,0,0,0]
                if BACK.check_for_click():
                    return ["","","","","","",""]
                if SAVE.check_for_click():
                    return names
                if RESET.check_for_click():
                    names = ["","","","","","",""]
                    #chosen_comp = [0,0,0,0,0,0,0]
                    RED_CO.text_input = "RED"
                    RED_CO.font = MENU_FONT_M
                    BLUE_CO.text_input = "BLUE"
                    BLUE_CO.font = MENU_FONT_M
                    GREEN_CO.text_input = "GREEN"
                    GREEN_CO.font = MENU_FONT_M
                    YELLOW_CO.text_input = "YELLOW"
                    YELLOW_CO.font = MENU_FONT_M
                    TEAL_CO.text_input = "TEAL"
                    TEAL_CO.font = MENU_FONT_M
                    PURPLE_CO.text_input = "PURPLE"
                    PURPLE_CO.font = MENU_FONT_M
                    ORANGE_CO.text_input = "ORANGE"
                    ORANGE_CO.font = MENU_FONT_M
                if BLUE_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[1] = 1
                    name = ""
                if RED_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[0] = 1
                    name = ""
                if GREEN_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[2] = 1
                    name = ""
                if YELLOW_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[3] = 1
                    name = ""
                if TEAL_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[4] = 1
                    name = ""
                if PURPLE_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[5] = 1
                    name = ""
                if ORANGE_CO.check_for_click():
                    #chosen_comp = [0,0,0,0,0,0,0]
                    chosen_comp[6] = 1
                    name = ""

        SAVE.update_menu_button(win,x,y)
        BACK.update_menu_button(win,x,y)
        RESET.update_menu_button(win,x,y)
        RED_CO.update_t_button(win,x,y,chosen_comp[0])
        BLUE_CO.update_t_button(win,x,y,chosen_comp[1])
        GREEN_CO.update_t_button(win,x,y,chosen_comp[2])
        YELLOW_CO.update_t_button(win,x,y,chosen_comp[3])
        TEAL_CO.update_t_button(win,x,y,chosen_comp[4])
        PURPLE_CO.update_t_button(win,x,y,chosen_comp[5])
        ORANGE_CO.update_t_button(win,x,y,chosen_comp[6])
        pygame.display.update()

def name_selection(win,num_of_players,saved_names):
    win.fill(ANTIQUE_WHITE)
    pygame.draw.rect(win, BLACK, (400 , 25, 700, 850))
    pygame.draw.rect(win, ANTIQUE_WHITE, (410,35,680,830))
    P_ONE = Toggle_Button(450,210,"Player 1", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH*2, MENU_BUTTON_HEIGHT-40)
    P_TWO = Toggle_Button(450,320,"Player 2", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH*2, MENU_BUTTON_HEIGHT-40)
    P_THREE = Toggle_Button(450,430,"Player 3", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH*2, MENU_BUTTON_HEIGHT-40)
    P_FOUR = Toggle_Button(450,540,"Player 4", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH*2, MENU_BUTTON_HEIGHT-40)
    P_FIVE = Toggle_Button(450,650,"Player 5", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH*2, MENU_BUTTON_HEIGHT-40)
    P_SIX = Toggle_Button(450,760,"Player 6", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH*2, MENU_BUTTON_HEIGHT-40)
    BACK = Menu_Button(0,0,"BACK", MENU_FONT_M, GREY, LIGHTISH_GREY, MENU_BUTTON_WIDTH-40, MENU_BUTTON_HEIGHT-40)
    SAVE = Menu_Button(1200,760,"SAVE",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-40,MENU_BUTTON_HEIGHT-40)
    RESET = Menu_Button(40,760,"RESET",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-25,MENU_BUTTON_HEIGHT-40)
    running = True
    chosen_player = [0 for i in range(num_of_players)]
    player_names = saved_names
    name = ""
    clock = pygame.time.Clock()
    if len([i for i in player_names if i != ""]) > 0:
        for q in range(len(player_names)):
            if player_names[q] != "":
                if len(player_names[q]) < 9:
                    if q == 0:
                        P_ONE.text_input = player_names[q]
                        P_ONE.font = MENU_FONT_S
                    if q == 1:
                        P_TWO.text_input = player_names[q]
                        P_TWO.font = MENU_FONT_S
                    if q == 2:
                        P_THREE.text_input = player_names[q]
                        P_THREE.font = MENU_FONT_S 
                    if q == 3:
                        P_FOUR.text_input = player_names[q]
                        P_FOUR.font = MENU_FONT_S
                    if q == 4:
                        P_FIVE.text_input = player_names[q]
                        P_FIVE.font = MENU_FONT_S
                    if q == 5:
                        P_SIX.text_input = player_names[q]
                        P_SIX.font = MENU_FONT_S
                else:
                    if q == 0:
                        P_ONE.text_input = player_names[q]
                        P_ONE.font = MENU_FONT_XS
                    if q == 1:
                        P_TWO.text_input = player_names[q]
                        P_TWO.font = MENU_FONT_XS
                    if q == 2:
                        P_THREE.text_input = player_names[q]
                        P_THREE.font = MENU_FONT_XS 
                    if q == 3:
                        P_FOUR.text_input = player_names[q]
                        P_FOUR.font = MENU_FONT_XS
                    if q == 4:
                        P_FIVE.text_input = player_names[q]
                        P_FIVE.font = MENU_FONT_XS
                    if q == 5:
                        P_SIX.text_input = player_names[q]
                        P_SIX.font = MENU_FONT_XS

    while running:
        P_ONE.draw_menu_button(win)
        P_TWO.draw_menu_button(win)
        P_THREE.draw_menu_button(win)
        P_FOUR.draw_menu_button(win)
        P_FIVE.draw_menu_button(win)
        P_SIX.draw_menu_button(win)
        BACK.draw_menu_button(win)
        SAVE.draw_menu_button(win)
        RESET.draw_menu_button(win)
        clock.tick(FPS)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                if event.key == pygame.K_TAB:
                        if 1 in chosen_player:
                            name = ""
                            if chosen_player[-1] == 1:
                                chosen_player[-1] = 0
                                chosen_player[0] = 1
                            else:
                                spot = chosen_player.index(max(chosen_player))
                                chosen_player[spot] = 0
                                chosen_player[spot + 1] = 1
                if len(name) < 11:
                    if event.key == pygame.K_q:
                        name += "Q"
                    if event.key == pygame.K_w:
                        name += "W"
                    if event.key == pygame.K_e:
                        name += "E"
                    if event.key == pygame.K_r:
                        name += "R"
                    if event.key == pygame.K_t:
                        name += "T"
                    if event.key == pygame.K_y:
                        name += "Y"
                    if event.key == pygame.K_u:
                        name += "U"
                    if event.key == pygame.K_i:
                        name += "I"
                    if event.key == pygame.K_o:
                        name += "O"
                    if event.key == pygame.K_p:
                        name += "P"
                    if event.key == pygame.K_a:
                        name += "A"
                    if event.key == pygame.K_s:
                        name += "S"
                    if event.key == pygame.K_d:
                        name += "D"
                    if event.key == pygame.K_f:
                        name += "F"
                    if event.key == pygame.K_g:
                        name += "G"
                    if event.key == pygame.K_h:
                        name += "H"
                    if event.key == pygame.K_j:
                        name += "J"
                    if event.key == pygame.K_k:
                        name += "K"
                    if event.key == pygame.K_l:
                        name += "L"
                    if event.key == pygame.K_z:
                        name += "Z"
                    if event.key == pygame.K_x:
                        name += "X"
                    if event.key == pygame.K_c:
                        name += "C"
                    if event.key == pygame.K_v:
                        name += "V"
                    if event.key == pygame.K_b:
                        name += "B"
                    if event.key == pygame.K_n:
                        name += "N"
                    if event.key == pygame.K_m:
                        name += "M"
                    if event.key == pygame.K_SPACE:
                        name += " "
                    if event.key == pygame.K_MINUS:
                        name += "-"
                    if event.key == pygame.K_QUOTE:
                        name += "'"

            if event.type == pygame.MOUSEBUTTONDOWN:
                chosen_player = [0 for i in range(num_of_players)]
                name = ""
                if BACK.check_for_click():
                    return []
                if SAVE.check_for_click():
                    return player_names
                if RESET.check_for_click():
                    player_names = []
                    P_ONE.text_input = "Player 1"
                    P_ONE.font = MENU_FONT_M
                    P_TWO.text_input = "Player 2"
                    P_TWO.font = MENU_FONT_M
                    P_THREE.text_input = "Player 3"
                    P_THREE.font = MENU_FONT_M
                    P_FOUR.text_input = "Player 4"
                    P_FOUR.font = MENU_FONT_M
                    P_FIVE.text_input = "Player 5"
                    P_FIVE.font = MENU_FONT_M
                    P_SIX.text_input = "Player 6"
                    P_SIX.font = MENU_FONT_M
                if P_ONE.check_for_click():
                    chosen_player[0] = 1
                if P_TWO.check_for_click():
                    chosen_player[1] = 1
                if num_of_players >= 3:
                    if P_THREE.check_for_click():
                        chosen_player[2] = 1
                if num_of_players >= 4:
                    if P_FOUR.check_for_click():
                        chosen_player[3] = 1
                if num_of_players >= 5:
                    if P_FIVE.check_for_click():
                        chosen_player[4] = 1
                if num_of_players == 6:
                    if P_SIX.check_for_click():
                        chosen_player[5] = 1


            if chosen_player[0]:
                player_names[0] = name.lstrip(" ")
                if player_names[0] == "":
                    P_ONE.text_input = "Player 1"
                    P_ONE.font = MENU_FONT_M
                else:
                    P_ONE.font = MENU_FONT_S
                    P_ONE.text_input = player_names[0]

            if chosen_player[1]:
                player_names[1] = name.lstrip(" ")
                if player_names[1] == "":
                    P_TWO.text_input = "Player 2"
                    P_TWO.font = MENU_FONT_M
                else:
                    P_TWO.font = MENU_FONT_S
                    P_TWO.text_input = player_names[1]

            if num_of_players >= 3:
                if chosen_player[2]:
                    player_names[2] = name.lstrip(" ")
                    if player_names[2] == "":
                        P_THREE.text_input = "Player 3"
                        P_THREE.font = MENU_FONT_M
                    else:
                        P_THREE.font = MENU_FONT_S
                        P_THREE.text_input = player_names[2]

            if num_of_players >= 4:
                if chosen_player[3]:
                    player_names[3] = name.lstrip(" ")
                    if player_names[3] == "":
                        P_FOUR.text_input = "Player 4"
                        P_FOUR.font = MENU_FONT_M
                    else:
                        P_FOUR.font = MENU_FONT_S
                        P_FOUR.text_input = player_names[3]

            if num_of_players >= 5:
                if chosen_player[4]:
                    player_names[4] = name.lstrip(" ")
                    if player_names[4] == "":
                        P_FIVE.text_input = "Player 5"
                        P_FIVE.font = MENU_FONT_M
                    else:
                        P_FIVE.font = MENU_FONT_S
                        P_FIVE.text_input = player_names[4]

            if num_of_players == 6:
                if chosen_player[5]:
                    player_names[5] = name.lstrip(" ")
                    if player_names[5] == "":
                        P_SIX.text_input = "Player 6"
                        P_SIX.font = MENU_FONT_M
                    else:
                        P_SIX.font = MENU_FONT_S
                        P_SIX.text_input = player_names[5]

        BACK.update_menu_button(win,x,y)
        SAVE.update_menu_button(win,x,y)
        RESET.update_menu_button(win,x,y)
        P_ONE.update_t_button(win,x,y,chosen_player[0])
        P_TWO.update_t_button(win,x,y,chosen_player[1])
        if num_of_players >= 3:
            P_THREE.update_t_button(win,x,y,chosen_player[2])
        if num_of_players >= 4:
            P_FOUR.update_t_button(win,x,y,chosen_player[3])
        if num_of_players >= 5:
            P_FIVE.update_t_button(win,x,y,chosen_player[4])
        if num_of_players == 6:
            P_SIX.update_t_button(win,x,y,chosen_player[5])
        pygame.display.update()
                    
def pick_order(win, player_names):
    win.fill(ANTIQUE_WHITE)
    QUIT_GAME = Menu_Button(0,0,"QUIT",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-40,MENU_BUTTON_HEIGHT-40)
    BEGIN =  Menu_Button(1200,600,"BEGIN",MENU_FONT_M,GREY,LIGHTISH_GREY,MENU_BUTTON_WIDTH-40,MENU_BUTTON_HEIGHT-40)
    pygame.draw.rect(win,BLACK,(340,340,845,550),10)
    name_rects = [0,0,0,0,0,0]
    moves = [[] for i in player_names]
    tile_name = ["" for i in player_names]
    tile_rects = [0,0,0,0,0,0]
    turn_order = [0 for i in player_names]
    turn = 0
    player_fonts = player_names.copy()
    available_pieces = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,"1A","2A","3A","4A","5A","6A","7A","8A","9A","10A","11A","12A",1],
     [1,"1B","2B","3B","4B","5B","6B","7B","8B","9B","10B","11B","12B",1],
     [1,"1C","2C","3C","4C","5C","6C","7C","8C","9C","10C","11C","12C",1],
     [1,"1D","2D","3D","4D","5D","6D","7D","8D","9D","10D","11D","12D",1],
     [1,"1E","2E","3E","4E","5E","6E","7E","8E","9E","10E","11E","12E",1],
     [1,"1F","2F","3F","4F","5F","6F","7F","8F","9F","10F","11F","12F",1],
     [1,"1G","2G","3G","4G","5G","6G","7G","8G","9G","10G","11G","12G",1],
     [1,"1H","2H","3H","4H","5H","6H","7H","8H","9H","10H","11H","12H",1],
     [1,"1I","2I","3I","4I","5I","6I","7I","8I","9I","10I","11I","12I",1],
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    piece_labels = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1],
     [1,"1A","2A","3A","4A","5A","6A","7A","8A","9A","10A","11A","12A",1],
     [1,"1B","2B","3B","4B","5B","6B","7B","8B","9B","10B","11B","12B",1],
     [1,"1C","2C","3C","4C","5C","6C","7C","8C","9C","10C","11C","12C",1],
     [1,"1D","2D","3D","4D","5D","6D","7D","8D","9D","10D","11D","12D",1],
     [1,"1E","2E","3E","4E","5E","6E","7E","8E","9E","10E","11E","12E",1],
     [1,"1F","2F","3F","4F","5F","6F","7F","8F","9F","10F","11F","12F",1],
     [1,"1G","2G","3G","4G","5G","6G","7G","8G","9G","10G","11G","12G",1],
     [1,"1H","2H","3H","4H","5H","6H","7H","8H","9H","10H","11H","12H",1],
     [1,"1I","2I","3I","4I","5I","6I","7I","8I","9I","10I","11I","12I",1],
     [1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    for i in range(108):
        randposx = random.randrange(400,1100)
        randposy = random.randrange(400,800)
        randrot = random.randrange(1,90)
        rotate_and_draw_piece(win,randposx,randposy,randrot)
    clock = pygame.time.Clock()
    
    for i in range(len(player_fonts)):
        player_fonts[i] = MENU_FONT_XS.render(player_fonts[i],True,BLACK)
        if len(player_fonts) == 2:
           name_rects[i] = player_fonts[i].get_rect(center=(375 + (i*750),125))
        if len(player_fonts) == 3:
            name_rects[i] = player_fonts[i].get_rect(center=(375 + (i*375),125))
        if len(player_fonts) == 4:
            name_rects[i] = player_fonts[i].get_rect(center=(300 + (i*300),125))
        if len(player_fonts) == 5:
            name_rects[i] = player_fonts[i].get_rect(center=(250 + (i*250),125))
        if len(player_fonts) == 6:
            name_rects[i] = player_fonts[i].get_rect(center=(214 + (i*214),125))
        #if names are too big they overlap with other names, fix this at some point
        win.blit(player_fonts[i],name_rects[i])

    run = True
    while run:
        QUIT_GAME.draw_menu_button(win)
        BEGIN.draw_menu_button(win)
        clock.tick(FPS)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_GAME.check_for_click():
                    main_menu(win)
                if turn > len(player_names):
                    if BEGIN.check_for_click():
                        #check this please
                        key = 1
                        for i in range(len(moves)):
                            for j in range(len(moves)):
                                for q in range(-1,2,2):
                                    if (moves[i][0] == moves[j][0] and moves[i][1] == moves[j][1] + q) or (moves[i][1] == moves[j][1] and moves[i][0] == moves[j][0] + q):
                                        if len(moves[i]) != 3:
                                            moves[i].append(key)
                                        if len(moves[j]) != 3:
                                            moves[j].append(key)
                                        key += 1
                            if len(moves[i]) != 3:
                                moves[i].append(0)
                                #it ends here
                        main(win, turn_order, available_pieces, moves, piece_labels, False)
                if x >= 340 and x <= 1185 and y >= 340 and y <= 890 and turn < len(player_names):
                    xpos = random.randrange(1,10)
                    ypos = random.randrange(1,13)
                    while available_pieces[xpos][ypos] == 0:
                        xpos = random.randrange(1,10)
                        ypos = random.randrange(1,13)
                    tile_name[turn] = available_pieces[xpos][ypos]
                    moves[turn] = [xpos,ypos]
                    available_pieces[xpos][ypos] = 0
                    tile_name[turn] = MENU_FONT_S.render(tile_name[turn],True,WHITE)
                    if len(player_names) == 2:
                       tile_rects[turn] = tile_name[turn].get_rect(center=(375 + (turn*750),200))
                       draw_piece(win,375 + (turn*750),200,GREY,LIGHTISH_GREY)
                    if len(player_names) == 3:
                        tile_rects[turn] = tile_name[turn].get_rect(center=(375 + (turn*375),200))
                        draw_piece(win,375 + (turn*375),200,GREY,LIGHTISH_GREY)
                    if len(player_names) == 4:
                        tile_rects[turn] = tile_name[turn].get_rect(center=(300 + (turn*300),200))
                        draw_piece(win,300 + (turn*300),200,GREY,LIGHTISH_GREY)
                    if len(player_names) == 5:
                        tile_rects[turn] = tile_name[turn].get_rect(center=(250 + (turn*250),200))
                        draw_piece(win,250 + (turn*250),200,GREY,LIGHTISH_GREY)
                    if len(player_names) == 6:
                        tile_rects[turn] = tile_name[turn].get_rect(center=(214 + (turn*214),200))
                        draw_piece(win,214 + (turn*214),200,GREY,LIGHTISH_GREY)
                    win.blit(tile_name[turn],tile_rects[turn])
                    turn += 1
                    
                if turn == len(player_names):
                    move_temp = moves.copy()
                    for i in range(len(player_names)):
                        turn_order[i] = player_names[move_temp.index(min(move_temp))]
                        move_temp[move_temp.index(min(move_temp))] = [20,23]
                    turn += 1


        BEGIN.update_menu_button(win,x,y)
        QUIT_GAME.update_menu_button(win,x,y)
        pygame.display.update()
        
def rotate_and_draw_piece(win,x,y,rot):
    bottom = pygame.Surface((PIECE_SIZE,PIECE_SIZE))
    top = pygame.Surface((PIECE_SIZE-10,PIECE_SIZE-10))
    bottom.fill(GREY)
    top.fill(LIGHTISH_GREY)
    top.set_colorkey(BLACK)
    bottom.set_colorkey(BLACK)
    top_rect = top.get_rect()
    bottom_rect = bottom.get_rect()
    top_rect.center = (x,y)
    bottom_rect.center = (x,y)
    bottom = pygame.transform.rotate(bottom,rot)
    top = pygame.transform.rotate(top,rot)
    win.blit(bottom,bottom_rect)
    win.blit(top, top_rect)

def draw_piece(win,x,y,color, light_color):
    bottom = pygame.Surface((PIECE_SIZE,PIECE_SIZE))
    top = pygame.Surface((PIECE_SIZE-10,PIECE_SIZE-10))
    bottom.fill(color)
    top.fill(light_color)
    top.set_colorkey(BLACK)
    bottom.set_colorkey(BLACK)
    top_rect = top.get_rect()
    bottom_rect = bottom.get_rect()
    top_rect.center = (x,y)
    bottom_rect.center = (x,y)
    win.blit(bottom,bottom_rect)
    win.blit(top, top_rect)
 

def view_pieces(win,game,piece_labels):
    clock = pygame.time.Clock()
    running = True
    discarding = False
    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
    BACK = Menu_Button(1210,300,"BACK", MENU_FONT_XS, GREY, LIGHTISH_GREY, 100,80)
    COLLECT_PIECE = Menu_Button(1205,645,"DRAW", MENU_FONT_XS, GREY, LIGHTISH_GREY, 105,70)
    SHOW_MOVES = Menu_Button(1315.5,645,"MY MOVES", MENU_FONT_XS, GREY, LIGHTISH_GREY, 200,70)
    UNPLAY_PIECES = Toggle_Button(1315.5,300,"DISCARD", MENU_FONT_XS, GREY, LIGHTISH_GREY, 175,80)
    TRASH_IT = Menu_Button(1210,730,"DISCARD PIECE", MENU_FONT_XS,GREY,LIGHTISH_GREY, 280,80)
    THE_DISCARDED = Menu_Button(1205,820,"DISCARDED PIECES", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 280,70)
    discarding_buttons = []
    discard_toggle = []
    for i in range(len(game.player_moves[game.turn])):
        if game.player_moves[game.turn][i][0] == 1:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"A",True,WHITE)
        if game.player_moves[game.turn][i][0] == 2:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"B",True,WHITE)
        if game.player_moves[game.turn][i][0] == 3:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"C",True,WHITE)
        if game.player_moves[game.turn][i][0] == 4:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"D",True,WHITE)
        if game.player_moves[game.turn][i][0] == 5:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"E",True,WHITE)
        if game.player_moves[game.turn][i][0] == 6:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"F",True,WHITE)
        if game.player_moves[game.turn][i][0] == 7:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"G",True,WHITE)
        if game.player_moves[game.turn][i][0] == 8:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"H",True,WHITE)
        if game.player_moves[game.turn][i][0] == 9:
            tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"I",True,WHITE)
        if i < 3:
            draw_piece(win,i*100+1252.5,460,GREY,LIGHTISH_GREY)
            tile_label_rect = tile_label.get_rect(center=(i*100+1252.5,460))
            win.blit(tile_label,tile_label_rect)
            discarding_buttons.append(Toggle_Button(i*100+1242.5,393,"",MENU_FONT_XXS,LIGHTISH_GREY,WHITE,20,20))
        if i >= 3:
            draw_piece(win,(i-3)*100+1252.5,565,GREY,LIGHTISH_GREY)
            tile_label_rect = tile_label.get_rect(center=((i-3)*100+1252.5,565))
            win.blit(tile_label,tile_label_rect)
            discarding_buttons.append(Toggle_Button((i-3)*100+1242.5,612,"",MENU_FONT_XXS,LIGHTISH_GREY,WHITE,20,20))
        discard_toggle.append(0)
    showing_moves = False
    while running:
        x,y = pygame.mouse.get_pos()
        UNPLAY_PIECES.draw_menu_button(win)
        BACK.draw_menu_button(win)
        COLLECT_PIECE.draw_menu_button(win)
        SHOW_MOVES.draw_menu_button(win)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.check_for_click():
                    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
                    game.draw_labels(win, piece_labels)
                    return []
                if SHOW_MOVES.check_for_click():
                    if not showing_moves:
                        game.draw_possible_moves(win, game, LIGHTISH_YELLOW, BLACK, piece_labels)
                        showing_moves = True
                    else:
                        game.draw_possible_moves(win, game, WHITE, BLACK, piece_labels)
                        showing_moves = False
                if UNPLAY_PIECES.check_for_click() and not game.piece_discarded:
                    #CAN ONLY DISCARD IF THE PLAYER HAS ALREADY PLAYED THEIR TILE, HAS TO PLAY A TILE
                    if game.piece_placed and not game.piece_drawn:
                        if discarding:
                            discarding = False
                            for i in range(len(game.player_moves[game.turn])):
                                if i < 3:
                                    pygame.draw.rect(win,ANTIQUE_WHITE,(i*100+1242.5,393,20,20))
                                if i >= 3:
                                    pygame.draw.rect(win,ANTIQUE_WHITE,((i-3)*100+1242.5,612,20,20))
                            pygame.draw.rect(win,ANTIQUE_WHITE,(1210,730,300,80))
                        else:
                            discarding = True
                if discarding:
                    for i in range(len(game.player_moves[game.turn])):
                        if discarding_buttons[i].check_for_click():
                            discard_toggle = [0 for i in game.player_moves[game.turn]]
                            discard_toggle[i] = 1
                    if THE_DISCARDED.check_for_click():
                        discarded_pieces(win,game)
                        for i in range(len(game.player_moves[game.turn])):
                            if game.player_moves[game.turn][i][0] == 1:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"A",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 2:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"B",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 3:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"C",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 4:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"D",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 5:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"E",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 6:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"F",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 7:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"G",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 8:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"H",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 9:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"I",True,WHITE)
                            if i < 3:
                                draw_piece(win,i*100+1252.5,460,GREY,LIGHTISH_GREY)
                                tile_label_rect = tile_label.get_rect(center=(i*100+1252.5,460))
                                win.blit(tile_label,tile_label_rect)
                            if i >= 3:
                                draw_piece(win,(i-3)*100+1252.5,565,GREY,LIGHTISH_GREY)
                                tile_label_rect = tile_label.get_rect(center=((i-3)*100+1252.5,565))
                                win.blit(tile_label,tile_label_rect)
                    if TRASH_IT.check_for_click():
                        if 1 in discard_toggle:
                            discarding = False
                            game.piece_discarded = True
                            game.discarded_pieces.append(game.player_moves[game.turn][discard_toggle.index(1)])
                            game.player_moves[game.turn].remove(game.player_moves[game.turn][discard_toggle.index(1)])
                            discard_toggle = [0 for i in game.player_moves[game.turn]]
                            pygame.draw.rect(win,ANTIQUE_WHITE,(1307.5,520,90,90))
                            pygame.draw.rect(win,ANTIQUE_WHITE,(1205,820,280,70))
                            for i in range(len(game.player_moves[game.turn])):
                                if game.player_moves[game.turn][i][0] == 1:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"A",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 2:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"B",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 3:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"C",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 4:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"D",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 5:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"E",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 6:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"F",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 7:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"G",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 8:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"H",True,WHITE)
                                if game.player_moves[game.turn][i][0] == 9:
                                    tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"I",True,WHITE)
                                if i < 3:
                                    draw_piece(win,i*100+1252.5,460,GREY,LIGHTISH_GREY)
                                    tile_label_rect = tile_label.get_rect(center=(i*100+1252.5,460))
                                    win.blit(tile_label,tile_label_rect)
                                    pygame.draw.rect(win,ANTIQUE_WHITE,(i*100+1242.5,393,20,20))
                                if i >= 3:
                                    draw_piece(win,(i-3)*100+1252.5,565,GREY,LIGHTISH_GREY)
                                    tile_label_rect = tile_label.get_rect(center=((i-3)*100+1252.5,565))
                                    win.blit(tile_label,tile_label_rect)
                                    pygame.draw.rect(win,ANTIQUE_WHITE,((i-3)*100+1242.5,612,20,20))
                            pygame.draw.rect(win,ANTIQUE_WHITE,((1)*100+1242.5,612,20,20))
                            pygame.draw.rect(win,ANTIQUE_WHITE,(1210,730,300,80))
                if len(game.player_moves[game.turn]) < 6:
                    if COLLECT_PIECE.check_for_click() and not discarding:
                        game.collect_tiles(game.turn, False)
                        game.piece_drawn = True
                        for i in range(len(game.player_moves[game.turn])):
                            if game.player_moves[game.turn][i][0] == 1:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"A",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 2:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"B",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 3:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"C",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 4:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"D",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 5:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"E",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 6:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"F",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 7:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"G",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 8:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"H",True,WHITE)
                            if game.player_moves[game.turn][i][0] == 9:
                                tile_label = MENU_FONT_XS.render(str(game.player_moves[game.turn][i][1])+"I",True,WHITE)
                            if i < 3:
                                draw_piece(win,i*100+1252.5,460,GREY,LIGHTISH_GREY)
                                tile_label_rect = tile_label.get_rect(center=(i*100+1252.5,460))
                                win.blit(tile_label,tile_label_rect)
                            if i >= 3:
                                draw_piece(win,(i-3)*100+1252.5,565,GREY,LIGHTISH_GREY)
                                tile_label_rect = tile_label.get_rect(center=((i-3)*100+1252.5,565))
                                win.blit(tile_label,tile_label_rect)

        SHOW_MOVES.update_menu_button(win,x,y)
        COLLECT_PIECE.update_menu_button(win,x,y)
        BACK.update_menu_button(win,x,y)
        UNPLAY_PIECES.update_t_button(win,x,y,discarding)
        if discarding:
            TRASH_IT.draw_menu_button(win)
            TRASH_IT.update_menu_button(win,x,y)
            THE_DISCARDED.draw_menu_button(win)
            THE_DISCARDED.update_menu_button(win,x,y)
            for i in range(len(game.player_moves[game.turn])):
                discarding_buttons[i].draw_menu_button(win)
                discarding_buttons[i].update_t_button(win,x,y,discard_toggle[i])
        pygame.display.update()

def view_my_info(win,game):
    game.count_tiles()
    clock = pygame.time.Clock()
    run = True
    color_list = [RED,BLUE,GREEN,YELLOW,TEAL,PURPLE,ORANGE]
    light_color_list = [LIGHTISH_RED,LIGHTISH_BLUE,LIGHTISH_GREEN,LIGHTISH_YELLOW,LIGHTISH_TEAL,LIGHTISH_PURPLE,LIGHTISH_ORANGE]
    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
    BACK = Menu_Button(1210,300,"BACK", MENU_FONT_XS, GREY, LIGHTISH_GREY, 100,80)
    win.blit(MENU_FONT_XS.render("Your Balance:",True,LIGHTISH_GREEN), MENU_FONT_XS.render("Your Balance:",True,LIGHTISH_GREEN).get_rect(center=(1405,315)))
    win.blit(MENU_FONT_XS.render("$" + str(game.balances[game.turn]),True,LIGHTISH_GREEN), MENU_FONT_XS.render("$" + str(game.balances[game.turn]),True,LIGHTISH_GREEN).get_rect(center=(1405,340)))
    win.blit(MENU_FONT_XXS.render("Price/per stock",True,BLACK),MENU_FONT_XXS.render("Price/per stock:",True,BLACK).get_rect(center=(1405,365)))
    for i in range(len(game.owned_stocks[game.turn])):
        pygame.draw.rect(win,color_list[i],(1210,i*50+390,100,40))
        pygame.draw.rect(win,light_color_list[i],(1215,i*50+395,90,30))
        win.blit(MENU_FONT_XS.render(str(game.owned_stocks[game.turn][i]),True,BLACK), MENU_FONT_XS.render(str(game.owned_stocks[game.turn][i]),True,BLACK).get_rect(center=(1335,i*50+410)))
        if game.stock_prices[i] == 0:
            win.blit(MENU_FONT_XS.render("-",True,GREEN),MENU_FONT_XS.render("-",True,GREEN).get_rect(center=(1405,i*50+410)))
        else:
            win.blit(MENU_FONT_XS.render("$"+str(game.stock_prices[i]),True,GREEN),MENU_FONT_XS.render("$"+str(game.stock_prices[i]),True,GREEN).get_rect(center=(1405,i*50+410)))
    while run:
        x,y = pygame.mouse.get_pos()
        BACK.draw_menu_button(win)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.check_for_click():
                    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
                    return []

        BACK.update_menu_button(win,x,y)
        pygame.display.update()

def purchase_stocks(win,game,total_purchases):
    game.count_tiles()
    clock = pygame.time.Clock()
    running = True
    color_list = [RED,BLUE,GREEN,YELLOW,TEAL,PURPLE,ORANGE]
    light_color_list = [LIGHTISH_RED,LIGHTISH_BLUE,LIGHTISH_GREEN,LIGHTISH_YELLOW,LIGHTISH_TEAL,LIGHTISH_PURPLE,LIGHTISH_ORANGE]
    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
    BACK = Menu_Button(1210,300,"BACK", MENU_FONT_XS, GREY, LIGHTISH_GREY, 100,80)
    CHECKOUT = Menu_Button(1320,300,"CHECKOUT", MENU_FONT_XXS,GREY,LIGHTISH_GREY,150,60)
    total = 0
    total_price = 0
    total_price_rendering = MENU_FONT_XXS.render("$"+str(total_price),True,GREEN)
    total_price_rect = total_price_rendering.get_rect(center=(1440,375))
    PLUS = []
    MINUS = []
    purchasing_num = []
    purchasing_num_rendering = []
    purchasing_num_rects = []
    remaining_num_rendering = []
    remaining_num_rect = []
    for i in range(7):
        pygame.draw.rect(win,color_list[i],(1210,i*50+390,100,40))
        pygame.draw.rect(win,light_color_list[i],(1215,i*50+395,90,30))
        pygame.draw.rect(win,LIGHTISH_GREY,(1350,i*50+395,60,30))
        pygame.draw.rect(win,WHITE,(1352,i*50+397,56,26))
        pygame.draw.rect(win,WHITE,(1450,i*50+390,40,40))
        if game.stock_prices[i] == 0:
            win.blit(MENU_FONT_XS.render("-",True,WHITE),MENU_FONT_XS.render("-",True,WHITE).get_rect(center=(1260,i*50+410)))
        else:
            win.blit(MENU_FONT_XS.render("$" + str(game.stock_prices[i]),True,WHITE),MENU_FONT_XS.render("$" + str(game.stock_prices[i]),True,WHITE).get_rect(center=(1260,i*50+410)))
        PLUS.append(Menu_Button(1320,i*50+395,"+", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30))
        MINUS.append(Menu_Button(1410,i*50+395,"-", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30))
        purchasing_num.append(0)
        purchasing_num_rendering.append(MENU_FONT_XXS.render("0",True,BLACK))
        purchasing_num_rects.append(purchasing_num_rendering[i].get_rect(center=(1378,i*50+410)))
        win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
        remaining_num_rendering.append(MENU_FONT_XXS.render(str(game.total_stocks[i]),True,BLACK))
        remaining_num_rect.append(remaining_num_rendering[i].get_rect(center=(1470,i*50+410)))
        win.blit(remaining_num_rendering[i],remaining_num_rect[i])
    win.blit(MENU_FONT_XXS.render("Total price: ",True,BLACK),MENU_FONT_XXS.render("Total price: ",True,BLACK).get_rect(center=(1375,375)))
    win.blit(total_price_rendering,total_price_rect)
    while running:
        clock.tick(FPS)
        BACK.draw_menu_button(win)
        CHECKOUT.draw_menu_button(win)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.check_for_click():
                    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
                    return total_purchases
                if CHECKOUT.check_for_click() and game.piece_placed:
                    if total > 0 and game.balances[game.turn] >= total_price:
                        game.balances[game.turn] -= total_price
                        total_price = 0
                        for i in range(len(game.total_stocks)):
                            if purchasing_num[i] > 0:
                                game.total_stocks[i] -= purchasing_num[i]
                                game.owned_stocks[game.turn][i] += purchasing_num[i]
                                total_purchases += purchasing_num[i]
                                purchasing_num[i] = 0
                                purchasing_num_rendering[i].fill(WHITE)
                                win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
                                purchasing_num_rendering[i] = MENU_FONT_XXS.render(str(purchasing_num[i]),True,BLACK)
                                win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
                        total_price_rendering.fill(ANTIQUE_WHITE)
                        win.blit(total_price_rendering,total_price_rect)
                        total_price_rendering = MENU_FONT_XXS.render("$"+str(total_price),True,GREEN)
                        win.blit(total_price_rendering,total_price_rect)
                        total = 0
                        remaining_num_rendering[i].fill(WHITE)
                        win.blit(remaining_num_rendering[i],remaining_num_rect[i])
                        remaining_num_rendering[i] = MENU_FONT_XXS.render(str(game.total_stocks[i]-purchasing_num[i]),True,BLACK)
                        win.blit(remaining_num_rendering[i],remaining_num_rect[i])

                for i in range(len(PLUS)):
                    if PLUS[i].check_for_click():
                        if total != 3 and game.total_stocks[i] != purchasing_num[i] and game.number_of_tiles[i] != 0 and total < 3 - total_purchases:
                            purchasing_num[i] += 1
                            total += 1
                            total_price += game.stock_prices[i]
                            purchasing_num_rendering[i].fill(WHITE)
                            win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
                            purchasing_num_rendering[i] = MENU_FONT_XXS.render(str(purchasing_num[i]),True,BLACK)
                            win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
                            total_price_rendering.fill(ANTIQUE_WHITE)
                            win.blit(total_price_rendering,total_price_rect)
                            total_price_rendering = MENU_FONT_XXS.render("$"+str(total_price),True,GREEN)
                            win.blit(total_price_rendering,total_price_rect)
                            remaining_num_rendering[i].fill(WHITE)
                            win.blit(remaining_num_rendering[i],remaining_num_rect[i])
                            remaining_num_rendering[i] = MENU_FONT_XXS.render(str(game.total_stocks[i]-purchasing_num[i]),True,BLACK)
                            win.blit(remaining_num_rendering[i],remaining_num_rect[i])
                    if MINUS[i].check_for_click():
                        if purchasing_num[i] != 0:
                            purchasing_num[i] -= 1
                            total -= 1
                            total_price -= game.stock_prices[i]
                            purchasing_num_rendering[i].fill(WHITE)
                            win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
                            purchasing_num_rendering[i] = MENU_FONT_XXS.render(str(purchasing_num[i]),True,BLACK)
                            win.blit(purchasing_num_rendering[i],purchasing_num_rects[i])
                            total_price_rendering.fill(ANTIQUE_WHITE)
                            win.blit(total_price_rendering,total_price_rect)
                            total_price_rendering = MENU_FONT_XXS.render("$"+str(total_price),True,GREEN)
                            win.blit(total_price_rendering,total_price_rect)
                            remaining_num_rendering[i].fill(WHITE)
                            win.blit(remaining_num_rendering[i],remaining_num_rect[i])
                            remaining_num_rendering[i] = MENU_FONT_XXS.render(str(game.total_stocks[i]-purchasing_num[i]),True,BLACK)
                            win.blit(remaining_num_rendering[i],remaining_num_rect[i])

        for i in range(len(PLUS)):
            PLUS[i].draw_menu_button(win)
            MINUS[i].draw_menu_button(win)
            PLUS[i].update_menu_button(win,x,y)
            MINUS[i].update_menu_button(win,x,y)
        CHECKOUT.update_menu_button(win,x,y)
        BACK.update_menu_button(win,x,y)
        pygame.display.update()



def discarded_pieces(win,game):
    clock = pygame.time.Clock()
    running = True
    BACK = Menu_Button(1210,300,"BACK", MENU_FONT_XS, GREY, LIGHTISH_GREY, 100,80)
    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
    for i in range(len(game.discarded_pieces)):
        if game.discarded_pieces[i][0] == 1:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"A",True,WHITE)
        if game.discarded_pieces[i][0] == 2:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"B",True,WHITE)
        if game.discarded_pieces[i][0] == 3:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"C",True,WHITE)
        if game.discarded_pieces[i][0] == 4:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"D",True,WHITE)
        if game.discarded_pieces[i][0] == 5:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"E",True,WHITE)
        if game.discarded_pieces[i][0] == 6:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"F",True,WHITE)
        if game.discarded_pieces[i][0] == 7:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"G",True,WHITE)
        if game.discarded_pieces[i][0] == 8:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"H",True,WHITE)
        if game.discarded_pieces[i][0] == 9:
            tile_label = MENU_FONT_XS.render(str(game.discarded_pieces[i][1])+"I",True,WHITE)
        if i < 3:
            x_val = i
        elif i >= 3 and i < 6:
            x_val = i - 3
        elif i >= 6 and i < 9:
            x_val = i - 6
        else:
            x_val = i - 9
        draw_piece(win,x_val*100+1252.5,460,GREY,LIGHTISH_GREY)
        tile_label_rect = tile_label.get_rect(center=(x_val+1252.5,460))
        win.blit(tile_label,tile_label_rect)

    while running:
        clock.tick(FPS)
        BACK.draw_menu_button(win)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK.check_for_click():
                    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
                    return []

        BACK.update_menu_button(win,x,y)
        pygame.display.update()

def handle_merge(win,game):
    #pciking order of the merges. If any comps are tied in size, the order is determined by number order. Allow the mergemaker to make this decision at some point
    merging_values_sizes = [game.number_of_tiles[w-3] for w in game.merging_values]
    merge_order = []
    if len(game.merging_values) == 1:
        pass
    else:
        for w in range(len(game.merging_values)):
            merge_order.append(game.merging_values[merging_values_sizes.index(max(merging_values_sizes))])
            game.merging_values.remove(game.merging_values[merging_values_sizes.index(max(merging_values_sizes))])
            merging_values_sizes.remove(max(merging_values_sizes))
        game.merging_values = merge_order
    for i in range(len(game.merging_values)):
        players_involved = []
        stocks_involved = []
        merging_turn = 0
        print(game.merging_values)
        print(game.merging_values[i])
        print(i)
        merging_co_index = game.merging_values[i] - 3
        absorbing_co_index = game.biggest_company - 3
        big_winners = []
        smaller_winners = []
        color_list = [RED,BLUE,GREEN,YELLOW,TEAL,PURPLE,ORANGE]
        light_color_list = [LIGHTISH_RED,LIGHTISH_BLUE,LIGHTISH_GREEN,LIGHTISH_YELLOW,LIGHTISH_TEAL,LIGHTISH_PURPLE,LIGHTISH_ORANGE]
        NEXT_PLAYER = Menu_Button(1200,820,"HANDLE MERGE", MENU_FONT_XS, GREY, LIGHTISH_GREY,300,80)
        started = False
        pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
        clock = pygame.time.Clock()
        for j in range(len(game.owned_stocks)):
            if game.owned_stocks[j][merging_co_index] > 0:
                players_involved.append(j)
                stocks_involved.append(game.owned_stocks[j][merging_co_index])
        buff = [20]
        buff.extend(players_involved)
        q = 0
        if game.turn in players_involved:
            big = game.turn
        while game.turn + q not in players_involved:
            if game.turn + q == len(game.player_names) - 1:
                q = -len(game.player_names)
            else:
                q += 1
        big = game.turn + q 
        mark = buff.index(big)
        mark += 1
        order = [big]
        while mark != buff.index(big):
            if mark == len(buff):
                mark = 0
            order.append(buff[mark])
            mark += 1
        order.remove(buff[0])
        second = None
        second_tie = None
        biggest = stocks_involved[0]
        tie = 0
        if len(stocks_involved) == 1:
            game.balances[players_involved[0]] += game.first_bonus[merging_co_index] + game.second_bonus[merging_co_index]
            big_winners.append(players_involved[0])
        else:
            for j in range(len(stocks_involved)):
                if stocks_involved[j] > biggest:
                    biggest = stocks_involved[j]
            for j in range(len(stocks_involved)):
                if biggest == stocks_involved[j]:
                    tie += 1
    
            if tie > 1:
                for j in range(len(stocks_involved)):
                    if stocks_involved[j] == biggest:
                        game.balances[players_involved[j]] += int(round_up(game.first_bonus[merging_co_index]/tie,-2)) + int(round_up(game.second_bonus[merging_co_index]/tie,-2))
                        big_winners.append(players_involved[j])
            else:
                game.balances[players_involved[stocks_involved.index(biggest)]] += game.first_bonus[merging_co_index]
                big_winners.append(players_involved[stocks_involved.index(biggest)])
            if tie < 2:
                second_tie = 0
                q = 1
                second = stocks_involved[0]
                while second == biggest:
                   second = stocks_involved[0+q]
                   q += 1
                for j in range(len(stocks_involved)):
                    if stocks_involved[j] > second and stocks_involved[j] != biggest:
                        second = stocks_involved[j]
                for j in range(len(stocks_involved)):
                    if second == stocks_involved[j]:
                        second_tie += 1
        
                if second_tie > 1:
                    for j in range(len(stocks_involved)):
                        if stocks_involved[j] == second:
                            game.balances[players_involved[j]] += int(round_up(game.second_bonus[merging_co_index]/second_tie,-2))
                            smaller_winners.append(players_involved[j])
                else:
                    game.balances[players_involved[stocks_involved.index(second)]] += game.second_bonus[merging_co_index]
                    smaller_winners.append(players_involved[stocks_involved.index(second)])
        pygame.draw.rect(win, color_list[merging_co_index],(1205,300,290,110))
        pygame.draw.rect(win, light_color_list[merging_co_index],(1210,305,280,100))
        win.blit(MENU_FONT_S.render("Merger!!",True,WHITE),MENU_FONT_S.render("Merger!!",True,WHITE).get_rect(center=(1351,355)))
        for j in range(len(game.player_names)):
            win.blit(MENU_FONT_XS.render(str(game.player_names[j]) + ":",True,BLACK),MENU_FONT_XS.render(str(game.player_names[j]) + ":",True,BLACK).get_rect(center=(1350,j*29.5+430)))
            if game.owned_stocks[j][merging_co_index] > 0:
                win.blit(MENU_FONT_XS.render(str(game.owned_stocks[j][merging_co_index]),True,color_list[merging_co_index]),MENU_FONT_XS.render(str(game.owned_stocks[j][merging_co_index]),True,color_list[merging_co_index]).get_rect(center=(1475,j*29.5+430)))
            else:
                win.blit(MENU_FONT_XS.render(str(game.owned_stocks[j][merging_co_index]),True,BLACK),MENU_FONT_XS.render(str(game.owned_stocks[j][merging_co_index]),True,BLACK).get_rect(center=(1475,j*29.5+430)))
        win.blit(MENU_FONT_XS.render("Majority Holders",True,BLACK),MENU_FONT_XS.render("Majority Holders",True,BLACK).get_rect(center=(1350,len(game.player_names)*27.5+435)))
        pygame.draw.line(win,color_list[merging_co_index],(1250,len(game.player_names)*27.5+450),(1450,len(game.player_names)*27.5+450),3)
        if second_tie != None:
            win.blit(MENU_FONT_XS.render("Minority Holders",True,BLACK),MENU_FONT_XS.render("Minority Holders",True,BLACK).get_rect(center=(1350,(len(game.player_names)*27.5+430)+len(big_winners)*27.5+40)))
            pygame.draw.line(win,color_list[merging_co_index],(1250,(len(game.player_names)*27.5+430)+len(big_winners)*27.5+55),(1450,(len(game.player_names)*27.5+430)+len(big_winners)*27.5+55),3)
            for j in range(len(big_winners)):
                win.blit(MENU_FONT_XXS.render(str(game.player_names[big_winners[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[big_winners[j]]),True,BLACK).get_rect(center=(1325,j*25+(len(game.player_names)*27.5+465))))
                win.blit(MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[merging_co_index]/tie,-2))),True,GREEN),MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[merging_co_index]/tie,-2))),True,GREEN).get_rect(center=(1450,j*25+(len(game.player_names)*27.5+465))))
            for j in range(len(smaller_winners)):
                win.blit(MENU_FONT_XXS.render(str(game.player_names[smaller_winners[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[smaller_winners[j]]),True,BLACK).get_rect(center=(1325,j*25+((len(game.player_names)*27.5+430)+len(big_winners)*27.5+70))))
                win.blit(MENU_FONT_XXS.render("+$" + str(int(round_up(game.second_bonus[merging_co_index]/second_tie,-2))),True,GREEN),MENU_FONT_XXS.render("+$" + str(int(round_up(game.second_bonus[merging_co_index]/second_tie,-2))),True,GREEN).get_rect(center=(1450,j*25+((len(game.player_names)*27.5+430)+len(big_winners)*27.5+70))))
        else:
            for j in range(len(big_winners)):
                win.blit(MENU_FONT_XXS.render(str(game.player_names[big_winners[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[big_winners[j]]),True,BLACK).get_rect(center=(1325,j*25+(len(game.player_names)*27.5+465))))
                win.blit(MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[merging_co_index]/len(big_winners),-2)) + int(round_up(game.second_bonus[merging_co_index]/len(big_winners),-2))),True,GREEN),MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[merging_co_index]/len(big_winners),-2)) + int(round_up(game.second_bonus[merging_co_index]/len(big_winners),-2))),True,GREEN).get_rect(center=(1450,j*25+(len(game.player_names)*27.5+465))))
        run = True
        while run:
            NEXT_PLAYER.draw_menu_button(win)
            clock.tick(FPS)
            x,y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if started:
                        if PLUS_HOLD.check_for_click() and remaining_stocks > 0:
                            holding_stocks += 1
                            remaining_stocks -= 1
                            holding_meter.fill(WHITE)
                            win.blit(holding_meter,holding_meter_rect)
                            holding_meter = MENU_FONT_XXS.render(str(holding_stocks),True,BLACK)
                            win.blit(holding_meter,holding_meter_rect)
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(remaining_stocks),True,color_list[merging_co_index])
                            win.blit(turn_title,turn_title_rect)
                        if MINUS_HOLD.check_for_click() and holding_stocks > 0:
                            holding_stocks -= 1
                            remaining_stocks += 1
                            holding_meter.fill(WHITE)
                            win.blit(holding_meter,holding_meter_rect)
                            holding_meter = MENU_FONT_XXS.render(str(holding_stocks),True,BLACK)
                            win.blit(holding_meter,holding_meter_rect)
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(remaining_stocks),True,color_list[merging_co_index])
                            win.blit(turn_title,turn_title_rect)
                        if PLUS_SELL.check_for_click() and remaining_stocks > 0:
                            selling_stocks += 1
                            remaining_stocks -= 1
                            game.balances[order[merging_turn]] += game.stock_prices[merging_co_index]
                            game.total_stocks[merging_co_index] += 1
                            selling_meter.fill(WHITE)
                            win.blit(selling_meter,selling_meter_rect)
                            selling_meter = MENU_FONT_XXS.render(str(selling_stocks),True,BLACK)
                            win.blit(selling_meter,selling_meter_rect)
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(remaining_stocks),True,color_list[merging_co_index])
                            win.blit(turn_title,turn_title_rect)
                        if MINUS_SELL.check_for_click() and selling_stocks > 0:
                            selling_stocks -= 1
                            remaining_stocks += 1
                            game.balances[order[merging_turn]] -= game.stock_prices[merging_co_index]
                            game.total_stocks[merging_co_index] -= 1
                            selling_meter.fill(WHITE)
                            win.blit(selling_meter,selling_meter_rect)
                            selling_meter = MENU_FONT_XXS.render(str(selling_stocks),True,BLACK)
                            win.blit(selling_meter,selling_meter_rect)
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(remaining_stocks),True,color_list[merging_co_index])
                            win.blit(turn_title,turn_title_rect)
                        if PLUS_TRADE.check_for_click() and remaining_stocks > 1 and game.total_stocks[absorbing_co_index] > 0:
                            trading_stocks += 2
                            remaining_stocks -= 2
                            game.owned_stocks[order[merging_turn]][absorbing_co_index] += 1
                            game.total_stocks[absorbing_co_index] -= 1
                            pygame.draw.rect(win,light_color_list[absorbing_co_index],(1410,660,50,50))
                            win.blit(MENU_FONT_XS.render(str(game.total_stocks[absorbing_co_index]),True,WHITE),MENU_FONT_XS.render(str(game.total_stocks[absorbing_co_index]),True,WHITE).get_rect(center=(1435,685)))
                            trading_meter.fill(WHITE)
                            win.blit(trading_meter,trading_meter_rect)
                            trading_meter = MENU_FONT_XXS.render(str(trading_stocks),True,BLACK)
                            win.blit(trading_meter,trading_meter_rect)
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(remaining_stocks),True,color_list[merging_co_index])
                            win.blit(turn_title,turn_title_rect)
                        if MINUS_TRADE.check_for_click() and trading_stocks > 1:
                            trading_stocks -= 2
                            remaining_stocks += 2
                            game.owned_stocks[order[merging_turn]][absorbing_co_index] -= 1
                            game.total_stocks[absorbing_co_index] += 1
                            pygame.draw.rect(win,light_color_list[absorbing_co_index],(1410,660,50,50))
                            win.blit(MENU_FONT_XS.render(str(game.total_stocks[absorbing_co_index]),True,WHITE),MENU_FONT_XS.render(str(game.total_stocks[absorbing_co_index]),True,WHITE).get_rect(center=(1435,685)))
                            trading_meter.fill(WHITE)
                            win.blit(trading_meter,trading_meter_rect)
                            trading_meter = MENU_FONT_XXS.render(str(trading_stocks),True,BLACK)
                            win.blit(trading_meter,trading_meter_rect)
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(remaining_stocks),True,color_list[merging_co_index])
                            win.blit(turn_title,turn_title_rect)


                    if NEXT_PLAYER.check_for_click():
                        if not started:
                            holding_stocks = 0
                            selling_stocks = 0
                            trading_stocks = 0
                            started = True
                            remaining_stocks = game.owned_stocks[order[merging_turn]][merging_co_index]
                            pygame.draw.rect(win,ANTIQUE_WHITE,(1203,412,297,408))
                            NEXT_PLAYER = Menu_Button(1200,820,"NEXT PLAYER", MENU_FONT_XS, GREY, LIGHTISH_GREY,300,80)
                            PLUS_HOLD = Menu_Button(1340,500,"+", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30)
                            MINUS_HOLD = Menu_Button(1430,500,"-", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30)
                            win.blit(MENU_FONT_S.render("Hold",True,BLACK),MENU_FONT_S.render("Hold",True,BLACK).get_rect(center=(1260,515)))
                            PLUS_SELL = Menu_Button(1340,550,"+", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30)
                            MINUS_SELL = Menu_Button(1430,550,"-", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30)
                            win.blit(MENU_FONT_S.render("Sell",True,BLACK),MENU_FONT_S.render("Sell",True,BLACK).get_rect(center=(1260,565)))
                            PLUS_TRADE = Menu_Button(1340,600,"+", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30)
                            MINUS_TRADE = Menu_Button(1430,600,"-", MENU_FONT_XXS, GREY, LIGHTISH_GREY, 30,30)
                            win.blit(MENU_FONT_S.render("Trade",True,BLACK),MENU_FONT_S.render("Trade",True,BLACK).get_rect(center=(1267,615)))
                            for j in range(3):
                                pygame.draw.rect(win,LIGHTISH_GREY,(1370,j*50+500,60,30))
                                pygame.draw.rect(win,WHITE,(1372,j*50+502,56,26))
                            holding_meter = MENU_FONT_XXS.render(str(holding_stocks),True,BLACK)
                            holding_meter_rect = holding_meter.get_rect(center=(1398,515))
                            win.blit(holding_meter,holding_meter_rect)
                            selling_meter = MENU_FONT_XXS.render(str(selling_stocks),True,BLACK)
                            selling_meter_rect = selling_meter.get_rect(center=(1398,565))
                            win.blit(selling_meter,selling_meter_rect)
                            trading_meter = MENU_FONT_XXS.render(str(trading_stocks),True,BLACK)
                            trading_meter_rect = trading_meter.get_rect(center=(1398,615))
                            win.blit(trading_meter,trading_meter_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(game.owned_stocks[order[merging_turn]][merging_co_index]),True,color_list[merging_co_index])
                            turn_title_rect = turn_title.get_rect(center=(1350,430))
                            win.blit(turn_title,turn_title_rect)
                            pygame.draw.rect(win,color_list[merging_co_index],(1230,650,100,70))
                            pygame.draw.rect(win,light_color_list[merging_co_index],(1235,655,90,60))
                            win.blit(MENU_FONT_XS.render("$"+str(game.stock_prices[merging_co_index]),True,WHITE),MENU_FONT_XS.render("$"+str(game.stock_prices[merging_co_index]),True,WHITE).get_rect(center=(1280,685)))
                            pygame.draw.rect(win,color_list[absorbing_co_index],(1400,650,70,70))
                            pygame.draw.rect(win,light_color_list[absorbing_co_index],(1405,655,60,60))
                            win.blit(MENU_FONT_XS.render(str(game.total_stocks[absorbing_co_index]),True,WHITE),MENU_FONT_XS.render(str(game.total_stocks[absorbing_co_index]),True,WHITE).get_rect(center=(1435,685)))
                        elif order[merging_turn] == order[-1] and remaining_stocks == 0:
                            game.owned_stocks[order[merging_turn]][merging_co_index] = holding_stocks
                            run = False
                        elif remaining_stocks == 0:
                            game.owned_stocks[order[merging_turn]][merging_co_index] = holding_stocks
                            merging_turn += 1
                            remaining_stocks = game.owned_stocks[order[merging_turn]][merging_co_index]
                            holding_stocks = 0
                            selling_stocks = 0
                            trading_stocks = 0
                            turn_title.fill(ANTIQUE_WHITE)
                            win.blit(turn_title,turn_title_rect)
                            turn_title = MENU_FONT_XXS.render(str(game.player_names[order[merging_turn]]) + "'S stocks: " + str(game.owned_stocks[order[merging_turn]][merging_co_index]),True,color_list[merging_co_index])
                            turn_title_rect = turn_title.get_rect(center=(1350,430))
                            win.blit(turn_title,turn_title_rect)
                            pygame.draw.rect(win,ANTIQUE_WHITE,(1210,790,280,20))
                            trading_meter.fill(WHITE)
                            win.blit(trading_meter,trading_meter_rect)
                            trading_meter = MENU_FONT_XXS.render(str(trading_stocks),True,BLACK)
                            win.blit(trading_meter,trading_meter_rect)
                            selling_meter.fill(WHITE)
                            win.blit(selling_meter,selling_meter_rect)
                            selling_meter = MENU_FONT_XXS.render(str(selling_stocks),True,BLACK)
                            win.blit(selling_meter,selling_meter_rect)
                            holding_meter.fill(WHITE)
                            win.blit(holding_meter,holding_meter_rect)
                            holding_meter = MENU_FONT_XXS.render(str(holding_stocks),True,BLACK)
                            win.blit(holding_meter,holding_meter_rect)
                        else:
                            win.blit(MENU_FONT_XXS.render("Allocate all of your stocks first",True,RED),MENU_FONT_XXS.render("Allocate all of your stocks first",True,RED).get_rect(center=(1350,800)))
            if order[merging_turn] == order[-1]:
                NEXT_PLAYER = Menu_Button(1200,820,"FINISH MERGER!!", MENU_FONT_XS, GREY, LIGHTISH_GREY,300,80)
            if started:
                PLUS_HOLD.draw_menu_button(win)
                MINUS_HOLD.draw_menu_button(win)
                PLUS_HOLD.update_menu_button(win,x,y)
                MINUS_HOLD.update_menu_button(win,x,y)
                PLUS_SELL.draw_menu_button(win)
                MINUS_SELL.draw_menu_button(win)
                PLUS_SELL.update_menu_button(win,x,y)
                MINUS_SELL.update_menu_button(win,x,y)
                PLUS_TRADE.draw_menu_button(win)
                MINUS_TRADE.draw_menu_button(win)
                PLUS_TRADE.update_menu_button(win,x,y)
                MINUS_TRADE.update_menu_button(win,x,y)
            NEXT_PLAYER.update_menu_button(win,x,y)
            pygame.display.update()

        pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
    return []


def round_up(n, decimals = 0):
    multiplier = 10 ** decimals
    return int(math.ceil(n * multiplier) / multiplier)

def game_over(win,game):
    win.fill(ANTIQUE_WHITE)
    pygame.draw.rect(win,ANTIQUE_WHITE,(1203,300,297,600))
    game.count_tiles()
    clock = pygame.time.Clock()
    running = True
    for i in range(7):
        final_count(win,game,i,i*214.28)
    rankings = []
    for j in range(len(game.player_names)):
        top = game.player_names[game.balances.index(max(game.balances))]
        rankings.append([top,max(game.balances)])
        game.balances.remove(max(game.balances))
        game.player_names.remove(rankings[j][0])
    count = -1
    going = True
    while going:
        if count*-1 != len(rankings):
            if rankings[count-1][1] == rankings[count][1]:
                rankings[count][0] = rankings[count-1][0] + " and " + rankings[count][0]
                rankings.remove(rankings[count-1])
        count -= 1
        if count*-1 == len(rankings)+1:
            going = False

    place_strings = ["1st", "2nd", "3rd", "4th", "5th","6th"]
    place_strings = place_strings[:len(rankings)]
    count = -1
    if len(rankings) <= 2:
        NEXT_PLACE = Menu_Button(350,795,"FIRST PLACE",MENU_FONT,GREY,LIGHTISH_GREY,800,100)
        nextup = rankings[0]
    else:
        NEXT_PLACE = Menu_Button(350,795,"LAST PLACE",MENU_FONT,GREY,LIGHTISH_GREY,800,100)
        nextup = rankings[count]

    while running:
        clock.tick(FPS)
        NEXT_PLACE.draw_menu_button(win)
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEXT_PLACE.check_for_click() and count*-1 != len(rankings)+1:
                    win.fill(ANTIQUE_WHITE)
                    if rankings[count] != rankings[0]:
                        if rankings[count-1] == rankings[0]:
                            NEXT_PLACE = Menu_Button(350,795,"FIRST PLACE",MENU_FONT,GREY,LIGHTISH_GREY,800,100)
                        else:
                            NEXT_PLACE = Menu_Button(350,795,"NEXT PLACE",MENU_FONT,GREY,LIGHTISH_GREY,800,100)

                    win.blit(MENU_FONT_M.render("In " + place_strings[count] + " Place:",True,BLACK),MENU_FONT_M.render("In " + place_strings[count] + "Place:",True,BLACK).get_rect(center=(750,200)))
                    win.blit(MENU_FONT.render(rankings[count][0],True,BLACK),MENU_FONT.render(rankings[count][0],True,BLACK).get_rect(center=(750,400)))
                    win.blit(MENU_FONT_M.render("$"+str(rankings[count][1]),True,GREEN),MENU_FONT_M.render("$"+str(rankings[count][1]),True,GREEN).get_rect(center=(750,600)))
                    count -= 1
                

                    #win.blit(MENU_FONT)
                    #display will happen
        NEXT_PLACE.update_menu_button(win,x,y)
        pygame.display.update()


def final_count(win,game,co_index,x):
    color_list = [RED,BLUE,GREEN,YELLOW,TEAL,PURPLE,ORANGE]
    light_color_list = [LIGHTISH_RED,LIGHTISH_BLUE,LIGHTISH_GREEN,LIGHTISH_YELLOW,LIGHTISH_TEAL,LIGHTISH_PURPLE,LIGHTISH_ORANGE]
    co_names = ["RED","BLUE","GREEN","YELLOW","TEAL","PURPLE","ORANGE"]
    if game.number_of_tiles[co_index] == 0:
        pygame.draw.rect(win, color_list[co_index],(x+3,50,210,110))
        pygame.draw.rect(win, light_color_list[co_index],(x+8,55,200,100))
        win.blit(MENU_FONT_lilS.render(str(co_names[co_index]),True,WHITE),MENU_FONT_lilS.render(str(co_names[co_index]),True,WHITE).get_rect(center=(x+106.5,105)))
        win.blit(MENU_FONT_XXS.render("Not on the board",True,BLACK),MENU_FONT_XXS.render("Not on the board",True,BLACK).get_rect(center=(x+106.5,200)))
    else:
        players_involved = []
        stocks_involved = []
        big_winners = []
        smaller_winners = []
        stock_payout = []
        for j in range(len(game.owned_stocks)):
            if game.owned_stocks[j][co_index] > 0:
                players_involved.append(j)
                stocks_involved.append(game.owned_stocks[j][co_index])
        second = None
        second_tie = None
        biggest = stocks_involved[0]
        tie = 0

        game.stock_prices[co_index]
        for j in range(len(players_involved)):
            stock_payout.append(game.stock_prices[co_index]*game.owned_stocks[players_involved[j]][co_index])
            game.balances[players_involved[j]] += stock_payout[j]




        if len(stocks_involved) == 1:
            game.balances[players_involved[0]] += game.first_bonus[co_index] + game.second_bonus[co_index]
            big_winners.append(players_involved[0])
        else:
            for j in range(len(stocks_involved)):
                if stocks_involved[j] > biggest:
                    biggest = stocks_involved[j]
            for j in range(len(stocks_involved)):
                if biggest == stocks_involved[j]:
                    tie += 1 
            if tie > 1:
                for j in range(len(stocks_involved)):
                    if stocks_involved[j] == biggest:
                        game.balances[players_involved[j]] += int(round_up(game.first_bonus[co_index]/tie,-2)) + int(round_up(game.second_bonus[co_index]/tie,-2))
                        big_winners.append(players_involved[j])
            else:
                game.balances[players_involved[stocks_involved.index(biggest)]] += game.first_bonus[co_index]
                big_winners.append(players_involved[stocks_involved.index(biggest)])
            if tie < 2:
                second_tie = 0
                q = 1
                second = stocks_involved[0]
                while second == biggest:
                    second = stocks_involved[0+q]
                    q += 1
                for j in range(len(stocks_involved)):
                    if stocks_involved[j] > second and stocks_involved[j] != biggest:
                        second = stocks_involved[j]
                for j in range(len(stocks_involved)):
                    if second == stocks_involved[j]:
                        second_tie += 1
                if second_tie > 1:
                    for j in range(len(stocks_involved)):
                        if stocks_involved[j] == second:
                           game.balances[players_involved[j]] += int(round_up(game.second_bonus[co_index]/second_tie,-2))
                           smaller_winners.append(players_involved[j])
                else:
                    game.balances[players_involved[stocks_involved.index(second)]] += game.second_bonus[co_index]
                    smaller_winners.append(players_involved[stocks_involved.index(second)])
        pygame.draw.rect(win, color_list[co_index],(x+3,50,210,110))
        pygame.draw.rect(win, light_color_list[co_index],(x+8,55,200,100))
        win.blit(MENU_FONT_lilS.render(str(co_names[co_index]),True,WHITE),MENU_FONT_lilS.render(str(co_names[co_index]),True,WHITE).get_rect(center=(x+106.5,105)))
        for j in range(len(game.player_names)):
            win.blit(MENU_FONT_XS.render(str(game.player_names[j]) + ":",True,BLACK),MENU_FONT_XS.render(str(game.player_names[j]) + ":",True,BLACK).get_rect(center=(x+95,j*29.5+180)))
            if game.owned_stocks[j][co_index] > 0:
                win.blit(MENU_FONT_XS.render(str(game.owned_stocks[j][co_index]),True,color_list[co_index]),MENU_FONT_XS.render(str(game.owned_stocks[j][co_index]),True,color_list[co_index]).get_rect(center=(x+200,j*29.5+180)))
            else:
                win.blit(MENU_FONT_XS.render(str(game.owned_stocks[j][co_index]),True,BLACK),MENU_FONT_XS.render(str(game.owned_stocks[j][co_index]),True,BLACK).get_rect(center=(x+200,j*29.5+180)))
        win.blit(MENU_FONT_XlilS.render("Majority Holders",True,BLACK),MENU_FONT_XlilS.render("Majority Holders",True,BLACK).get_rect(center=(x+106.5,len(game.player_names)*27.5+205)))#adding 20
        pygame.draw.line(win,color_list[co_index],(x+10.5,len(game.player_names)*27.5+220),(x+205.5,len(game.player_names)*27.5+220),3)
        if second_tie != None:
            win.blit(MENU_FONT_XlilS.render("Minority Holders",True,BLACK),MENU_FONT_XlilS.render("Minority Holders",True,BLACK).get_rect(center=(x+106.5,(len(game.player_names)*27.5+180)+len(big_winners)*27.5+60)))
            pygame.draw.line(win,color_list[co_index],(x+10.5,(len(game.player_names)*27.5+180)+len(big_winners)*27.5+75),(x+205.5,(len(game.player_names)*27.5+180)+len(big_winners)*27.5+75),3)
            for j in range(len(big_winners)):
                win.blit(MENU_FONT_XXS.render(str(game.player_names[big_winners[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[big_winners[j]])+":",True,BLACK).get_rect(center=(x+70,j*25+(len(game.player_names)*27.5+235))))
                win.blit(MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[co_index]/tie,-2))),True,GREEN),MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[co_index]/tie,-2))),True,GREEN).get_rect(center=(x+170,j*25+(len(game.player_names)*27.5+235))))
            for j in range(len(smaller_winners)):
                win.blit(MENU_FONT_XXS.render(str(game.player_names[smaller_winners[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[smaller_winners[j]])+":",True,BLACK).get_rect(center=(x+70,j*25+((len(game.player_names)*27.5+180)+len(big_winners)*27.5+90))))
                win.blit(MENU_FONT_XXS.render("+$" + str(int(round_up(game.second_bonus[co_index]/second_tie,-2))),True,GREEN),MENU_FONT_XXS.render("+$" + str(int(round_up(game.second_bonus[co_index]/second_tie,-2))),True,GREEN).get_rect(center=(x+170,j*25+((len(game.player_names)*27.5+180)+len(big_winners)*27.5+90))))
            bottom = j*25+((len(game.player_names)*27.5+180)+len(big_winners)*27.5+90)
        else:
            for j in range(len(big_winners)):
                win.blit(MENU_FONT_XXS.render(str(game.player_names[big_winners[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[big_winners[j]])+":",True,BLACK).get_rect(center=(x+70,j*25+(len(game.player_names)*27.5+235))))
                win.blit(MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[co_index]/len(big_winners),-2)) + int(round_up(game.second_bonus[co_index]/len(big_winners),-2))),True,GREEN),MENU_FONT_XXS.render("+$" + str(int(round_up(game.first_bonus[co_index]/len(big_winners),-2)) + int(round_up(game.second_bonus[co_index]/len(big_winners),-2))),True,GREEN).get_rect(center=(x+170,j*25+(len(game.player_names)*27.5+235))))
            bottom = j*25+(len(game.player_names)*27.5+235)
        win.blit(MENU_FONT_XlilS.render("Stock Price:",True,BLACK),MENU_FONT_XlilS.render("Stock Price:",True,BLACK).get_rect(center=(x+75,bottom+40)))
        pygame.draw.line(win,color_list[co_index],(x+10.5,bottom+55),(x+205.5,bottom+55),3)
        win.blit(MENU_FONT_XlilS.render("$" + str(game.stock_prices[co_index]),True,GREEN),MENU_FONT_XlilS.render("$" + str(game.stock_prices[co_index]),True,GREEN).get_rect(center=(x+175,bottom+40)))
        for j in range(len(players_involved)):
            win.blit(MENU_FONT_XXS.render(str(game.player_names[players_involved[j]])+":",True,BLACK),MENU_FONT_XXS.render(str(game.player_names[players_involved[j]])+":",True,BLACK).get_rect(center=(x+70,bottom+70+j*25)))
            win.blit(MENU_FONT_XXS.render("+$"+str(stock_payout[j]),True,GREEN),MENU_FONT_XXS.render("+$"+str(stock_payout[j]),True,GREEN).get_rect(center=(x+160,bottom+70+j*25)))


def load_board(win,game,piece_labels):
    color_list = [GREY,RED,BLUE,GREEN,YELLOW,TEAL,PURPLE,ORANGE]
    l_color_list = [LIGHTISH_GREY,LIGHTISH_RED,LIGHTISH_BLUE,LIGHTISH_GREEN,LIGHTISH_YELLOW,LIGHTISH_TEAL,LIGHTISH_PURPLE,LIGHTISH_ORANGE]
    for col in range(COLS+2):
            for row in range(ROWS+2):
                if game.board[row][col] > 1:
                    draw_piece(win,col*100-50,row*100-50,color_list[game.board[row][col]-2],l_color_list[game.board[row][col]-2])
    game.draw_labels(win,piece_labels)


main_menu(WIN)