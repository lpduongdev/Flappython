import hashlib

import pygame
import sys
import db
import game
import menu


class Account:
    def __init__(self, username_text, plain_password, plain_password_confirm=None):
        self.__username = username_text
        self.__plain_password = plain_password
        self.__plain_password_confirm = ''
        if plain_password_confirm is not None:
            self.__plain_password_confirm = str(plain_password_confirm)

    def get_username(self):
        return self.__username

    def _set_username(self, username_text):
        self.__username = username_text

    def _get_password_length(self):
        return len(self.__plain_password)

    def _set_plain_password(self, is_delete, character=None):
        if is_delete and character is None:
            self.__plain_password = self.__plain_password[:-1]
            return
        self.__plain_password += character
        return

    def _get_password_confirm_length(self):
        return len(self.__plain_password_confirm)

    def _set_plain_password_confirm(self, is_delete, character=None):
        if is_delete and character is None:
            self.__plain_password_confirm = self.__plain_password_confirm[:-1]
            return
        self.__plain_password_confirm += character
        return

    def _get_hashed_password(self):
        hashed_password = hashlib.sha256(self.__plain_password.encode('utf-8')).hexdigest()
        hashed_password = hashed_password[0:7] + '1ae5' + hashed_password[7:12] + '3ee1' + hashed_password[10:] + 'aHV5'
        self.__plain_password = ''
        return hashed_password

    def _get_hashed_password_confirm(self):
        hashed_password = hashlib.sha256(self.__plain_password_confirm.encode('utf-8')).hexdigest()
        hashed_password = hashed_password[0:7] + '1ae5' + hashed_password[7:12] + '3ee1' + hashed_password[10:] + 'aHV5'
        self.__plain_password_confirm = ''
        return hashed_password


pygame.init()
BTN_REG_IMG_LOCATION = '../../../res/btn_register.png'
BTN_LOGIN_IMG_LOCATION = '../../../res/btn_login.png'


def generate_password_display(number):
    string = ''
    for x in range(0, number):
        string += '*'
    return str(string)


def is_valid(acc, plain_password, plain_password_confirm=None):
    if len(acc) <= 3:
        show_dialog("username_text too short")
        return False
    if len(plain_password) <= 3:
        show_dialog("password too short")
        return False
    if plain_password_confirm is not None:
        if len(plain_password_confirm) <= 3:
            show_dialog("password confirm too short")
            return False
        if plain_password != plain_password_confirm:
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
            screen.blit(pygame.image.load('../../../res/btn_ok_hover.png'), (220, 430))
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
        game_title = pygame.font.Font('../../../04B_19.TTF', 24).render(context, True, (207, 59, 59))
        game_title_react = game_title.get_rect(center=(200, 350))
        screen.blit(game_title, game_title_react)
        pygame.display.update()
        clock.tick(120)


def show_register():
    global color_username, color_password, color_password_confirm, username, username_active, password, password_active, password_confirm, password_confirm_active, click, btn_click
    reg_account = Account('', '', '')
    is_running = True
    while is_running:
        screen.blit(bg, (0, 0))
        screen.blit(btn_back, (10, 10))
        mx, my = pygame.mouse.get_pos()
        if btn_back_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('../../../res/btn_back_hover.png'), (10, 10))
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
                        reg_account._set_username(reg_account.get_username()[:-1])
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(reg_account.get_username()) < 15:
                        reg_account._set_username(reg_account.get_username() + event.unicode)
                if password_active:
                    if event.key == pygame.K_BACKSPACE:
                        reg_account._set_plain_password(True)
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and (reg_account._get_password_length()) < 10:
                        reg_account._set_plain_password(False, event.unicode)
                if password_confirm_active:
                    if event.key == pygame.K_BACKSPACE:
                        reg_account._set_plain_password_confirm(True)
                    if (
                            97 <= event.key <= 122 or 48 <= event.key <= 57) and reg_account._get_password_confirm_length() < 10:
                        # password_confirm += event.unicode
                        reg_account._set_plain_password_confirm(False, event.unicode)
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

        game_title = pygame.font.Font('../../../04B_19.TTF', 60).render("Flappython", True, (255, 255, 255))
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

        username_surface = game_font.render(reg_account.get_username(), True, (255, 255, 255))
        screen.blit(username_surface, (80, 240))

        password_surface = game_font.render(generate_password_display(reg_account._get_password_length()), True,
                                            (255, 255, 255))
        screen.blit(password_surface, (80, 360))

        password_confirm_surface = game_font.render(
            generate_password_display(reg_account._get_password_confirm_length()), True,
            (255, 255, 255))
        screen.blit(password_confirm_surface, (80, 490))

        btn_reg_rect = pygame.Rect(115, 580, 200, 80)
        screen.blit(reg_btn, (115, 580))

        if btn_reg_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('../../../res/btn_register_hover.png'), (115, 580))
            if btn_click:
                handle_register(reg_account)
                is_running = False
        btn_click = False
        pygame.display.update()
        clock.tick(120)


