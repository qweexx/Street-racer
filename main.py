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
enemy_speed = 5

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
cash = []
cash_timer = 30
running = True
score = 0
best_score = 0
cash_count = 0
best_cash = 0
game_over = False
in_menu = True
speed = 5
# картинки машин
try:
    player_img = pygame.image.load('images/player_car.png')
    player_img = pygame.transform.scale(player_img, (car_width, car_height))
except:
    player_img = None
try:
    enemy_img = pygame.image.load('images/enemy_car.png')
    enemy_img = pygame.transform.scale(enemy_img, (car_width, car_height))
    enemy_img = pygame.transform.flip(enemy_img, False, True)
except:
    enemy_img = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # перезапуск или старт по пробелу
            if event.key == pygame.K_SPACE:
                if game_over:
                    car_lane = 1
                    enemies.clear()
                    cash.clear()
                    cash_timer = 0
                    cash_count = 0
                    spawn_timer = 0
                    score = 0
                    enemy_speed = 5
                    game_over = False
                elif in_menu:
                    in_menu = False
            # выход в меню или выход из игры
            if event.key == pygame.K_ESCAPE:
                if in_menu:
                    running = False
                else:
                    in_menu = True
                    game_over = False

            # управление если игра идет
            if not game_over and not in_menu:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if car_lane > 0:
                        car_lane -= 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if car_lane < NUM_LANES - 1:
                        car_lane += 1

    # меню
    if in_menu:
        screen.fill((0, 0, 0))

        big_font = pygame.font.Font(None, 72)
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        title = big_font.render("STREET RACER", True, YELLOW)
        start = font.render("Press SPACE to start", True, WHITE)
        exit_text = small_font.render("Press ESC to exit", True, GRAY)
        best = font.render(f"Best Score: {best_score}", True, GREEN)
        best_c = font.render(f"Best Cash: {best_cash}", True, GREEN)

        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        screen.blit(start, start.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(exit_text, exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        screen.blit(best, best.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))
        screen.blit(best_c, best_c.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140)))

        pygame.display.flip()
        clock.tick(60)
        continue

    # обновление только если игра идет
    if not game_over and not in_menu:
        # анимка движения дороги
        road_offset = (road_offset + ROAD_SPEED) % 100

        # обнов поз кар
        car_x = LANE_WIDTH * car_lane + (LANE_WIDTH - car_width) // 2

        # счет
        score += 1
        # скорость врагов
        if score % 60 == 0:
            enemy_speed += 0.5

        # спавн врагов
        spawn_timer += 1
        if spawn_timer > 30:
            busy_lanes = []
            for enemy in enemies:
                if enemy[1] < 200:
                    busy_lanes.append(enemy[2])
            free_lanes = [l for l in range(NUM_LANES) if l not in busy_lanes]
            if free_lanes:
                lane = random.choice(free_lanes)
                enemy_x = lane * LANE_WIDTH + (LANE_WIDTH - car_width) // 2
                enemy_y = -car_height
                enemies.append([enemy_x, enemy_y, lane])
            spawn_timer = 0

        # спавн лавэхи
        cash_timer += 1
        if cash_timer > 60:
            free_lanes = []
            for l in range(NUM_LANES):
                closest_enemy = 999
                for enemy in enemies:
                    if enemy[2] == l and enemy[1] < closest_enemy:
                        closest_enemy = enemy[1]
                if closest_enemy > 150 or closest_enemy == 999:
                    free_lanes.append(l)

            if not free_lanes:
                best_lane = 0
                best_distance = 0
                for l in range(NUM_LANES):
                    closest_enemy = 999
                    for enemy in enemies:
                        if enemy[2] == l and enemy[1] < closest_enemy:
                            closest_enemy = enemy[1]
                    if closest_enemy > best_distance:
                        best_distance = closest_enemy
                        best_lane = l
                cash_lane = best_lane
            else:
                cash_lane = random.choice(free_lanes)

            cash_x = cash_lane * LANE_WIDTH + LANE_WIDTH // 2
            cash_y = -30
            cash.append([cash_x, cash_y])
            cash_timer = 0

        # враги вниз
        for enemy in enemies:
            enemy[1] += enemy_speed
        for c in cash:
            c[1] += enemy_speed

        # удаление врагов за экраном
        enemies = [e for e in enemies if e[1] < HEIGHT]

        # ДТП
        player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], car_width, car_height)
            if player_rect.colliderect(enemy_rect):
                game_over = True

        # сбор денег
        for c in cash[:]:
            cash_rect = pygame.Rect(c[0] - 10, c[1] - 10, 20, 20)
            if player_rect.colliderect(cash_rect):
                cash.remove(c)
                score += 10
                cash_count += 1

        # удаление лавэхи за экраном
        cash = [c for c in cash if c[1] < HEIGHT]

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
    if player_img:
        screen.blit(player_img, (car_x, car_y))
    else:
        pygame.draw.rect(screen, YELLOW, (car_x, car_y, car_width, car_height))
        pygame.draw.rect(screen, (0, 0, 0), (car_x + 5, car_y + 10, car_width - 10, 20))

    # рисовка врага
    for enemy in enemies:
        if enemy_img:
            screen.blit(enemy_img, (enemy[0], enemy[1]))
        else:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], car_width, car_height))

    # рисовка денег
    for c in cash:
        pygame.draw.circle(screen, GREEN, (c[0], c[1]), 10)

    # счет на экран
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    best_text = font.render(f'Best: {best_score}', True, YELLOW)
    cash_text = font.render(f'Cash: {cash_count}', True, GREEN)
    best_cash_text = font.render(f'Best Cash: {best_cash}', True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(best_text, (10, 40))
    screen.blit(cash_text, (10, 70))
    screen.blit(best_cash_text, (10, 100))

    # экран проигрыша
    if game_over:
        if score > best_score:
            best_score = score
        if cash_count > best_cash:
            best_cash = cash_count

        dark = pygame.Surface((WIDTH, HEIGHT))
        dark.set_alpha(180)
        dark.fill((0, 0, 0))
        screen.blit(dark, (0, 0))

        big_font = pygame.font.Font(None, 72)
        game_over_text = big_font.render("GAME OVER", True, RED)
        score_final = font.render(f'Score: {score}', True, WHITE)
        cash_final = font.render(f'Cash: {cash_count}', True, GREEN)
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        menu_text = font.render("Press ESC for menu", True, GRAY)

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        screen.blit(score_final, score_final.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(cash_final, cash_final.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))
        screen.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 110)))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()