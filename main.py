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

day_time = 0
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
shield_active = False
shield_timer = 0
shield_items = []
shield_spawn_timer = 0
police_items = []
police_spawn_timer = 0
# звуки
pygame.mixer.init()

# сложность
difficulty = 'normal'

try:
    crash_sound = pygame.mixer.Sound('sounds/crash.wav')
except:
    crash_sound = None
try:
    coin_sound = pygame.mixer.Sound('sounds/coin.wav')
except:
    coin_sound = None
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

# table redordov
def load_records():
    records = []
    try:
        with open('records.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    records.append((int(parts[0]), int(parts[1])))
    except:
        pass
    return records

def save_records(records):
    with open('records.txt', 'w') as f:
        for score, cash in records:
            f.write(f'{score}, {cash}\n')

def add_record(score, cash, records):
    records.append((score, cash))
    records.sort(reverse=True)
    return records[:5]

records = load_records()
if records:
    best_score = records[0][0]
    best_cash = records[0][1]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if in_menu:
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                if event.key == pygame.K_2:
                    difficulty = 'normal'
                if event.key == pygame.K_3:
                    difficulty = 'hard'
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
                    shield_active = False
                    shield_timer = 0
                    shield_items.clear()
                    shield_spawn_timer = 0
                    police_items.clear()
                    police_spawn_timer = 0
                    game_over = False
                elif in_menu:
                    in_menu = False
                    # сложность
                    if difficulty == 'easy':
                        enemy_speed = 3
                        ROAD_SPEED = 3
                    elif difficulty == 'hard':
                        enemy_speed = 7
                        ROAD_SPEED = 7
                    else:
                        enemy_speed = 5
                        ROAD_SPEED = 5
                    shield_active = False
                    shield_timer = 0
                    shield_items.clear()
                    shield_spawn_timer = 0
                    police_items.clear()
                    police_spawn_timer = 0
                    game_over = False
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

        big_font = pygame.font.Font(None, 50)
        font = pygame.font.Font(None, 24)
        small_font = pygame.font.Font(None, 18)

        title = big_font.render("STREET RACER", True, YELLOW)
        diff_text = font.render(f'Difficulty: {difficulty.upper()}', True, WHITE)
        hint = small_font.render('1-EASY  2-NORMAL  3-HARD', True, GRAY)
        start = font.render("SPACE to start", True, WHITE)
        exit_text = small_font.render("ESC to exit", True, GRAY)
        best = font.render(f"Best: {best_score} pts | {best_cash} cash", True, GREEN)

        # заголовок сверху
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))
        # сложность
        screen.blit(diff_text, diff_text.get_rect(center=(WIDTH // 2, 90)))
        # подсказка
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 120)))
        # старт
        screen.blit(start, start.get_rect(center=(WIDTH // 2, 160)))
        # выход
        screen.blit(exit_text, exit_text.get_rect(center=(WIDTH // 2, 190)))
        # рекорд
        screen.blit(best, best.get_rect(center=(WIDTH // 2, 230)))

        # таблица рекордов
        top_label = small_font.render('TOP 5:', True, WHITE)
        screen.blit(top_label, (WIDTH // 2 - 25, 260))
        for i, (sc, ca) in enumerate(records):
            line = small_font.render(f'{i + 1}. {sc} pts | {ca} cash', True, (180, 180, 180))
            screen.blit(line, (WIDTH // 2 - 50, 280 + i * 18))

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
        day_time = (day_time + 1) % 3600
        # скорость врагов
        speed_up = 0.3 if difficulty == 'easy' else (0.8 if difficulty == 'hard' else 0.5)
        if score % 60 == 0:
            enemy_speed += speed_up

        # спавн врагов
        spawn_delay = 40 if difficulty == 'easy' else (20 if difficulty == 'hard' else 30)
        spawn_timer += 1
        if spawn_timer > spawn_delay:
            spawn_timer = 0
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
        # спавн защиты
        shield_spawn_timer += 1
        if shield_spawn_timer > 180:
            shield_lane = random.randint(0, NUM_LANES - 1)
            shield_x = shield_lane * LANE_WIDTH + LANE_WIDTH // 2
            shield_y = -30
            shield_items.append([shield_x, shield_y])
            shield_spawn_timer = 0

        # спавн полис
        police_spawn_timer += 1
        if police_spawn_timer > 600:
            police_lane = random.randint(0, NUM_LANES - 1)
            police_x = police_lane * LANE_WIDTH + (LANE_WIDTH - car_width) // 2
            police_y = -car_height
            police_items.append([police_x, police_y, police_lane, 0])
            police_spawn_timer = 0
        # враги вниз
        for enemy in enemies:
            enemy[1] += enemy_speed
        for c in cash:
            c[1] += enemy_speed
        for p in police_items:
            p[1] += enemy_speed * 1.5

        # удаление врагов за экраном
        enemies = [e for e in enemies if e[1] < HEIGHT]

        # таймер зашиты
        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        # ДТП
        player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], car_width, car_height)
            if player_rect.colliderect(enemy_rect):
                if shield_active:
                    enemies.remove(enemy)
                    score += 20
                else:
                    if crash_sound:
                        crash_sound.play()
                    game_over = True
        # проверка на обезд полис
        for p in police_items[:]:
            police_rect = pygame.Rect(p[0], p[1], car_width, car_height)
            # если задел то щит не спасает - дэд
            if player_rect.colliderect(police_rect):
                if crash_sound:
                    crash_sound.play()
                game_over = True
            if p[1] > HEIGHT and p[3] == 0:
                p[3] = 1
                score += 50


        # сбор денег
        for c in cash[:]:
            cash_rect = pygame.Rect(c[0] - 10, c[1] - 10, 20, 20)
            if player_rect.colliderect(cash_rect):
                cash.remove(c)
                score += 10
                cash_count += 1
                if coin_sound:
                    coin_sound.play()
        for s in shield_items:
            s[1] += enemy_speed
        #сбор защиты
        for s in shield_items[:]:
            shield_rect = pygame.Rect(s[0] - 12, s[1] - 12, 24, 24)
            if player_rect.colliderect(shield_rect):
                shield_items.remove(s)
                shield_active = True
                shield_timer = 180

        # удаление лавэхи за экраном
        cash = [c for c in cash if c[1] < HEIGHT]
        shield_items = [s for s in shield_items if s[1] < HEIGHT]
        police_items = [p for p in police_items if p[1] < HEIGHT + 50]
    # day time 0 день 900 закат 1800 ночь 2700 рассвет
    if day_time < 900:
        t = day_time / 900
        bg_color = (100 + int(55 * t), 130 + int(30 * t), 100 + int(50 * t))
        road_color = (50 + int(20 * t), 50, 50)
    elif day_time < 1800:
        t = (day_time - 900) / 900
        bg_color = (155 - int(100 * t), 160 - int(100 * t), 150 - int(100 * t))
        road_color = (70  - int(35 * t), 50 - int(25 * t), 50 - int(25 * t))
    elif day_time < 2700:
        t = (day_time - 1800) / 900
        bg_color = (55 + int(100 * t), 60 + int(100 * t), 50 + int(100 * t))
        road_color = (35 + int(35 * t), 25 + int(25 * t), 25 + int(25 * t))
    else:
        t = (day_time - 2700) / 900  # рассвет → день
        bg_color = (155 - int(55 * t), 160 - int(30 * t), 150 - int(50 * t))
        road_color = (70 - int(20 * t), 50, 50)
    # рисовка
    screen.fill(bg_color)

    # рисовка дороги
    for i in range(NUM_LANES):
        pygame.draw.rect(screen, road_color, (i * LANE_WIDTH, 0, LANE_WIDTH, HEIGHT))

    # ЛИния разметки
    for lane in range(1, NUM_LANES):
        line_x = lane * LANE_WIDTH
        for y in range(0, HEIGHT, 40):
            line_y = (y + road_offset) % HEIGHT
            line_color = (180, 180, 180) if day_time > 900 and day_time < 2700 else WHITE
            pygame.draw.rect(screen, line_color, (line_x - 2, line_y, 4, 20))

    # свет когда игрок вщял щит
    if shield_active:
        pygame.draw.rect(screen, (50, 100, 255), (car_x -5, car_y -5, car_width + 10, car_height + 10), 3)

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

    # risovka police
    for p in police_items:
        flash_color = (0, 0, 255) if(score // 10) % 2 == 0 else (255, 0, 0)
        if enemy_img:
            screen.blit(enemy_img, (p[0], p[1]))
        else:
            pygame.draw.rect(screen, (0, 0, 100), (p[0], p[1], car_width, car_height))
        pygame.draw.rect(screen, flash_color, (p[0] + car_width//2 - 5, p[1] - 10, 10, 10))

    # рисовка денег
    for c in cash:
        pygame.draw.circle(screen, GREEN, (c[0], c[1]), 10)

    # рисовка щита
    for s in shield_items:
        pygame.draw.circle(screen, (50, 100, 255), (s[0], s[1]), 12)
        s_text = font.render("S", True, WHITE)
        screen.blit(s_text, s_text.get_rect(center=(s[0], s[1])))

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
        records = add_record(score, cash_count, records)
        save_records(records)

        screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
        screen.blit(score_final, score_final.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        screen.blit(cash_final, cash_final.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))
        screen.blit(menu_text, menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 110)))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()