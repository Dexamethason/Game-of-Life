# Game-of-Life

To create & start using python venv:
      python -m venv venv
      source venv/bin/activate

Install specific modules with pip:
f.e.:   pip install pygame

Requirements
1. Make simulation real time
2. Add pause / resume logic
3. Add save / load logic

High-level logic
1. Create and init the simulation grid
2. Start the simulation with a tick interval of <n> seconds
3. At each tick:
  3.1. Update the grid - loop over each element of the board
  3.2. Render new generation

General approach
1. Plan & write down the general workflow
 1.1. Define Input&Output 
 1.2. Consider adding validation
2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
3. Define communication between the objects
4. List the patterns you could apply
5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
   and combine them into a complete application
6. Refine if needed

Deadline - 15th of December 2023
Mail with: 
1. short screen recording demonstrating the new features
2. Linked code
3. Short description of the changes. Which design patterns you used and how you applied them. 

## The code uses the following libraries:
- `Pygame:` Has modules designed for writing video games.

- `Numpy:` It's adding support for multi-dimensional arrays and matrices.

- `Time:` The time module used for real-time simulating.

- `Tickle:` It's used to save and load the game state.

## Classes & Methods
- `__new__(cls):` Method called when object is created. It makes sure that we have one instance of the class.

- `initialize():` Initializes the game parameters such as screen & grid dimensions, colors, buttons etc.

- `draw_button():` Draws the pause/resume button on the screen.

- `draw_save_button():` Draws the "Save" button on the screen.

- `draw_load_button():` Draws the "Load" button on the screen.

- `draw_grid():` Draws the grid on the screen.

- `next_generation():` Calculates the next gen of the Game of Life.

- `draw_cells():` Draws the living cells.

- `run():` Method running the game loop.
