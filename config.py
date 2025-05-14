# config.py
"""Configuration for the Hex game."""

class Config:
    # Board settings
    BOARD_SIZE = 11
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 900
    
    # Colors
    BACKGROUND_COLOR = (50, 100, 200)      # Blue background
    BOARD_COLOR = (220, 220, 220)          # Light gray for hexagons
    GRID_COLOR = (0, 0, 0)                 # Black borders
    PLAYER1_COLOR = (200, 0, 0)            # Red (Human)
    PLAYER2_COLOR = (0, 0, 200)            # Blue (AI)
    EDGE_RED = (200, 0, 0)                 # Red for top/bottom edges
    EDGE_BLUE = (0, 0, 200)                # Blue for left/right edges
    TEXT_COLOR = (0, 0, 0)                 # Black text
    WHITE = (255, 255, 255)                # White
    BLACK = (0, 0, 0)                      # Black
    GREEN = (0, 200, 0)                    # Green for pawn
    GRAY = (128, 128, 128)                 # Gray
    
    # Layout settings
    HEX_RADIUS = 28
    BOARD_OFFSET_X = 400
    BOARD_OFFSET_Y = 120
    
    # Panel settings
    PANEL_WIDTH = 250
    PANEL_X = 50
    PANEL_Y = 250
    PANEL_HEIGHT = 350
    
    # Font settings
    LABEL_FONT_SIZE = 20
    TITLE_FONT_SIZE = 32
    
    # Difficulty settings
    DIFFICULTY_LEVELS = {
        "Beginner": {"simulations": 10, "time_limit": 0.5},
        "Easy": {"simulations": 50, "time_limit": 1.0},
        "Medium": {"simulations": 100, "time_limit": 1.5},
        "Hard": {"simulations": 200, "time_limit": 2.0},
        "Expert": {"simulations": 400, "time_limit": 3.0},
        "Unbeatable": {"simulations": 800, "time_limit": 4.0}
    }