#!/usr/bin/env python
# coding: utf-8

import sqlite3
import random
import time
import os
import glob

class Tic_Tac_Toe:
    def __init__(self):
        # connect to sqlite database
        # check if db already exists
        self.db = glob.glob('tic_tac_toe.db', recursive = True)
        if self.db:
            self.conn = sqlite3.connect(self.db[0])
            self.cursor = self.conn.cursor()

            # fetch data from database
            self.cursor.execute('select * from total_plays')
            self.total_plays = self.cursor.fetchone()[0]

            self.cursor.execute('select name from players')
            self.all_players = []
            for name in self.cursor.fetchall():
                self.all_players.append(name[0])
    
        else: # create a db and 2 tables
            os.system('touch tic_tac_toe.db')
            self.conn = sqlite3.connect('tic_tac_toe.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                'CREATE TABLE players (id integer primary key autoincrement, name varchar(255) not null, win integer default 0, lose integer default 0, tie integer default 0)'
                )
            self.cursor.execute('CREATE TABLE total_plays (count integer default 0)')
            self.cursor.execute('insert into total_plays (count) values (0)')
            # create two variables
            self.total_plays = 0
            self.all_players = []

        self.players = []   
        self.board = {'7': ' ', '8': ' ', '9': ' ',
                      '4': ' ', '5': ' ', '6': ' ',
                      '1': ' ', '2': ' ', '3': ' ',}

        self.sample_keypad = {'7': '7', '8': '8', '9': '9',
                              '4': '4', '5': '5', '6': '6',
                              '1': '1', '2': '2', '3': '3'}

        self.board_keys = self.board.keys()



    def printBoard(self, board_sample):
        print(board_sample['7'] + '|' + board_sample['8'] + '|' + board_sample['9'] ) 
        print('-+-+-')
        print(board_sample['4'] + '|' + board_sample['5'] + '|' + board_sample['6'] )
        print('-+-+-')
        print(board_sample['1'] + '|' + board_sample['2'] + '|' + board_sample['3'] )
        return ''



    def db_update(self, win, lose):
        self.cursor.execute('update players set win= win + 1 where name = "' + win + '"' )
        self.cursor.execute('update players set lose = lose + 1 where name = "' + lose + '"' )
        self.conn.commit()
        return


    
    def greeting(self, player_name):
        if player_name.capitalize() in self.all_players:
            return 'Welcome Back!'
        else:
            try:
                self.cursor.execute('insert into players (name) values ("' + player_name.capitalize() + '")')
                self.conn.commit()
                return 'New player! Welcome!!'
            except:
                return 'New player! Welcome!'




