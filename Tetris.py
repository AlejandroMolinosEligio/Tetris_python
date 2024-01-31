#####################################
#             TERTIS                # 
#####################################

#####################################
#             IMPORTS               # 
#####################################

from enum import Enum
import random
from pynput import keyboard
from pynput.keyboard import Key
import os
import threading
import time
from playsound import playsound

#####################################
#             OBJECTS             # 
#####################################

class Piece():

    def __init__(self, lista:list,row:int =0,col:int =0) -> None:
        self.piece = lista
        self.row = row
        self.col = col
        self.weight= len(self.piece[0])
        self.height= len(self.piece) 

#####################################
#              THREADS              # 
#####################################
        
def start_counter():

    while True:

        time.sleep(seconds)

        if check_movement(piece.row+1,piece.col):
                piece.row+=1
                update_piece()
                if not check_colision(piece.row,piece.col): update_board()
        else:

            if not check_colision(piece.row,piece.col): update_board()

        print_screen()

        if not end: break

    return None

def start_music():
    while end:
        playsound('./Tetris.mp3')

    return None

#####################################
#               GLOBAL              # 
#####################################

cuadrado_blanco = "⬜"
cuadrado_negro = "⬛"
board_weight=10
board_height=20
piece = Piece([""],0,0)
screen = []
screen_old = []
clear=''
end=True
seconds = 1
x = threading.Thread(target=start_counter)
music = threading.Thread(target=start_music)

#####################################
#             ENUMERATE             # 
#####################################

PICES = {
    1:[[cuadrado_negro,cuadrado_negro],[cuadrado_negro,cuadrado_negro]],
    2:[[cuadrado_negro,cuadrado_negro,cuadrado_negro],[cuadrado_negro,"NaN","NaN"]],
    3:[[cuadrado_negro,cuadrado_negro,cuadrado_negro],["NaN","NaN",cuadrado_negro]],
    4:[[cuadrado_negro,cuadrado_negro,cuadrado_negro],["NaN",cuadrado_negro,"NaN"]],
    5:[[cuadrado_negro,cuadrado_negro,cuadrado_negro]]
}

#####################################
#             FUNCTIONS             # 
#####################################

def create_board(weight: int, height: int)->list:

    return [[cuadrado_blanco]*weight for _ in range(height)]

def print_screen()-> None:

    os.system(str(clear))

    print("\nTETRIS\n")

    for row in screen:
        print("".join(map(str,row)))


def new_piece()->list:

    piece_list = PICES[random.choice(list(PICES.keys()))]

    return Piece(piece_list,
                 2,
                 random.randint(0,board_weight-len(piece_list[0]))         
    )

def update_piece() -> None:

    row_start = 0
    col_start = 0
    row_add = False

    for row in range(board_height):


        for i in range(board_weight):

            if i >= piece.col and i<piece.col+piece.weight and row >piece.row-piece.height and row<=piece.row:
                
                if piece.piece[row_start][col_start]=="NaN": screen[row][i] = screen_old[row][i]
                else: screen[row][i] = piece.piece[row_start][col_start]
                col_start +=1

                row_add = True

            else:
                screen[row][i] = screen_old[row][i]
        
        if row_add:
            row_start+=1
            col_start = 0
            row_add=False


    return None

def check_movement(row,col)->bool:

    # Corner

    corner = col < 0 or col > board_weight-piece.weight

    # Colision

    colision = not corner

    if not colision: return False

    for i,block in enumerate(piece.piece[-1]):
        if block==cuadrado_negro and screen_old[row][col+i]==cuadrado_negro:
            colision = colision and False

    return colision

def check_colision(row,col)->bool:

    if row==board_height-1: return False
    
    colision = True
    row_start = piece.height-1


    for piece_list in piece.piece:

        for i,block in enumerate(piece_list):
            if block == '⬛' and screen_old[row+1-row_start][col+i]=='⬛':
                colision = colision and False
            else:
                pass
                
        row_start-=1


    return colision

def update_board()->None:

    global screen_old
    global piece
    global end

    screen_old = [i.copy() for i in screen]

    piece = new_piece()

    check_score()

    for lista in screen_old[:3]:
        for item in lista:
            if item==cuadrado_negro: 
                print("END GAME")
                end = False
                exit()

    update_piece()

    return None

def check_score():

    global screen
    global screen_old
    global end
    global seconds
    global x

    delete=[]

    for i,lista in enumerate(screen):
        check = True

        for block in lista:
            check = check and block==cuadrado_negro

        if check: delete.append(i)

    screen_old = [[cuadrado_blanco]*board_weight for _ in range(len(delete))]
    screen_old = screen_old + [screen[i].copy() for i in range(len(screen)) if i not in delete]

    screen = [i.copy() for i in screen_old]

    if len(delete)>0: 
        seconds = seconds-0.1*len(delete)
        


    return None

def rotate_piece():

    global piece

    list_pieces = []

    for i in range(len(piece.piece[0])-1,-1,-1):
        list_aux = []
        for j in range(len(piece.piece)):
            list_aux.append(piece.piece[j][i])
        list_pieces.append(list_aux)

    pieceaux = Piece(list_pieces,
                 piece.row,
                 piece.col)
    
    rowaux = -1

    for list in list_pieces:
        for i in range(len(list)):
            if list[i]==cuadrado_negro and screen_old[pieceaux.row-rowaux][pieceaux.col+i]==cuadrado_negro: return None
        rowaux+=1    

    piece = Piece(pieceaux.piece,pieceaux.row,pieceaux.col)

    update_piece()

    return None

def move_piece(key):

    global end

    if key == Key.right:
        if check_movement(piece.row,piece.col+1):
            piece.col+=1
            update_piece()
    elif key == Key.left:
        if check_movement(piece.row,piece.col-1):
            piece.col-=1
            update_piece()
    elif key == Key.down:
        if check_movement(piece.row+1,piece.col):
            piece.row+=1
            update_piece()
            if not check_colision(piece.row,piece.col): update_board()
    elif key == Key.up:
        rotate_piece()
    elif key == Key.esc:
        end = False
        exit()

    print_screen()
    

    return None

if __name__=='__main__':

    if os.name=='posix':
        clear = 'clear'
    else:
        clear = 'cls'

    #music.start()

    screen = create_board(board_weight,board_height)
    screen_old = [lista.copy() for lista in screen]
    piece = new_piece()
    update_piece()

    print_screen()

    x.start()

    with keyboard.Listener(on_press=move_piece) as listener:
        listener.join()




'''

END GAME

FALTA SCORE

'''