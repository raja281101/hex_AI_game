# Hex Game with AI - Monte Carlo Tree Search

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An implementation of the classic Hex board game featuring an AI opponent powered by Monte Carlo Tree Search (MCTS). This project was developed as part of an AI Lab course.

## 🎮 About Hex

Hex is a two-player abstract strategy game played on an 11×11 hexagonal grid. Players take turns placing stones of their color, with the goal of creating an unbroken chain connecting opposite sides of the board:
- **Red Player (Human)**: Connects top edge to bottom edge
- **Blue Player (AI)**: Connects left edge to right edge

## ✨ Features

- **Intelligent AI**: Monte Carlo Tree Search algorithm with configurable difficulty
- **6 Difficulty Levels**: From Beginner to Unbeatable
- **Clean GUI**: Intuitive interface built with Pygame
- **Non-blocking AI**: Responsive gameplay with threaded AI calculations
- **Game Controls**: Easy keyboard shortcuts for restart and menu navigation

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/hex-game-ai.git
cd hex-game-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## 🎯 How to Play

1. **Select Difficulty**: Choose from 6 AI difficulty levels
2. **Make Your Move**: Click on any empty hexagon to place your piece (red)
3. **AI Response**: The AI will calculate and place its piece (blue)
4. **Win Condition**: Create an unbroken chain connecting your edges

### Controls
- **Mouse Click**: Place piece
- **R**: Restart current game
- **M**: Return to menu
- **ESC**: Exit game

## 🧠 AI Difficulty Levels

| Difficulty | Simulations | Think Time | Description |
|------------|-------------|------------|-------------|
| Beginner   | 10         | 0.5s       | Perfect for learning |
| Easy       | 50         | 1.0s       | Casual gameplay |
| Medium     | 100        | 1.5s       | Balanced challenge |
| Hard       | 200        | 2.0s       | Experienced players |
| Expert     | 400        | 3.0s       | Very challenging |
| Unbeatable | 800        | 4.0s       | Nearly impossible |

## 📁 Project Structure

```
hex-game-ai/
├── main.py              # Entry point
├── config.py            # Game configuration
├── hex_game.py          # Core game logic
├── ai.py                # MCTS AI implementation
├── gui.py               # Graphical interface
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## 🛠️ Technical Implementation

### Core Components
- **Game Engine**: Implements Hex rules and win detection using DFS
- **AI System**: Monte Carlo Tree Search with UCT selection
- **Graphics**: Pygame-based rendering with responsive design
- **Threading**: Non-blocking AI calculations for smooth gameplay

### Key Algorithms
- **Monte Carlo Tree Search (MCTS)**: For AI decision making
- **Depth-First Search (DFS)**: For win condition checking
- **UCT (Upper Confidence Bound)**: For node selection in MCTS

## 📊 Performance Optimization

- Threaded AI calculations prevent UI freezing
- Efficient NumPy arrays for board representation
- Optimized hex coordinate calculations
- Time-limited AI thinking for consistent performance

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Authors:
K21-4790 Sohaib Ali
K22-4785 Shaiq Hussain
K22-4782 Mavia Mehmood

## 🙏 Acknowledgments

- Hex game inventors: Piet Hein and John Nash
- Monte Carlo Tree Search research community
- Pygame development team

---

**Project Status**: ✅ Complete

Feel free to star ⭐ this repository if you find it helpful!
