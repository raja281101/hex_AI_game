# ai.py
"""AI implementation using Monte Carlo Tree Search."""

import math
import random
import time
from typing import Optional, List, Tuple, Dict
from hex_game import HexGame, Player
import threading
from queue import Queue

class MCTSNode:
    def __init__(self, game_state: HexGame, parent: Optional['MCTSNode'] = None, move: Optional[Tuple[int, int]] = None):
        self.game_state = game_state.copy()
        self.parent = parent
        self.move = move
        self.children: List[MCTSNode] = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = game_state.get_valid_moves()
        random.shuffle(self.untried_moves)
    
    def uct_select_child(self, exploration_constant: float = 1.414) -> 'MCTSNode':
        """Select a child node using UCT formula."""
        return max(self.children, key=lambda child: 
                   child.wins / child.visits + exploration_constant * math.sqrt(math.log(self.visits) / child.visits))
    
    def add_child(self, move: Tuple[int, int], game_state: HexGame) -> 'MCTSNode':
        """Add a new child node."""
        child = MCTSNode(game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

class HexAI:
    def __init__(self, difficulty_settings: Dict):
        self.simulations = difficulty_settings["simulations"]
        self.time_limit = difficulty_settings["time_limit"]
        self.result_queue = Queue()
        self.current_thread = None
    
    def get_best_move_async(self, game_state: HexGame):
        """Start AI calculation in a separate thread."""
        if self.current_thread and self.current_thread.is_alive():
            return
        
        self.current_thread = threading.Thread(
            target=self._calculate_move,
            args=(game_state,)
        )
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def _calculate_move(self, game_state: HexGame):
        """Calculate the best move (runs in separate thread)."""
        try:
            move = self._mcts_search(game_state)
            self.result_queue.put(move)
        except Exception as e:
            print(f"AI error: {e}")
            # Fallback to random move
            valid_moves = game_state.get_valid_moves()
            if valid_moves:
                self.result_queue.put(random.choice(valid_moves))
            else:
                self.result_queue.put(None)
    
    def _mcts_search(self, game_state: HexGame) -> Tuple[int, int]:
        """Perform MCTS search."""
        root = MCTSNode(game_state)
        start_time = time.time()
        simulations_done = 0
        
        while simulations_done < self.simulations and time.time() - start_time < self.time_limit:
            node = root
            temp_game = game_state.copy()
            
            # Selection
            while node.untried_moves == [] and node.children != []:
                node = node.uct_select_child()
                temp_game.make_move(node.move[0], node.move[1])
            
            # Expansion
            if node.untried_moves != []:
                move = random.choice(node.untried_moves)
                temp_game.make_move(move[0], move[1])
                node = node.add_child(move, temp_game)
            
            # Simulation
            simulation_game = temp_game.copy()
            moves = 0
            while not simulation_game.is_game_over() and moves < 30:
                valid_moves = simulation_game.get_valid_moves()
                if not valid_moves:
                    break
                move = random.choice(valid_moves)
                simulation_game.make_move(move[0], move[1])
                moves += 1
            
            # Backpropagation
            winner = simulation_game.winner
            while node is not None:
                node.visits += 1
                if winner == game_state.current_player:
                    node.wins += 1
                node = node.parent
            
            simulations_done += 1
        
        # Select best move
        if root.children:
            return max(root.children, key=lambda child: child.visits).move
        else:
            valid_moves = game_state.get_valid_moves()
            return random.choice(valid_moves) if valid_moves else (0, 0)
    
    def get_move_result(self) -> Optional[Tuple[int, int]]:
        """Check if AI has completed its calculation."""
        if not self.result_queue.empty():
            return self.result_queue.get()
        return None