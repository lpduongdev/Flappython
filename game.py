import pygame
import random
import sys

# GLOBAL VARIATIONS
OBJECT_IMG_CHANGE_TIMER = 200
SCREEN_SIZE_X = 432
SCREEN_SIZE_Y = 768
GRAVITY = 0.10
SPAWN_PIPE_TIMER = 1200
PIPE_MOVING_SPEED = 5
PIPE_HEIGHT = [300, 400, 500]
PIPE_BTW_HEIGHT = 750
SCORE_TIMER = 0
BIRD_MOVEMENT = -5
FONT_SIZE = 35
IS_ACTIVE = False
GAME_SPEED = 120
GAME_TYPE = -1

IN_GAME_STATE = 0
OVER_STATE = 1


# DIR
FONT_LOCATION = '04B_19.ttf'
BG_LOCATION = 'res/background-night.png'
BG_DIM_LOCATION = 'res/background-night-dimmed.png'
ROAD_LOCATION = 'res/road.png'
BTN_EASY_IMG_LOCATION = 'res/btn_easy.png'
BTN_MED_IMG_LOCATION = 'res/btn_medium.png'
BTN_HARD_IMG_LOCATION = 'res/btn_hard.png'
BTN_OPTIONS_IMG_LOCATION = 'res/btn_options.png'
BIRD_DOWN_LOCATION = 'res/yellowbird-downflap.png'
BIRD_MID_LOCATION = 'res/yellowbird-midflap.png'
BIRD_UP_LOCATION = 'res/yellowbird-upflap.png'
PIPE_LOCATION = 'res/pipe-green.png'
MSG_LOCATION = 'res/message.png'
OVER_LOCATION = 'res/gameover.png'
SFX_SWING_LOCATION = 'sound/sfx_wing.wav'
SFX_HIT_LOCATION = 'sound/sfx_hit.wav'
SFX_PASS_LOCATION = 'sound/sfx_point.wav'


def generate_road():
    screen.blit(road, (road_x_pos, 650))
    screen.blit(road, (road_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(PIPE_HEIGHT)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - PIPE_BTW_HEIGHT))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_MOVING_SPEED
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(state):
    if state == 0:
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if state == 1:
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def is_passed_pipe(pipes):
    if len(pipes) > 0:
        if (pipes[-1].centerx - 100) < 60 and (pipes[-1].centerx - 100) > 50:
            score_sound.play()
            return True
    return False


def start_game():
    check_first_start = False
    is_running = True
    global game_active, bird_movement, score, high_score, road_x_pos, bird_index, pipe_list, bird_rect, bird, click
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_active:
                        bird_movement = BIRD_MOVEMENT
                        flap_sound.play()
                    if event.key == pygame.K_SPACE and game_active is False:
                        game_active = True
                        check_first_start = True
                        pipe_list.clear()
                        bird_rect.center = (100, 384)
                        bird_movement = 0
                        score = 0
                    if event.key == K_ESCAPE:
                        is_running = False
            if event.type == MOUSEBUTTONDOWN:
                if game_active:
                    bird_movement = BIRD_MOVEMENT
                    flap_sound.play()
                else:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 384)
                    bird_movement = 0
                    score = 0
            if event.type == spawnpipe:
                pipe_list.extend(create_pipe())
            if event.type == birdflap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird, bird_rect = bird_animation()

        screen.blit(bg, (0, 0))
        if game_active:
            # chim

            bird_movement += GRAVITY
            rotated_bird = rotate_bird(bird)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)

            # ống
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list)

            if is_passed_pipe(pipe_list):
                score += 1
            score_display(IN_GAME_STATE)
        elif game_active is False and check_first_start is False:
            screen.blit(stop_screen_surface, stop_screen_react)
        else:
            screen.blit(game_over_surface, game_over_react)
            high_score = update_score(score, high_score)
            score_display(OVER_STATE)
        # sàn
        road_x_pos -= 1
        generate_road()
        if road_x_pos <= -432:
            road_x_pos = 0

        pygame.display.update()
        clock.tick(GAME_SPEED)


def main_menu():
    global click, road_x_pos, GAME_TYPE, GRAVITY, PIPE_BTW_HEIGHT, PIPE_MOVING_SPEED
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
                GAME_TYPE = 0
                GRAVITY = 0.10
                PIPE_BTW_HEIGHT = 750
                PIPE_MOVING_SPEED = 5
                start_game()
        if btn_med_rect.collidepoint((mx, my)):
            if click:
                GAME_TYPE = 1
                GRAVITY = 0.16
                PIPE_BTW_HEIGHT = 675
                PIPE_MOVING_SPEED = 5
                start_game()
        if btn_hard_rect.collidepoint((mx, my)):
            if click:
                GAME_TYPE = 2
                GRAVITY = 0.16
                PIPE_BTW_HEIGHT = 650
                PIPE_MOVING_SPEED = 7
                start_game()
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
        road_x_pos -= 1
        generate_road()
        if road_x_pos <= -432:
            road_x_pos = 0
        pygame.display.update()
        mainClock.tick(GAME_SPEED)


def options():
    global road_x_pos
    is_running = True
    while is_running:
        screen.blit(bg_dim, (0, 0))
        text = game_font.render("Options", True, (255, 255, 255))
        text_rect = text.get_rect(center=(216, 100))
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    is_running = False
        road_x_pos -= 1
        generate_road()
        if road_x_pos <= -432:
            road_x_pos = 0
        pygame.display.update()
        mainClock.tick(GAME_SPEED)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()


screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
clock = pygame.time.Clock()
game_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE)

easy_btn = pygame.image.load(BTN_EASY_IMG_LOCATION).convert()
medium_btn = pygame.image.load(BTN_MED_IMG_LOCATION).convert()
hard_btn = pygame.image.load(BTN_HARD_IMG_LOCATION).convert()
options_btn = pygame.image.load(BTN_OPTIONS_IMG_LOCATION).convert()

# Tạo các biến cho trò chơi
bird_movement = 0
game_active = IS_ACTIVE
score = 0
high_score = 0

# chèn background
bg = pygame.image.load(BG_LOCATION).convert()
bg_dim = pygame.image.load(BG_DIM_LOCATION).convert()
# chèn sàn
road = pygame.image.load(ROAD_LOCATION).convert()
# floor = pygame.transform.scale2x(floor)
road_x_pos = 0

# tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load(BIRD_DOWN_LOCATION).convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load(BIRD_MID_LOCATION).convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load(BIRD_UP_LOCATION).convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, OBJECT_IMG_CHANGE_TIMER)

# tạo ống
pipe_surface = pygame.image.load(PIPE_LOCATION).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, SPAWN_PIPE_TIMER)

# Tạo màn hình kết thúc
stop_screen_surface = pygame.transform.scale2x(pygame.image.load(MSG_LOCATION).convert_alpha())
stop_screen_react = stop_screen_surface.get_rect(center=(216, 384))

game_over_surface = pygame.transform.scale2x(pygame.image.load(OVER_LOCATION).convert_alpha())
game_over_react = game_over_surface.get_rect(center=(216, 384))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound(SFX_SWING_LOCATION)
hit_sound = pygame.mixer.Sound(SFX_HIT_LOCATION)
score_sound = pygame.mixer.Sound(SFX_PASS_LOCATION)

# start_game()

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Flappython')

click = False
main_menu()
