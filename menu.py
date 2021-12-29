import pygame
import game
import sys
from pygame.locals import *

BTN_EASY_IMG_LOCATION = 'res/btn_easy.png'
BTN_MED_IMG_LOCATION = 'res/btn_medium.png'
BTN_HARD_IMG_LOCATION = 'res/btn_hard.png'
BTN_OPTIONS_IMG_LOCATION = 'res/btn_options.png'

def main_menu():
    global click
    while True:
        screen.blit(bg_dim, (0, 0))

        text = game_font.render("Choose difficult", True, (255, 255, 255))
        text_rect = text.get_rect(center=(216, 100))
        screen.blit(text, text_rect)

        options_text = game_font.render("Game options", True, (255, 255, 255))
        options_rect = options_text.get_rect(center=(216, 490))
        screen.blit(options_text, options_rect)

        mx, my = pygame.mouse.get_pos()

        btn_easy_rect = pygame.Rect(116, 150, 200, 80)
        btn_med_rect = pygame.Rect(116, 250, 200, 80)
        btn_hard_rect = pygame.Rect(116, 350, 200, 80)
        btn_options_rect = pygame.Rect(116, 550, 200, 80)

        screen.blit(easy_btn, (115, 150))
        screen.blit(medium_btn, (115, 250))
        screen.blit(hard_btn, (115, 350))
        screen.blit(options_btn, (115, 550))

        if btn_easy_rect.collidepoint((mx, my)):
            if click:
                game.GAME_TYPE = 0
                game.GRAVITY = 0.10
                game.PIPE_BTW_HEIGHT = 750
                game.PIPE_MOVING_SPEED = 5
                game.start_game()
        if btn_med_rect.collidepoint((mx, my)):
            if click:
                game.GAME_TYPE = 1
                game.GRAVITY = 0.16
                game.PIPE_BTW_HEIGHT = 675
                game.PIPE_MOVING_SPEED = 5
                game.start_game()
        if btn_hard_rect.collidepoint((mx, my)):
            if click:
                game.GAME_TYPE = 2
                game.GRAVITY = 0.16
                game.PIPE_BTW_HEIGHT = 650
                game.PIPE_MOVING_SPEED = 7
                game.start_game()
        if btn_options_rect.collidepoint((mx, my)):
            if click:
                options()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        game.road_x_pos -= 1
        game.generate_road()
        if game.road_x_pos <= -432:
            game.road_x_pos = 0
        pygame.display.update()
        mainClock.tick(120)


def options():
    global click
    is_running = True
    while is_running:
        mx, my = pygame.mouse.get_pos()
        if btn_back_rect.collidepoint((mx, my)):
            if click:
                is_running = False
        click = False
        screen.blit(bg_dim, (0, 0))
        text = game_font.render("Options", True, (255, 255, 255))
        text_rect = text.get_rect(center=(216, 100))
        screen.blit(text, text_rect)
        screen.blit(btn_back, (10, 10))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        game.road_x_pos -= 1
        game.generate_road()
        if game.road_x_pos <= -432:
            game.road_x_pos = 0
        pygame.display.update()
        mainClock.tick(120)


pygame.init()
screen = pygame.display.set_mode((432, 786))


btn_back = pygame.image.load(game.BTN_BACK_LOCATION).convert_alpha()
btn_back_rect = pygame.Rect(10, 10, 110, 80)
game_font = pygame.font.Font('04B_19.TTF', 35)
easy_btn = pygame.image.load(BTN_EASY_IMG_LOCATION).convert_alpha()
medium_btn = pygame.image.load(BTN_MED_IMG_LOCATION).convert_alpha()
hard_btn = pygame.image.load(BTN_HARD_IMG_LOCATION).convert_alpha()
options_btn = pygame.image.load(BTN_OPTIONS_IMG_LOCATION).convert_alpha()
bg_dim = pygame.image.load(game.BG_DIM_LOCATION).convert()
mainClock = pygame.time.Clock()
pygame.display.set_caption('Flappython')
click = False

if __name__ == "__main__":
    main_menu()
