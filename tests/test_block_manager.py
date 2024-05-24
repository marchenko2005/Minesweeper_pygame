import pytest
from minesweeper import Block, GRID_SIZE


# Тестуємо метод get_block_at для різних координат
@pytest.mark.parametrize("x, y, expected", [
    (0, 0, True),  # Крайній лівий верхній блок (очікується True)
    (1, 1, True),  # Блок всередині поля (очікується True)
    (8, 8, True),  # Крайній правий нижній блок (очікується True)
    (9, 9, False),  # Координати поза полем (очікується False)
    (-1, -1, False),  # Від'ємні координати (очікується False)
])
def test_get_block_at(block_manager, x, y, expected):
    block = block_manager.get_block_at(x, y)
    if expected:
        assert block is not None  # Перевірка, що блок існує
        assert block.x == x  # Перевірка координати x
        assert block.y == y  # Перевірка координати y
    else:
        assert block is None  # Перевірка, що блок не існує


@pytest.mark.parametrize("x, y, expected_positions, expected_length", [
    (4, 4, [(3, 4), (5, 4), (4, 3), (4, 5)], 4),  # Тест для центральної позиції
    (0, 0, [(1, 0), (0, 1)], 2),                   # Тест для кутової позиції у верхньому лівому куті
    (GRID_SIZE - 1, GRID_SIZE - 1, [(GRID_SIZE - 2, GRID_SIZE - 1), (GRID_SIZE - 1, GRID_SIZE - 2)], 2)  # Тест для кутової позиції у нижньому правому куті
])
def test_get_cross_path(block_manager, x, y, expected_positions, expected_length):
    # Отримуємо блок за заданими координатами.
    block = block_manager.get_block_at(x, y)
    # Отримуємо хрестоподібні блоки навколо заданого блоку.
    cross_blocks = block_manager.get_cross_path(block)
    
    # Створюємо список позицій отриманих блоків для порівняння з очікуваними.
    cross_positions = [(b.x, b.y) for b in cross_blocks]
    
    # Перевіряємо, що кількість отриманих блоків відповідає очікуваній.
    assert len(cross_blocks) == expected_length
    # Переконуємося, що всі отримані позиції відповідають очікуваним.
    assert all(pos in expected_positions for pos in cross_positions)


# Тестуємо метод get_adjacent_blocks для різних координат
@pytest.mark.parametrize("x, y, expected_len", [
    (0, 0, 3),  # Крайній лівий верхній блок (очікується 3 сусіди)
    (1, 1, 8),  # Блок всередині поля (очікується 8 сусідів)
    (8, 8, 3),  # Крайній правий нижній блок (очікується 3 сусіди)
    (0, 8, 3),  # Крайній лівий нижній блок (очікується 3 сусіди)
    (8, 0, 3),  # Крайній правий верхній блок (очікується 3 сусіди)
])
def test_get_adjacent_blocks(block_manager, x, y, expected_len):
    block = block_manager.get_block_at(x, y)
    adjacent_blocks = block_manager.get_adjacent_blocks(block)
    assert len(adjacent_blocks) == expected_len  # Перевірка кількості сусідніх блоків


# Тестуємо ініціалізацію блоків
def test_initialize_blocks(block_manager):
    assert len(block_manager.blocks) == 81  # Перевірка загальної кількості блоків
    for block in block_manager.blocks:
        assert isinstance(block, Block)  # Перевірка, що всі елементи є екземплярами класу Block


# Тестуємо розміщення бомб
def test_place_bombs(block_manager):
    block_manager.place_bombs()
    bomb_count = sum(1 for block in block_manager.blocks if block.is_bomb)
    assert bomb_count == 10  # Перевірка, що розміщено 10 бомб


# Тестуємо метод find_path
def test_find_path(block_manager):
    block = block_manager.get_block_at(0, 0)
    block_manager.find_path(block)
    assert block in block_manager.checked_blocks  # Перевірка, що блок додано до списку перевірених блоків


# Тестуємо метод get_warning_count
def test_get_warning_count(block_manager):
    block_manager.place_bombs()
    for block in block_manager.blocks:
        if block.is_bomb:
            continue  # Пропускаємо блоки з бомбами
        warning_count = block_manager.get_warning_count(block)
        adjacent_bomb_count = sum(1 for neighbor in block_manager.get_adjacent_blocks(block) if neighbor.is_bomb)
        assert warning_count == adjacent_bomb_count  # Перевірка, що кількість попереджень відповідає кількості сусідніх бомб
