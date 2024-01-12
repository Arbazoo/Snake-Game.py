import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
BAR_HEIGHT = 65
WALL_WIDTH = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT + BAR_HEIGHT))
pygame.display.set_caption("The Snake")

# Load the background image
background_image = pygame.image.load("background_image.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT + BAR_HEIGHT))

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

snake_size = 20
snake_speed = 15

point_size = 20
point = (random.randint(0, (WIDTH - point_size) // 20) * 20, random.randint(0, (HEIGHT - point_size) // 20) * 20 + BAR_HEIGHT)

score = 0
highest_score = 0

try:
    highest_score = int(open("highest_score.txt", "r").read())
except FileNotFoundError:
    pass

def reset_game():
    global snake, snake_direction, point, score
    snake, snake_direction, score = [(100, 100 + BAR_HEIGHT), (90, 100 + BAR_HEIGHT), (80, 100 + BAR_HEIGHT)], (1, 0), 0
    point = (random.randint(0, (WIDTH - point_size - 2 * WALL_WIDTH) // 20) * 20 + WALL_WIDTH, random.randint(0, (HEIGHT - point_size - 2 * WALL_WIDTH) // 20) * 20 + BAR_HEIGHT + WALL_WIDTH)

def update_highest_score():
    global highest_score
    if score > highest_score:
        highest_score = score
        open("highest_score.txt", "w").write(str(highest_score))

reset_game()


def game_over_screen():
    game_over_textfont = pygame.font.Font(None, 100)
    restart_textfont = pygame.font.Font(None, 50)
    game_over_text = game_over_textfont.render("Game Over", True, (232, 54, 42))
    restart_text = restart_textfont.render("Press R to Restart or Q to Quit", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 30))
    screen.blit(restart_text, (WIDTH // 2 - 250, HEIGHT // 2 + 100))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_highest_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    update_highest_score()
                    reset_game()
                    return
                elif event.key == pygame.K_q:
                    update_highest_score()
                    pygame.quit()
                    sys.exit()

reset_game()

# Define the walls
left_wall = pygame.image.load("left_wall_image.png")
right_wall = pygame.image.load("right_wall_image.png")
top_wall = pygame.image.load("top_wall_image.png")
bottom_wall = pygame.image.load("bottom_wall_image.png")

# Scale the images to fit the walls
left_wall = pygame.transform.scale(left_wall, (WALL_WIDTH, HEIGHT))
right_wall = pygame.transform.scale(right_wall, (WALL_WIDTH, HEIGHT))
top_wall = pygame.transform.scale(top_wall, (WIDTH, WALL_WIDTH))
bottom_wall = pygame.transform.scale(bottom_wall, (WIDTH, WALL_WIDTH))

# Load point, head, and body images
point_image = pygame.image.load("point_image.png")
point_image = pygame.transform.scale(point_image, (point_size, point_size))

head_image = pygame.image.load("head_image.png")
head_image = pygame.transform.scale(head_image, (snake_size, snake_size))

body_image = pygame.image.load("body_image.png")
body_image = pygame.transform.scale(body_image, (snake_size, snake_size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_highest_score()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1): snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1): snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0): snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0): snake_direction = (1, 0)
            elif event.key == pygame.K_r: update_highest_score(); reset_game()

    new_head = (snake[0][0] + snake_direction[0] * snake_size, snake[0][1] + snake_direction[1] * snake_size)
    snake.insert(0, new_head)

    if snake[0] == point:
        score += 1
        point = (random.randint(0, (WIDTH - point_size - 2 * WALL_WIDTH) // 20) * 20 + WALL_WIDTH, random.randint(0, (HEIGHT - point_size - 2 * WALL_WIDTH) // 20) * 20 + BAR_HEIGHT + WALL_WIDTH)
    else:
        snake.pop()

    if (
        snake[0][0] < WALL_WIDTH
        or snake[0][0] >= WIDTH - WALL_WIDTH
        or snake[0][1] < BAR_HEIGHT + WALL_WIDTH
        or snake[0][1] >= HEIGHT + BAR_HEIGHT - WALL_WIDTH
    ):
        game_over_screen()

    if len(snake) > 1 and new_head in snake[1:]:
        game_over_screen()

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw walls
    screen.blit(left_wall, (0, BAR_HEIGHT))
    screen.blit(right_wall, (WIDTH - WALL_WIDTH, BAR_HEIGHT))
    screen.blit(top_wall, (0, BAR_HEIGHT))
    screen.blit(bottom_wall, (0, HEIGHT + BAR_HEIGHT - WALL_WIDTH))

    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, BAR_HEIGHT))

    # Draw snake
    for i, segment in enumerate(snake):
        if i == 0:
            # Rotate the head image based on the snake direction
            angle = 0
            if snake_direction == (1, 0):
                angle = 180
            elif snake_direction == (0, 1):
                angle = 90
            elif snake_direction == (0, -1):
                angle = -90
            rotated_head = pygame.transform.rotate(head_image, angle)
            screen.blit(rotated_head, (segment[0], segment[1]))
            
        else:
            screen.blit(body_image, (segment[0], segment[1]))

    # Draw point image
    screen.blit(point_image, (point[0], point[1]))

    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    highest_score_text = font.render(f"Highest Score: {highest_score}", True, (232, 54, 42))
    screen.blit(highest_score_text, (10, 40))
    
    Names = font.render("Project by: Arbaz, Shariq, Aliyan & Hafsa ", True, (212, 180, 2))
    screen.blit(Names, (380, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(snake_speed)