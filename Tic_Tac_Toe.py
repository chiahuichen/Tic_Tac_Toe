#!/usr/bin/env python
# coding: utf-8
import sqlite3
import random
import time
import os
import glob
from collections import deque

class Tic_Tac_Toe:
    def __init__(self):
        # connect to sqlite database
        # check if db already exists
        self.db = glob.glob('tic_tac_toe.db', recursive=True)
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
        self.mode = 2
        self.previous_track = []
        self.current_track = []
        self.cpu_track = []
        self.count = 0
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


    def db_update(self, win, lose):
        if win:
            self.cursor.execute('update players set win= win + 1 where name = "' + win + '"' )
        if lose:
            self.cursor.execute('update players set lose = lose + 1 where name = "' + lose + '"' )
        self.conn.commit()
        return


    def cpu_move(self):
        winning_path = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'],
                        ['1', '4', '7'], ['2', '5', '8'], ['3', '6', '9'],
                        ['1', '5', '9'], ['7', '5', '3']]
        if len(self.cpu_track) >= 2: # find the possibility to win the game
            for x in range(len(self.cpu_track) - 1):
                for y in range(x + 1, len(self.cpu_track)): 
                    for path in winning_path:
                        subset = [self.cpu_track[x], self.cpu_track[y]]
                        if set(subset).issubset(set(path)):
                            next_move = (set(path) - set(subset)).pop()
                            if self.board[next_move] == ' ': # CPU wins the game
                                self.board[next_move] = 'O' if self.count % 2 else 'X'
                                return
        if len(self.current_track) >= 2: # prevent player1 from winning
            for x in range(len(self.current_track) - 1):
                for y in range(x + 1, len(self.current_track)): 
                    for path in winning_path:
                        subset = [self.current_track[x], self.current_track[y]]
                        if set(subset).issubset(set(path)):
                            next_move = (set(path) - set(subset)).pop()
                            if self.board[next_move] == ' ': # blocks the player1's winning path
                                self.board[next_move] = 'O' if self.count % 2 else 'X'
                                self.cpu_track.append(next_move)
                                return
        while self.previous_track: # check player1 previous pattern
            popped = self.previous_track.popleft()
            if self.board[popped] == ' ':
                self.board[popped] = 'O' if self.count % 2 else 'X'
                self.cpu_track.append(popped)
                return
        availables = [x for x, y in self.board.items() if y == ' '] # random choice
        next_move = random.sample(availables,1)[0]
        self.board[next_move] = 'O' if self.count % 2 else 'X'
        self.cpu_track.append(next_move)
        return
                    
                

