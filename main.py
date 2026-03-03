import pygame
import random
import sys
import os

pygame.init()

# Screen dimensions
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Colorful Snake Game with High Score')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load sounds
eat_sound = pygame.mixer.Sound('eat.wav')
gameover_sound = pygame.mixer.Sound('gameover.wav')

# Snake settings
block_size = 20
snake_speed = 15

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)

# High score file path
high_score_file = "high_score.txt"

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open(high_score_file, 'w') as file:
        file.write(str(score))

def get_color(index, total_segments):
    """Generate rainbow colors for snake segments."""
    hue = int(255 * index / total_segments)
    return (hue, 255 - hue, 128)

def show_score(score, high_score):
    """Display current score and high score."""
    score_text = font.render("Score: " + str(score), True, white)
    high_score_text = font.render("High Score: " + str(high_score), True, white)
    window.blit(score_text, [0, 0])
    window.blit(high_score_text, [0, 30])

def show_game_over(score, high_score):
    font_large = pygame.font.SysFont(None, 50)
    text = font_large.render("Game Over! Score: " + str(score), True, white)
    high_score_text = font.render("High Score: " + str(high_score), True, white)
    restart_text = font.render("Press R to Restart or Q to Quit", True, white)
    window.fill(black)
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 70))
    window.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, height // 2 - 20))
    window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def game_loop():
    high_score = load_high_score()

    # Initialize snake position
    x1 = width // 2
    y1 = height // 2
    x1_change = 0
    y1_change = 0

    snake_body = []
    length_of_snake = 1
    score = 0
    milestone_bonus = 50  # Bonus points for milestones
    last_milestone = 0

    # Food positions and types
    foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, height - block_size) / block_size) * block_size
    # Food type: normal or special
    food_type = 'normal'  # can be 'normal' or 'special'

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Fill background
        window.fill(black)

        # Draw food with different colors based on type
        if food_type == 'normal':
            food_color = (0, 255, 0)
            food_points = 10
        else:  # special food
            food_color = (255, 215, 0)
            food_points = 30

        pygame.draw.rect(window, food_color, [foodx, foody, block_size, block_size])

        # Update snake body
        snake_head = [x1, y1]
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        # Draw snake with rainbow colors
        total_segments = len(snake_body)
        for index, segment in enumerate(snake_body):
            color = get_color(index, total_segments)
            pygame.draw.rect(window, color, [segment[0], segment[1], block_size, block_size])

        # Show scores
        show_score(score, high_score)

        pygame.display.update()

        # Check for collision with food
        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            score += food_points
            # Check for milestone bonus
            if score - last_milestone >= milestone_bonus:
                score += 20  # bonus points
                last_milestone = score
            if score > high_score:
                high_score = score
            # Generate new food
            foodx = round(random.randrange(0, width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, height - block_size) / block_size) * block_size
            # Randomly decide new food type
            food_type = 'special' if random.random() < 0.2 else 'normal'
            # Increase snake length
            length_of_snake += 1

        # Check for collisions with walls
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            pygame.mixer.Sound.play(gameover_sound)
            save_high_score(high_score)
            game_over = True

        # Check for self-collision
        for segment in snake_body[:-1]:
            if segment == snake_head:
                pygame.mixer.Sound.play(gameover_sound)
                save_high_score(high_score)
                game_over = True

        clock.tick(snake_speed)

    # Show game over screen
    show_game_over(score, high_score)

# Start the game
game_loop()
