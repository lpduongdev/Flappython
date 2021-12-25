import pygame
import sys

SCREEN_X_SIZE = 432
SCREEN_Y_SIZE = 768
FLOOR_Y_POSITION = 600
FPS_60 = 60
FPS_120 = 120


def generate_floor(x_position):
    screen.blit(floor, (x_position, FLOOR_Y_POSITION))
    screen.blit(floor, (x_position + SCREEN_X_SIZE, FLOOR_Y_POSITION))


# Start pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_X_SIZE, SCREEN_Y_SIZE))
clock = pygame.time.Clock()

background = pygame.transform.scale2x(pygame.image.load('res/background-night.png'))
floor = pygame.transform.scale2x(pygame.image.load('res/floor.png'))
floor_x = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0, 0))
    floor_x -= 1
    generate_floor(floor_x)
    if floor_x <= -SCREEN_X_SIZE:
        floor_x = 0
    pygame.display.update()
    clock.tick(FPS_60)
