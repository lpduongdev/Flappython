import pygame
import sys
import db
import game
import menu

pygame.init()
BTN_REG_IMG_LOCATION = 'res/btn_register.png'
BTN_LOGIN_IMG_LOCATION = 'res/btn_login.png'


def hide_password_text(passwd):
    length = len(passwd)
    string = ''
    for x in range(0, length):
        string += '*'
    return str(string)


def show_register():
    global color_username, color_password, color_password_confirm, username, username_active, password, password_active, password_confirm, password_confirm_active, click, btn_click
    username = ''
    password = ''
    password_confirm = ''
    is_running = True
    while is_running:
        screen.blit(bg, (0, 0))
        screen.blit(btn_back, (10, 10))
        mx, my = pygame.mouse.get_pos()
        if btn_back_rect.collidepoint((mx, my)):
            if click:
                is_running = False
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(username) < 15:
                        username += event.unicode
                if password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(password) < 10:
                        password += event.unicode
                if password_confirm_active:
                    if event.key == pygame.K_BACKSPACE:
                        password_confirm = password_confirm[:-1]
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(password_confirm) < 10:
                        password_confirm += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back_rect.collidepoint((mx, my)):
                    if event.button == 1:
                        is_running = False
                if event.button == 1:
                    click = True
                    btn_click = True
        if username_input_rect.collidepoint((mx, my)):
            if click:
                username_active = True
                password_active = False
                password_confirm_active = False
        if password_input_rect.collidepoint((mx, my)):
            if click:
                username_active = False
                password_active = True
                password_confirm_active = False
        if password_confirm_input_rect.collidepoint((mx, my)):
            if click:
                username_active = False
                password_active = False
                password_confirm_active = True
        click = False
        if username_active:
            color_username = color_active
            color_password = color_passive
            color_password_confirm = color_passive

        if password_active:
            color_password = color_active
            color_username = color_passive
            color_password_confirm = color_passive

        if password_confirm_active:
            color_username = color_passive
            color_password = color_passive
            color_password_confirm = color_active

        pygame.draw.rect(screen, color_username, username_input_rect, 3)

        game_title = pygame.font.Font('04B_19.TTF', 60).render("Flappython", True, (255, 255, 255))
        game_title_react = game_title.get_rect(center=(225, 120))
        screen.blit(game_title, game_title_react)

        username_title = game_font.render("Account:", True, (255, 255, 255))
        username_title_rect = username_title.get_rect(center=(100, 200))
        screen.blit(username_title, username_title_rect)

        pygame.draw.rect(screen, color_password, password_input_rect, 3)

        password_title = game_font.render("Password:", True, (255, 255, 255))
        password_title_rect = password_title.get_rect(center=(115, 320))
        screen.blit(password_title, password_title_rect)

        pygame.draw.rect(screen, color_password_confirm, password_confirm_input_rect, 3)

        password_confirm_title = game_font.render("Confirm password:", True, (255, 255, 255))
        password_confirm_title_rect = password_confirm_title.get_rect(center=(190, 440))
        screen.blit(password_confirm_title, password_confirm_title_rect)

        username_surface = game_font.render(username, True, (255, 255, 255))
        screen.blit(username_surface, (80, 240))

        password_surface = game_font.render(hide_password_text(password), True, (255, 255, 255))
        screen.blit(password_surface, (80, 360))

        password_confirm_surface = game_font.render(hide_password_text(password_confirm), True, (255, 255, 255))
        screen.blit(password_confirm_surface, (80, 490))

        btn_reg_rect = pygame.Rect(115, 580, 200, 80)
        screen.blit(reg_btn, (115, 580))

        if btn_reg_rect.collidepoint((mx, my)):
            if btn_click:
                handle_register(username, password, password_confirm)
                is_running = False
        btn_click = False
        pygame.display.update()
        clock.tick(120)


def is_valid_input(acc, passwd, passwd_confirm):
    if len(acc) <= 3:
        show_dialog("username too short")
        return False
    if len(passwd) <= 3:
        show_dialog("password too short")
        return False
    if passwd_confirm != "":
        if len(passwd_confirm) <= 3:
            show_dialog("password confirm too short")
            return False
        if passwd != passwd_confirm:
            show_dialog("password doesn't match")
            return False
    return True


