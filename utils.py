# utils.py
"""Utility functions for the Hex game."""

import numpy as np
from typing import List, Tuple
from hex_game import HexGame, Player

def save_game(game: HexGame, filename: str):
    """Save game state to file."""
    data = {
        'board': game.board.tolist(),
        'current_player': game.current_player.value,
        'winner': game.winner.value if game.winner else None,
        'move_history': game.move_history,
        'board_size': game.board_size
    }
    
    import json
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_game(filename: str) -> HexGame:
    """Load game state from file."""
    import json
    with open(filename, 'r') as f:
        data = json.load(f)
    
    game = HexGame(data['board_size'])
    game.board = np.array(data['board'])
    game.current_player = Player(data['current_player'])
    game.winner = Player(data['winner']) if data['winner'] else None
    game.move_history = data['move_history']
    
    return game

def generate_training_data(num_games: int = 100) -> List[Tuple[np.ndarray, int]]:
    """Generate training data from self-play games."""
    from ai import HexAI
    
    training_data = []
    ai = HexAI(simulations=500)
    
    for game_num in range(num_games):
        game = HexGame()
        states_and_outcomes = []
        
        while not game.is_game_over():
            # Store current state
            state = game.board.copy()
            current_player = game.current_player
            
            # Make AI move
            move = ai.get_best_move(game)
            game.make_move(move[0], move[1])
            
            states_and_outcomes.append((state, current_player))
        
        # Update outcomes based on winner
        winner = game.winner
        for state, player in states_and_outcomes:
            outcome = 1 if player == winner else -1
            training_data.append((state, outcome))
        
        print(f"Generated game {game_num + 1}/{num_games}")
    
    return training_data
