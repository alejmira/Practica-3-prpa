#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 17:55:16 2022

@author: alejandro
"""

import pygame
import time
import random

window_x= 720
window_y = 480

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
white = pygame.Color(255, 255, 255)

snake_speed = 15

pygame.init()

pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()


snake_position1 = [100, 50]
snake_body1 = [snake_position1]

snake_position2 = [window_x - 110, window_y - 60]
snake_body2 = [snake_position2]

fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True

direction1 = 'RIGHT'
change_to1 = direction1

direction2 = "LEFT"
change_to2 = direction2


score1 = 0
score2 = 0

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


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # blue
            if event.key == pygame.K_UP:
                change_to1 = 'UP'
            if event.key == pygame.K_DOWN:
                change_to1 = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to1 = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to1 = 'RIGHT'
            
            # yellow
            if event.key == pygame.K_w:
                change_to2 = "UP"
            if event.key == pygame.K_s:
                change_to2 = 'DOWN'
            if event.key == pygame.K_a:
                change_to2 = 'LEFT'
            if event.key == pygame.K_d:
                change_to2 = 'RIGHT'
    
    # Blue
    if change_to1 == 'UP' and direction1 != 'DOWN':
        direction1 = 'UP'
    if change_to1 == 'DOWN' and direction1 != 'UP':
        direction1 = 'DOWN'
    if change_to1 == 'LEFT' and direction1 != 'RIGHT':
        direction1 = 'LEFT'
    if change_to1 == 'RIGHT' and direction1 != 'LEFT':
        direction1 = 'RIGHT'
    
    # Yellow
    if change_to2 == 'UP' and direction2 != 'DOWN':
        direction2 = 'UP'
    if change_to2 == 'DOWN' and direction2 != 'UP':
        direction2 = 'DOWN'
    if change_to2 == 'LEFT' and direction2 != 'RIGHT':
        direction2 = 'LEFT'
    if change_to2 == 'RIGHT' and direction2 != 'LEFT':
        direction2 = 'RIGHT'
    
    # Blue
    if direction1 == 'UP':
        snake_position1[1] -= 10
    if direction1 == 'DOWN':
        snake_position1[1] += 10
    if direction1 == 'LEFT':
        snake_position1[0] -= 10
    if direction1 == 'RIGHT':
        snake_position1[0] += 10
 
    # Yellow
    if direction2 == 'UP':
        snake_position2[1] -= 10
    if direction2 == 'DOWN':
        snake_position2[1] += 10
    if direction2 == 'LEFT':
        snake_position2[0] -= 10
    if direction2 == 'RIGHT':
        snake_position2[0] += 10    
    
    # Blue
    snake_body1.insert(0, list(snake_position1))
    if snake_position1[0] == fruit_position[0] and snake_position1[1] == fruit_position[1]:
        score1 += 10
        fruit_spawn = False
    else:
        snake_body1.pop()
    
    # Yellow
    snake_body2.insert(0, list(snake_position2))
    if snake_position2[0] == fruit_position[0] and snake_position2[1] == fruit_position[1]:
        score2 += 10
        fruit_spawn = False
    else:
        snake_body2.pop()
         
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
         
    fruit_spawn = True
    game_window.fill(black)
    
    # Blue
    for pos in snake_body1:
        pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
    
    # Yellow
    for pos in snake_body2:
        pygame.draw.rect(game_window, yellow, pygame.Rect(pos[0], pos[1], 10, 10))
        
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    
    # GAME OVER CONDITIONS
    
    # Draw
    if (snake_position1[0] < 0 or snake_position1[0] > window_x-10 or snake_position1[1] < 0 or snake_position1[1] > window_y-10) and (snake_position2[0] < 0 or snake_position2[0] > window_x-10 or snake_position2[1] < 0 or snake_position2[1] > window_y-10):
        game_over(3)
    
    # Blue
    if snake_position1[0] < 0 or snake_position1[0] > window_x-10 or snake_position1[1] < 0 or snake_position1[1] > window_y-10:
        game_over(2)
        
    # Yellow
    if snake_position2[0] < 0 or snake_position2[0] > window_x-10 or snake_position2[1] < 0 or snake_position2[1] > window_y-10:
        game_over(1)
    
    # Draw
    if snake_position1 == snake_position2:
        game_over(3)
    
    # Blue
    for block in snake_body1[1:]:
        if snake_position1 == block and snake_position2 == block:
            game_over(3)
        elif snake_position1 == block:
            game_over(2)
        elif snake_position2 == block:
            game_over(1)
    
    # Yellow
    for block in snake_body2[1:]:
        if snake_position1 == block and snake_position2 == block:
            game_over(3)
        elif snake_position2 == block:
            game_over(1)
        elif snake_position1 == block:
            game_over(2)
    
    # Blue wins by score
    if score1 == 500:
        game_over(1)    
    
    # Yellow wins by score
    elif score2 == 500:
        game_over(2)
     
        
    show_score(1, 'times new roman', 20)
     
    pygame.display.update()
 
    fps.tick(snake_speed)