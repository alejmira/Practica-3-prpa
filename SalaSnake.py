#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:42:26 2022

@author: alejandro
"""

import traceback
import time
import random
import sys
from multiprocessing.connection import Listener
from multiprocessing import Process, Manager, Value, Lock

window_x= 720
window_y = 480


snake_speed = 15

class Snake():
    def __init__(self, color):
        self.color = color
        if self.color == "BLUE":
            self.pos = [100, 50]
            self.body = [[100, 50]]
            self.direction = "RIGHT"
        elif self.color == "YELLOW":
            self.pos = [window_x-110, window_y-60]
            self.body = [[window_x-110, window_y-60]]
            self.direction = "LEFT"
        self.change_to = self.direction
        
    def get_color(self): #Color jugador
        return self.color
        
    def get_pos(self): #Posición jugador
        return self.pos
    
    def get_body(self): #Tamaño cuerpo actual del jugador
        return self.body
    
    def set_body(self, body): #Reestablecimiento del tamaño del cuerpo tras comerse una manzana
        self.body = body
    
    def get_direction(self): #Dirección y sentido actual hacia la que va el jugador
        return self.direction
    
    def get_change_to(self): 
        return self.change_to
    
    def change_direction(self, key): #Cambio de dirección
        self.change_to = key
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP' #No podemos cambiar dirección de arriba a abajo, primero hay que mverse hacia uno de los lados
        elif self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT' #Igual que antes, no podemos cambiar el sentido directamente dentro de la misma dirección
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
    
    def move(self):
        if self.direction == 'UP':
            self.pos[1] -= 10 #Movimiento que realizamos cuando cambiamos dirección
        if self.direction == 'DOWN':
            self.pos[1] += 10
        if self.direction == 'LEFT':
            self.pos[0] -= 10
        if self.direction == 'RIGHT':
            self.pos[0] += 10
            
    
class Apple():
    def __init__(self):
        self.pos = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
         #La posición inicial de la manzana es aleatoria
    def get_pos(self):
        return self.pos #Devuelve posición de la manzana
    
    
class Game():
    def __init__(self, manager):
        self.players = manager.list([Snake("BLUE"), Snake("YELLOW")]) #Juego dispuesto para dos jugadores/serpientes
        self.apple = manager.list([Apple()]) #Una sola manzana, cuando es comida se genera una nueva en una nueva posición aleatoria
        self.score = manager.list([0,0])  #puntuación marcador, número de manzanas que ha comido un jugador, cada una *10
        self.game_over = 0
        self.running = Value('i', 1)
        self.lock = Lock()
    
    def get_player(self, player): # 0: BLUE, 1: YELLOW
        return self.players[player]
    
    def set_body(self, player, body):
        self.lock.acquire()
        p = self.players[player]
        p.set_body(body)
        self.players[player] = p
        self.lock.release()
    
    def get_apple(self):
        return self.apple[0]
    
    def get_score(self, player): # 0: BLUE, 1: YELLOW
        return self.score[player]
    
    def set_score(self, player): #reestablecimiento del marcador
        self.score[player] += 10
    
    def get_game_over(self):
        return self.game_over
    
    def set_game_over(self, i): #Cambia el estado de gameover (partida acabada o no)
        self.game_over = i
        
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
            'is_running': self.running.value == 1,
            'game_over': self.game_over
        }
        return info
   
    
def player(number, conn, game):
    try:
        #print(game.get_info())
        conn.send(game.get_info())
        while game.is_running():
            command = ""
            while command != "next":
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
            L = game.players[number].body
            L.insert(0, game.players[number].pos)
            game.set_body(number, L)
            if game.players[number].pos == game.apple[0].pos: 
                game.set_score(number)
                game.apple[0] = Apple()
            else:
                L.pop()
                game.set_body(number, L)
                
            # Por algún motivo que no alcanza a mi comprensión, si borras una de estas fos líneas de código repetido, no funciona    
            
            #print(game.get_info())
            conn.send(game.get_info())
            
            #print(game.get_info())
            conn.send(game.get_info())
            
            
            # CONDICIONES DE GAME OVER
            
            # Los dos se salen de la pantalla a la vez
            if (game.players[0].pos[0] < 0 or game.players[0].pos[0] > window_x-10 or game.players[0].pos[1] < 0 or game.players[0].pos[1] > window_y-10) and (game.players[1].pos[0] < 0 or game.players[1].pos[0] > window_x-10 or game.players[1].pos[1] < 0 or game.players[1].pos[1] > window_y-10):
                game.set_game_over(3)
                conn.send(game.get_info())
            
            # El azul se sale de la pantalla
            if game.players[0].pos[0] < 0 or game.players[0].pos[0] > window_x-10 or game.players[0].pos[1] < 0 or game.players[0].pos[1] > window_y-10:
                game.set_game_over(2)
                conn.send(game.get_info())
                
            # El amarillo se sale de la pantalla
            if game.players[1].pos[0] < 0 or game.players[1].pos[0] > window_x-10 or game.players[1].pos[1] < 0 or game.players[1].pos[1] > window_y-10:
                game.set_game_over(1)
                conn.send(game.get_info())
                
            # Colisión frontal
            if game.players[0].pos == game.players[1].pos:
                game.set_game_over(3)
                conn.send(game.get_info())
            
            # Alguno se choca en el cuerpo del azul, posiblemente los dos a la vez
            for block in game.players[0].body[1:]:
                if game.players[0].pos == block and game.players[1] == block:
                    game.set_game_over(3)
                elif game.players[0].pos == block:
                    game.set_game_over(2)
                elif game.players[1] == block:
                    game.set_game_over(1)
            
            # Alguno se choca en el cuerpo del amarillo, posiblemente los dos a la vez
            for block in game.players[1].body[1:]:
                if game.players[1].pos == block and game.players[0] == block:
                    game.set_game_over(3)
                elif game.players[1].pos == block:
                    game.set_game_over(1)
                elif game.players[0] == block:
                    game.set_game_over(2)
             
            # Alguno alcanza la puntuación máxima
            if game.score[0] == 500:
                game.set_game_over(1)
            elif game.score[1] == 500:
                game.set_game_over(2)
                
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

