import pygame, sys
from random import randrange
from pygame.locals import *
from ctypes import windll

pygame.init()
clock = pygame.time.Clock()
icon_bomb = pygame.image.load("images/bomb.png")
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

game_font = pygame.font.Font("fonts/Agitpropc.otf", 36)

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
game_font = pygame.font.Font("fonts/Agitpropc.otf", 36)

# Завантаження зображень блоків
block_image = pygame.transform.scale(pygame.image.load("images/block.png"), (34, 34))
selected_block_image = pygame.transform.scale(pygame.image.load("images/selblock.png"), (34, 34))
blank_block_image = pygame.transform.scale(pygame.image.load("images/blankblock.png"), (34, 34))

# Завантаження зображень попереджень
warning_images = [pygame.transform.scale(pygame.image.load(f"images/num{i}.png"), (34, 34)) for i in range(1, 9)]
# Завантаження зображення вибуху
explode_image = pygame.transform.scale(pygame.image.load("images/explode.png"), (34, 34))
# Завантаження зображення прапора та знака питання
flag_image = pygame.transform.scale(pygame.image.load("images/flag.png"), (34, 34))
question_image = pygame.transform.scale(pygame.image.load("images/question.png"), (34, 34))
# Завантаження зображення годинника
clock_image = pygame.transform.scale(pygame.image.load("images/time.png"), (34, 34))

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

# Функція для пошуку шляхів (рекурсивна)
def get_cross_path(block):
    paths = []
    if block.x > 0:
        paths.append(get_block_at(block.x - 1, block.y))
    if block.x < 9:
        paths.append(get_block_at(block.x + 1, block.y))
    if block.y > 0:
        paths.append(get_block_at(block.x, block.y - 1))
    if block.y < 9:
        paths.append(get_block_at(block.x, block.y + 1))
    return paths

def find_path(block):
    for cross_block in get_cross_path(block):
        if cross_block and get_warning_count(cross_block) == 0:
            cross_block.flag_status = 0
    for adj_block in get_adjacent_blocks(block):
        warning = get_warning_count(adj_block)
        if 0 < warning < 9:
            adj_block.flag_status = warning
    checked_blocks.append(block)

last_game_time = 0


# Функція для програшу
def handle_loss():
    response = showMessageBox("Вибачте, ви програли!", "Ви програли! Повторити гру?", 1)
    if response == 1:  # ID 1 відповідає кнопці "ОК" або "Так"
        reset_game()
    else:
        pygame.quit()
        sys.exit()

# Функція для виграшу
def handle_win():
    response = showMessageBox("Вітаємо, ви виграли!", "Ви виграли! Повторити гру?", 1)
    if response == 1:  # ID 1 відповідає кнопці "ОК" або "Так"
        reset_game()
    else:
        pygame.quit()
        sys.exit()

# Функція для скидання гри
def reset_game():
    global clock
    global blocks
    global total_bombs
    global flags_used
    global checked_blocks
    global remaining_blocks
    global last_game_time
    clock = pygame.time.Clock()
    blocks[:] = []
    total_bombs = 0
    initialize_blocks()
    place_bombs()
    flags_used = 0
    checked_blocks = []
    remaining_blocks = 0
    last_game_time = pygame.time.get_ticks()


while True:
    screen.fill(color_beige)
    screen.blit(clock_image, (20, 346))
    screen.blit(icon_bomb, (294, 346))

    remaining_bombs_text = game_font.render(str(10 - flags_used), True, color_black)
    remaining_bombs_rect = remaining_bombs_text.get_rect()
    remaining_bombs_rect.topleft = (240, 346)
    screen.blit(remaining_bombs_text, remaining_bombs_rect)

    if last_game_time != 0:
        mins = (pygame.time.get_ticks() - last_game_time) / 1000 / 60
        secs = (pygame.time.get_ticks() - last_game_time) / 1000 % 60
    else:
        mins = pygame.time.get_ticks() / 1000 / 60
        secs = pygame.time.get_ticks() / 1000 % 60

    mins_str = f"{int(mins):02}"
    secs_str = f"{int(secs):02}"

    timer_text = game_font.render(mins_str + ":" + secs_str, True, color_black)
    timer_rect = timer_text.get_rect()
    timer_rect.topleft = (60, 346)
    screen.blit(timer_text, timer_rect)

    draw_grid()
    render_blocks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            selected_block = get_hovered_block(event.pos)
            if not is_within_bounds(event.pos):
                selected_block = reference_block
        elif event.type == MOUSEBUTTONUP:
            if is_within_bounds(event.pos):
                selected_block = get_hovered_block(event.pos)
                if selected_block:
                    if event.button == 1:
                        selected_block.flag_status = get_warning_count(selected_block)
                        if selected_block.flag_status == 0:
                            blocks_to_check.append(selected_block)
                            find_path(selected_block)
                        if selected_block.is_bomb:
                            selected_block.flag_status = 9
                    elif event.button == 3:
                        if selected_block.flag_status == -3:
                            selected_block.flag_status = -2
                        elif selected_block.flag_status == -2:
                            selected_block.flag_status = -1
                        elif selected_block.flag_status == -1:
                            selected_block.flag_status = -3
    if selected_block and selected_block.flag_status == -3:
        screen.blit(selected_block_image, selected_block.position)

    pygame.display.update()
    clock.tick(30)
