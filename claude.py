import pygame
import random
import os
import math
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Tennis")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
player_img = pygame.image.load("img/player1.png")
ai_img = pygame.image.load("img/player2.png")
ball_img = pygame.image.load("img/ball.png")

# Scale images
player_img = pygame.transform.scale(player_img, (60, 60))
ai_img = pygame.transform.scale(ai_img, (60, 60))
ball_img = current_ball_img = pygame.transform.scale(ball_img, (30, 30))

# Player attributes
player_width, player_height = 60, 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

# AI attributes
ai_width, ai_height = 60, 60
ai_x = WIDTH // 2 - ai_width // 2
ai_y = 20
ai_speed = 3

# Ball attributes
ball_width, ball_height = 30, 30
ball_x = WIDTH // 2 - ball_width // 2
ball_y = HEIGHT // 2 - ball_height // 2
ball_speed_x = ball_speed_x_const = 5
ball_speed_y = ball_speed_y_const = -5

# Score
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

# menu, game, settings etc.
cur = "menu"

# Slider properties
slider_width = 300
slider_height = 10
slider_x = (WIDTH - slider_width) // 2
slider_y = HEIGHT // 2

knob_radius = 15
knob_x = 240 # starts at 3
knob_y = slider_y + slider_height // 2

player_collision_delay = 0
ai_collision_delay = 0
COLLISION_DELAY_TIME = 30  # Frames of delay (adjust as needed)



dragging = False
belief = False

# Button class
class Button:
    def __init__(self, text, y_pos):
        self.text = text
        self.y_pos = y_pos
        self.button_rect = pygame.Rect(WIDTH // 2 - 100, y_pos, 200, 50)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = GRAY if self.button_rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(surface, color, self.button_rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.button_rect.collidepoint(event.pos)
        return False

# Create buttons
play_button = Button("Play", 200)
settings_button = Button("Settings", 300)
quit_button = Button("Quit", 400)

def menu():
    screen.fill(WHITE)

    # draw title
    title_text = pygame.font.Font(None, 72).render("Tennis", True, GREEN)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)     

    play_button.draw(screen)
    settings_button.draw(screen)
    quit_button.draw(screen)