if __name__ == '__main__':
    t = Tic_Tac_Toe()
        
    print('\nTic Tac Toe\n  By C**C\n')
    time.sleep(1)
    if t.total_plays != 0:
        print('Total play count of this game is ' + str(t.total_plays) + '!\n')
    t.mode = input('''\nLet's choose the number of the players.\n
    1 player, Press 1
    2 players, Press 2\n''')

    while t.mode not in ['1', '2']:
        t.mode = input('That is not an option. Please enter either 1 or 2\n')
 
    if t.mode == '2':
        t.player1 = input('Hey you, Player 1!  Please enter your name: ')
        t.players.append(t.player1)
        print(t.greeting(t.player1)) 
        t.player2 = input('And you, Player 2! Please enter your name: ')
        t.players.append(t.player2)
        print(t.greeting(t.player2))
        time.sleep(1)
        print(t.player1 + ' vs. ' + t.player2 + '\n')
        time.sleep(1)
        print('This game will randomly choose a player to start the game.\n')
        time.sleep(2)
        t.turn = random.choice(t.players)
        t.current_turn = t.turn
        print(t.current_turn + ' will go first!' + '\n')
    else:
        t.player1 = input('Hi, Player! Please enter your name: ')
        print(t.greeting(t.player1))
        t.player2 = 'CPU'
        t.current_turn = t.player1          
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
            if t.mode == '2' or t.current_turn == t.player1:
                print(t.current_turn + ', your turn now.\n')
                t.inputs= input('Which number do you choose?\n')
                time.sleep(1)
                while t.inputs not in ('1', '2', '3', '4', '5', '6', '7', '8', '9') or t.board[t.inputs] !=' ':
                    print('This is not a valid input, Try again!\n')
                    time.sleep(1)
                    t.inputs= input('Which number do you choose this time?\n')
                if t.count % 2:
                    t.board[t.inputs] = 'O'
                else:
                    t.board[t.inputs] = 'X'

                if t.mode == '1':
                    t.current_track.append(t.inputs)      
            else:
                t.cpu_move()
            t.count += 1
            if t.current_turn == t.player1:
                t.current_turn = t.player2
            else: 
                t.current_turn = t.player1           
            if t.count >= 5:
                print('pass')
                if (t.board['7'] == t.board['8'] == t.board['9'] and t.board['9'] in ('X','O')) or (
                    t.board['4'] == t.board['5'] == t.board['6']and t.board['6'] in ('X','O')) or (
                        t.board['1'] == t.board['2'] == t.board['3'] and t.board['3'] in ('X','O')) or (
                            t.board['1'] == t.board['4'] == t.board['7'] and t.board['7'] in ('X','O')) or (
                                t.board['2'] == t.board['5'] == t.board['8'] and t.board['8'] in ('X','O')) or (
                                    t.board['3'] == t.board['6'] == t.board['9'] and t.board['9'] in ('X','O')) or (
                                        t.board['7'] == t.board['5'] == t.board['3'] and t.board['3'] in ('X','O')) or (
                                            t.board['9'] == t.board['5'] == t.board['1'] and t.board['1'] in ('X','O')):
                    print(t.printBoard(t.board))
                    t.game_over = True
                    if t.current_turn == t.player1:
                        t.winner = t.player2
                        t.loser = t.player1
                        t.player2_winning += 1
                    else:
                        t.winner = t.player1
                        t.loser = t.player2
                        t.player1_winning += 1
                    print('Excellent match.\n' + t.winner + ' wins this game!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
                    if t.mode == '2':
                        t.db_update(t.winner.capitalize(), t.loser.capitalize())
                    else:
                        if t.player1 == t.winner:
                            t.db_update(t.winner.capitalize(), None)
                        else:
                            t.db_update(None, t.loser.capitalize()) 
                    time.sleep(1)
                    break
        if t.game_over and t.winning_count not in (t.player1_winning, t.player2_winning):       
            t.current_turn = t.loser
            print('Next battle.\nHere we go!\n')   
        elif t.game_over == False:
            print(t.printBoard(t.board))
            print('It\'s a tie!\nGood Game Guys!\n')
            time.sleep(1)
            if t.mode == '2':
                for player in t.players:
                    t.cursor.execute('update players set tie = tie + 1 where name = "' + player.capitalize() + '"')
                    t.conn.commit()
            else:
                t.cursor.execute('update players set tie = tie + 1 where name = "' + t.player1.capitalize() + '"')
                t.conn.commit()    
            print('Current Game Status:\n' + t.player1 + ' vs. ' + t.player2 + '\n' + str(t.player1_winning) + ' : ' + str(t.player2_winning) + '\n')
            print('Next battle.\nHere we go!\n')
        t.cursor.execute('update total_plays set count = count + 1')
        t.conn.commit()
        t.previous_track = deque(t.current_track)
        t.current_track = []
        t.cpu_track = []
        for key in t.board.keys():
            t.board[key] = ' '                   
    if t.winning_count == t.player1_winning:
        print('Congratulations! '+ t.player1.upper() + ' is the winner!' )
    else:
        if t.mode == '2':
            print('Congratulations! '+ t.player2.upper() + ' is the winner!' )
        else:
            print('CPU is the winner!')
    t.cursor.close()
    t.conn.close()
    time.sleep(1)
  
