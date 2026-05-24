import pygame
import sys

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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if car_lane > 0:
                    car_lane -= 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if car_lane < NUM_LANES - 1:
                    car_lane += 1

    # анимка движения дороги
    road_offset = (road_offset + ROAD_SPEED) % 100

    #обнов поз кар
    car_x = LANE_WIDTH * car_lane + (LANE_WIDTH - car_width) // 2

# рисовка
    screen.fill(GRAY)

# рисовка дороги
    for i in range(NUM_LANES):
        pygame.draw.rect(screen, (50, 50,50), (i * LANE_WIDTH, 0, LANE_WIDTH, HEIGHT))

# ЛИния разметки
    for lane in range(1, NUM_LANES):
        line_x = lane * LANE_WIDTH
        for y in range(0, HEIGHT, 40 ):
            line_y = (y + road_offset) % HEIGHT
            pygame.draw.rect(screen, WHITE, (line_x - 2, line_y, 4, 20))

# рисовка кар гг
    pygame.draw.rect(screen, YELLOW, (car_x, car_y, car_width, car_height))
    pygame.draw.rect(screen, (0, 0, 0), (car_x + 5, car_y + 10, car_width - 10, 20))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()