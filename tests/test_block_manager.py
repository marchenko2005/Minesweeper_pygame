import pytest
from minesweeper import Block


@pytest.mark.parametrize("x, y, expected", [
    (0, 0, True),
    (1, 1, True),
    (8, 8, True),
    (9, 9, False),
    (-1, -1, False),
])
def test_get_block_at(block_manager, x, y, expected):
    block = block_manager.get_block_at(x, y)
    if expected:
        assert block is not None
        assert block.x == x
        assert block.y == y
    else:
        assert block is None


@pytest.mark.parametrize("x, y, expected_len", [
    (0, 0, 3),
    (1, 1, 8),
    (8, 8, 3),
    (0, 8, 3),
    (8, 0, 3),
])
def test_get_adjacent_blocks(block_manager, x, y, expected_len):
    block = block_manager.get_block_at(x, y)
    adjacent_blocks = block_manager.get_adjacent_blocks(block)
    assert len(adjacent_blocks) == expected_len


def test_initialize_blocks(block_manager):
    assert len(block_manager.blocks) == 81
    for block in block_manager.blocks:
        assert isinstance(block, Block)


def test_place_bombs(block_manager):
    block_manager.place_bombs()
    bomb_count = sum(1 for block in block_manager.blocks if block.is_bomb)
    assert bomb_count == 10


def test_find_path(block_manager):
    block = block_manager.get_block_at(0, 0)
    block_manager.find_path(block)
    assert block in block_manager.checked_blocks


def test_get_warning_count(block_manager):
    block_manager.place_bombs()
    for block in block_manager.blocks:
        if block.is_bomb:
            continue
        warning_count = block_manager.get_warning_count(block)
        adjacent_bomb_count = sum(1 for neighbor in block_manager.get_adjacent_blocks(block) if neighbor.is_bomb)
        assert warning_count == adjacent_bomb_count
