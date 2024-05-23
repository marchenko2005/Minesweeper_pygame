import pytest
from minesweeper import BlockManager
from minesweeper import Block


@pytest.fixture
def block_manager():
    bm = BlockManager()
    bm.initialize_blocks()
    return bm