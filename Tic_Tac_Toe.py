#!/usr/bin/env python
# coding: utf-8

import sqlite3
import random
import time
import os
import glob

# connect to sqlite database
# check if db already exists
if glob.glob('**/tic_tac_toe.db', recursive = True):
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()
else: # if not, create a db and 2 tables
    os.system('touch tic_tac_toe.db')
    conn = sqlite3.connect('tic_tac_toe.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE players (id integer primary key autoincrement, name varchar(255) not null, win integer default 0, lose integer default 0, tie integer default 0)'
        )
    cursor.execute(
        'CREATE TABLE total_plays (count integer default 0)'
        )

# fetch data from database if exists already    
try:
    cursor.execute('select * from total_plays')
    total_plays = cursor.fetchone()[0]

    cursor.execute('select name from players')
    all_players = []
    for name in cursor.fetchall():
        all_players.append(name[0])
        
    cursor.execute('select * from total_plays')
    total_plays = cursor.fetchone()[0]
except: # database just created and has no data
    total_plays = 0
    all_players = []
    pass


def db_update(win, lose):
    cursor.execute('update players set win= win + 1 where name = "' + win + '"' )
    cursor.execute('update players set lose = lose + 1 where name = "' + lose + '"' )
    conn.commit()
    return 
   
board = {'7': ' ', '8': ' ', '9': ' ',
        '4': ' ', '5': ' ', '6': ' ',
        '1': ' ', '2': ' ', '3': ' '}

sample_keypad = {'7': '7', '8': '8', '9': '9', '4': '4', '5': '5', '6': '6','1': '1', '2': '2', '3': '3'}



def greeting(player_name):
    if player_name.capitalize() in all_players:
        return 'Welcome Back!'
    else:
        try:
            cursor.execute('insert into players (name) values ("' + player_name.capitalize() + '")')
            conn.commit()
            return 'New player! Welcome!!'
        except:
            return 'New player! Welcome!'



board_keys = board.keys()



def printBoard(board_sample):
    print(board_sample['7'] + '|' + board_sample['8'] + '|' + board_sample['9'] ) 
    print('-+-+-')
    print(board_sample['4'] + '|' + board_sample['5'] + '|' + board_sample['6'] )
    print('-+-+-')
    print(board_sample['1'] + '|' + board_sample['2'] + '|' + board_sample['3'] )
    return ''



def Tic_Tac_Toe():
    print('\nTic Tac Toe\n  By C**C\n')
    time.sleep(1)
    if total_plays != 0:
        print('Total play count of this game is ' + str(total_plays) + '!\n') 
    players = []
    player1 = input('Hey you, Player 1!  Enter your name: ')
    players.append(player1)
    
    print(greeting(player1))
    
    
    player2 = input('And you, Player 2! Enter your name: ')
    players.append(player2)

    print(greeting(player2))

    cursor.execute('update total_plays set count = count + 1')
    conn.commit()
    
    time.sleep(1)
    
    print(player1 + ' vs. ' + player2 + '\n')
    
    time.sleep(1)
    print('This game will randomly choose a player to start the game.\n')
    
    time.sleep(2)
    
    
    turn = random.choice(players)
    current_turn = turn
    print(current_turn + ' will go first!' + '\n')
    
    time.sleep(1)
    
    print('Instruction: ' + '\n' + 'How to put the mark on the grid?' + '\n')
    print(printBoard(board))
    
    time.sleep(2)
    
    print('Think of the grid as a keypad, like this\n')
    
    time.sleep(1)
    
    print(printBoard(sample_keypad))
    
    time.sleep(2)
    
    print('Simply type the number that coordinates the square.\n')
    
    time.sleep(2)

    winning_count = input('''\nNow, let\'s choose the winning path.\n\nWho will be the winner?\n
    If you prefer "The player who wins the first game." Press 1.
    If you prefer "The player who wins the first three games." Press 3.\n''')
    
    while winning_count not in ['1', '3']:
        winning_count = input('That is not an option. Please enter either 1 or 3\n')

    winning_count = int(winning_count)
    player1_winning = 0
    player2_winning = 0
    
    print('Ready, Set, Go!\n')

    
    while winning_count not in ( player1_winning, player2_winning):
        count = 0
        game_over = False
    
        for i in range(9):       
            print(printBoard(board) + '\n')
            print(current_turn + ', your turn now.\n')
            inputs= input('Which number do you choose?\n')
            time.sleep(1)
        
            while inputs not in ('1', '2', '3', '4', '5', '6', '7', '8', '9') or board[inputs]!=' ':
                print('This is not a valid input, Try again!\n')
                time.sleep(1)
                inputs= input('Which number do you choose this time?\n')
        
       
            if count % 2:
                board[inputs] = 'O'
                count += 1
                if current_turn == player1:
                    current_turn = player2
                else: 
                    current_turn = player1
            
            else:
                board[inputs] = 'X'
                count += 1
                if current_turn == player1:
                    current_turn = player2
                else: 
                    current_turn = player1
                        
            if count >= 5:
                if board['7'] == board['8'] == board['9'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['4'] == board['5'] == board['6'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['1'] == board['2'] == board['3'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['1'] == board['4'] == board['7'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['2'] == board['5'] == board['8'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['3'] == board['6'] == board['9'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['7'] == board['5'] == board['3'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['9'] == board['5'] == board['1'] == 'X':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['7'] == board['8'] == board['9'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['4'] == board['5'] == board['6'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['1'] == board['2'] == board['3'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['1'] == board['4'] == board['7'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['2'] == board['5'] == board['8'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['3'] == board['6'] == board['9'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['7'] == board['5'] == board['3'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                elif board['9'] == board['5'] == board['1'] == 'O':
                    print(printBoard(board))
                    game_over = True
                    if current_turn == player1:
                        winner = player2
                        loser = player1
                        player2_winning +=1
                    else:
                        winner = player1
                        loser = player2
                        player1_winning +=1
                    print('Excellent match.\n' + winner + ' is the winner!!!\n')
                    time.sleep(1)
                    print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
                    db_update(winner.capitalize(), loser.capitalize())
                    time.sleep(2)
                    break
                
        
        
        if game_over and winning_count not in ( player1_winning, player2_winning):       
            game_over = False
            count = 0
            current_turn = winner
            for key in board.keys():
                board[key] = ' '
            print('Next battle.\nHere we go!\n')
        
        elif game_over == False:
            print(printBoard(board))
            print('It\'s a tie!\nGood Game Guys!\n')
            time.sleep(1)
            for player in players:
                cursor.execute('update players set tie = tie + 1 where name = "' + player.capitalize() + '"')
                conn.commit()
            for key in board.keys():
                board[key] = ' '
            print('Current Game Status:\n' + player1 + ' vs. ' + player2 + '\n' + str(player1_winning) + ' : ' + str(player2_winning) + '\n')
            print('Next battle.\nHere we go!\n')
            count = 0
            
                  
    if winning_count == player1_winning:
        print('Congratulations! '+ player1.upper() + ' is the champ!' )
    else:
        print('Congratulations! '+ player2.upper() + ' is the champ!' )

    cursor.close()
    conn.close()
    time.sleep(2)
    


if __name__ == '__main__':
    Tic_Tac_Toe()
    
