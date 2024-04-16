import math
import tkinter as tk
from tkinter import messagebox

PLAYER = "O"
AI = "X"


class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.initialize_board()

    def initialize_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.root,
                    text="",
                    font="Arial 20 bold",
                    height=2,
                    width=5,
                    command=lambda row=i, col=j: self.player_move(row, col),
                )
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def player_move(self, row, col):
        if self.board[row][col] == " " and not self.check_game_over():
            self.board[row][col] = PLAYER
            self.buttons[row][col].config(text=PLAYER)
            if not self.check_game_over():
                self.ai_move()

    def ai_move(self):
        move = self.best_move()
        if move:
            self.board[move[0]][move[1]] = AI
            self.buttons[move[0]][move[1]].config(text=AI)
            self.check_game_over()

    def best_move(self):
        best_score = -math.inf
        best_move = None
        for i, j in self.get_available_moves():
            self.board[i][j] = AI
            score = self.minimax_algorithm(0, False)
            self.board[i][j] = " "
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_move

    def check_game_over(self):
        if self.victory(PLAYER):
            messagebox.showinfo("Game Over", "Você ganhou!")
            return True
        if self.victory(AI):
            messagebox.showinfo("Game Over", "A IA ganhou!")
            return True
        if not self.get_available_moves():
            messagebox.showinfo("Game Over", "Empate!")
            return True
        return False

    def victory(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
            if all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def get_available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]

    def minimax_algorithm(self, depth, is_maximizing):
        if self.victory(AI):
            return 10 - depth
        if self.victory(PLAYER):
            return depth - 10
        if not self.get_available_moves():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.get_available_moves():
                self.board[move[0]][move[1]] = AI
                score = self.minimax_algorithm(depth + 1, False)
                self.board[move[0]][move[1]] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.get_available_moves():
                self.board[move[0]][move[1]] = PLAYER
                score = self.minimax_algorithm(depth + 1, True)
                self.board[move[0]][move[1]] = " "
                best_score = min(score, best_score)
            return best_score


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
