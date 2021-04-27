import pygame
import pyperclip
from random import choice

pygame.init()

abc = 'abcdefghijklmnopqrstuvwxyz'
ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nums = '0123456789'
special = '@#%"&*()_-+={}<>?:[].~'
sym_types = {'abc': True, 'ABC': True, '123': True, '#^~': False}


def generate_password(m):
    a = ''
    sym1 = ''
    if sym_types['abc']:
        sym1 += abc
    if sym_types['ABC']:
        sym1 += ABC
    if sym_types['123']:
        sym1 += nums
    if sym_types['#^~']:
        sym1 += special
    for i in range(m):
        a += choice(sym1)
    return a


class RedGreen:
    def __init__(self, surface, top_left_cords, size, font, text):
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(topleft=top_left_cords)
        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom + 25))
        self.draw_surface = surface
        self.name = text

    def draw(self):
        self.draw_surface.blit(self.surf, self.rect)
        self.draw_surface.blit(self.text_surf, self.text_rect)

    def check(self, pos):
        if self.rect.collidepoint(pos):
            if sym_types[self.name]:
                sym_types[self.name] = False
            else:
                sym_types[self.name] = True
        self.change_color()

    def change_color(self):
        if sym_types[self.name]:
            self.surf.fill((0, 255, 0))
        else:
            self.surf.fill((255, 0, 0))


width = 1000
height = 600
centerX, centerY = width // 2, height // 2

FPS = 20

background_color = (255, 255, 255)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Генератор паролей")

main_screen = pygame.Surface((width, height))
settings_screen = pygame.Surface((width, height))

main_button = pygame.image.load('main_button.png').convert_alpha()
main_button = pygame.transform.scale(main_button, (320, 160))
main_button_pressed = pygame.image.load('main_button_pressed.png').convert_alpha()
main_button_pressed = pygame.transform.scale(main_button_pressed, (320, 160))
surf = main_button
rect = surf.get_rect(center=(centerX, 400))

setting_button = pygame.image.load('settings_button.png').convert_alpha()
setting_button = pygame.transform.scale(setting_button, (62, 62))
settings_rect = setting_button.get_rect(center=(width - 50, height - 50))

password = 100 * " " + "Press button" + " " * 100
password_lenght = 12

main_font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 40)

text = main_font.render(password, True, (0, 0, 0))
text_rect = text.get_rect(center=(centerX, centerY - 100))

surf_copy = pygame.image.load('copy_button.png').convert_alpha()
rect_copy = surf_copy.get_rect(center=(text_rect.right + 30, centerY - 100))

text_len = main_font.render(str(password_lenght), True, (0, 0, 0))
text_len_rect = text_len.get_rect(center=(centerX, centerY - 50))

surf_up_unpressed = pygame.image.load('up_button.png').convert_alpha()
surf_up_unpressed = pygame.transform.scale(surf_up_unpressed, (80, 80))
surf_up_pressed = pygame.image.load('up_button_pressed.png').convert_alpha()
surf_up_pressed = pygame.transform.scale(surf_up_pressed, (80, 80))
surf_up = surf_up_unpressed

surf_down_unpressed = pygame.image.load('down_button.png').convert_alpha()
surf_down_unpressed = pygame.transform.scale(surf_down_unpressed, (80, 80))
surf_down_pressed = pygame.image.load('down_button_pressed.png').convert_alpha()
surf_down_pressed = pygame.transform.scale(surf_down_pressed, (80, 80))
surf_down = surf_up_unpressed

rect_up = surf_up.get_rect(center=(text_len_rect.right + 70, centerY - 50))
reft_down = surf_down.get_rect(center=(text_len_rect.left - 70, centerY - 50))

copy_text_surf = small_font.render("Copied", True, (0, 0, 0))
copy_text_rect = copy_text_surf.get_rect(center=(centerX, 30))

red_green_list = []
x, y = centerX - 265, centerY + 160
for i in sym_types:
    red_green_list.append(RedGreen(settings_screen, (x, y), (80, 80), small_font, i))
    red_green_list[-1].check(pygame.mouse.get_pos())
    x += 150


def draw_main():
    global transparency
    main_screen.fill(background_color)

    main_screen.blit(surf, rect)
    main_screen.blit(text, text_rect)
    main_screen.blit(surf_copy, rect_copy)
    main_screen.blit(setting_button, settings_rect)

    if transparency > 0:
        copy_text_surf.set_alpha(transparency)
        main_screen.blit(copy_text_surf, copy_text_rect)
        transparency -= 6

    screen.blit(main_screen, (0, 0))


def draw_settings():
    settings_screen.fill(background_color)

    settings_screen.blit(setting_button, settings_rect)
    settings_screen.blit(text_len, text_len_rect)

    settings_screen.blit(surf_up, rect_up)
    settings_screen.blit(surf_down, reft_down)

    for i in red_green_list:
        i.draw()

    screen.blit(settings_screen, (0, 0))


transparency = 0

running = True

flMain = True

draw_main()

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos) and flMain:
                surf = main_button_pressed
            if rect_up.collidepoint(event.pos) and not flMain:
                surf_up = surf_up_pressed
            if reft_down.collidepoint(event.pos) and not flMain:
                surf_down = surf_down_pressed
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = event.pos
            surf = main_button
            surf_up = surf_up_unpressed
            surf_down = surf_down_unpressed
            if rect.collidepoint(pos) and flMain:
                if not (sym_types['abc'] or sym_types['ABC'] or sym_types['123'] or sym_types['#^~']):
                    password = 100 * " " + "Select at least one filter" + " " * 100
                else:
                    password = generate_password(password_lenght)
                text = main_font.render(password, True, (0, 0, 0))
                text_rect = text.get_rect(center=(width // 2, height // 3))
                rect_copy = surf_copy.get_rect(center=(text_rect.right + 30, height // 6 * 2))
            elif rect_copy.collidepoint(pos) and flMain:
                pyperclip.copy(password)
                transparency = 285
            elif settings_rect.collidepoint(pos):
                flMain = not flMain
            elif reft_down.collidepoint(pos) and not flMain:
                password_lenght = password_lenght - 1 if password_lenght - 1 >= 4 else password_lenght
                text_len = main_font.render(str(password_lenght), True, (0, 0, 0))
                text_len_rect = text_len.get_rect(center=(centerX, centerY - 50))
            elif rect_up.collidepoint(pos) and not flMain:
                password_lenght = password_lenght + 1 if password_lenght + 1 <= 22 else password_lenght
                text_len = main_font.render(str(password_lenght), True, (0, 0, 0))
                text_len_rect = text_len.get_rect(center=(centerX, centerY - 50))
            for i in red_green_list:
                i.check(event.pos)

    if flMain:
        draw_main()
    else:
        draw_settings()

    pygame.display.update()

pygame.quit()
