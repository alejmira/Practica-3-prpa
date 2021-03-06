#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 17:52:53 2022

@author: alejandro
"""

import traceback
import pygame
import time
import random
import sys
from multiprocessing.connection import Client

# Constantes del juego
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
    
    def set_pos(self, pos): # Cambia la posición de la serpiente
        self.pos = pos
    
    def get_body(self):
        return self.body
    
    def set_body(self, body): # Cambia el cuerpo de la serpiente
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

    def set_pos(self, pos): # Cambia la posición de la manzana
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
    
    def set_pos_player(self, number, pos): # Cambia la posición de la serpiente del jugador number
        self.players[number].set_pos(pos)
        
    def set_body_player(self, number, body): # Cambia el cuerpo de la serpiente del jugador number
        self.players[number].set_body(body)
    
    def get_apple(self):
        return self.apple
    
    def set_apple_pos(self, pos): # Cambia la posición de la manzana
        self.apple.set_pos(pos)
    
    def get_score(self, number):
        return self.score[number]
    
    def set_score(self, score): # Cambia la puntuación
        self.score = score
    
    def get_game_over(self):
        return self.game_over
    
    def set_game_over(self, i): # Cambia el estado de game over
        self.game_over = i
    
    def is_running(self):
        return self.running
    
    def stop(self): # Detiene la ejecución del bucle principal
        self.running = False 

    def update(self, gameinfo): # Actualiza la información del juego recibida en gameinfo
        self.set_pos_player(0, gameinfo["pos_blue"])
        self.set_pos_player(1, gameinfo["pos_yellow"])
        self.set_body_player(0, gameinfo["body_blue"])
        self.set_body_player(1, gameinfo["body_yellow"])
        self.set_apple_pos(gameinfo['pos_apple'])
        self.set_score(gameinfo['score'])
        self.running = gameinfo['is_running']
        self.game_over = gameinfo['game_over']
    
    def gameOver(self, i, game_window): # Método que muestra la pantalla de fin del juego
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
        
        if i == 1: # Gana azul
            winner_surface = my_font.render("Player 1 WINNER!", True, green)
            winner_rect = winner_surface.get_rect()
            winner_rect.midtop = (window_x//2, window_y//2)
            game_window.blit(winner_surface, winner_rect)
            
        elif i == 2: # Gana amarillo
            winner_surface = my_font.render("Player 2 WINNER!", True, green)
            winner_rect = winner_surface.get_rect()
            winner_rect.midtop = (window_x//2, window_y//2)
            game_window.blit(winner_surface, winner_rect)
        
        elif i == 3: # Posible empate. Se miran a las puntuaciones para ver si hay desempate
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
    
    def show_score(self, font, size, game_window): # Método que enseña la puntuación actual de los jugadores
        score_font = pygame.font.SysFont(font, size)
        # Azul
        score_surface1 = score_font.render('Player 1 score: ' + str(self.score[0]), True, blue)
        score_rect1 = score_surface1.get_rect()
        score_rect1.midtop = (70, 5)
        
        # Amarillo
        score_surface2 = score_font.render('Player 2 score: ' + str(self.score[1]), True, yellow)
        score_rect2 = score_surface2.get_rect()
        score_rect2.midtop = (window_x-90, 5)
        
        game_window.blit(score_surface1, score_rect1)
        game_window.blit(score_surface2, score_rect2)
        
        
def main(ip_address):
    try:
        with Client((ip_address, 6111), authkey=b'secret password') as conn:
            # Inicialización de la ventana de juego
            pygame.init()
            pygame.display.set_caption("Snake")
            game_window = pygame.display.set_mode((window_x, window_y))
            fps = pygame.time.Clock()
            
            game = Game()
            gameinfo = conn.recv()
            game.update(gameinfo)
            
            
            while game.is_running(): # Bucle principal
                
                # Dinámica de entrada de movimiento del usuario y su envío al servidor
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
                
                # Dibujo de las serpientes
                game_window.fill(black)
                for pos in game.players[0].body:
                    pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
                for pos in game.players[1].body:
                    pygame.draw.rect(game_window, yellow, pygame.Rect(pos[0], pos[1], 10, 10))
                
                # Dibujo de la manzana
                pygame.draw.rect(game_window, red, pygame.Rect(game.apple.pos[0], game.apple.pos[1], 10, 10))
                
                # Actualización de los parámetros del juego
                gameinfo = conn.recv()
                game.update(gameinfo) 
                
                # Chequeo de game over
                if game.game_over == 1:
                    game.gameOver(1, game_window)
                    game.stop()
                elif game.game_over == 2:
                    game.gameOver(2, game_window)
                    game.stop()
                elif game.game_over == 3:
                    game.gameOver(3, game_window)
                    game.stop()
                
                # Dibujo de las puntuaciones
                game.show_score('times new roman', 20, game_window)
                
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






