from http import server
import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[" "," "," "],
                      [" "," "," "],
                      [" "," "," "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "0"
        self.winner = None
        self.game_over = False
        self.counter = 0
        
    def host_game(self,host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,port))
        # listen for one connection
        server.listen(1)
        
        
        client, addr = server.accept()
        
        self.you = "X"
        self.opponent = "0"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()
        
    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))
        self.you = "0"
        self.opponent = "X"
        
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        
    def handle_connection(self, client):
        while not self.game_over:
            # your turn
            if self.turn == self.you:
                move = input("Enter a move (row,column): ")
                if self.check_valid_move(move.split(',')):
                    self.apply_move(client,move.split(','),self.you)
                    self.turn = self.opponent
                    client.send(move.encode("utf-8"))
                else:
                    print("Invalid move!")
                
            else:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(client,data.decode("utf-8").split(','),self.opponent)
                    self.turn = self.you
                    
        client.close()
    
    def apply_move(self,client,move,player):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        
        if self.check_if_won():
            if self.winner == self.you:
                print("you win!")
                self.restart(client)
                
                
            elif self.winner == self.opponent:
                print("you loose!")
                self.restart(client)
        else:
            if self.counter == 9:
                print("Its a tie!")
                self.restart(client)
                
    def check_valid_move(self,move):
        return self.board[int(move[0])][int(move[1])] == " "
    
    def check_if_won(self):
        # check rows 
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        # check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True      
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ": 
            self.winner = self.board[0][0]
            self.game_over = True
            return True     
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ": 
            self.winner = self.board[0][2]
            self.game_over = True
            return True    
        
        return False
    
    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("——————————")            
                    
                    
    def restart(self,client):
        restart = input("Do want to play Again?(y/n)")
        if restart == "y" or restart == "Y":  
            game = TicTacToe()
            threading.Thread(target=self.handle_connection, args=(client,)).start()
        else:
            exit()



