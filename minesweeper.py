import pygame, sys
from random import randrange
from pygame.locals import *
from ctypes import windll

pygame.init()

# Constants
SCREEN_WIDTH = 350
SCREEN_HEIGHT = 400
GRID_SIZE = 9
BLOCK_SIZE = 34
MARGIN = 20
TOTAL_BOMBS = 10
FPS = 30

# Colors
COLOR_BROWN = pygame.Color(84, 51, 16)
COLOR_BEIGE = pygame.Color(254, 253, 237)
COLOR_RED = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(0, 255, 0)
COLOR_BLUE = pygame.Color(0, 0, 255)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = Rect(x * BLOCK_SIZE + MARGIN, y * BLOCK_SIZE + MARGIN, BLOCK_SIZE, BLOCK_SIZE)
        self.is_bomb = False
        self.flag_status = -3  # -3 = no flag, -2 = flag, -1 = question mark, 0 = blank, 1-8 = warnings, 9 = explosion
        self.index = 0

class BlockManager:
    def __init__(self):
        self.blocks = []
        self.checked_blocks = []
        self.total_bombs = 0
        self.flags_used = 0
        self.remaining_blocks = 0

    def initialize_blocks(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                block = Block(x, y)
                block.index = len(self.blocks)
                self.blocks.append(block)
    
    def place_bombs(self):
        while self.total_bombs < TOTAL_BOMBS:
            index = randrange(0, len(self.blocks))
            if not self.blocks[index].is_bomb:
                self.blocks[index].is_bomb = True
                self.total_bombs += 1

    def get_block_at(self, x, y):
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
        return None

    def get_adjacent_blocks(self, block):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = self.get_block_at(block.x + dx, block.y + dy)
                if neighbor:
                    neighbors.append(neighbor)
        return neighbors

    def get_warning_count(self, block):
        warning_count = 0
        neighbors = self.get_adjacent_blocks(block)
        for neighbor in neighbors:
            if neighbor.is_bomb:
                warning_count += 1
        return warning_count

    def find_path(self, block):
        cross_blocks = self.get_cross_path(block)
        for cross_block in cross_blocks:
            if cross_block and self.get_warning_count(cross_block) == 0:
                cross_block.flag_status = 0
        adjacent_blocks = self.get_adjacent_blocks(block)
        for adj_block in adjacent_blocks:
            warning = self.get_warning_count(adj_block)
            if 0 < warning < 9:
                adj_block.flag_status = warning
        self.checked_blocks.append(block)
    
    def get_cross_path(self, block):
        paths = []
        if block.x > 0:
            paths.append(self.get_block_at(block.x - 1, block.y))
        if block.x < GRID_SIZE - 1:
            paths.append(self.get_block_at(block.x + 1, block.y))
        if block.y > 0:
            paths.append(self.get_block_at(block.x, block.y - 1))
        if block.y < GRID_SIZE - 1:
            paths.append(self.get_block_at(block.x, block.y + 1))
        return paths

class MinesweeperUI:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.icon_bomb = pygame.image.load("images/bomb.png")
        pygame.display.set_icon(self.icon_bomb)
        self.game_font = pygame.font.Font("fonts/Agitpropc.otf", 36)
        self.load_images()
    
    def load_images(self):
        self.block_image = pygame.transform.scale(pygame.image.load("images/block.png"), (BLOCK_SIZE, BLOCK_SIZE))
        self.selected_block_image = pygame.transform.scale(pygame.image.load("images/selblock.png"), (BLOCK_SIZE, BLOCK_SIZE))
        self.blank_block_image = pygame.transform.scale(pygame.image.load("images/blankblock.png"), (BLOCK_SIZE, BLOCK_SIZE))
        self.warning_images = [pygame.transform.scale(pygame.image.load(f"images/num{i}.png"), (BLOCK_SIZE, BLOCK_SIZE)) for i in range(1, 9)]
        self.explode_image = pygame.transform.scale(pygame.image.load("images/explode.png"), (BLOCK_SIZE, BLOCK_SIZE))
        self.flag_image = pygame.transform.scale(pygame.image.load("images/flag.png"), (BLOCK_SIZE, BLOCK_SIZE))
        self.question_image = pygame.transform.scale(pygame.image.load("images/question.png"), (BLOCK_SIZE, BLOCK_SIZE))
        self.clock_image = pygame.transform.scale(pygame.image.load("images/time.png"), (BLOCK_SIZE, BLOCK_SIZE))

    def draw_grid(self):
        pygame.draw.line(self.screen, COLOR_BROWN, (MARGIN, MARGIN), (MARGIN + GRID_SIZE * BLOCK_SIZE, MARGIN))
        pygame.draw.line(self.screen, COLOR_BROWN, (MARGIN, MARGIN), (MARGIN, MARGIN + GRID_SIZE * BLOCK_SIZE))
        pygame.draw.line(self.screen, COLOR_BROWN, (MARGIN, MARGIN + GRID_SIZE * BLOCK_SIZE), (MARGIN + GRID_SIZE * BLOCK_SIZE, MARGIN + GRID_SIZE * BLOCK_SIZE))
        pygame.draw.line(self.screen, COLOR_BROWN, (MARGIN + GRID_SIZE * BLOCK_SIZE, MARGIN), (MARGIN + GRID_SIZE * BLOCK_SIZE, MARGIN + GRID_SIZE * BLOCK_SIZE))

    def render_blocks(self):
        self.game.block_manager.flags_used = 0
        self.game.block_manager.remaining_blocks = 0
        for block in self.game.block_manager.blocks:
            if block.flag_status == -3:
                self.game.block_manager.remaining_blocks += 1
                self.screen.blit(self.block_image, block.position)
            elif block.flag_status == 0:
                if block not in self.game.block_manager.checked_blocks:
                    self.game.block_manager.find_path(block)
                self.screen.blit(self.blank_block_image, block.position)
            elif block.flag_status == 9:
                self.screen.blit(self.explode_image, block.position)
                self.game.handle_loss()
            elif block.flag_status == -2:
                self.screen.blit(self.flag_image, block.position)
                self.game.block_manager.flags_used += 1
            elif block.flag_status == -1:
                self.screen.blit(self.question_image, block.position)
            elif 1 <= block.flag_status <= 8:
                self.screen.blit(self.warning_images[block.flag_status - 1], block.position)
        if self.game.block_manager.remaining_blocks == TOTAL_BOMBS:
            self.game.handle_win()
    
    def display(self):
        self.screen.fill(COLOR_BEIGE)
        self.screen.blit(self.clock_image, (MARGIN, SCREEN_HEIGHT - MARGIN - BLOCK_SIZE))
        self.screen.blit(self.icon_bomb, (SCREEN_WIDTH - MARGIN - BLOCK_SIZE, SCREEN_HEIGHT - MARGIN - BLOCK_SIZE))

        remaining_bombs_text = self.game_font.render(str(TOTAL_BOMBS - self.game.block_manager.flags_used), True, COLOR_BLACK)
        remaining_bombs_rect = remaining_bombs_text.get_rect()
        remaining_bombs_rect.topleft = (SCREEN_WIDTH - MARGIN * 2 - remaining_bombs_rect.width, SCREEN_HEIGHT - MARGIN - BLOCK_SIZE)
        self.screen.blit(remaining_bombs_text, remaining_bombs_rect)

        mins, secs = divmod((pygame.time.get_ticks() - self.game.last_game_time) / 1000, 60)
        mins_str = f"{int(mins):02}"
        secs_str = f"{int(secs):02}"

        timer_text = self.game_font.render(f"{mins_str}:{secs_str}", True, COLOR_BLACK)
        timer_rect = timer_text.get_rect()
        timer_rect.topleft = (MARGIN + BLOCK_SIZE, SCREEN_HEIGHT - MARGIN - BLOCK_SIZE)
        self.screen.blit(timer_text, timer_rect)

        self.draw_grid()
        self.render_blocks()
        pygame.display.update()

class Game:
    def __init__(self):
        self.ui = MinesweeperUI(self)
        self.block_manager = BlockManager()
        self.selected_block = None
        self.reference_block = Block(-10, -10)
        self.last_game_time = 0
        self.reset_game()

    def reset_game(self):
        self.block_manager.blocks.clear()
        self.block_manager.checked_blocks.clear()
        self.block_manager.total_bombs = 0
        self.block_manager.flags_used = 0
        self.block_manager.remaining_blocks = 0
        self.block_manager.initialize_blocks()
        self.block_manager.place_bombs()
        self.last_game_time = pygame.time.get_ticks()

    def show_message_box(self, title, text, style):
        return windll.user32.MessageBoxW(0, text, title, style)

    def handle_loss(self):
        response = self.show_message_box("Вибачте, ви програли!", "Ви програли! Повторити гру?", 1)
        if response == 1:
            self.reset_game()
        else:
            pygame.quit()
            sys.exit()

    def handle_win(self):
        response = self.show_message_box("Вітаємо, ви виграли!", "Ви виграли! Повторити гру?", 1)
        if response == 1:
            self.reset_game()
        else:
            pygame.quit()
            sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                self.selected_block = self.get_hovered_block(event.pos)
                if not self.is_within_bounds(event.pos):
                    self.selected_block = self.reference_block
            elif event.type == MOUSEBUTTONUP:
                if self.is_within_bounds(event.pos):
                    self.selected_block = self.get_hovered_block(event.pos)
                    if self.selected_block:
                        if event.button == 1:
                            self.selected_block.flag_status = self.block_manager.get_warning_count(self.selected_block)
                            if self.selected_block.flag_status == 0:
                                self.block_manager.find_path(self.selected_block)
                            if self.selected_block.is_bomb:
                                self.selected_block.flag_status = 9
                        elif event.button == 3:
                            if self.selected_block.flag_status == -3:
                                self.selected_block.flag_status = -2
                            elif self.selected_block.flag_status == -2:
                                self.selected_block.flag_status = -1
                            elif self.selected_block.flag_status == -1:
                                self.selected_block.flag_status = -3
        if self.selected_block and self.selected_block.flag_status == -3:
            self.ui.screen.blit(self.ui.selected_block_image, self.selected_block.position)

    def is_within_bounds(self, pos):
        return Rect(MARGIN, MARGIN, GRID_SIZE * BLOCK_SIZE, GRID_SIZE * BLOCK_SIZE).collidepoint(pos)

    def get_hovered_block(self, pos):
        for block in self.block_manager.blocks:
            if block.position.collidepoint(pos):
                return block
        return None

    def run(self):
        while True:
            self.handle_events()
            self.ui.display()
            self.ui.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
