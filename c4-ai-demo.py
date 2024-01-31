import pygame
import time
import math
import random

import connectfour
import c4minimax as c4

RED = (255, 0, 0)
YELLOW = (255,255,0)
EMPTY = (0, 0, 0)


class ConnectFour:
    def __init__(self):
        pygame.init()

        self._surface = pygame.display.set_mode((700, 700))
        self._running = True

        self.game_state = connectfour.new_game(7, 6)
        self.turn = 1
        self.winner = -1

    def draw_screen(self):
        self._surface.fill((0, 0, 0))

        self.draw_frame()

        pygame.display.flip()

    def draw_frame(self):
        """Starts at y=100, x = 50 with radius of 20, and """
        pygame.draw.rect(self._surface, (0, 0, 255), pygame.Rect(0, 100, 700, 600))
        board = _flip_board(self.game_state)
        for j in range(6):
            y = 150 + j * 100
            for i in range(7):
                x = 50 + i * 100
                if board[j][i] == 0:
                    color = EMPTY
                elif board[j][i] == 1:
                    color = RED
                elif board[j][i] == 2:
                    color = YELLOW

                pygame.draw.circle(self._surface, color, (x, y), 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
            if event.type == pygame.MOUSEBUTTONUP and self.turn == 1:
                mouse_pos = pygame.mouse.get_pos()[0] // 100
                # print(mouse_pos)
                try:
                    self.game_state = connectfour.drop(self.game_state, mouse_pos)
                    self.turn = 2
                    self.draw_screen()
                except connectfour.InvalidMoveError:
                    pass

    def check_win(self):
        winner = connectfour.winner(self.game_state)

        if winner == 0:
            if connectfour.is_full(self.game_state):
                self.winner = 0
                return True
            else:
                return False
        elif winner == 1 or winner == 2:
            self.winner = winner
            return True

    def run(self):
        while self._running:
            self.handle_events()

            if self.check_win():
                if self.winner == 1:
                    print("RED WON")
                elif self.winner == 2:
                    print("YELLOW WON")
                elif self.winner == 0:
                    print("IT'S A TIE")

                pygame.time.wait(5000)
                break

            if self.turn == 2:
                ai_move = c4.mini_max(self.game_state, alpha = -math.inf, beta = math.inf,
                                                maximizing_player = True, depth = 6)[0]
                self.game_state = connectfour.drop(self.game_state, ai_move)
                self.turn = 1

            self.draw_screen()


def _flip_board(game_state: connectfour.GameState):
    converted_board = [[None for x in range(7)] for y in range(6)]

    # flips the x and y axis so they are correctly oriented
    for y in range(6):
        for x in range(7):
            converted_board[y][x] = game_state.board[x][y]

    return converted_board


if __name__ == '__main__':
    ConnectFour().run()