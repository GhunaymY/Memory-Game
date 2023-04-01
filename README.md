# Memory-Game
This is a Python code for a memory game built with Pygame library. In this game, the player attempts to match two identical images on a rectangular grid. The game scores the player based on the time taken to complete the game.
The code defines a Game class that manages the game state, and a Tile class that manages individual tiles on the game board. It utilizes functions to create images, create the game board, and handle mouse button up events.

The game uses eight different images and randomizes their placement on a 4x4 grid. The player clicks on a tile to reveal the image underneath it, then clicks on another tile to try and find its match. If the tiles match, they remain uncovered, otherwise, they are covered again. The game continues until all tiles are uncovered.

The score of the game is displayed on the screen, and the player can quit the game by clicking the close box.
