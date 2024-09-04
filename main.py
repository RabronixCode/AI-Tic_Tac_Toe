import pygame as pg
import sys
import time
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

XO = 'x'

winner = None
draw = None

width = 400
height = 400

white = (255, 255, 255)

line_color = (0, 0, 0)

board = [[None]*3, [None]*3, [None]*3]
ai_board = [[None]*3, [None]*3, [None]*3]


pg.init()
fps = 30

CLOCK = pg.time.Clock()

# ovo je za display ekrana
screen = pg.display.set_mode((width, height + 100), 0, 32)

# Ovo je za X i O i pocetni
initiating_window = pg.image.load("INIT.png")
x_img = pg.image.load("X.png")
o_img = pg.image.load("O.png")

initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))

def game_initiating_window():

    messagebox.showinfo('Info','Press any button to be the second player')

    # prvi displej
    screen.blit(initiating_window, (0, 0))

    pg.display.update()
    time.sleep(1)
    screen.fill(white)

    # veritkalne linije
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), width=7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    # horizontalne linije
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)

    draw_status()

def draw_status():

    global draw

    if winner is None:
        message = XO.upper() + "'s turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = "Game draw!"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global board, winner, draw
 
    # checking for winning rows
    for row in range(0, 3):
        if((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1)*height / 3 - height / 6),
                         (width, (row + 1)*height / 3 - height / 6),
                         4)
            break
 
    # checking for winning columns
    for col in range(0, 3):
        if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break
 
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
 
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)
 
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
 
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)
 
    if(all([all(row) for row in board]) and winner is None):
        draw = True
    draw_status()
 
 
def drawXO(row, col):
    global board, XO, ai_board
 
    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin
    if row == 1:
        posx = 30
 
    # for the second row, the image
    # should be pasted at a x coordinate
    # of 30 from the game line
    if row == 2:
 
        # margin or width / 3 + 30 from
        # the left margin of the window
        posx = width / 3 + 30
 
    if row == 3:
        posx = width / 3 * 2 + 30
 
    if col == 1:
        posy = 30
 
    if col == 2:
        posy = height / 3 + 30
 
    if col == 3:
        posy = height / 3 * 2 + 30
 
    # setting up the required board
    # value to display
    board[row-1][col-1] = XO
    if (not draw and not winner):
        ai_board[row-1][col-1] = XO
 
        if(XO == 'x'):
            # pasting x_img over the screen
            # at a coordinate position of
            # (pos_y, posx) defined in the
            # above code
            screen.blit(x_img, (posy, posx))
            XO = 'o'
    
        else:
            screen.blit(o_img, (posy, posx))
            XO = 'x'
    pg.display.update()
 
 
def user_click():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()
 
    # get column of mouse click (1-3)
    if(x < width / 3):
        col = 1
 
    elif (x < width / 3 * 2):
        col = 2
 
    elif(x < width):
        col = 3
 
    else:
        col = None
 
    # get row of mouse click (1-3)
    if(y < height / 3):
        row = 1
 
    elif (y < height / 3 * 2):
        row = 2
 
    elif(y < height):
        row = 3
 
    else:
        row = None

    
 
    # after getting the row and col,
    # we need to draw the images at
    # the desired positions
    if(row and col and board[row-1][col-1] is None):
        global XO
        drawXO(row, col)
        check_win()

    if not draw and not winner:
    
        get_best_move(XO)
        check_win()


def get_best_move(XO):

    global ai_board
    maximizer = XO
    best_score = -100
    r = 0
    c = 0


    for row in range(0,3):
        for col in range(0,3):
            if ai_board[row][col] is None:
                ai_board[row][col] = XO
                score = minimax(maximizer, XO, ai_board)
                ai_board[row][col] = None
                if score > best_score:
                    best_score = score
                    r = row
                    c = col
                    
    drawXO(r+1, c+1)
    
 
def minimax(maximizer, player, ai_board):

    win = None
    win = check_win_minimax()

    if player != maximizer and win:
        return -1

    if player == maximizer and win:
        return 1
    
    if(all([all(row) for row in ai_board]) and win is None):
        return 0
    
    
    scores = []
    for row in range(0,3):
        for col in range(0,3):
            if ai_board[row][col] is None:
                ai_board[row][col] = next_player(player)
                scores.append(minimax(maximizer, next_player(player), ai_board))
                ai_board[row][col] = None
                
    
    return max(scores) if player != maximizer else min(scores)
    

def next_player(player):
    if player == 'x':
        return 'o'
    else:
        return 'x' 

def check_win_minimax():

    global ai_board

    for row in range(0, 3):
        if((ai_board[row][0] == ai_board[row][1] == ai_board[row][2]) and (ai_board[row][0] is not None)):
            return True
            
 
    # checking for winning columns
    for col in range(0, 3):
        if((ai_board[0][col] == ai_board[1][col] == ai_board[2][col]) and (ai_board[0][col] is not None)):
            return True
 
    # check for diagonal winners
    if (ai_board[0][0] == ai_board[1][1] == ai_board[2][2]) and (ai_board[0][0] is not None):
        return True
 
    if (ai_board[0][2] == ai_board[1][1] == ai_board[2][0]) and (ai_board[0][2] is not None):
        return True

def reset_game():
    global board, winner, XO, draw, ai_board
    time.sleep(3)
    XO = 'x'
    draw = False
    game_initiating_window()
    winner = None
    board = [[None]*3, [None]*3, [None]*3]
    ai_board = [[None]*3, [None]*3, [None]*3]
    draw_status()
 
 
game_initiating_window()
 
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            user_click()
            if(winner or draw):
                reset_game()
        elif event.type == pg.KEYDOWN:
            get_best_move(XO)
            draw_status()
    pg.display.update()
    CLOCK.tick(fps)