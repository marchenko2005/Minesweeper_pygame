import pygame, sys
from random import randrange
from pygame.locals import *
from ctypes import windll

pygame.init()
clock = pygame.time.Clock()
icon_bomb = pygame.image.load("bomb.png")
pygame.display.set_icon(icon_bomb)
screen = pygame.display.set_mode((350, 400))
pygame.display.set_caption("Minesweeper")

color_brown = pygame.Color(84, 51, 16)
color_beige = pygame.Color(254, 253, 237)
color_red = pygame.Color(255, 0, 0)
color_green = pygame.Color(0, 255, 0)
color_blue = pygame.Color(0, 0, 255)
color_white = pygame.Color(255, 255, 255)
color_black = pygame.Color(0, 0, 0)

game_font = pygame.font.Font("UniversLTStd-BoldEx.otf", 36)

# Функція для показу повідомлення
def showMessageBox(title, text, style):
    return windll.user32.MessageBoxW(0, text, title, style)


# Визначення кольорів
color_brown = pygame.Color(84, 51, 16)
color_beige = pygame.Color(254, 253, 237)
color_red = pygame.Color(255, 0, 0)
color_green = pygame.Color(0, 255, 0)
color_blue = pygame.Color(0, 0, 255)
color_white = pygame.Color(255, 255, 255)
color_black = pygame.Color(0, 0, 0)

# Завантаження шрифту
game_font = pygame.font.Font("AGCrownStyle (1).ttf", 36)

# Завантаження зображень блоків
block_image = pygame.transform.scale(pygame.image.load("block.png"), (34, 34))
selected_block_image = pygame.transform.scale(pygame.image.load("selblock.png"), (34, 34))
blank_block_image = pygame.transform.scale(pygame.image.load("blankblock.png"), (34, 34))

# Завантаження зображень попереджень
warning_images = [pygame.transform.scale(pygame.image.load(f"num{i}.png"), (34, 34)) for i in range(1, 9)]
# Завантаження зображення вибуху
explode_image = pygame.transform.scale(pygame.image.load("explode.png"), (34, 34))
# Завантаження зображення прапора та знака питання
flag_image = pygame.transform.scale(pygame.image.load("flag.png"), (34, 34))
question_image = pygame.transform.scale(pygame.image.load("question.png"), (34, 34))
# Завантаження зображення годинника
clock_image = pygame.transform.scale(pygame.image.load("time.png"), (34, 34))

# Список для зберігання блоків
blocks = []
# Кількість бомб
total_bombs = 0

# Клас для блоків
class Block():
    is_bomb = False
    index = 0
    x = 0
    y = 0
    def __init__(self, position):
        self.position = position
        self.flag_status = -3  # -3 = БЕЗ ПРАПОРА; -2 = ПРАПОР; -1 = ЗНАК ПИТАННЯ; 0 = ПУСТИЙ; 1-8 = ПОПЕРЕДЖЕННЯ; 9 = ВИБУХ

reference_block = Block(Rect(-200, -200, 0, 0))
reference_block.x = -10
reference_block.y = -10
selected_block = reference_block

# Функція для малювання поля гри
def draw_grid():
    pygame.draw.line(screen, color_brown, (20, 20), (326, 20))
    pygame.draw.line(screen, color_brown, (20, 20), (20, 326))
    pygame.draw.line(screen, color_brown, (20, 326), (326, 326))
    pygame.draw.line(screen, color_brown, (326, 20), (326, 326))

# Функція для ініціалізації блоків
def initialize_blocks():
    for x in range(0, 9):
        for y in range(0, 9):
            block = Block(Rect(x*34+20, y*34+20, 34, 34))
            block.index = len(blocks)
            block.x = x
            block.y = y
            blocks.append(block)
            screen.blit(block_image, (x*34 + 20, y*34 + 20))

initialize_blocks()