def game():
    global ai_x
    global player_x
    global ball_x
    global ball_y
    global ball_speed_x
    global ball_speed_y
    global player_score
    global ai_score
    global player_collision_delay
    global ai_collision_delay
    global current_ball_img
    global WHITE
    global GREEN
    global BLUE


    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Move AI
    if ai_x + ai_width // 2 < ball_x + ball_width // 2:
        ai_x += ai_speed
    elif ai_x + ai_width // 2 > ball_x + ball_width // 2:
        ai_x -= ai_speed

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= WIDTH - ball_width:
        ball_speed_x = -ball_speed_x

    # Ball collision with player/AI
    if ball_y <= ai_y + ai_height and ai_x < ball_x < ai_x + ai_width and ai_collision_delay == 0: # AI
        ball_speed_y = -ball_speed_y
        ai_collision_delay = COLLISION_DELAY_TIME
        current_ball_img = ball_img
        if belief:
            ball_speed_x = ball_speed_x_const if ball_speed_x > 0 else -ball_speed_x_const
            ball_speed_y = ball_speed_y_const if ball_speed_y < 0 else -ball_speed_y_const
    elif ball_y + ball_height >= player_y and player_x < ball_x < player_x + player_width and player_collision_delay == 0: # PLAYER
        ball_speed_y = -ball_speed_y
        player_collision_delay = COLLISION_DELAY_TIME
        
        if belief:
            if rng(90):
                play_sound("persona", vol=.3)
                ball_speed_x = ai_speed + 1 if ball_speed_x > 0 else -ai_speed - 1
                ball_speed_y = ai_speed * -2
                current_ball_img = apply_color_overlay(ball_img, random.choice(vibrant_colors))  # RANDOM overlay
            else:
                play_sound()
        
        # Get cursor position
        cursor_x, cursor_y = pygame.mouse.get_pos()
        
        # Calculate direction vector
        dx = cursor_x - (ball_x + ball_width // 2)
        dy = cursor_y - (ball_y + ball_height // 2)
        
        # Normalize the direction vector
        length = math.sqrt(dx**2 + dy**2)
        if length != 0:
            dx /= length
            dy /= length
        
        # Set new ball speed
        speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
        ball_speed_x = dx * speed
        ball_speed_y = -abs(dy * speed)  # Ensure the ball always goes up
    
    # Decrease collision delays
    if player_collision_delay > 0:
        player_collision_delay -= 1
    if ai_collision_delay > 0:
        ai_collision_delay -= 1
    


    # Scoring
    if ball_y <= 0: # player scores
        player_score += 1
        ball_x, ball_y = random.randint(70, 330), HEIGHT // 2 - ball_height // 2 + 100
        current_ball_img = ball_img
        if not belief:
            pygame.mixer.stop()
        play_sound("goal")
        if belief:
            ball_speed_x = ball_speed_x_const if ball_speed_x > 0 else -ball_speed_x_const
            ball_speed_y = ball_speed_y_const if ball_speed_y < 0 else -ball_speed_y_const
    elif ball_y >= HEIGHT: # ai scores
        ai_score += 1
        ball_x, ball_y = ai_x, HEIGHT // 2 - ball_height // 2 - 100
        if not belief:
            pygame.mixer.stop()
        play_sound()



    # Draw background
    screen.fill(GREEN)

    # Draw court lines
    pygame.draw.rect(screen, WHITE, (20, 20, WIDTH - 40, HEIGHT - 40), 2)
    pygame.draw.line(screen, WHITE, (20, HEIGHT // 2), (WIDTH - 20, HEIGHT // 2), 2)

    # Draw players and ball
    screen.blit(player_img, (player_x, player_y))
    screen.blit(ai_img, (ai_x, ai_y))
    screen.blit(current_ball_img, (ball_x, ball_y))

    # Draw cursor position indicator
    cursor_x, cursor_y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, RED, (cursor_x, cursor_y), 5)

    # Draw score backgrounds
    pygame.draw.rect(screen, WHITE, (5, HEIGHT - 45, 120 + (int(math.log10(player_score))) * 10 if player_score > 0 else 120, 40)) # Player score background; increases by 10 px for each digit
    pygame.draw.rect(screen, WHITE, (5, 5, 70 + (int(math.log10(ai_score))) * 10 if ai_score > 0 else 70, 40)) # AI

    # Draw score
    player_text = font.render(f"Player: {player_score}", True, BLACK)
    ai_text = font.render(f"AI: {ai_score}", True, BLACK)
    screen.blit(player_text, (10, HEIGHT - 40))
    screen.blit(ai_text, (10, 10))

def settings():

    # Drawing
    screen.fill(WHITE)

    diff = pygame.font.Font(None, 72).render("AI Difficulty", True, RED)
    title_rect = diff.get_rect(center=(WIDTH // 2, 100))
    screen.blit(diff, title_rect)
    
    # Draw slider bar
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
    
    # Draw knob
    pygame.draw.circle(screen, RED, (int(knob_x), knob_y), knob_radius)
    
    # Display value
    font = pygame.font.Font(None, 36)
    text = font.render(f"Value: {ai_speed}", True, BLACK if ai_speed < ball_speed_x_const else RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + 50))


def play_sound(dir="sfx", vol=1):
    sound = pygame.mixer.Sound(dir + "/" + random.choice(os.listdir(dir))) # random file from folder
    sound.set_volume(vol)
    if dir == "sfx" or sound.get_length() == 2:
        sound.set_volume(.3)
    sound.play()

def rng(n):
    x = random.randint(0, 100)
    if x <= n:
        return 1
    return 0

def apply_color_overlay(surface, color, alpha=128):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill(color + (alpha,))
    new_surface = surface.copy()
    new_surface.blit(overlay, (0,0), special_flags=pygame.BLEND_ADD)
    return new_surface

vibrant_colors = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128)
    ]





ball_img_fast = apply_color_overlay(ball_img, random.choice(vibrant_colors))  # RANDOM overlay

# Game loop
clock = pygame.time.Clock()
running = True

# lets dance
dance = pygame.mixer.Sound("sfx/dance.wav")
dance.set_volume(.3)

# vanadis
v = pygame.mixer.Sound("sfx/vanadis.wav")
v.set_volume(.3)

# i believe
believe = pygame.mixer.Sound("sfx/believe.wav")


# main
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or quit_button.is_clicked(event) and cur == "menu":
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and cur != "menu":
                cur = "menu"
                pygame.mixer.stop()
                play_sound()
        if play_button.is_clicked(event) and cur == "menu":
            print("Play clicked")
            cur = "game"
            pygame.mixer.stop()
            dance.play()
            if belief:
                believe.play(loops=-1)
        if settings_button.is_clicked(event) and cur == "menu":
            print("Settings clicked")
            cur = "settings"
            pygame.mixer.stop()
            v.play()
        
        if cur == "settings": 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    if (knob_x - knob_radius <= mouse_x <= knob_x + knob_radius and
                        knob_y - knob_radius <= mouse_y <= knob_y + knob_radius):
                        dragging = True
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            
            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, _ = event.pos
                knob_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                ai_speed = int((knob_x - slider_x) / slider_width * 6) + 1
                belief = True if ai_speed >= ball_speed_x_const else False

    if cur == "game":            
        game()
    if cur == "menu":
        menu()
    if cur == "settings":
        settings()
    # ... 



    # Update display
    pygame.display.flip()

    # frame rate
    clock.tick(75)



# Quit Pygame
pygame.quit()