def show_dialog(context):
    global click
    is_running = True
    while is_running:
        screen.blit(bg, (0, 0))
        screen.blit(dialog_bg, (5, 300))
        mx, my = pygame.mouse.get_pos()
        screen.blit(btn_ok, (220, 430))
        if btn_ok_rect.collidepoint((mx, my)):
            if click:
                is_running = False
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_running = False
        game_title = pygame.font.Font('04B_19.TTF', 24).render(context, True, (207, 59, 59))
        game_title_react = game_title.get_rect(center=(200, 350))
        screen.blit(game_title, game_title_react)
        pygame.display.update()
        clock.tick(120)


def handle_register(acc, passwd, passwd_confirm):
    global username, password, password_confirm
    if is_valid_input(acc, passwd, passwd_confirm):
        if db.signup(acc, passwd):
            show_dialog("Create completed")
        else:
            show_dialog("This username already used!")
    username = ''
    password = ''
    password_confirm = ''


def handle_login(acc, passwd):
    global username, password
    if is_valid_input(acc, passwd, ""):
        if db.login(acc, passwd):
            show_dialog("Login successful!")
            menu.main_menu(acc)
        else:
            show_dialog("wrong username/password")
    password = ''


def show_login_box():
    global color_username, color_password, username, username_active, password, password_active, click, btn_click
    is_running = True
    while is_running:
        screen.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(username) < 15:
                        username += event.unicode
                if password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(password) < 10:
                        password += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    btn_click = True
        if username_input_rect.collidepoint((mx, my)):
            if click:
                username_active = True
                password_active = False
        if password_input_rect.collidepoint((mx, my)):
            if click:
                username_active = False
                password_active = True
        click = False
        if username_active:
            color_username = color_active
        else:
            color_username = color_passive

        if password_active:
            color_password = color_active
        else:
            color_password = color_passive
        pygame.draw.rect(screen, color_username, username_input_rect, 3)

        game_title = pygame.font.Font('04B_19.TTF', 60).render("Flappython", True, (255, 255, 255))
        game_title_react = game_title.get_rect(center=(225, 75))
        screen.blit(game_title, game_title_react)

        username_title = game_font.render("Account:", True, (255, 255, 255))
        username_title_rect = username_title.get_rect(center=(100, 200))
        screen.blit(username_title, username_title_rect)

        pygame.draw.rect(screen, color_password, password_input_rect, 3)

        password_title = game_font.render("Password:", True, (255, 255, 255))
        password_title_rect = password_title.get_rect(center=(115, 320))
        screen.blit(password_title, password_title_rect)

        username_surface = game_font.render(username, True, (255, 255, 255))
        screen.blit(username_surface, (80, 240))

        password_surface = game_font.render(hide_password_text(password), True, (255, 255, 255))
        screen.blit(password_surface, (80, 360))

        btn_reg_rect = pygame.Rect(115, 420, 200, 80)
        btn_login_rect = pygame.Rect(115, 520, 200, 80)
        screen.blit(reg_btn, (115, 420))
        screen.blit(login_btn, (115, 520))

        if btn_reg_rect.collidepoint((mx, my)):
            if btn_click:
                show_register()
        if btn_login_rect.collidepoint((mx, my)):
            if btn_click:
                handle_login(username, password)
        btn_click = False

        pygame.display.update()
        clock.tick(120)


DIALOG_BG = 'res/dialog_bg.png'
BTN_OK_LOCATION = 'res/btn_ok.png'

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('black')
color_username = color_passive
color_password = color_passive
color_password_confirm = color_passive

username_active = True
password_active = False
password_confirm_active = False

username_input_rect = pygame.Rect(60, 230, 320, 50)
password_input_rect = pygame.Rect(60, 350, 320, 50)
password_confirm_input_rect = pygame.Rect(60, 480, 320, 50)

screen = pygame.display.set_mode((432, 768))

reg_btn = pygame.image.load(BTN_REG_IMG_LOCATION).convert_alpha()
login_btn = pygame.image.load(BTN_LOGIN_IMG_LOCATION).convert_alpha()

btn_back = pygame.image.load(game.BTN_BACK_LOCATION).convert_alpha()
btn_back_rect = pygame.Rect(10, 10, 110, 80)

dialog_bg = pygame.image.load(DIALOG_BG).convert_alpha()

btn_ok = pygame.image.load(BTN_OK_LOCATION).convert_alpha()
btn_ok_rect = pygame.Rect(220, 430, 110, 80)

bg = pygame.image.load('res/background-night-dimmed.png').convert()
game_font = pygame.font.Font('04B_19.TTF', 35)

username = ''
password = ''
password_confirm = ''

click = True
btn_click = True
clock = pygame.time.Clock()
show_login_box()
