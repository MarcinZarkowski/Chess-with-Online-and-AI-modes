import pygame 
import os
from CagnusMarlsen import predict, to_game


# Set the current working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("Current Working Directory set to:", os.getcwd())
from piece import *
from tkinter import *
import time

import sys


from board import Board
from network import Network
import chess



pygame.init()

width=360
height=360
screen= pygame.display.set_mode([width,height])

pygame.display.set_caption("Two Player Chess")


timer=pygame.time.Clock()

rect=(4,4,352,352)
board=pygame.image.load(os.path.join("img","board.png"))
BG=pygame.transform.scale2x(board)


def ClickedPosition(position):
    x,y=position
    col = int(x // (width / 8))
    row = int(y // (height / 8))
    return col, row
   
def Drawtimer(PlayersTime, screen):
        minutes = PlayersTime // 6000
        seconds = PlayersTime % 6000
        timer_text = f"Timer: {minutes}min {seconds//100}sec"
        timer_surface = font.render(timer_text, True, (255, 0, 0))
        screen.blit(timer_surface, (0, 0))
        pygame.display.update()
    
def run_TkinterWindow():

    global chosen
    global finalstring
    

    root = Tk()
    root.title("Promotion Selection")
    e = Entry(root, width=55, borderwidth=5)
    e.insert(0, "Pick promotion, write: Rook, Bishop, Knight, or Queen: ")
    e.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    chosen=False
    
        
       
    def Enter_button():
        global chosen
        global finalstring

        finalstring = e.get()[55:]  # Extracting the input string
        if finalstring not in ["Rook", "Bishop", "Knight", "Queen"]:
            # Handling invalid input
            e.delete(0, END)
            e.insert(0, "Pick promotion, write: Rook, Bishop, Knight, or Queen: ")
            return

        chosen = True
        root.destroy()  # Destroying the Tkinter window after processing input
    
    def WriteInBox(choice):
        e.insert(55, choice)

    button_Bishop=Button(root, text="Bishop", padx=30, pady=10, command=lambda:WriteInBox("Bishop"))
    button_Knight=Button(root, text="Knight", padx=30, pady=10, command=lambda:WriteInBox("Knight"))
    button_Rook=Button(root, text="Rook", padx=30, pady=10, command=lambda:WriteInBox("Rook"))
    button_Queen=Button(root, text="Queen", padx=30, pady=10, command=lambda:WriteInBox("Queen"))
    
    button_enter = Button(root, text="Enter", padx=30, pady=10, command=Enter_button)

    button_enter.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    button_Bishop.grid(row=2, column=0,  padx=10, pady=10)
    button_Rook.grid(row=2, column=1,  padx=10, pady=10)
    button_Knight.grid(row=3, column=0,  padx=10, pady=10)
    button_Queen.grid(row=3, column=1, padx=10, pady=10)
    root.mainloop()

    if chosen:
        return finalstring
    else:
        return "no choice"
    
        









backGround = pygame.Surface(screen.get_size())
font = pygame.font.Font('freesansbold.ttf', 20)
large = pygame.font.Font('freesansbold.ttf', 50)

canBlackcastle=True
canWhitecastle=True



def main(black, white):
    
    

    def CheckMate(bo, ID, black, white):
        from piece import King
        kingfound=False
        for i in range(8):
                for j in range(8):
                    
                    if bo.board[i][j] is not None and bo.board[i][j].color==ID:
                        moves, length=bo.board[i][j].finalvalidMoves(bo, black, white)
                        if length>0:
                            return False
                    if type(bo.board[i][j])== King and bo.board[i][j].color==ID and length>0:
                        kingfound=True
                        if bo.board[i][j].InCheck==False:
                            return False
        return True
    
    def IteratePawnsForPassant(bo, ID):
        from piece import Pawn
        if ID=='w':
            for i in range(8):
                for j in range(8):
                    if type(bo.board[i][j])==Pawn and bo.board[i][j].color=='w' and bo.board[i][j].turn==1 and bo.board[i][j].UsedMove==1:
                        bo.board[i][j].turn+=1

        
        elif ID=='b':  
            for i in range(8):
                for j in range(8):
                    if type(bo.board[i][j])==Pawn and bo.board[i][j].color=='b' and bo.board[i][j].turn==1 and bo.board[i][j].UsedMove==1:
                        bo.board[i][j].turn+=1
   
    def loading(n=None, ID=None) -> bool:
        n = Network()
        ID = n.piece
        while True:
            screen.blit(backGround, (0, 0))
            screen.blit(large.render("Chess", True, (255, 255, 255)), (20, 20))
            screen.blit(font.render("Cancel", True, (255, 0, 0)), (20, 250))

            if ID is not None:
                if ID == "w":
                    screen.blit(font.render("You're white", True, (255, 255, 255)), (20, 150))
                else:
                    screen.blit(font.render("You're black", True, (255, 255, 255)), (20, 150))

                n.getNumOfPlayer()
                if n.NumberofPlayers == 2:
                    pygame.display.flip()
                    return True, n,ID
            else:
                screen.blit(font.render("Searching for connection", True, (255, 255, 255)), (20, 150))
                n.connect()
                ID = n.piece
                time.sleep(1)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if 20 <= pos[0] <= 20+68 and 250 <= pos[1] <= 250+20:
                        return False, n, ID
        
    def menu():
        AI_game=False
        online_game=False
        while True:
            screen.blit(backGround, (0, 0))
            screen.blit(large.render("Chess", True, (255, 255, 255)), (20, 20))
            screen.blit(font.render("Play Against AI", True, (255, 0, 0)), (20, 150))
            screen.blit(font.render("Play Online", True, (255, 0, 0)), (20, 250))

            if online_game :
                return n,ID , "online"
            elif AI_game:
                return n, ID, "AI"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if 20 <= pos[0] <= 171 and 150 <= pos[1] <= 171:
                        AI_game = True
                        n=1
                        ID='w'
                    elif 20 <= pos[0] <= 132 and 250 <= pos[1] <= 270:
                        stop,n,ID = loading()
                        if stop:
                            online_game = True
                            break

            pygame.display.update()


    def start_game(n,ID,game_type):

        board_to_uci={0:'a',
                      1:'b',
                     2:'c',
                     3:'d',
                     4:'e',
                     5:'f',
                     6:'g',
                     7:'h',
        }

        run=True
    
        canBlackcastle=black
        canWhitecastle=white
    
    
        selected=False
        if game_type=="online":
            bo=n.getBoard()
        elif game_type=="AI":
            
            bo=Board(8,8)
            board_for_AI=chess.Board()
            promotion_to_uci={"Rook":'r', "Bishop":'b', "Queen":'q', "Knight":'n'}#used to represent promotion of pawns in UCI format for AI. 
            startTime=time.time()

        updatedboard=False
        updatedPawns=False

        elapsed_time=0
        PlayersTime=150*600
        ActivePlayer='w'
        print("This is a ",game_type, "game")
        while run :
            
            #getting moves from AI
            #if game_type=="AI":

            
            if game_type=="online":
                n.getNumOfPlayer()
                if n.NumberofPlayers<2:
                    screen.blit(large.render("Opponent", True, (255, 0, 0)), (10, 150))
                    screen.blit(large.render("Disconnected", True, (255, 0, 0)), (10, 225))
                    pygame.display.update()
                    time.sleep(2)

                    n.disconnect()
                    return
                ActivePlayer=n.getCurrentTurn()

               
            

            screen.blit(BG, (0,0))
            bo.draw(screen, bo, canBlackcastle,canWhitecastle)  
              
           # if game_type=="AI":
              #  if 
            if (game_type=="online" and ActivePlayer==ID) or (game_type=="AI" and ActivePlayer=="w"):
                
                if updatedboard==False and game_type=="online":
                    bo=n.getBoard()
                    updatedboard=True
                    startTime=time.time()
                
                elapsed_time=time.time()-startTime 
                PlayersTime-=elapsed_time
                
            
            if game_type=="online":    
                if PlayersTime<=0:
                    screen.blit(large.render("Time's up", True, (255, 0, 0)), (10, 150))
                    screen.blit(large.render("You Lost", True, (255, 0, 0)), (10, 225))
                   
                    n.oponentWins(ID,"Time")
                    pygame.display.update()
                    time.sleep(2)
                    
                    n.disconnect()
                    return
            pygame.display.update()
           
            
            if game_type=="online":  
                n.getGameState()

                if n.whoWon==ID:
                    screen.blit(large.render("You Won", True, (255, 0, 0)), (10, 150))
                    screen.blit(font.render("By "+n.HowWon, True, (255, 0, 0)), (10, 225))
                            
                    pygame.display.update()
                    time.sleep(2)

                    n.disconnect()
                    return
                Drawtimer(PlayersTime, screen)
           
            timer.tick(20)  

            for event in pygame.event.get():
                
                    
                
                if event.type == pygame.QUIT:
                    
                    run=False
                    pygame.quit()
                    sys.exit()
                   
                
                
                if (event.type==pygame.MOUSEBUTTONDOWN and game_type=="online" and ID==ActivePlayer)or (event.type==pygame.MOUSEBUTTONDOWN and game_type=="AI" and ActivePlayer=="w"):
                    if updatedPawns==False:
                        IteratePawnsForPassant(bo,ID)
                        if CheckMate(bo,ID,canBlackcastle,canWhitecastle ):
                            screen.blit(large.render("CheckMate", True, (255, 0, 0)), (10, 150))
                            screen.blit(large.render("You Lost", True, (255, 0, 0)), (10, 225))
                            if game_type=="online":
                                n.oponentWins(ID,"CheckMate")
                                
                            pygame.display.update()
                            time.sleep(2)
                            if game_type=="online":#gives time to send message to server and then disconnect
                                n.disconnect()
                            return
                        
                        updatedPawns=True
            
                        
                    position=pygame.mouse.get_pos()
                    col, row=ClickedPosition(position)
                    
                    
                    from piece import King
                

                    if bo.board[row][col] is not None  and selected==True:
                    
                        foundcapture=0
                        
                        
                        xcoord=movingpiece.x
                        ycoord=movingpiece.y
                        if type(movingpiece)!=King:
                            validMoves, size= movingpiece.finalvalidMoves(bo, canBlackcastle, canWhitecastle)    
                        else:
                            validMoves, size= movingpiece.validMoves(bo, canBlackcastle, canWhitecastle) 
                        
                        for x in range(size):
                            movesX, movesY=validMoves[x]
                            if row==movesY and col ==movesX :
                                
                                movingpiece.x=col
                                movingpiece.y=row
                                bo.board[row][col]=movingpiece
                                bo.board[ycoord][xcoord]=None
                                bo.board[row][col].selected=False

                                if game_type=="AI":
                                    move_uci=move_uci[:2]+board_to_uci[col]+str(8-row)

                                from piece import Pawn

                                
                                if type(movingpiece)==Pawn:
                                    movingpiece.turn+=1
                                    

                                
                                    

                                    

                                from piece import Rook

                                if  type(movingpiece)== Rook:
                                
                                    ThisPiece=bo.board[row][col]
                                
                                    ThisPiece.CanCastle=False
                                
                                if type(movingpiece)==King:
                                    if movingpiece.color=='b':
                                        canBlackcastle=False
                                    elif movingpiece.color=='w':
                                        canWhitecastle=False
                                    
                                
                                
                                
                                
                                '''if TurnPiece==0:
                                    TurnPiece=1
                                elif TurnPiece==1:
                                    TurnPiece=0'''
                                
                                
                                foundcapture=1
                                
                                if type(movingpiece)==Pawn:
                                    from piece import Knight
                                    from piece import Bishop
                                    
                                    from piece import Queen
                                    
                            
                                    if movingpiece.color=='w':
                                        if movingpiece.y==0:    
                                            while(True):
                                                PieceChosen=run_TkinterWindow( )
                                                
                                                if PieceChosen=="Rook":
                                                    bo.board[row][col]=Rook(col, row, 'w')                                                   
                                                    break
                                                elif PieceChosen=="Bishop":
                                                    bo.board[row][col]=Bishop(col, row, 'w')                                                  
                                                    break
                                                elif PieceChosen=="Queen":
                                                    bo.board[row][col]=Queen(col, row, 'w')                                                   
                                                    break
                                                elif PieceChosen=="Knight":
                                                    bo.board[row][col]=Knight(col, row, 'w')                                                
                                                    break
                                                elif PieceChosen=="no choice":
                                                    pass

                                            if game_type=="AI":
                                                move_uci=move_uci[:2]+board_to_uci[bo.board[row][col].x]+str(8-bo.board[row][col].y)+promotion_to_uci[PieceChosen]            
                                                print(move_uci)
                                                

                                    elif movingpiece.color=='b':
                                        if movingpiece.y==7:
                                            
                                                
                                            while(True):
                                                PieceChosen=run_TkinterWindow()
                                                if PieceChosen=="Rook":
                                                    bo.board[row][col]=Rook(col, row, 'b')                                                  
                                                    break
                                                elif PieceChosen=="Bishop":
                                                    bo.board[row][col]=Bishop(col, row, 'b')                                                   
                                                    break
                                                elif PieceChosen=="Queen":
                                                    bo.board[row][col]=Queen(col, row, 'b')                                                 
                                                    break
                                                elif PieceChosen=="Knight":
                                                    bo.board[row][col]=Knight(col, row, 'b')                                                   
                                                    break                                              
                                                elif PieceChosen=="no choice":
                                                    pass

                                            if game_type=="AI":
                                                move_uci=move_uci[:2]+board_to_uci[bo.board[row][col].x]+str(8-bo.board[row][col].y)+promotion_to_uci[PieceChosen]                                                                    
                                                print(move_uci) 


                                                    
                                                
                                
                                if game_type=="online":
                                    n.send(bo) 
                                    ActivePlayer=n.getCurrentTurn()
                                updatedboard=False
                                selected=False
                                if game_type=="AI":

                                    board_for_AI.push(chess.Move.from_uci(move_uci))
                                
                                    AI_move=predict(board_for_AI)
                                    print("move generated", AI_move)
                                    if AI_move==None:
                                        screen.blit(large.render("You Won", True, (255, 0, 0)), (10, 150))
                                        screen.blit(font.render("By Checkmate", True, (255, 0, 0)), (10, 225))
                                        pygame.display.update()
                                        time.sleep(2)
                                        return
                                    board_for_AI.push(chess.Move.from_uci(AI_move))
                                    print(board_for_AI)
                                    time.sleep(1)#so moves aren't instant
                                    bo=to_game(board_for_AI)
                                updatedPawns=False 
                                        
                                break
                                        
                        if foundcapture!=1 and bo.board[row][col].color==ID:
                            for i in range(8):
                                for j in range(8):
                                    if bo.board[i][j]is not None:
                                        bo.board[i][j].selected=False
                                        
                                    
                        

                            bo.board[row][col].selected=True
                            if game_type=="AI":
                                move_uci=board_to_uci[bo.board[row][col].x]+str(8 - bo.board[row][col].y )
                                print(move_uci,chr(bo.board[row][col].y + 1))
                            movingpiece=bo.board[row][col]
                            selected =True
                            foundcapture=0
                        
                        
                    
                    elif bo.board[row][col] is not None and bo.board[row][col].selected==False and bo.board[row][col].color==ActivePlayer:
                        for i in range(8):
                            for j in range(8):
                                if bo.board[i][j]is not None:
                                    bo.board[i][j].selected=False
                                    
                                
                                

                        bo.board[row][col].selected=True
                        if game_type=="AI":
                            move_uci=board_to_uci[bo.board[row][col].x]+str(8 - bo.board[row][col].y )
                            print(move_uci)
                        foundcapture=0
                        selected =True
                        movingpiece=bo.board[row][col]
                        
                        
                        
                    
                    
            

                    elif bo.board[row][col]==None and selected==True:#if user clicks on empty space and a piece is selected
                    
                        if type(movingpiece)!=King:
                            validMoves, size= movingpiece.finalvalidMoves(bo, canBlackcastle, canWhitecastle)    
                        else:
                            validMoves, size= movingpiece.validMoves(bo, canBlackcastle, canWhitecastle) 

                        xcoord=movingpiece.x
                        ycoord=movingpiece.y
                        for x in range(size):
                            movesX, movesY=validMoves[x]
                            if row==movesY and col ==movesX :
                        
                                movingpiece.selected=False
                                movingpiece.x=col
                                movingpiece.y=row
                                bo.board[row][col]=movingpiece
                                bo.board[ycoord][xcoord]=None
                                from piece import Pawn
                                from piece import Rook
                                if type(movingpiece)==Pawn:
                                    movingpiece.turn+=1

                                    if movingpiece.color=='b':
                                        if ycoord==row-2:
                                            movingpiece.UsedMove=1
                                        
                                    elif movingpiece.color=='w':
                                        if ycoord==row+2:
                                            movingpiece.UsedMove=1
                                            


                                    if movingpiece.color=='w':
                                        if row==ycoord-1 and col==xcoord-1:
                                            bo.board[row+1][col]=None
                                            
                                        elif row==ycoord-1 and col==xcoord+1:
                                            bo.board[row+1][col]=None
                                            
                                    elif movingpiece.color=='b':
                                        if row==ycoord+1 and col==xcoord-1:
                                            bo.board[row-1][col]=None
                                            
                                        elif row==ycoord+1 and col==xcoord+1:
                                            bo.board[row-1][col]=None
                                        

                                if  type(movingpiece)== Rook:
                                
                                    ThisPiece=bo.board[row][col]
                                
                                    ThisPiece.CanCastle=False
                                    
                                if type(movingpiece)==King:
                                    if movingpiece.color=='b':
                                        canBlackcastle=False
                                    elif movingpiece.color=='w':
                                        canWhitecastle=False
                                
                                if type(movingpiece)==King:
                                    if movingpiece.color=='b':
                                        if xcoord==col+2:
                                            RookHolder=bo.board[0][0]
                                            RookHolder.y=ycoord
                                            RookHolder.x=col+1
                                            bo.board[ycoord][col+1]=RookHolder
                                            bo.board[0][0]=None
                                            bo.board[ycoord][col+1].CanCastle=False
                                            movingpiece.CanCastle=False
                                        elif xcoord==col-2:
                                            RookHolder=bo.board[0][7]
                                            RookHolder.y=ycoord
                                            RookHolder.x=col-1
                                            bo.board[ycoord][col-1]=RookHolder
                                            bo.board[0][7]=None
                                            bo.board[ycoord][col-1].CanCastle=False
                                            movingpiece.CanCastle=False
                                    elif movingpiece.color=='w':
                                        if xcoord==col+2:
                                            RookHolder=bo.board[7][0]
                                            RookHolder.y=ycoord
                                            RookHolder.x=col+1
                                            bo.board[ycoord][col+1]=RookHolder
                                            bo.board[7][0]=None
                                            bo.board[ycoord][col+1].CanCastle=False
                                            movingpiece.CanCastle=False
                                        elif xcoord==col-2:
                                            RookHolder=bo.board[7][7]
                                            RookHolder.y=ycoord
                                            RookHolder.x=col-1
                                            bo.board[ycoord][col-1]=RookHolder
                                            bo.board[7][7]=None
                                            bo.board[ycoord][col-1].CanCastle=False
                                            movingpiece.CanCastle=False

                                if type(movingpiece)==Pawn:
                                    from piece import Knight
                                    from piece import Bishop
                                    from piece import Rook
                                    from piece import Queen
                                    
                                    
                                    if movingpiece.color=='w':
                                        if movingpiece.y==0:
                                                 
                                            while(True):
                                                PieceChosen=run_TkinterWindow()
                                                if PieceChosen=="Rook":
                                                    bo.board[row][col]=Rook(col, row, 'w')                                                   
                                                    break
                                                elif PieceChosen=="Bishop":
                                                    bo.board[row][col]=Bishop(col, row, 'w')                                               
                                                    break
                                                elif PieceChosen=="Queen":
                                                    bo.board[row][col]=Queen(col, row, 'w')                                                   
                                                    break
                                                elif PieceChosen=="Knight":
                                                    bo.board[row][col]=Knight(col, row, 'w')                                                  
                                                    break
                                                elif PieceChosen=="no choice":
                                                    pass

                                            if game_type=="AI":
                                                move_uci=move_uci[:2]+board_to_uci[bo.board[row][col].x]+str(8-bo.board[row][col].y)+promotion_to_uci[PieceChosen]
                                               

                                    elif movingpiece.color=='b':
                                        if movingpiece.y==7:
                                            
                                           

                                                
                                            while(True):
                                                PieceChosen=run_TkinterWindow()
                                                if PieceChosen=="Rook":
                                                    bo.board[row][col]=Rook(col, row, 'b')
                                                    break
                                                elif PieceChosen=="Bishop":
                                                    bo.board[row][col]=Bishop(col, row, 'b')                                                   
                                                    break
                                                elif PieceChosen=="Queen":
                                                    bo.board[row][col]=Queen(col, row, 'b')                                                
                                                    break
                                                elif PieceChosen=="Knight":
                                                    bo.board[row][col]=Knight(col, row, 'b')                                                
                                                    break
                                                elif PieceChosen=="no choice":
                                                    pass

                                            if game_type=="AI":
                                                move_uci=move_uci[:2]+board_to_uci[bo.board[row][col].x]+str(8-bo.board[row][col].y)+promotion_to_uci[PieceChosen]
                                               
                                
                                selected=False
                                updatedboard=False
                                updatedPawns=False
                                if game_type=="online":
                                    bo=n.send(bo)
                                    ActivePlayer=n.getCurrentTurn()
                                elif game_type=="AI":
                                    try:
                                        if PieceChosen!=None:
                                             board_for_AI.push(chess.Move.from_uci(move_uci))
                                        print(board_for_AI)
                                        AI_move=predict(board_for_AI)
                                        print("move generated",AI_move)

                                        if AI_move==None:
                                            screen.blit(large.render("You Won", True, (255, 0, 0)), (10, 150))
                                            screen.blit(font.render("By Checkmate", True, (255, 0, 0)), (10, 225))
                                            screen.blit(font.render("", True, (255, 0, 0)), (10, 225))
                                            pygame.display.update()
                                            time.sleep(4)
                                            return

                                        board_for_AI.push(chess.Move.from_uci(AI_move))
                                        print(board_for_AI)
                                        time.sleep(1)
                                        bo=to_game(board_for_AI)
                                    except:
                                        move_uci=move_uci[:2]+board_to_uci[movingpiece.x]+str(8-movingpiece.y)
                                        
                                        board_for_AI.push(chess.Move.from_uci(move_uci))
                                        print(board_for_AI)
                                        AI_move=predict(board_for_AI)
                                        print("move generated",AI_move)

                                        if AI_move==None:
                                            screen.blit(large.render("You Won", True, (255, 0, 0)), (10, 150))
                                            screen.blit(font.render("By Checkmate", True, (255, 0, 0)), (10, 225))
                                            screen.blit(font.render("", True, (255, 0, 0)), (10, 225))
                                            pygame.display.update()
                                            time.sleep(4)
                                            return

                                        board_for_AI.push(chess.Move.from_uci(AI_move))
                                        print(board_for_AI)
                                        time.sleep(1)
                                        bo=to_game(board_for_AI)
                                        #if None player wins
                                
                                    #ActivePlayer='b'
                                break

    while True:
        n,ID,game_type=menu()
        start_game(n,ID,game_type)




    


if __name__ == "__main__":
    main(canBlackcastle,canWhitecastle)


    
