import pygame
from random import randrange

# pygame initialisation
pygame.init()
clock = pygame.time.Clock()

# create game window, set resolution and window caption
resolution = 800
window = pygame.display.set_mode((resolution, resolution))
pygame.display.set_caption("Snake")

# game elements variables
size = 50
snake_x, snake_y = randrange(0, resolution, size), randrange(0, resolution, size)
food_x, food_y = randrange(0, resolution, size), randrange(0, resolution, size)
snake = [(snake_x, snake_y)]

snake_length = 1
colors = {
    "snake_color": (0, 255, 0),
    "food_color": (255, 0, 0),
}

# score
score = 0
font_score = pygame.font.SysFont("Arial", 26, bold=True)

# game over font
font_game_over = pygame.font.SysFont("Arial", 60, bold=True)

# directions
dx, dy = 0, 0
fps = 5

move_up, move_down, move_left, move_right = False, False, False, False


# game main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))

    # draw snake
    for i, j in snake:
        pygame.draw.rect(window, (colors["snake_color"]), (i, j, size, size))
    # draw food
    pygame.draw.rect(window, (colors["food_color"]), (food_x, food_y, size, size))


    # keyboard
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and not move_down:
        dx = 0
        dy = -1
        move_up = True
        move_down = False
        move_left = False
        move_right = False
    if key[pygame.K_DOWN] and not move_up:
        dx = 0
        dy = 1
        move_up = False
        move_down = True
        move_left = False
        move_right = False
    if key[pygame.K_LEFT] and not move_right:
        dx = -1
        dy = 0
        move_up = False
        move_down = False
        move_left = True
        move_right = False

    if key[pygame.K_RIGHT] and not move_left:
        dx = 1
        dy = 0
        move_up = False
        move_down = False
        move_left = False
        move_right = True

    # snake movement
    snake_x += dx * size
    snake_y += dy * size
    snake.append((snake_x, snake_y))
    snake = snake[-snake_length:]

    # collision with food
    if snake[-1][0] == food_x and snake[-1][1] == food_y:
        snake_length += 1
        food_x, food_y = randrange(0, resolution, size), randrange(0, resolution, size)
        fps += 1
        score += 1

    # if food appear on snakes body
    for i, j in enumerate(snake):
        if food_x == snake[i][0] and food_y == snake[i][1]:
            food_x, food_y = randrange(0, resolution, size), randrange(0, resolution, size)

    # snake touches window margins, teleport to other side
    if snake_y < 0:
        snake_y = resolution
    elif snake_y + size > resolution:
        snake_y = 0 - size
    elif snake_x < 0:
        snake_x = resolution
    elif snake_x + size > resolution:
        snake_x = 0 - size

    # detect body collision. GAME OVER
    snake_without_head = snake[:-1]
    for i, j in enumerate(snake_without_head):
        if snake_x == snake_without_head[i][0] and snake_y == snake_without_head[i][1]:
            while run:
                render_end = font_game_over.render("GAME OVER", 1, (255, 255, 255))
                window.blit(render_end, (resolution//2 - 150, resolution //3))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
    # score
    render_score = font_score.render(f'SCORE: {score}', 1, (255, 255, 255))
    window.blit(render_score, (5, 5))

    pygame.display.flip()
    clock.tick(fps)
