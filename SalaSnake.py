#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:42:26 2022

@author: alejandro
"""

import pygame
import time
import random
import sys
from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock

window_x= 720
window_y = 480

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
white = pygame.Color(255, 255, 255)

snake_speed = 15

class Snake():
    def __init__(self, color):
        self.color = color
        if self.color == "BLUE":
            self.pos = [100, 50]
            self.direction = "RIGHT"
        elif self.color == "YELLOW":
            self.pos = [window_x-110, window_y-60]
            self.direction = "LEFT"
        self.body = [self.pos]
        self.change_to = self.direction
        
    def get_color(self):
        return self.color
        
    def get_pos(self):
        return self.pos
    
    def get_body(self):
        return self.body
    
    def get_direction(self):
        return self.direction
    
    def get_change_to(self):
        return self.change_to
    
    def change_direction(self, key):
        self.change_to = key
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
    
    def move(self):
        if self.direction == 'UP':
            self.position[1] -= 10
        if self.direction == 'DOWN':
            self.position[1] += 10
        if self.direction == 'LEFT':
            self.position[0] -= 10
        if self.direction == 'RIGHT':
            self.position[0] += 10
            
    
class Apple():
    def __init__(self):
        self.pos = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]

    def get_pos(self):
        return self.pos
  
    
class Game():
    def __init__(self, manager):
        self.players = manager.list([Snake("BLUE"), Snake("YELLOW")])
        self.apple = manager.list([Apple()])
        self.score = manager.list([0,0])
        self.running = Value('i', 1)
        self.lock = Lock()
    
    def get_player(self, player): # 0: BLUE, 1: YELLOW
        return self.players[player]

    def get_apple(self):
        return self.apple[0]
    
    def get_score(self, player): # 0: BLUE, 1: YELLOW
        return self.score[player]
    
    def is_running(self):
        return self.running.value == 1
    
    def stop(self):
        self.running.value = 0
    
    def change_direction(self, player, key):
        self.lock.acquire()
        p = self.players[player]
        p.change_direction(key)
        self.players[player] = p
        self.lock.release()
    
    def move(self, player):
        self.lock.acquire()
        p = self.players[player]
        p.move()
        self.players[player] = p
        self.lock.release()

    def get_info(self):
        info = {
            'pos_blue': self.players[0].get_pos(),
            'pos_yellow': self.players[1].get_pos(),
            'body_blue': self.players[0].get_body(),
            'body_yellow': self.players[1].get_body(),
            'pos_apple': self.apple[0].get_pos(),
            'score': list(self.score),
            'is_running': self.running.value == 1
        }
        return info
   
    
def player(number, conn, game):
    try:
        conn.send(game.get_info())
        while game.is_running():
            command = conn.recv()
            if command == "up":
                game.change_direction(number, "UP")
            elif command == "down":
                game.change_direction(number, "DOWN")
            elif command == "left":
                game.change_direction(number, "LEFT")
            elif command == "right":
                game.change_direction(number, "RIGHT")
                
            game.move(number)
            game.players[number].body.insert(0, game.players[number].pos)
# =============================================================================
#             if snake_position1[0] == fruit_position[0] and snake_position1[1] == fruit_position[1]:
#                 score1 += 10
#                 fruit_spawn = False
#             else:
# =============================================================================
            game.players[number].body.pop()
            
            conn.send(game.get_info())
            
                
            
            
            game.move(number)
            conn.send(game.get_info())
    except:
        traceback.print_exc()
        conn.close()
    finally:
        print(f"Game ended {game}")

def main(ip_address):
    manager = Manager()
    try:
        with Listener((ip_address, 6111), authkey=b'secret password') as listener:
            n_player = 0
            players = [None, None]
            game = Game(manager)
            while True:
                print(f"accepting connection {n_player}")
                conn = listener.accept()
                players[n_player] = Process(target=player, args=(n_player, conn, game))
                n_player += 1
                if n_player == 2:
                    players[0].start()
                    players[1].start()
                    n_player = 0
                    players = [None, None]
                    game = Game(manager)

    except Exception as e:
        traceback.print_exc()

if __name__=='__main__':
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]

    main(ip_address)










def show_score(choice, font, size):
    score_font = pygame.font.SysFont(font, size)
    # Blue
    score_surface1 = score_font.render('Player 1 score: ' + str(score1), True, blue)
    score_rect1 = score_surface1.get_rect()
    score_rect1.midtop = (70, 5)
    
    #Yellow
    score_surface2 = score_font.render('Player 2 score: ' + str(score2), True, yellow)
    score_rect2 = score_surface2.get_rect()
    score_rect2.midtop = (window_x-90, 5)
    
    game_window.blit(score_surface1, score_rect1)
    game_window.blit(score_surface2, score_rect2)


def game_over(i):
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface1 = my_font.render('Player 1 Score: ' + str(score1), True, blue)
    game_over_rect1 = game_over_surface1.get_rect()
    game_over_rect1.midtop = (window_x//2, window_y//6)
    game_window.blit(game_over_surface1, game_over_rect1)
    
    game_over_surface2 = my_font.render('Player 2 Score: ' + str(score2), True, yellow)
    game_over_rect2 = game_over_surface2.get_rect()
    game_over_rect2.midtop = (window_x//2, window_y//3)
    game_window.blit(game_over_surface2, game_over_rect2)
    
    if i == 1:
        winner_surface = my_font.render("Player 1 WINNER!", True, green)
        winner_rect = winner_surface.get_rect()
        winner_rect.midtop = (window_x//2, window_y//2)
        game_window.blit(winner_surface, winner_rect)
        
    elif i == 2:
        winner_surface = my_font.render("Player 2 WINNER!", True, green)
        winner_rect = winner_surface.get_rect()
        winner_rect.midtop = (window_x//2, window_y//2)
        game_window.blit(winner_surface, winner_rect)
    
    elif i == 3:
        if score1 > score2:
            winner_surface = my_font.render("Player 1 WINNER!", True, green)
            winner_rect = winner_surface.get_rect()
            winner_rect.midtop = (window_x//2, window_y//2)
            game_window.blit(winner_surface, winner_rect)
        elif score1 < score2:
            winner_surface = my_font.render("Player 2 WINNER!", True, green)
            winner_rect = winner_surface.get_rect()
            winner_rect.midtop = (window_x//2, window_y//2)
            game_window.blit(winner_surface, winner_rect)
        elif score1 == score2: # Sólo es empate si se chocan a la vez y tienen la misma puntuación
            draw_surface = my_font.render("DRAW!", True, white)
            draw_rect = draw_surface.get_rect()
            draw_rect.midtop = (window_x//2, window_y//2)
            game_window.blit(draw_surface, draw_rect)
    
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()
    quit()