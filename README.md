# AI Flappy Bird

This project is an AI-powered version of the classic Flappy Bird game. The AI uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train a neural network to play the game by controlling the bird's movements.

## Features

- **AI Training**: The AI learns to play Flappy Bird using the NEAT algorithm.
- **Dynamic Gameplay**: The bird avoids pipes and interacts with the environment, including a scrolling base and background.
- **Customizable Configurations**: The NEAT algorithm parameters can be adjusted via the `config.txt` file.

## Project Structure

- `main.py`: The main Python script that runs the game and trains the AI.
- `config.txt`: Configuration file for the NEAT algorithm.
- `imgs/`: Contains all the game assets, including images for the bird, pipes, base, and background.

## Requirements

- Python 3.x
- Pygame
- NEAT-Python

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/VNamanMehta/FlappyBirdAI.git
   cd ai-flappy-bird
   ```
2. Install the required Python packages:
   ```
    pip install pygame neat-python
   ```
3. Run the game:
   ```
   python main.py
   ```
## How It Works

1 .Game Mechanics:
The bird can jump to avoid pipes.
Pipes move from right to left, and the bird must navigate through the gaps.
The base scrolls to create an endless effect.

2. AI Training:
Each bird is controlled by a neural network.
The NEAT algorithm evolves the neural networks over generations to improve their performance.
Fitness is determined by how far the bird progresses in the game.

3. Configuration:
The config.txt file defines parameters for the NEAT algorithm, such as population size, mutation rates, and fitness thresholds.

## Controls
The AI controls the bird automatically. No manual input is required.

## Customization
Modify the config.txt file to adjust the NEAT algorithm parameters.
Replace the images in the imgs/ folder to customize the game's appearance.

## Acknowledgments
The NEAT algorithm is implemented using the NEAT-Python library.
Game assets are inspired by the original Flappy Bird game.
