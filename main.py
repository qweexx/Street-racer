import pygame
import sys
import random

pygame.init()

# Настройка окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Street Racer')
clock = pygame.time.Clock()

# цвет
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# настр дороги
NUM_LANES = 4
LANE_WIDTH = WIDTH // NUM_LANES
ROAD_Y_START = 0
ROAD_SPEED = 5

# машина
car_width = 50
car_height = 100
# старт поз 2 полоса
car_lane = 1
car_x = LANE_WIDTH * car_lane + (LANE_WIDTH - car_width) // 2
car_y = HEIGHT - car_height - 50

road_offset = 0
enemies = []
spawn_timer = 0
running = True
score = 0
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # перезапуск по пробелу
            if game_over and event.key == pygame.K_SPACE:
                car_lane = 1
                enemies.clear()
                spawn_timer = 0
                score = 0
                game_over = False

            # управление если игра идет
            if not game_over:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if car_lane > 0:
                        car_lane -= 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if car_lane < NUM_LANES - 1:
                        car_lane += 1

    # обновление только если игра идет
    if not game_over:
        # анимка движения дороги
        road_offset = (road_offset + ROAD_SPEED) % 100

        # обнов поз кар
        car_x = LANE_WIDTH * car_lane + (LANE_WIDTH - car_width) // 2

        # счет
        score += 1

        # спавн врагов
        spawn_timer += 1
        if spawn_timer > 30:
            lane = random.randint(0, NUM_LANES - 1)
            enemy_x = lane * LANE_WIDTH + (LANE_WIDTH - car_width) // 2
            enemy_y = -car_height
            enemies.append([enemy_x, enemy_y, lane])
            spawn_timer = 0

        # враги вниз
        for enemy in enemies:
            enemy[1] += 5

        # удаление врагов за экраном
        enemies = [e for e in enemies if e[1] < HEIGHT]

        # ДТП
        player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], car_width, car_height)
            if player_rect.colliderect(enemy_rect):
                game_over = True

    # рисовка
    screen.fill(GRAY)

    # рисовка дороги
    for i in range(NUM_LANES):
        pygame.draw.rect(screen, (50, 50, 50), (i * LANE_WIDTH, 0, LANE_WIDTH, HEIGHT))

    # ЛИния разметки
    for lane in range(1, NUM_LANES):
        line_x = lane * LANE_WIDTH
        for y in range(0, HEIGHT, 40):
            line_y = (y + road_offset) % HEIGHT
            pygame.draw.rect(screen, WHITE, (line_x - 2, line_y, 4, 20))

    # рисовка кар гг
    pygame.draw.rect(screen, YELLOW, (car_x, car_y, car_width, car_height))
    pygame.draw.rect(screen, (0, 0, 0), (car_x + 5, car_y + 10, car_width - 10, 20))

    # рисовка врага
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], car_width, car_height))

    # счет на экран
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # экран проигрыша
    if game_over:
        dark = pygame.Surface((WIDTH, HEIGHT))
        dark.set_alpha(180)
        dark.fill((0, 0, 0))
        screen.blit(dark, (0, 0))

        big_font = pygame.font.Font(None, 72)
        game_over_text = big_font.render("GAME OVER", True, RED)
        score_final = font.render(f'Score: {score}', True, WHITE)
        restart_text = font.render("Press SPACE to restart", True, WHITE)

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        screen.blit(score_final, score_final.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()