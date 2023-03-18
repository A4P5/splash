import os
import pygame
os.system('cls')
import sys
import time
import clipboard
import os
import requests
import threading
import mouse
from pygame._sdl2 import Window

os.system('title RunDEBUGGER OS   /   Ready')
chars = []
for c in (chr(i) for i in range(32, 127)):
    chars.append(c)


def execute(code):

    if '://' in code:
        code = requests.get(code).text

    with open('temp.py', 'w') as f:
        f.write(code)
    os.startfile('temp.py')


def display():
    input_text = ""
    input_box = pygame.Rect(100, 130, 400, 50)
    selected_color = (107, 25, 115)
    start_color = (81, 117, 74)
    start_hover_color = (105, 150, 96)

    def quit_loop():
        pygame.quit()
        sys.exit(0)

    def draw_text(text, size, color, x, y, z=False, hide=False):
        font = pygame.font.SysFont('segoeui', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        if not hide:
            screen.blit(text_surface, text_rect)

        if z:
            return text_surface.get_rect().width

    click = False
    first_collide = True
    while True:
        screen.fill((39, 5, 54))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_loop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_loop()
                if event.key == pygame.K_RETURN:
                    threading.Thread(target=execute, args=[input_text,]).start()
                else:
                    for char in chars:
                        if char == event.unicode:
                            input_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            if keys[pygame.K_BACKSPACE]:
                input_text = ""
        if keys[pygame.K_LCTRL]:
            if keys[pygame.K_v]:
                input_text += clipboard.paste()
                time.sleep(0.3)

        if keys[pygame.K_BACKSPACE]:
            input_text = input_text[:-1]
            time.sleep(0.2)

        box_size = draw_text(input_text, 35, (235, 160, 233), input_box.x + 10, input_box.y - 7 + 5, z=True, hide=True)

        if box_size > 365:
            draw_text(input_text, 35, (235, 160, 233), (input_box.x + 10) - (box_size-365), input_box.y - 7 + 5, z=True)
        else:
            draw_text(input_text, 35, (235, 160, 233), input_box.x + 20, input_box.y - 7 + 5, z=True)

        draw_text('execute(', 40, (237, 140, 236), 100, 65)
        draw_text(')', 40, (237, 140, 236), 105, 185)

        mx, my = pygame.mouse.get_pos()
        real_mx, real_my = mouse.get_position()

        if input_box.collidepoint(mx, my):
            color = selected_color
        else:
            color = (87, 25, 115)

        pygame.draw.rect(screen, (39, 5, 54), pygame.Rect(0, 130, 120, 50))

        pygame.draw.rect(screen, color, input_box, 2, 20)

        start_hitbox = pygame.Rect(475, 125, 55, 60)

        frame_hitbox = pygame.Rect(0, 0, 600, 20)
        pygame.draw.rect(screen, (70, 38, 84), frame_hitbox)

        if frame_hitbox.collidepoint(mx, my):
            if first_collide:
                get_mx = mx
                get_my = my
            if click:
                if first_collide:
                    first_collide = False
                pgwindow.position = (real_mx - get_mx, real_my - get_my)

        if not click:
            first_collide = True

        if start_hitbox.collidepoint(mx, my):
            run_color = start_hover_color
            if click:
                execute(input_text)
                click = False
        else:
            run_color = start_color

        pygame.draw.rect(screen, run_color, pygame.Rect(480, 130, 20, 50), 0, 0)
        pygame.draw.rect(screen, run_color, pygame.Rect(480, 130, 50, 50), 0, 20)

        pygame.draw.polygon(screen, (30, 225, 50), ((518, 155), (492, 140), (492, 170)))

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 340), pygame.NOFRAME)
    pgwindow = Window.from_display_module()
    display()
