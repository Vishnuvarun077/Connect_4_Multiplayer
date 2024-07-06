import pygame
import socket
import pickle
import threading
import random
import math
import sys
# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 700
GRID_SIZE = (7, 6)
CIRCLE_RADIUS = 40
GRID_OFFSET = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Multiplayer Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Create the game grid
grid = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]

# Scores and current player
score = [0, 0]
current_player = 1

# Game state
game_over = False
winner = None
game_started = False
show_instructions = False

# Player colors
player_colors = [RED, YELLOW]

# Network settings
HOST = '127.0.0.1'
PORT = 65432

# Socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
is_server = input("Do you want to be the server? (y/n): ").lower() == 'y'

if is_server:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
else:
    s.connect((HOST, PORT))
    conn = s

# Animation variables
particles = []
bubbles = []

def create_particles(x, y):
    for _ in range(20):
        particles.append({
            'x': x,
            'y': y,
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-2, 2),
            'radius': random.randint(2, 5),
            'color': random.choice([RED, YELLOW, BLUE, GREEN, PURPLE]),
            'life': 100
        })

def update_particles():
    for particle in particles[:]:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['life'] -= 1
        if particle['life'] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['radius'])

def create_bubbles():
    for _ in range(20):
        bubbles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(HEIGHT, HEIGHT + 100),
            'radius': random.randint(5, 20),
            'speed': random.uniform(0.5, 2),
            'color': random.choice([RED, YELLOW, BLUE, GREEN, PURPLE])
        })

def update_bubbles():
    for bubble in bubbles:
        bubble['y'] -= bubble['speed']
        if bubble['y'] + bubble['radius'] < 0:
            bubble['y'] = HEIGHT + bubble['radius']

def draw_bubbles():
    for bubble in bubbles:
        pygame.draw.circle(screen, bubble['color'], (int(bubble['x']), int(bubble['y'])), bubble['radius'])

