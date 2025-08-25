import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600  
FONT = pygame.font.Font("C:\\Users\\SHIKO\\Downloads\\Roboto-Regular.ttf", 60)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("XO Game")

BOARD = pygame.transform.scale(pygame.image.load("C:\\Users\\SHIKO\\Downloads\\Board.png"), (WIDTH - 64, HEIGHT - 64))
X_IMG = pygame.transform.scale(pygame.image.load("C:\\Users\\SHIKO\\Downloads\\X.png"), (120, 120))
O_IMG = pygame.transform.scale(pygame.image.load("C:\\Users\\SHIKO\\Downloads\\O.png"), (120, 120))
O_IMG_WIN = pygame.transform.scale(pygame.image.load("C:\\Users\\SHIKO\\Downloads\\Winning O.png"), (120, 120))

BG_COLOR = (214, 201, 227)

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
graphical_board = [[[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]]]
to_move = 'X'

def render_board(lettered_board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if lettered_board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j*200+100, i*200+100))
            elif lettered_board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j*200+100, i*200+100))

def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = current_pos[0] // 200
    converted_y = current_pos[1] // 200

    if board[converted_y][converted_x] == ' ':
        board[converted_y][converted_x] = to_move
        render_board(board, X_IMG, O_IMG)
        return board, 'O' if to_move == 'X' else 'X'
    return board, to_move

def check_winner(board):
    for row in board:
        if row.count(row[0]) == 3 and row[0] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

def get_winning_positions(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return [(i, 0), (i, 1), (i, 2)]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return [(0, i), (1, i), (2, i)]
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return [(0, 2), (1, 1), (2, 0)]
    return []

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def minimax(board, is_maximizing , depth):
    winner = check_winner(board)
    if winner == 'X':
        return -10 + depth
    elif winner == 'O':
        return 10 - depth
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, False , depth + 1)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, True , depth + 1)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def ai_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, False , 0)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
        return True
    return False


SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (32, 32))
pygame.display.update()


game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and to_move == 'X' and not game_over:
            board, to_move = add_XO(board, graphical_board, to_move)

            winner = check_winner(board)
            SCREEN.fill(BG_COLOR)
            SCREEN.blit(BOARD, (32, 32))
            render_board(board, X_IMG, O_IMG)
            
        
            if check_winner(board) is None and not is_draw(board) and to_move == 'O' :
                ai_move(board)
                to_move = 'X'
                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (32, 32))
                render_board(board, X_IMG, O_IMG)

            if to_move == 'O' and not game_over:
             ai_move(board)
            winner = check_winner(board)
            if winner == 'O':
                winning_cells = get_winning_positions(board)

                for i, j in winning_cells:
                    graphical_board[i][j][0] = O_IMG_WIN

                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (32, 32))
                for i in range(3):
                    for j in range(3):
                        if graphical_board[i][j][0] is not None:
                            SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
                pygame.display.update()      

                pygame.time.delay(1000)
                SCREEN.fill(BG_COLOR)
                pygame.display.update()

                msg = FONT.render("AI Wins!", True, (255, 0, 0))
                SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
                pygame.display.update()

                game_over = True

            elif is_draw(board):

                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (32, 32))
                render_board(board, X_IMG, O_IMG)
                for i in range(3):
                    for j in range(3):
                        if graphical_board[i][j][0] is not None:
                            SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
                pygame.display.update()

                pygame.time.delay(1000)

                SCREEN.fill(BG_COLOR)
                pygame.display.update()


                msg = FONT.render("It's a Draw!", True, (255, 0, 0))
                SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
                pygame.display.update()

                game_over = True
            else:
               to_move = "X"
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                board = [[' ' for _ in range(3)] for _ in range(3)]
                graphical_board = [[[None, None] for _ in range(3)] for _ in range(3)] 
                to_move = 'X'
                game_over = False
                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (32, 32))
                pygame.display.update()

    if not game_over:
        for i in range(3):
            for j in range(3):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
        pygame.display.update()