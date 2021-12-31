import pygame
import game
import sys
from pygame.locals import *

import db

BTN_EASY_IMG_LOCATION = 'res/btn_easy.png'
BTN_MED_IMG_LOCATION = 'res/btn_medium.png'
BTN_HARD_IMG_LOCATION = 'res/btn_hard.png'
BTN_OPTIONS_IMG_LOCATION = 'res/btn_options.png'
GAME_MODE_EASY = 'easy_score'
GAME_MODE_MEDIUM = 'medium_score'
GAME_MODE_HARD = 'hard_score'


def main_menu(username):
    global click
    bg_music.play(-1)
    is_running = True
    while is_running:
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
            screen.blit(pygame.image.load('res/btn_easy_hover.png'), (115, 150))
            if click:
                game.GAME_TYPE = 0
                game.GRAVITY = 0.10
                game.PIPE_BTW_HEIGHT = 750
                game.PIPE_MOVING_SPEED = 5
                game.start_game(username, GAME_MODE_EASY)
        if btn_med_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('res/btn_medium_hover.png'), (115, 250))
            if click:
                game.GAME_TYPE = 1
                game.GRAVITY = 0.16
                game.PIPE_BTW_HEIGHT = 675
                game.PIPE_MOVING_SPEED = 5
                game.start_game(username, GAME_MODE_MEDIUM)
        if btn_hard_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('res/btn_hard_hover.png'), (115, 350))
            if click:
                game.GAME_TYPE = 2
                game.GRAVITY = 0.16
                game.PIPE_BTW_HEIGHT = 650
                game.PIPE_MOVING_SPEED = 7
                game.start_game(username, GAME_MODE_HARD)
        if btn_options_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('res/btn_options_hover.png'), (115, 550))
            if click:
                if options(username) == 0:
                    is_running = False
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
        game.animate_road()
        pygame.display.update()
        mainClock.tick(120)
    bg_music.stop()


def show_user_info(user_info):
    easy_score_text = pygame.font.Font('04B_19.TTF', 24).render("Score easy: " + str(user_info[0]),
                                                                True, (255, 255, 255))
    easy_score_rect = easy_score_text.get_rect(center=(150, 250))
    screen.blit(easy_score_text, easy_score_rect)

    medium_score_text = pygame.font.Font('04B_19.TTF', 24).render("Score medium: " + str(user_info[1]),
                                                                  True,
                                                                  (255, 255, 255))
    medium_score_rect = medium_score_text.get_rect(center=(165, 300))
    screen.blit(medium_score_text, medium_score_rect)

    hard_score_text = pygame.font.Font('04B_19.TTF', 24).render("Score hard: " + str(user_info[2]), True,
                                                                (255, 255, 255))
    hard_score_rect = hard_score_text.get_rect(center=(150, 350))
    screen.blit(hard_score_text, hard_score_rect)

    times_text = pygame.font.Font('04B_19.TTF', 24).render(
        "You have played: " + str(user_info[3]) + " times", True,
        (255, 255, 255))
    times_rect = times_text.get_rect(center=(200, 400))
    screen.blit(times_text, times_rect)


def options(username):
    global click, btn_music_mute, btn_sfx_mute, is_music_on, is_sfx_on
    is_running = True
    user_info = None
    if username != "guest":
        user_info = db.get_score(username)
    while is_running:
        mx, my = pygame.mouse.get_pos()
        screen.blit(bg_dim, (0, 0))

        game.animate_road()

        text = game_font.render("Options", True, (255, 255, 255))
        text_rect = text.get_rect(center=(216, 100))
        screen.blit(text, text_rect)

        title_text = pygame.font.Font('04B_19.TTF', 24).render("You are login as: " + str(username), True,
                                                               (255, 255, 255))
        if username != 'guest':
            show_user_info(user_info)
        title_rect = title_text.get_rect(center=(200, 200))
        screen.blit(title_text, title_rect)

        screen.blit(btn_back, (10, 10))
        screen.blit(btn_music_mute, (80, 450))
        screen.blit(btn_sfx_mute, (250, 450))
        screen.blit(btn_logout, (115, 650))

        if btn_back_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('res/btn_back_hover.png'), (10, 10))
            if click:
                is_running = False
        if btn_logout_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('res/btn_logout_hover.png'), (115, 650))
            if click:
                return 0
        if btn_mute_rect.collidepoint((mx, my)):
            if is_music_on:
                screen.blit(pygame.image.load('res/btn_mute_hover.png'), (80, 450))
            if click:
                if is_music_on:
                    bg_music.set_volume(0)
                    btn_music_mute = btn_mute_off
                    is_music_on = False
                else:
                    bg_music.set_volume(100)
                    btn_music_mute = btn_mute
                    is_music_on = True
        if btn_sfx_rect.collidepoint((mx, my)):
            if is_sfx_on:
                screen.blit(pygame.image.load('res/btn_sfx_hover.png'), (250, 450))
            if click:
                if is_sfx_on:
                    game.flap_sound.set_volume(0)
                    game.hit_sound.set_volume(0)
                    game.score_sound.set_volume(0)
                    btn_sfx_mute = btn_sfx_off
                    is_sfx_on = False
                else:
                    game.flap_sound.set_volume(100)
                    game.hit_sound.set_volume(100)
                    game.score_sound.set_volume(100)
                    btn_sfx_mute = btn_sfx
                    is_sfx_on = True
        click = False

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
        pygame.display.update()
        mainClock.tick(120)


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

pygame.init()
screen = pygame.display.set_mode((432, 786))
bg_music = pygame.mixer.Sound('sound/bg_music.mp3')

btn_back = pygame.image.load(game.BTN_BACK_LOCATION).convert_alpha()
btn_back_rect = pygame.Rect(10, 10, 110, 80)

btn_mute = pygame.image.load('res/btn_mute_on.png').convert_alpha()
btn_mute_rect = pygame.Rect(80, 450, 109, 100)
btn_mute_off = pygame.image.load('res/btn_mute_off.png').convert_alpha()
btn_music_mute = btn_mute

btn_sfx = pygame.image.load('res/btn_sfx_on.png').convert_alpha()
btn_sfx_rect = pygame.Rect(250, 450, 109, 100)
btn_sfx_off = pygame.image.load('res/btn_sfx_off.png').convert_alpha()
btn_sfx_mute = btn_sfx

btn_logout = pygame.image.load('res/btn_logout.png').convert_alpha()
btn_logout_rect = pygame.Rect(115, 650, 210, 90)

game_font = pygame.font.Font('04B_19.TTF', 35)
easy_btn = pygame.image.load(BTN_EASY_IMG_LOCATION).convert_alpha()
medium_btn = pygame.image.load(BTN_MED_IMG_LOCATION).convert_alpha()
hard_btn = pygame.image.load(BTN_HARD_IMG_LOCATION).convert_alpha()
options_btn = pygame.image.load(BTN_OPTIONS_IMG_LOCATION).convert_alpha()
bg_dim = pygame.image.load(game.BG_DIM_LOCATION).convert()
mainClock = pygame.time.Clock()
click = False

is_music_on = True
is_sfx_on = True
