import math

PLAYER = "O"
AI = "X"


def print_board(board):
    """Imprime o tabuleiro"""
    for row in board:
        print("|".join(row))
    print()


def victory(board_state, player):
    """Verifica se o jogador venceu"""
    for i in range(3):
        # Vitoria por linha
        if all([cell == player for cell in board_state[i]]):
            return True

        # Vitoria por coluna
        if all([board_state[j][i] == player for j in range(3)]):
            return True

    # Vitoria por diagonal
    if all([board_state[i][i] == player for i in range(3)]):
        return True
    if all([board_state[i][2 - i] == player for i in range(3)]):
        return True

    return False


def get_available_moves(board_state):
    """Retorna as jogadas disponíveis no tabuleiro"""
    return [(i, j) for i in range(3) for j in range(3) if board_state[i][j] == " "]


def minimax_algorithm(board_state, depth, is_maximizing):
    """Algoritmo minimax"""
    if victory(board_state, AI):
        return 10 - depth
    if victory(board_state, PLAYER):
        return depth - 10
    if not get_available_moves(board_state):
        return 0

    # Para maximizar o score da IA
    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board_state):
            board_state[move[0]][move[1]] = AI
            score = minimax_algorithm(board_state, depth + 1, False)
            board_state[move[0]][move[1]] = " "
            best_score = max(score, best_score)
        return best_score
    # Para minimizar o score do jogador
    else:
        best_score = math.inf
        for move in get_available_moves(board_state):
            board_state[move[0]][move[1]] = PLAYER
            score = minimax_algorithm(board_state, depth + 1, True)
            board_state[move[0]][move[1]] = " "
            best_score = min(score, best_score)
        return best_score


def best_move(board_state):
    """Retorna a melhor jogada utilizando o algoritmo minimax"""
    best_score = -math.inf
    best_move = None
    for i, j in get_available_moves(board_state):
        board_state[i][j] = AI
        score = minimax_algorithm(board_state, 0, False)
        board_state[i][j] = " "
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move


def check_game_over(board_state):
    """Verifica se o jogo acabou"""
    if victory(board_state, PLAYER):
        print_board(board_state)
        print("Você venceu!")
        return True
    if victory(board_state, AI):
        print_board(board_state)
        print("A IA venceu!")
        return True
    if not get_available_moves(board_state):
        print_board(board_state)
        print("Empate!")
        return True
    return False


def main():
    """Função principal do jogo"""
    board = [[" " for _ in range(3)] for _ in range(3)]
    print_board(board)

    while True:
        try:
            row, col = map(int, input("Digite a linha e a coluna (0-2): ").split())
            if not (0 <= row <= 2 and 0 <= col <= 2):
                raise ValueError("Valores inválidos")
            if board[row][col] != " ":
                raise ValueError("Joga inválida")
            board[row][col] = PLAYER
        except ValueError as e:
            print(e)
            continue

        if check_game_over(board):
            break

        move = best_move(board)
        if move:
            board[move[0]][move[1]] = AI
        else:
            print("Não há mais jogadas disponíveis")

        if check_game_over(board):
            break

        print_board(board)


if __name__ == "__main__":
    main()
