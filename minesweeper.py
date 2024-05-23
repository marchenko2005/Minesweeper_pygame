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

# Функція для розміщення бомб
def place_bombs():
    global total_bombs
    while total_bombs < 10:
        index = randrange(0, len(blocks))
        if not blocks[index].is_bomb:
            blocks[index].is_bomb = True
            total_bombs += 1

place_bombs()
flags_used = 0
checked_blocks = []
remaining_blocks = 0


# Функція для малювання блоків
def render_blocks():
    global flags_used
    global remaining_blocks
    flags_used = 0
    remaining_blocks = 0
    for block in blocks:
        if block.flag_status == -3:
            remaining_blocks += 1
            screen.blit(block_image, block.position)
        elif block.flag_status == 0:
            if block not in checked_blocks:
                find_path(block)
            screen.blit(blank_block_image, block.position)
        elif block.flag_status == 9:
            screen.blit(explode_image, block.position)
            handle_loss()
        elif block.flag_status == -2:
            screen.blit(flag_image, block.position)
            flags_used += 1
        elif block.flag_status == -1:
            screen.blit(question_image, block.position)
        elif 1 <= block.flag_status <= 8:
            screen.blit(warning_images[block.flag_status - 1], block.position)
    if remaining_blocks == 10:
        handle_win()

# Функція для перевірки меж екрану
def is_within_bounds(pos):
    return Rect(20, 20, 306, 306).collidepoint(pos)

# Функція для визначення блоку під курсором миші
def get_hovered_block(pos):
    for block in blocks:
        if block.position.collidepoint(pos):
            return block
    return None

# Функція для визначення блоку за координатами
def get_block_at(x, y):
    for block in blocks:
        if block.x == x and block.y == y:
            return block
    return None

# Функція для визначення сусідніх блоків
def get_adjacent_blocks(block):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbor = get_block_at(block.x + dx, block.y + dy)
            if neighbor:
                neighbors.append(neighbor)
    return neighbors

# Функція для отримання кількості попереджень
def get_warning_count(block):
    warning_count = 0
    neighbors = get_adjacent_blocks(block)
    for neighbor in neighbors:
        if neighbor.is_bomb:
            warning_count += 1
    return warning_count

blocks_to_check = []
