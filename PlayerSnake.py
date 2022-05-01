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
        self.game_over = None
        self.running = True
    
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
    
    def get_game_over(self):
        return self.game_over
    
    def set_game_over(self, i):
        self.game_over = i
    
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
        self.game_over = gameinfo['game_over']
    
    def gameOver(self, i, game_window):
        game_window.fill(black)
        my_font =  pygame.font.SysFont('times new roman', 50)
        game_over_surface1 =my_font.render('Player 1 Score: ' + str(self.score[0]), True, blue)
        game_over_rect1 = game_over_surface1.get_rect()
        game_over_rect1.midtop = (window_x//2, window_y//6)
        game_window.blit(game_over_surface1, game_over_rect1)
        
        game_over_surface2 = my_font.render('Player 2 Score: ' + str(self.score[1]), True, yellow)
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
            if self.score[0] > self.score[1]:
                winner_surface = my_font.render("Player 1 WINNER!", True, green)
                winner_rect = winner_surface.get_rect()
                winner_rect.midtop = (window_x//2, window_y//2)
                game_window.blit(winner_surface, winner_rect)
            elif self.score[0] < self.score[1]:
                winner_surface = my_font.render("Player 2 WINNER!", True, green)
                winner_rect = winner_surface.get_rect()
                winner_rect.midtop = (window_x//2, window_y//2)
                game_window.blit(winner_surface, winner_rect)
            elif self.score[0] == self.score[1]: # Sólo es empate si se chocan a la vez y tienen la misma puntuación
                draw_surface = my_font.render("DRAW!", True, white)
                draw_rect = draw_surface.get_rect()
                draw_rect.midtop = (window_x//2, window_y//2)
                game_window.blit(draw_surface, draw_rect)
        
        pygame.display.flip()
        time.sleep(10)
        pygame.quit()
        quit()
        
def main(ip_address):
    try:
        with Client((ip_address, 6111), authkey=b'secret password') as conn:
            pygame.init()
            pygame.display.set_caption("Snake")
            game_window = pygame.display.set_mode((window_x, window_y))
            fps = pygame.time.Clock()
            
            
            game = Game()
            gameinfo = conn.recv()
            game.update(gameinfo)
            
            #print(gameinfo)
            
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
                #print(gameinfo)
                
                game_window.fill(black)
                
                for pos in game.players[0].body:
                    pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
                for pos in game.players[1].body:
                    pygame.draw.rect(game_window, yellow, pygame.Rect(pos[0], pos[1], 10, 10))
                
                pygame.draw.rect(game_window, red, pygame.Rect(game.apple.pos[0], game.apple.pos[1], 10, 10))
                
                gameinfo = conn.recv()
                game.update(gameinfo) 
                #print(gameinfo)
                
                if game.game_over == 1:
                    game.gameOver(1, game_window)
                    game.stop()
                elif game.game_over == 2:
                    game.gameOver(2, game_window)
                    game.stop()
                elif game.game_over == 3:
                    game.gameOver(3, game_window)
                    game.stop()
                
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






