import unittest
from unittest.mock import patch
from minesweeper import BlockManager, Block, GRID_SIZE


class TestBlockManager(unittest.TestCase):
 
    def setUp(self):
        self.block_manager = BlockManager()
        self.block_manager.initialize_blocks()
    
    def test_get_cross_path(self):
        block = self.block_manager.get_block_at(4, 4)
        cross_blocks = self.block_manager.get_cross_path(block)
        
        expected_positions = [(3, 4), (5, 4), (4, 3), (4, 5)]
        cross_positions = [(b.x, b.y) for b in cross_blocks]
        
        self.assertEqual(len(cross_blocks), 4)
        self.assertTrue(all(pos in expected_positions for pos in cross_positions))
    
    def test_get_cross_path_edge(self):
        block = self.block_manager.get_block_at(0, 0)
        cross_blocks = self.block_manager.get_cross_path(block)
        
        expected_positions = [(1, 0), (0, 1)]
        cross_positions = [(b.x, b.y) for b in cross_blocks]
        
        self.assertEqual(len(cross_blocks), 2)
        self.assertTrue(all(pos in expected_positions for pos in cross_positions))
    
    def test_get_cross_path_corner(self):
        block = self.block_manager.get_block_at(GRID_SIZE - 1, GRID_SIZE - 1)
        cross_blocks = self.block_manager.get_cross_path(block)
        
        expected_positions = [(GRID_SIZE - 2, GRID_SIZE - 1), (GRID_SIZE - 1, GRID_SIZE - 2)]
        cross_positions = [(b.x, b.y) for b in cross_blocks]
        
        self.assertEqual(len(cross_blocks), 2)
        self.assertTrue(all(pos in expected_positions for pos in cross_positions))

    @patch('minesweeper.BlockManager.get_block_at')
    def test_get_cross_path_mock(self, mock_get_block_at):
        # Мокаємо повернення блоків
        mock_get_block_at.side_effect = lambda x, y: Block(x, y)
        block = Block(4, 4)
        cross_blocks = self.block_manager.get_cross_path(block)

        expected_positions = [(3, 4), (5, 4), (4, 3), (4, 5)]
        cross_positions = [(b.x, b.y) for b in cross_blocks]
        
        self.assertEqual(len(cross_blocks), 4)
        self.assertTrue(all(pos in expected_positions for pos in cross_positions))