if __name__ == '__main__':
    t = Tic_Tac_Toe()
        
    print('\nTic Tac Toe\n  By C**C\n')
    time.sleep(1)
    if t.total_plays != 0:
        print('Total play count of this game is ' + str(t.total_plays) + '!\n') 
    
    t.player1 = input('Hey you, Player 1!  Enter your name: ')
    t.players.append(t.player1)
    print(t.greeting(t.player1))
    
    
    t.player2 = input('And you, Player 2! Enter your name: ')
    t.players.append(t.player2)
    print(t.greeting(t.player2))

    t.cursor.execute('update total_plays set count = count + 1')
    t.conn.commit()

    
    time.sleep(1)
    
    print(t.player1 + ' vs. ' + t.player2 + '\n')
    
    time.sleep(1)
    print('This game will randomly choose a player to start the game.\n')
    
    time.sleep(2)
    
    
    t.turn = random.choice(t.players)
    t.current_turn = t.turn
    print(t.current_turn + ' will go first!' + '\n')
    
    time.sleep(1)
    
    print('Instruction: ' + '\n' + 'How to put the mark on the grid?' + '\n')
    print(t.printBoard(t.board))
    
    time.sleep(2)
    
    print('Think of the grid as a keypad, like this\n')
    
    time.sleep(1)
    
    print(t.printBoard(t.sample_keypad))
    
    time.sleep(2)
    
    print('Simply type the number that coordinates the square.\n')
    
    time.sleep(2)

    t.winning_count = input('''\nNow, let\'s choose the winning path.\n\nWho will be the winner?\n
    If you prefer "The player who wins the first game." Press 1.
    If you prefer "The player who wins the first three games." Press 3.\n''')
    
    while t.winning_count not in ['1', '3']:
        t.winning_count = input('That is not an option. Please enter either 1 or 3\n')

    t.winning_count = int(t.winning_count)
    t.player1_winning = 0
    t.player2_winning = 0
    
    print('Ready, Set, Go!\n')

    
    while t.winning_count not in (t.player1_winning, t.player2_winning):
        t.count = 0
        t.game_over = False
    
        for i in range(9):       
            print(t.printBoard(t.board) + '\n')
            print(t.current_turn + ', your turn now.\n')
            t.inputs= input('Which number do you choose?\n')
            time.sleep(1)
        
            while t.inputs not in ('1', '2', '3', '4', '5', '6', '7', '8', '9') or t.board[t.inputs]!=' ':
                print('This is not a valid input, Try again!\n')
                time.sleep(1)
                t.inputs= input('Which number do you choose this time?\n')
        
       
            if t.count % 2:
                t.board[t.inputs] = 'O'
                t.count += 1
                if t.current_turn == t.player1:
                    t.current_turn = t.player2
                else: 
                   t.current_turn = t.player1
            else:
                t.board[t.inputs] = 'X'
                t.count += 1
                if t.current_turn == t.player1:
                    t.current_turn = t.player2
                else: 
                    t.current_turn = t.player1
                        
            if t.count >= 5:
                if t.board['7'] == t.board['8'] == t.board['9'] == 'X' or t.board['7'] == t.board['8'] == t.board['9'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['4'] == t.board['5'] == t.board['6'] == 'X' or t.board['4'] == t.board['5'] == t.board['6'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['1'] == t.board['2'] == t.board['3'] == 'X'or t.board['1'] == t.board['2'] == t.board['3'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['1'] == t.board['4'] == t.board['7'] == 'X' or t.board['1'] == t.board['4'] == t.board['7'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['2'] == t.board['5'] == t.board['8'] == 'X' or t.board['2'] == t.board['5'] == t.board['8'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['3'] == t.board['6'] == t.board['9'] == 'X' or t.board['3'] == t.board['6'] == t.board['9'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['7'] == t.board['5'] == t.board['3'] == 'X' or t.board['7'] == t.board['5'] == t.board['3'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break
                elif t.board['9'] == t.board['5'] == t.board['1'] == 'X' or t.board['9'] == t.board['5'] == t.board['1'] == 'O':
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning +=1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning +=1
                    print('Excellent match.\n' + t.winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    time.sleep(2)
                    break  
        
        
        if t.game_over and t.winning_count not in (t.player1_winning, t.player2_winning):       
            t.game_over = False
            t.count = 0
            t.current_turn = t.winner
            for key in t.board.keys():
                t.board[key] = ' '
            print('Next battle.\nHere we go!\n')
        
        elif t.game_over == False:
            print(t.printBoard(t.board))
            print('It\'s a tie!\nGood Game Guys!\n')
            time.sleep(1)
            for player in t.players:
                t.cursor.execute('update players set tie = tie + 1 where name = "' + player.capitalize() + '"')
                t.conn.commit()
            for key in t.board.keys():
                t.board[key] = ' '
            print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
            print('Next battle.\nHere we go!\n')
            t.count = 0
            
                  
    if t.winning_count == t.player1_winning:
        print('Congratulations! '+ t.player1.upper() + ' is the champ!' )
    else:
        print('Congratulations! '+ t.player2.upper() + ' is the champ!' )

    t.cursor.close()
    t.conn.close()
    time.sleep(2)
    

    
    