def handle_register(account):
    global username, password, password_confirm
    acc = account.get_username()
    passwd = account._get_hashed_password()
    passwd_confirm = account._get_hashed_password_confirm()
    if is_valid(acc, passwd, passwd_confirm):
        if db.signup(acc, passwd):
            show_dialog("Create completed")
        else:
            show_dialog("This username_text already used!")


def handle_login(account):
    hashed_password = account._get_hashed_password()
    if is_valid(account.get_username(), hashed_password):
        if db.login(account.get_username(), hashed_password):
            show_dialog("Login successful!")
            menu.main_menu(account.get_username())
        else:
            show_dialog("wrong username_text/password")


def show_login_box():
    global color_username, color_password, username_active, password_active, click, btn_click
    is_running = True
    account = Account('', '')
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
                        account._set_username(account.get_username()[:-1])
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and len(account.get_username()) < 15:
                        account._set_username(account.get_username() + event.unicode)
                if password_active:
                    if event.key == pygame.K_BACKSPACE:
                        account._set_plain_password(True)
                    if (97 <= event.key <= 122 or 48 <= event.key <= 57) and account._get_password_length() < 10:
                        account._set_plain_password(False, event.unicode)
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
            color_password = color_passive

        if password_active:
            color_password = color_active
            color_username = color_passive

        pygame.draw.rect(screen, color_username, username_input_rect, 3)

        game_title = pygame.font.Font('../../../04B_19.TTF', 60).render("Flappython", True, (255, 255, 255))
        game_title_react = game_title.get_rect(center=(225, 75))
        screen.blit(game_title, game_title_react)

        username_title = game_font.render("Account:", True, (255, 255, 255))
        username_title_rect = username_title.get_rect(center=(100, 200))
        screen.blit(username_title, username_title_rect)

        pygame.draw.rect(screen, color_password, password_input_rect, 3)

        password_title = game_font.render("Password:", True, (255, 255, 255))
        password_title_rect = password_title.get_rect(center=(115, 320))
        screen.blit(password_title, password_title_rect)

        username_surface = game_font.render(account.get_username(), True, (255, 255, 255))
        screen.blit(username_surface, (80, 240))

        password_surface = game_font.render(generate_password_display(account._get_password_length()), True,
                                            (255, 255, 255))
        screen.blit(password_surface, (80, 360))

        btn_reg_rect = pygame.Rect(115, 420, 200, 80)
        btn_login_rect = pygame.Rect(115, 520, 200, 80)
        screen.blit(reg_btn, (115, 420))
        screen.blit(login_btn, (115, 520))

        if btn_reg_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('../../../res/btn_register_hover.png'), (115, 420))
            if btn_click:
                show_register()
        if btn_login_rect.collidepoint((mx, my)):
            screen.blit(pygame.image.load('../../../res/btn_login_hover.png'), (115, 520))
            if btn_click:
                handle_login(account)
        btn_click = False

        pygame.display.update()
        clock.tick(120)


DIALOG_BG = '../../../res/dialog_bg.png'
BTN_OK_LOCATION = '../../../res/btn_ok.png'

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

bg = pygame.image.load('../../../res/background-night-dimmed.png').convert()
game_font = pygame.font.Font('../../../04B_19.TTF', 35)
pygame.display.set_icon(
    pygame.transform.scale2x(pygame.image.load('../../../res/yellowbird-midflap.png').convert_alpha()))
pygame.display.set_caption("Flappython")

click = True
btn_click = True
clock = pygame.time.Clock()

if __name__ == "__main__":
    show_login_box()
