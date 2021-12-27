import pygame
import random
import sys


# GLOBAL VARIATIONS
OBJECT_IMG_CHANGE_TIMER = 200
SCREEN_SIZE_X = 432
SCREEN_SIZE_Y = 768
GRAVITY = 0.10
SPAWN_PIPE_TIMER = 1200
PIPE_HEIGHT = [300, 400, 500]
SCORE_TIMER = 0
BIRD_MOVEMENT = -5
FONT_SIZE = 35
IS_ACTIVE = False
GAME_SPEED = 120

# DIR
FONT_LOCATION = '04B_19.ttf'
BG_LOCATION = 'res/background-night.png'
ROAD_LOCATION = 'res/road.png'
BIRD_DOWN_LOCATION = 'res/yellowbird-downflap.png'
BIRD_MID_LOCATION = 'res/yellowbird-midflap.png'
BIRD_UP_LOCATION = 'res/yellowbird-upflap.png'
PIPE_LOCATION = 'res/pipe-green.png'
MSG_LOCATION = 'res/message.png'
SFX_SWING_LOCATION = 'sound/sfx_wing.wav'
SFX_HIT_LOCATION = 'sound/sfx_hit.wav'
SFX_PASS_LOCATION = 'sound/sfx_point.wav'


def generate_road():
    screen.blit(road, (road_x_pos, 650))
    screen.blit(road, (road_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 750))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
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


def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
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


def bird_over_pipe(pipes):
    if len(pipes) > 0:
        if (pipes[-1].centerx - 100) == 60:
            score_sound.play()
            return True
    return False

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)


pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
clock = pygame.time.Clock()
game_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE)

# Tạo các biến cho trò chơi
gravity = GRAVITY
bird_movement = 0
game_active = IS_ACTIVE
score = 0
high_score = 0

# chèn background
bg = pygame.image.load(BG_LOCATION).convert()
# bg = pygame.transform.scale2x(bg)

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
pipe_height = PIPE_HEIGHT

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load(MSG_LOCATION).convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound(SFX_SWING_LOCATION)
hit_sound = pygame.mixer.Sound(SFX_HIT_LOCATION)
score_sound = pygame.mixer.Sound(SFX_PASS_LOCATION)

# while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = BIRD_MOVEMENT
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
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

        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        if bird_over_pipe(pipe_list):
            score += 1
        score_display('main game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    # sàn
    road_x_pos -= 1
    generate_road()
    if road_x_pos <= -432:
        road_x_pos = 0

    pygame.display.update()
    clock.tick(GAME_SPEED)