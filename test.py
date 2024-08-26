import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tennis Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Game states
MENU = 0
SETTINGS = 1
GAME = 2

# Game variables
player_score = 0
ai_score = 0
ai_difficulty = 5  # Default difficulty (1-10)

# Player paddle
player = pygame.Rect(50, HEIGHT // 2 - 40, 10, 80)
player_speed = 5

# AI paddle
ai = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 40, 10, 80)
ai_speed = 5

# Ball
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Tennis court dimensions
court_width = WIDTH - 100
court_height = HEIGHT - 100
court = pygame.Rect(50, 50, court_width, court_height)

# Main menu buttons
play_button = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
settings_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
quit_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)

# Settings
difficulty_slider = pygame.Rect(WIDTH // 2 - 100, 300, 200, 20)
slider_handle = pygame.Rect(WIDTH // 2 - 100 + (ai_difficulty - 1) * 20, 295, 10, 30)

def draw_menu():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, play_button)
    pygame.draw.rect(screen, WHITE, settings_button)
    pygame.draw.rect(screen, WHITE, quit_button)
    
    play_text = font.render("Play", True, BLACK)
    settings_text = font.render("Settings", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)
    
    screen.blit(play_text, (play_button.x + 70, play_button.y + 10))
    screen.blit(settings_text, (settings_button.x + 50, settings_button.y + 10))
    screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

def draw_settings():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, difficulty_slider)
    pygame.draw.rect(screen, BLACK, slider_handle)
    
    difficulty_text = font.render(f"AI Difficulty: {ai_difficulty}", True, WHITE)
    screen.blit(difficulty_text, (WIDTH // 2 - 100, 250))

def draw_game():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, court, 2)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), 2)
    
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, ai)
    pygame.draw.rect(screen, WHITE, ball)
    
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_score}", True, WHITE)
    screen.blit(player_text, (50, 20))
    screen.blit(ai_text, (WIDTH - 150, 20))

def move_ai():
    if ai.top < ball.y:
        ai.y += min(ai_speed, ball.y - ai.top)
    elif ai.bottom > ball.y:
        ai.y -= min(ai_speed, ai.bottom - ball.y)

def move_ball():
    global ball_speed_x, ball_speed_y, player_score, ai_score
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    if ball.top <= 50 or ball.bottom >= HEIGHT - 50:
        ball_speed_y *= -1
    
    if ball.colliderect(player) or ball.colliderect(ai):
        ball_speed_x *= -1
    
    if ball.left <= 0:
        ai_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
    
    if ball.right >= WIDTH:
        player_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))

def main():
    global ai_difficulty, ai_speed
    
    clock = pygame.time.Clock()
    game_state = MENU
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == MENU:
                    if play_button.collidepoint(event.pos):
                        game_state = GAME
                    elif settings_button.collidepoint(event.pos):
                        game_state = SETTINGS
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                elif game_state == SETTINGS:
                    if difficulty_slider.collidepoint(event.pos):
                        ai_difficulty = (event.pos[0] - difficulty_slider.x) // 20 + 1
                        slider_handle.x = difficulty_slider.x + (ai_difficulty - 1) * 20
                        ai_speed = ai_difficulty * 0.5
        
        keys = pygame.key.get_pressed()
        if game_state == GAME:
            if keys[pygame.K_UP] and player.top > 50:
                player.y -= player_speed
            if keys[pygame.K_DOWN] and player.bottom < HEIGHT - 50:
                player.y += player_speed
            
            move_ai()
            move_ball()
        
        if game_state == MENU:
            draw_menu()
        elif game_state == SETTINGS:
            draw_settings()
        elif game_state == GAME:
            draw_game()
        
        pygame.display.flip()
        clock.tick(75)

if __name__ == "__main__":
    main()