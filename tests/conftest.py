import pytest
from minesweeper import initialize_blocks, blocks

@pytest.fixture
def setup_blocks():
    """Фікстура для ініціалізації блоків перед кожним тестом."""
    global blocks
    blocks.clear()
    initialize_blocks()
    yield blocks
    blocks.clear()
