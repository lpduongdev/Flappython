import pygame
import random
import sys
import db

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

GAME_MODE_EASY = 'easy_score'
GAME_MODE_MEDIUM = 'medium_score'
GAME_MODE_HARD = 'hard_score'

# DIR
FONT_LOCATION = '04B_19.ttf'
BG_LOCATION = 'res/background-night.png'
BG_DIM_LOCATION = 'res/background-night-dimmed.png'
ROAD_LOCATION = 'res/road.png'
BTN_BACK_LOCATION = 'res/btn_back.png'
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
        tmp_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        tmp_rect = tmp_surface.get_rect(center=(216, 360))
        screen.blit(tmp_surface, tmp_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 400))
        screen.blit(high_score_surface, high_score_rect)

        high_score_surface = game_font.render("Press space", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 500))
        screen.blit(high_score_surface, high_score_rect)

        high_score_surface = game_font.render("or click mouse", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 540))
        screen.blit(high_score_surface, high_score_rect)

        high_score_surface = game_font.render("to continue", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 580))
        screen.blit(high_score_surface, high_score_rect)

        high_score_surface = game_font.render("Press ESC to quit", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 40))
        screen.blit(high_score_surface, high_score_rect)


def generate_top_five(top_info):
    global top1_text, top2_text, top3_text, top4_text, top5_text
    index = 0
    for x in top_info:
        if index == 0:
            top1_text = top_list_font.render(str(index + 1) + ": " + str(top_info[index]['name']), True,
                                             (255, 255, 255))
            screen.blit(top1_text, top1_rect)
            score_text = top_list_font.render(str(top_info[index]['point']), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(380, 350))
            screen.blit(score_text, score_rect)
        elif index == 1:
            top2_text = top_list_font.render(str(index + 1) + ": " + str(top_info[index]['name']), True,
                                             (255, 255, 255))
            screen.blit(top2_text, top2_rect)
            score_text = top_list_font.render(str(top_info[index]['point']), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(380, 400))
            screen.blit(score_text, score_rect)
        if index == 2:
            top3_text = top_list_font.render(str(index + 1) + ": " + str(top_info[index]['name']), True,
                                             (255, 255, 255))
            screen.blit(top3_text, top3_rect)
            score_text = top_list_font.render(str(top_info[index]['point']), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(380, 450))
            screen.blit(score_text, score_rect)
        if index == 3:
            top4_text = top_list_font.render(str(index + 1) + ": " + str(top_info[index]['name']), True,
                                             (255, 255, 255))
            screen.blit(top4_text, top4_rect)
            score_text = top_list_font.render(str(top_info[index]['point']), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(380, 500))
            screen.blit(score_text, score_rect)
        if index == 4:
            top5_text = top_list_font.render(str(index + 1) + ": " + str(top_info[index]['name']), True,
                                             (255, 255, 255))
            screen.blit(top5_text, top5_rect)
            score_text = top_list_font.render(str(top_info[index]['point']), True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(380, 550))
            screen.blit(score_text, score_rect)
        index += 1


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


