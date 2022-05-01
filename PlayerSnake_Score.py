#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 17:52:53 2022

@author: alejandro
"""

import pygame
import time
import random
import sys
from multiprocessing.connection import Client

window_x= 720
window_y = 480
game_window = pygame.display.set_mode((window_x, window_y))

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
white = pygame.Color(255, 255, 255)
score =[0,0]

snake_speed = 15

class Snake():
    def __init__(self, color):
        self.color = color
        self.pos = [None, None]
        self.direction = None
        self.body = [[None, None]]
        self.change_to = self.direction
        
    def get_color(self):
        return self.color
        
    def get_pos(self):
        return self.pos
    
    def set_pos(self, pos):
        self.pos = pos
    
    def get_body(self):
        return self.body
    
    def set_body(self, body):
        self.body = body
    
    def get_direction(self):
        return self.direction
    
    def get_change_to(self):
        return self.change_to

    
class Apple():
    def __init__(self):
        self.pos = [None, None]

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos



class Game():
    def __init__(self):
        self.players = [Snake("BLUE"), Snake("YELLOW")]
        self.apple = Apple()
        self.score = [0,0]
        self.running = True
        self.game_window = pygame.display.set_mode((window_x, window_y))
    
    def get_player(self, number): # 0: BLUE, 1: YELLOW
        return self.players[number]
    
    def set_pos_player(self, number, pos):
        self.players[number].set_pos(pos)
        
    def set_body_player(self, number, body):
        self.players[number].set_body(body)
    
    def get_apple(self):
        return self.apple
    
    def set_apple_pos(self, pos):
        self.apple.set_pos(pos)
    
    def set_apple_spawn(self, spawn):
        self.apple.set_spawn(spawn)
    
    def get_score(self, number): # 0: BLUE, 1: YELLOW
        return self.score[number]
    
    def set_score(self, score):
        self.score = score
    
    def is_running(self):
        return self.running
    
    def stop(self):
        self.running = False
    
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

    def update(self, gameinfo):
        self.set_pos_player(0, gameinfo["pos_blue"])
        self.set_pos_player(1, gameinfo["pos_yellow"])
        self.set_body_player(0, gameinfo["body_blue"])
        self.set_body_player(1, gameinfo["body_yellow"])
        self.set_apple_pos(gameinfo['pos_apple'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']
    
    def show_score(self,game_window,score):
        game_window.fill(black)
        score_font = pygame.font.SysFont('arial', 26)
    # Blue
        score_surface1 = score_font.render('Player 1 score: ' + str(self.score[0]), True, blue)
        score_rect1 = score_surface1.get_rect()
        score_rect1.midtop = (70, 5)
    
    #Yellow
        score_surface2 = score_font.render('Player 2 score: ' + str(self.score[1]), True, yellow)
        score_rect2 = score_surface2.get_rect()
        score_rect2.midtop = (window_x-90, 5)
        return
        self.game_window.blit(score_surface1, score_rect1)
        self.game_window.blit(score_surface2, score_rect2)


def main(ip_address):
    try:
        with Client((ip_address, 6111), authkey=b'secret password') as conn:
            pygame.init()
            pygame.display.set_caption("Snake")
            fps = pygame.time.Clock()
            
            
            game = Game()
            gameinfo = conn.recv()
            game.update(gameinfo)
            
            print(gameinfo)
            
            while game.is_running():
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            conn.send("up")
                        if event.key == pygame.K_DOWN:
                            conn.send("down")
                        if event.key == pygame.K_LEFT:
                            conn.send("left")
                        if event.key == pygame.K_RIGHT:
                            conn.send("right")
                        
                
                conn.send("next")
                gameinfo = conn.recv()
                game.update(gameinfo) 
                print(gameinfo)
                
                
                game.show_score(game_window,score)
                game_window.fill(black)
                
                for pos in game.players[0].body:
                    pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
                for pos in game.players[1].body:
                    pygame.draw.rect(game_window, yellow, pygame.Rect(pos[0], pos[1], 10, 10))
                
                pygame.draw.rect(game_window, red, pygame.Rect(game.apple.pos[0], game.apple.pos[1], 10, 10))
                
                gameinfo = conn.recv()
                game.update(gameinfo) 
                print(gameinfo)
                pygame.display.update()
                fps.tick(snake_speed)
                
    except:
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__=="__main__":
    ip_address = "127.0.0.1"
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    print(ip_address)
    main(ip_address)