def draw_welcome_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    title = font.render("Connect 4 Multiplayer Game", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start Game", True, BLACK)
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT // 2, 200, 50))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 10))

    draw_bubbles()

def draw_instructions():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    instructions = [
        "How to play:",
        "1. Click on a column to drop your piece",
        "2. Try to connect 4 pieces vertically, horizontally, or diagonally",
        "3. The first player to connect 4 pieces wins!",
        "4. Use the restart button to start a new game",
        "5. Click the end button to quit the game"
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 50 + i * 40))

    proceed_text = font.render("Proceed", True, BLACK)
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT - 100, 200, 50))
    screen.blit(proceed_text, (WIDTH // 2 - proceed_text.get_width() // 2, HEIGHT - 90))

def draw_board():
    screen.fill(BLACK)
    for row in range(GRID_SIZE[1]):
        for col in range(GRID_SIZE[0]):
            pygame.draw.circle(screen, WHITE, 
                               (col * (CIRCLE_RADIUS * 2 + 10) + GRID_OFFSET, 
                                row * (CIRCLE_RADIUS * 2 + 10) + GRID_OFFSET), 
                               CIRCLE_RADIUS)
            if grid[row][col] != 0:
                pygame.draw.circle(screen, player_colors[grid[row][col]-1], 
                                   (col * (CIRCLE_RADIUS * 2 + 10) + GRID_OFFSET, 
                                    row * (CIRCLE_RADIUS * 2 + 10) + GRID_OFFSET), 
                                   CIRCLE_RADIUS - 5)

    # Draw scoreboard
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Player 1: {score[0]}  Player 2: {score[1]}", True, WHITE)
    screen.blit(score_text, (20, HEIGHT - 60))

    # Draw active player indicator
    active_text = font.render(f"Active Player: {current_player}", True, WHITE)
    screen.blit(active_text, (WIDTH // 2 - active_text.get_width() // 2, HEIGHT - 60))

    # Draw restart button
    pygame.draw.rect(screen, GREEN, (20, HEIGHT - 40, 130, 30))
    restart_text = font.render("Restart", True, BLACK)
    screen.blit(restart_text, (30, HEIGHT - 35))

    # Draw end button
    pygame.draw.rect(screen, RED, (WIDTH - 150, HEIGHT - 40, 130, 30))
    end_text = font.render("End Game", True, BLACK)
    screen.blit(end_text, (WIDTH - 140, HEIGHT - 35))

    # Draw game over message
    if game_over:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0, 0))
        if winner:
            message = f"Player {winner} wins! Click to play again."
        else:
            message = "It's a draw! Click to play again."
        game_over_text = font.render(message, True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    draw_particles()

def get_column(pos):
    return (pos[0] - GRID_OFFSET) // (CIRCLE_RADIUS * 2 + 10)

def check_win(player):
    # Check horizontal
    for row in range(GRID_SIZE[1]):
        for col in range(GRID_SIZE[0] - 3):
            if all(grid[row][col+i] == player for i in range(4)):
                return True

    # Check vertical
    for row in range(GRID_SIZE[1] - 3):
        for col in range(GRID_SIZE[0]):
            if all(grid[row+i][col] == player for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(GRID_SIZE[1] - 3):
        for col in range(GRID_SIZE[0] - 3):
            if all(grid[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(GRID_SIZE[1] - 3):
        for col in range(3, GRID_SIZE[0]):
            if all(grid[row+i][col-i] == player for i in range(4)):
                return True

    return False

def check_draw():
    return all(grid[0][col] != 0 for col in range(GRID_SIZE[0]))

def reset_game():
    global grid, current_player, game_over, winner
    grid = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
    current_player = 1
    game_over = False
    winner = None

def receive_data():
    global grid, current_player, game_over, winner, score, player_colors
    while True:
        try:
            data = conn.recv(1024)
            if data:
                received = pickle.loads(data)
                grid = received['grid']
                current_player = received['current_player']
                game_over = received['game_over']
                winner = received['winner']
                score = received['score']
                player_colors = received['player_colors']
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def send_data():
    try:
        conn.sendall(pickle.dumps({
            'grid': grid,
            'current_player': current_player,
            'game_over': game_over,
            'winner': winner,
            'score': score,
            'player_colors': player_colors
        }))
    except Exception as e:
        print(f"Error sending data: {e}")

def choose_color():
    global player_colors
    colors = [RED, YELLOW, BLUE, GREEN]
    random.shuffle(colors)
    player_colors = colors[:2]
    send_data()

# Start receive thread
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

# Choose initial colors
if is_server:
    choose_color()

# Create initial bubbles
create_bubbles()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                if WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 <= event.pos[1] <= HEIGHT // 2 + 50:
                    show_instructions = True
                    game_started = True
                    create_particles(event.pos[0], event.pos[1])
            elif show_instructions:
                if WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT - 100 <= event.pos[1] <= HEIGHT - 50:
                    show_instructions = False
                    create_particles(event.pos[0], event.pos[1])
            elif game_over:
                reset_game()
                send_data()
            elif 20 <= event.pos[0] <= 150 and HEIGHT - 40 <= event.pos[1] <= HEIGHT - 10:
                # Restart button clicked
                reset_game()
                if is_server:
                    choose_color()
                send_data()
            elif WIDTH - 150 <= event.pos[0] <= WIDTH - 20 and HEIGHT - 40 <= event.pos[1] <= HEIGHT - 10:
                # End button clicked
                running = False
            elif (is_server and current_player == 1) or (not is_server and current_player == 2):
                col = get_column(event.pos)
                if 0 <= col < GRID_SIZE[0]:
                    for row in range(GRID_SIZE[1]-1, -1, -1):
                        if grid[row][col] == 0:
                            grid[row][col] = current_player
                            create_particles(event.pos[0], event.pos[1])
                            if check_win(current_player):
                                print(f"Player {current_player} wins!")
                                score[current_player - 1] += 1
                                game_over = True
                                winner = current_player
                            elif check_draw():
                                print("It's a draw!")
                                game_over = True
                            else:
                                current_player = 3 - current_player  # Switch player
                            send_data()
                            break

    update_particles()
    update_bubbles()

    if not game_started:
        draw_welcome_screen()
    elif show_instructions:
        draw_instructions()
    else:
        draw_board()

    pygame.display.flip()
    clock.tick(60)
# Clean up
print("Thanks for playing!")
s.close()
pygame.quit()

if is_server:
    print("Server has been freed. You can now reuse it.")
else:
    print("Connection to server has been closed.")

sys.exit()
