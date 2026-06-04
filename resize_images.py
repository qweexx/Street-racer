import pygame

pygame.init()

# размер как в игре
car_width = 65
car_height = 110

images = ["car_yellow.png", "car_red.png", "car_black.png"]

for img_name in images:
    try:
        img = pygame.image.load(f"images/{img_name}")
        img = pygame.transform.scale(img, (car_width, car_height))
        pygame.image.save(img, f"images/{img_name}")
        print(f"Готово: {img_name}")
    except Exception as e:
        print(f"Ошибка {img_name}: {e}")

print("Всё!")