def stop_screen(level, point):
    global bg_dim, click, road_x_pos, top1_text, top2_text, top3_text, top4_text, top5_text
    is_running = True
    while is_running:
        is_hover = False
        screen.blit(bg_dim, (0, 0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        screen.blit(btn_back, (10, 10))
        screen.blit(game_over_surface, game_over_react)
        top_info = None
        if level == GAME_MODE_EASY:
            screen.blit(easy_score_text, easy_score_rect)
            top_info = db.get_top_five_easy()
            generate_top_five(top_info)
        if level == GAME_MODE_MEDIUM:
            screen.blit(medium_score_text, medium_score_rect)
            top_info = db.get_top_five_medium()
            generate_top_five(top_info)
        if level == GAME_MODE_HARD:
            screen.blit(hard_score_text, hard_score_rect)
            top_info = db.get_top_five_hard()
            generate_top_five(top_info)
        your_score_text = game_font.render("Your point: " + str(point), True, (255, 255, 255))
        screen.blit(your_score_text, your_score_rect)
        road_x_pos -= 1
        generate_road()
        if road_x_pos <= -432:
            road_x_pos = 0
        btn_again_rect = pygame.Rect(116, 650, 200, 80)
        screen.blit(pygame.image.load('res/btn_again.png').convert_alpha(), (116, 650))
        if btn_again_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('res/btn_again_hover.png'), (115, 650))
            if click:
                is_running = False
        if btn_back_rect.collidepoint((mx, my)):
            is_hover = True
            if click:
                return False
        click = False
        if is_hover:
            screen.blit(pygame.image.load('res/btn_back_hover.png'), (10, 10))
        pygame.display.update()
        clock.tick(GAME_SPEED)
    return True


def animate_road():
    global road_x_pos
    road_x_pos -= 1
    generate_road()
    if road_x_pos <= -432:
        road_x_pos = 0


def start_game(username, level):
    global bird_movement, score, high_score, road_x_pos, bird_index, pipe_list, bird_rect, bird, click
    game_active = IS_ACTIVE
    show_pause_screen = True
    is_running = True
    while is_running:
        mx, my = pygame.mouse.get_pos()
        screen.blit(bg, (0, 0))

        if game_active:
            bird_movement += GRAVITY
            rotated_bird = rotate_bird(bird)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list)
            if is_passed_pipe(pipe_list):
                score += 1
            score_display(IN_GAME_STATE)
        elif not game_active and show_pause_screen:
            screen.blit(bg_dim, (0,0))
            screen.blit(stop_screen_surface, stop_screen_react)
        else:
            if username != "GUEST":
                db.save_result(score, username, level)
                if stop_screen(level, score):
                    pipe_list.clear()
                    bird_rect.center = (100, 384)
                    bird_movement = 0
                    score = 0
                else:
                    is_running = False
                show_pause_screen = True
            else:
                screen.blit(bg_dim, (0,0))
                screen.blit(game_over_surface, game_over_react)
                high_score = update_score(score, high_score)
                score_display(OVER_STATE)
        if btn_back_rect.collidepoint((mx, my)):
            if click:
                is_running = False
        else:
            if click:
                game_active = True
                show_pause_screen = False
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_active:
                        bird_movement = BIRD_MOVEMENT
                        flap_sound.play()
                    if event.key == pygame.K_SPACE and not game_active:
                        game_active = True
                        show_pause_screen = False
                        pipe_list.clear()
                        bird_rect.center = (100, 384)
                        bird_movement = 0
                        score = 0
                    if event.key == pygame.K_ESCAPE:
                        is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if game_active:
                    bird_movement = BIRD_MOVEMENT
                    flap_sound.play()
                else:
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
        animate_road()
        pygame.display.update()
        clock.tick(GAME_SPEED)


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
clock = pygame.time.Clock()
game_font = pygame.font.Font(FONT_LOCATION, FONT_SIZE)

bird_movement = 0
score = 0
high_score = 0

bg = pygame.image.load(BG_LOCATION).convert()
bg_dim = pygame.image.load(BG_DIM_LOCATION).convert()

road = pygame.image.load(ROAD_LOCATION).convert()

road_x_pos = 0

btn_back = pygame.image.load(BTN_BACK_LOCATION).convert_alpha()
btn_back_rect = pygame.Rect(10, 10, 110, 80)
click = False

bird_down = pygame.transform.scale2x(pygame.image.load(BIRD_DOWN_LOCATION).convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load(BIRD_MID_LOCATION).convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load(BIRD_UP_LOCATION).convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, OBJECT_IMG_CHANGE_TIMER)

pipe_surface = pygame.image.load(PIPE_LOCATION).convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, SPAWN_PIPE_TIMER)

stop_screen_surface = pygame.transform.scale2x(pygame.image.load(MSG_LOCATION).convert_alpha())
stop_screen_react = stop_screen_surface.get_rect(center=(216, 384))

game_over_surface = pygame.transform.scale2x(pygame.image.load(OVER_LOCATION).convert_alpha())
game_over_react = game_over_surface.get_rect(center=(216, 150))

flap_sound = pygame.mixer.Sound(SFX_SWING_LOCATION)
hit_sound = pygame.mixer.Sound(SFX_HIT_LOCATION)
score_sound = pygame.mixer.Sound(SFX_PASS_LOCATION)

your_score_text = game_font.render("Your point: " + str(score), True, (255, 255, 255))
your_score_rect = your_score_text.get_rect(center=(216, 600))

easy_score_text = game_font.render("Top point easy: ", True, (255, 255, 255))
easy_score_rect = easy_score_text.get_rect(center=(170, 250))
medium_score_text = game_font.render("Top point medium: ", True, (255, 255, 255))
medium_score_rect = medium_score_text.get_rect(center=(200, 250))
hard_score_text = game_font.render("Top point hard: ", True, (255, 255, 255))
hard_score_rect = hard_score_text.get_rect(center=(170, 250))

top_list_font = pygame.font.Font('04B_19.TTF', 26)

top1_text = top_list_font.render("Top 1: ", True, (255, 255, 255))
top1_rect = top1_text.get_rect(center=(70, 350))

top2_text = top_list_font.render("Top 2: ", True, (255, 255, 255))
top2_rect = top2_text.get_rect(center=(70, 400))

top3_text = top_list_font.render("Top 3: ", True, (255, 255, 255))
top3_rect = top3_text.get_rect(center=(70, 450))

top4_text = top_list_font.render("Top 4: ", True, (255, 255, 255))
top4_rect = top4_text.get_rect(center=(70, 500))

top5_text = top_list_font.render("Top 5: ", True, (255, 255, 255))
top5_rect = top5_text.get_rect(center=(70, 550))
