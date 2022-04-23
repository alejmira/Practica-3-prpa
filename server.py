import socket
import pickle
import random
import pygame
import time

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 102)
white = pygame.Color(255, 255, 255)

pygame.init()

pygame.display.set_caption("Snake")
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()


def show_score(choice, font, size):
    score_font = pygame.font.SysFont(font, size)
    # Blue
    score_surface1 = score_font.render(
        'Player 1 score: ' + str(score1), True, blue)
    score_rect1 = score_surface1.get_rect()
    score_rect1.midtop = (70, 5)

    #Yellow
    score_surface2 = score_font.render(
        'Player 2 score: ' + str(score2), True, yellow)
    score_rect2 = score_surface2.get_rect()
    score_rect2.midtop = (window_x-90, 5)

    game_window.blit(score_surface1, score_rect1)
    game_window.blit(score_surface2, score_rect2)


def get_ip():
    host_name = socket.gethostname()
    IP = socket.gethostbyname(host_name)
    return IP


class Server():
    def __init__(self):
        self.running = True

    def Game(self, Connections):
        data_snake1 = []
        data_snake2 = []
        fruit_position = []
        fruit_spawn = True
        while self.running:
            data_snake1 = Connections[0].recv(2*2048)
            data_snake2 = Connections[1].recv(2*2048)
            if not data_snake1 or not data_snake2:
                break
            data_snake1 = pickle.loads(data_snake1)
            data_snake2 = pickle.loads(data_snake2)

            if not fruit_position:
                fruit_spawn = True
            else:
                fruit_spawn = False
            while fruit_spawn == True:
                fruit_position = [random.randrange(
                    1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
        #falta añadir lo que pasa cuando una serpiente se come la fruta
        #fruit_position = []
        #aumentar cuerpo de la serpiente
            data_snake1=pickle.dumps(data_snake1)
            data_snake2=pickle.dumps(data_snake2)

            # manda la informacion de la serpiente 2 al cliente 1
            Connections[0].sendall(data_snake2)
            # manda la informacion de la serpiente 1 al cloente 2
            Connections[1].sendall(data_snake1)

        def Start_game(self):
            self.running=True
            HOST=get_ip()

            PORT=55555

            self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.s.bind((HOST, PORT))
            self.s.listen(5)
            conn_list=[]
            print("Server is Running")
            while self.running:
                for i in range(2):
                    try:
                        if i:
                            print("Waiting for 2nd Player to connect")
                        conn, addr=self.s.accept()
                        print('Connected by', addr[0])
                        conn_list.append(conn)
                    except:
                        self.running=False
                    """
        por lo que he visto habria que usar threads o process para snake_position
        """
