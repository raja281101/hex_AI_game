# gui.py
"""GUI implementation for the Hex game."""

import pygame
import math
from typing import Tuple, Optional, List
from hex_game import HexGame, Player
from ai import HexAI
from config import Config

class DifficultyMenu:
    def __init__(self, config: Config):
        self.config = config
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.desc_font = pygame.font.Font(None, 24)
        
        # Button settings
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 80
        self.selected_difficulty = None
    
    def draw(self, screen: pygame.Surface):
        """Draw the difficulty selection menu."""
        screen.fill(self.config.BACKGROUND_COLOR)
        
        # Title
        title = self.title_font.render("HEX", True, self.config.WHITE)
        title_rect = title.get_rect(center=(self.config.WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font.render("Select Difficulty", True, self.config.WHITE)
        subtitle_rect = subtitle.get_rect(center=(self.config.WINDOW_WIDTH // 2, 180))
        screen.blit(subtitle, subtitle_rect)
        
        # Difficulty buttons
        difficulties = list(self.config.DIFFICULTY_LEVELS.keys())
        start_y = 250
        
        for i, difficulty in enumerate(difficulties):
            # Button
            button_x = (self.config.WINDOW_WIDTH - self.button_width) // 2
            button_y = start_y + i * self.button_spacing
            
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            pygame.draw.rect(screen, self.config.WHITE, button_rect)
            pygame.draw.rect(screen, self.config.TEXT_COLOR, button_rect, 2)
            
            # Button text
            text = self.font.render(difficulty, True, self.config.TEXT_COLOR)
            text_rect = text.get_rect(center=(button_x + self.button_width // 2, button_y + self.button_height // 2))
            screen.blit(text, text_rect)
            
            # Description (below button)
            descriptions = {
                "Beginner": "Perfect for learning",
                "Easy": "Casual gameplay",
                "Medium": "Balanced challenge",
                "Hard": "For experienced players",
                "Expert": "Very challenging",
                "Unbeatable": "Nearly impossible"
            }
            
            desc_text = self.desc_font.render(descriptions[difficulty], True, self.config.WHITE)
            desc_rect = desc_text.get_rect(center=(self.config.WINDOW_WIDTH // 2, button_y + self.button_height + 20))
            screen.blit(desc_text, desc_rect)
    
    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """Handle mouse click and return selected difficulty."""
        difficulties = list(self.config.DIFFICULTY_LEVELS.keys())
        start_y = 250
        
        for i, difficulty in enumerate(difficulties):
            button_x = (self.config.WINDOW_WIDTH - self.button_width) // 2
            button_y = start_y + i * self.button_spacing
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            
            if button_rect.collidepoint(pos):
                return difficulty
        return None

class HexGUI:
    def __init__(self):
        pygame.init()
        self.config = Config()
        
        self.screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT))
        pygame.display.set_caption("Hex Game - AI Lab Project")
        
        # Game state
        self.show_menu = True
        self.difficulty_menu = DifficultyMenu(self.config)
        self.game = None
        self.ai = None
        self.difficulty = None
        self.ai_calculating = False
        
        # Fonts
        self.label_font = pygame.font.Font(None, self.config.LABEL_FONT_SIZE)
        self.bold_font = pygame.font.Font(None, self.config.TITLE_FONT_SIZE)
        self.bold_font.set_bold(True)
    
    def start_game(self, difficulty: str):
        """Start a new game with selected difficulty."""
        self.difficulty = difficulty
        self.show_menu = False
        self.game = HexGame()
        
        # Initialize AI
        difficulty_settings = self.config.DIFFICULTY_LEVELS[difficulty]
        self.ai = HexAI(difficulty_settings)
        
        # Calculate hex centers
        self.hex_centers = self._calculate_hex_centers()
    
    def _calculate_hex_centers(self) -> List[List[Tuple[float, float]]]:
        """Calculate center coordinates for each hexagon."""
        centers = []
        radius = self.config.HEX_RADIUS
        
        # Hexagon dimensions
        hex_width = radius * 2
        hex_height = radius * math.sqrt(3)
        
        # Spacing between hexagons
        horizontal_spacing = radius * 1.5
        vertical_spacing = hex_height
        
        for row in range(self.game.board_size):
            row_centers = []
            for col in range(self.game.board_size):
                # Calculate position
                x = self.config.BOARD_OFFSET_X + col * horizontal_spacing
                y = self.config.BOARD_OFFSET_Y + row * vertical_spacing
                
                # Offset each row to create the diagonal pattern
                x += row * radius * 0.75
                
                row_centers.append((x, y))
            centers.append(row_centers)
        
        return centers
    
    def _draw_hexagon(self, center: Tuple[float, float], color: Tuple[int, int, int]):
        """Draw a hexagon with black border."""
        points = []
        # Flat-top hexagon
        for i in range(6):
            angle = math.pi / 3 * i
            x = center[0] + self.config.HEX_RADIUS * math.cos(angle)
            y = center[1] + self.config.HEX_RADIUS * math.sin(angle)
            points.append((x, y))
        
        # Fill
        pygame.draw.polygon(self.screen, color, points)
        # Border
        pygame.draw.polygon(self.screen, self.config.GRID_COLOR, points, 2)
    
    def _draw_board(self):
        """Draw the hexagonal board."""
        # Draw hexagons
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                center = self.hex_centers[row][col]
                self._draw_hexagon(center, self.config.BOARD_COLOR)
        
        # Draw colored edges
        self._draw_colored_edges()
        
        # Draw labels
        self._draw_labels()
        
        # Draw pieces
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.game.board[row, col] != Player.EMPTY.value:
                    center = self.hex_centers[row][col]
                    color = self.config.PLAYER1_COLOR if self.game.board[row, col] == Player.PLAYER1.value else self.config.PLAYER2_COLOR
                    pygame.draw.circle(self.screen, color, center, self.config.HEX_RADIUS * 0.6)
    
    def _draw_colored_edges(self):
        """Draw red and blue colored borders."""
        margin = 30
        edge_width = 40
        
        # Get board boundaries
        top_left = self.hex_centers[0][0]
        top_right = self.hex_centers[0][-1]
        bottom_left = self.hex_centers[-1][0]
        bottom_right = self.hex_centers[-1][-1]
        
        # Adjust for hexagon shape and diagonal offset
        offset = self.config.HEX_RADIUS
        diagonal_offset = (self.game.board_size - 1) * self.config.HEX_RADIUS * 0.75
        
        # Top edge (red)
        top_points = [
            (top_left[0] - offset - margin, top_left[1] - offset - margin),
            (top_right[0] + offset + margin + diagonal_offset, top_left[1] - offset - margin),
            (top_right[0] + offset + margin + diagonal_offset, top_left[1] - offset - margin + edge_width),
            (top_left[0] - offset - margin, top_left[1] - offset - margin + edge_width)
        ]
        pygame.draw.polygon(self.screen, self.config.EDGE_RED, top_points)
        
        # Bottom edge (red)
        bottom_points = [
            (bottom_left[0] - offset - margin, bottom_left[1] + offset + margin - edge_width),
            (bottom_right[0] + offset + margin, bottom_left[1] + offset + margin - edge_width),
            (bottom_right[0] + offset + margin, bottom_left[1] + offset + margin),
            (bottom_left[0] - offset - margin, bottom_left[1] + offset + margin)
        ]
        pygame.draw.polygon(self.screen, self.config.EDGE_RED, bottom_points)
        
        # Left edge (blue)
        left_points = [
            (top_left[0] - offset - margin, top_left[1] - offset - margin),
            (top_left[0] - offset - margin + edge_width, top_left[1] - offset - margin),
            (bottom_left[0] - offset - margin + edge_width, bottom_left[1] + offset + margin),
            (bottom_left[0] - offset - margin, bottom_left[1] + offset + margin)
        ]
        pygame.draw.polygon(self.screen, self.config.EDGE_BLUE, left_points)
        
        # Right edge (blue)
        right_points = [
            (top_right[0] + offset + margin - edge_width + diagonal_offset, top_right[1] - offset - margin),
            (top_right[0] + offset + margin + diagonal_offset, top_right[1] - offset - margin),
            (bottom_right[0] + offset + margin, bottom_right[1] + offset + margin),
            (bottom_right[0] + offset + margin - edge_width, bottom_right[1] + offset + margin)
        ]
        pygame.draw.polygon(self.screen, self.config.EDGE_BLUE, right_points)
    
    def _draw_labels(self):
        """Draw row and column labels."""
        # Column labels (A-K)
        for col in range(self.game.board_size):
            label = chr(65 + col)  # A, B, C, ...
            
            # Top label
            top_pos = self.hex_centers[0][col]
            text = self.label_font.render(label, True, self.config.WHITE)
            text_rect = text.get_rect(center=(top_pos[0], top_pos[1] - self.config.HEX_RADIUS - 50))
            self.screen.blit(text, text_rect)
            
            # Bottom label
            bottom_pos = self.hex_centers[-1][col]
            text_rect = text.get_rect(center=(bottom_pos[0], bottom_pos[1] + self.config.HEX_RADIUS + 50))
            self.screen.blit(text, text_rect)
        
        # Row labels (1-11)
        for row in range(self.game.board_size):
            label = str(row + 1)
            
            # Left label
            left_pos = self.hex_centers[row][0]
            text = self.label_font.render(label, True, self.config.WHITE)
            text_rect = text.get_rect(center=(left_pos[0] - self.config.HEX_RADIUS - 60, left_pos[1]))
            self.screen.blit(text, text_rect)
            
            # Right label
            right_pos = self.hex_centers[row][-1]
            text_rect = text.get_rect(center=(right_pos[0] + self.config.HEX_RADIUS + 60, right_pos[1]))
            self.screen.blit(text, text_rect)
    
    def _draw_player_indicator(self):
        """Draw the player turn indicator panel."""
        # Background box
        box_x = self.config.PANEL_X
        box_y = self.config.PANEL_Y
        box_width = self.config.PANEL_WIDTH
        box_height = self.config.PANEL_HEIGHT
        
        pygame.draw.rect(self.screen, self.config.WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, self.config.TEXT_COLOR, (box_x, box_y, box_width, box_height), 2)
        
        # Human's Turn / Computer's Turn text
        text = "Human's Turn" if self.game.current_player == Player.PLAYER1 else "Computer's Turn"
        text_surface = self.bold_font.render(text, True, self.config.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(box_x + box_width // 2, box_y + 40))
        self.screen.blit(text_surface, text_rect)
        
        # Green pawn
        pawn_y = box_y + 100
        pygame.draw.circle(self.screen, self.config.GREEN, (box_x + box_width // 2, pawn_y), 25)
        
        # Player circles
        circle_y = box_y + 180
        red_x = box_x + 70     # Human is red
        blue_x = box_x + 180   # AI is blue
        
        # Red circle (human)
        pygame.draw.circle(self.screen, self.config.PLAYER1_COLOR, (red_x, circle_y), 25)
        if self.game.current_player == Player.PLAYER1:
            pygame.draw.rect(self.screen, self.config.BLACK, (red_x - 35, circle_y - 35, 70, 70), 3)
        
        # Blue circle (AI)
        pygame.draw.circle(self.screen, self.config.PLAYER2_COLOR, (blue_x, circle_y), 25)
        if self.game.current_player == Player.PLAYER2:
            pygame.draw.rect(self.screen, self.config.BLACK, (blue_x - 35, circle_y - 35, 70, 70), 3)
        
        # Computer icon
        comp_y = box_y + 260
        comp_rect = pygame.Rect(box_x + box_width // 2 - 40, comp_y, 80, 50)
        pygame.draw.rect(self.screen, self.config.GRAY, comp_rect)
        pygame.draw.rect(self.screen, self.config.TEXT_COLOR, comp_rect, 2)
        screen_rect = pygame.Rect(box_x + box_width // 2 - 35, comp_y + 5, 70, 35)
        pygame.draw.rect(self.screen, self.config.TEXT_COLOR, screen_rect)
        stand_rect = pygame.Rect(box_x + box_width // 2 - 10, comp_y + 50, 20, 10)
        pygame.draw.rect(self.screen, self.config.GRAY, stand_rect)
        
        # AI thinking indicator
        if self.ai_calculating:
            thinking_text = "Thinking..."
            thinking_surface = self.label_font.render(thinking_text, True, self.config.TEXT_COLOR)
            thinking_rect = thinking_surface.get_rect(center=(box_x + box_width // 2, box_y + box_height - 25))
            self.screen.blit(thinking_surface, thinking_rect)
    
    def _get_hex_from_pixel(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to hex coordinates."""
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                center = self.hex_centers[row][col]
                dx = pos[0] - center[0]
                dy = pos[1] - center[1]
                distance = math.sqrt(dx * dx + dy * dy)
                
                if distance <= self.config.HEX_RADIUS * 0.9:
                    return (row, col)
        return None
    
    def _check_ai_move(self):
        """Check if AI has completed its calculation."""
        if self.ai_calculating:
            move = self.ai.get_move_result()
            if move:
                self.game.make_move(move[0], move[1])
                self.ai_calculating = False
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse clicks."""
        if self.show_menu:
            selected = self.difficulty_menu.handle_click(pos)
            if selected:
                self.start_game(selected)
        else:
            if self.game.winner or self.ai_calculating:
                return
            
            hex_pos = self._get_hex_from_pixel(pos)
            if hex_pos and self.game.current_player == Player.PLAYER1:
                row, col = hex_pos
                if self.game.make_move(row, col):
                    # Start AI calculation
                    if not self.game.winner:
                        self.ai_calculating = True
                        self.ai.get_best_move_async(self.game)
    
    def draw(self):
        """Draw the current state."""
        self.screen.fill(self.config.BACKGROUND_COLOR)
        
        if self.show_menu:
            self.difficulty_menu.draw(self.screen)
        else:
            self._draw_board()
            self._draw_player_indicator()
            
            # Draw winner message
            if self.game.winner:
                winner_text = f"{'Human' if self.game.winner == Player.PLAYER1 else 'Computer'} Wins!"
                font = pygame.font.Font(None, 72)
                text = font.render(winner_text, True, self.config.WHITE)
                text_rect = text.get_rect(center=(self.config.WINDOW_WIDTH // 2, 50))
                self.screen.blit(text, text_rect)
                
                # Restart instruction
                inst_text = "Press R to restart or M for menu"
                inst_font = pygame.font.Font(None, 36)
                inst_surface = inst_font.render(inst_text, True, self.config.WHITE)
                inst_rect = inst_surface.get_rect(center=(self.config.WINDOW_WIDTH // 2, 120))
                self.screen.blit(inst_surface, inst_rect)
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game:
                        # Restart
                        self.start_game(self.difficulty)
                    elif event.key == pygame.K_m:
                        # Menu
                        self.show_menu = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Check for AI move completion
            if self.game and not self.show_menu:
                self._check_ai_move()
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()