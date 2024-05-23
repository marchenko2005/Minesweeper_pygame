import pytest
from minesweeper import BlockManager


@pytest.fixture
def block_manager():
    bm = BlockManager()
    bm.initialize_blocks()
    return bm
