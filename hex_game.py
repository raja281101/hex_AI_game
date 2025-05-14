# hex_game.py
"""Core game logic for Hex."""

import numpy as np
from enum import Enum
from typing import List, Tuple, Optional

class Player(Enum):
    EMPTY = 0
    PLAYER1 = 1  # Red (Human) - connects top to bottom
    PLAYER2 = 2  # Blue (AI) - connects left to right

class HexGame:
    def __init__(self, board_size: int = 11):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = Player.PLAYER1
        self.winner = None
        self.move_history = []
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all valid neighboring cells for a hexagonal grid."""
        neighbors = []
        # Six directions for hex grid
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                neighbors.append((new_row, new_col))
        return neighbors
    
    def make_move(self, row: int, col: int) -> bool:
        """Attempt to place a piece at the given position."""
        if self.board[row, col] != Player.EMPTY.value or self.winner:
            return False
        
        self.board[row, col] = self.current_player.value
        self.move_history.append((row, col, self.current_player))
        
        # Check for winner
        if self.check_winner(self.current_player):
            self.winner = self.current_player
        else:
            # Switch player
            self.current_player = Player.PLAYER2 if self.current_player == Player.PLAYER1 else Player.PLAYER1
        
        return True
    
    def check_winner(self, player: Player) -> bool:
        """Check if the given player has won."""
        if player == Player.PLAYER1:
            # Red connects top to bottom
            for col in range(self.board_size):
                if self.board[0, col] == player.value:
                    if self._dfs_check(0, col, player, "vertical"):
                        return True
        else:  # Player.PLAYER2
            # Blue connects left to right
            for row in range(self.board_size):
                if self.board[row, 0] == player.value:
                    if self._dfs_check(row, 0, player, "horizontal"):
                        return True
        return False
    
    def _dfs_check(self, row: int, col: int, player: Player, direction: str) -> bool:
        """DFS to check if there's a path connecting opposite sides."""
        visited = set()
        stack = [(row, col)]
        
        while stack:
            curr_row, curr_col = stack.pop()
            
            if (curr_row, curr_col) in visited:
                continue
            
            visited.add((curr_row, curr_col))
            
            # Check if we've reached the opposite side
            if direction == "vertical" and curr_row == self.board_size - 1:
                return True
            elif direction == "horizontal" and curr_col == self.board_size - 1:
                return True
            
            # Add valid neighbors
            for next_row, next_col in self.get_neighbors(curr_row, curr_col):
                if (next_row, next_col) not in visited and self.board[next_row, next_col] == player.value:
                    stack.append((next_row, next_col))
        
        return False
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Get all valid moves (empty cells)."""
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row, col] == Player.EMPTY.value:
                    valid_moves.append((row, col))
        return valid_moves
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.winner is not None
    
    def copy(self):
        """Create a deep copy of the game state."""
        new_game = HexGame(self.board_size)
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.move_history = self.move_history.copy()
        return new_game