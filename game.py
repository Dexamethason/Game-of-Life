import pygame
import numpy as np
import time
import pickle

class GameOfLife:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameOfLife, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.width, self.height = 1200, 900
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Grid dimensions
        self.n_cells_x, self.n_cells_y = 40, 30
        self.cell_width = self.width // self.n_cells_x
        self.cell_height = self.height // self.n_cells_y

        # Game state
        self.game_state = np.random.choice([0, 1], size=(self.n_cells_x, self.n_cells_y), p=[0.8, 0.2])

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)

        # Button dimensions
        self.button_width, self.button_height = 200, 50
        self.button_x, self.button_y = (self.width - self.button_width) // 2, self.height - self.button_height - 10
        self.save_button_x, self.save_button_y = 10, self.height - self.button_height - 10
        self.load_button_x, self.load_button_y = 990, self.height - self.button_height - 10

        # File to save/load game state
        self.save_file = "save.pkl"

        # Tick interval in seconds
        self.tick_interval = 1

        # Time of the last tick
        self.last_tick_time = time.time()

        # Flag to control pause/resume
        self.paused = False

    def draw_button(self):
        pygame.draw.rect(self.screen, self.green, (self.button_x, self.button_y, self.button_width, self.button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("PAUSE/RESUME", True, self.black)
        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2, self.button_y + self.button_height // 2))
        self.screen.blit(text, text_rect)

    def draw_save_button(self):
        pygame.draw.rect(self.screen, self.green, (self.save_button_x, self.save_button_y, self.button_width, self.button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Save", True, self.black)
        text_rect = text.get_rect(center=(self.save_button_x + self.button_width // 2, self.save_button_y + self.button_height // 2))
        self.screen.blit(text, text_rect)

    def draw_load_button(self):
        pygame.draw.rect(self.screen, self.green, (self.load_button_x, self.load_button_y, self.button_width, self.button_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Load", True, self.black)
        text_rect = text.get_rect(center=(self.load_button_x + self.button_width // 2, self.load_button_y + self.button_height // 2))
        self.screen.blit(text, text_rect)

    def draw_grid(self):
        for y in range(0, self.height, self.cell_height):
            for x in range(0, self.width, self.cell_width):
                cell = pygame.Rect(x, y, self.cell_width, self.cell_height)
                pygame.draw.rect(self.screen, self.gray, cell, 1)

    def next_generation(self):
        new_state = np.copy(self.game_state)

        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                n_neighbors = self.game_state[(x - 1) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y - 1) % self.n_cells_y] + \
                              self.game_state[(x - 1) % self.n_cells_x, (y) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y) % self.n_cells_y] + \
                              self.game_state[(x - 1) % self.n_cells_x, (y + 1) % self.n_cells_y] + \
                              self.game_state[(x) % self.n_cells_x, (y + 1) % self.n_cells_y] + \
                              self.game_state[(x + 1) % self.n_cells_x, (y + 1) % self.n_cells_y]

                if self.game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                    new_state[x, y] = 0
                elif self.game_state[x, y] == 0 and n_neighbors == 3:
                    new_state[x, y] = 1

        self.game_state = new_state

    def draw_cells(self):
        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                cell = pygame.Rect(x * self.cell_width, y * self.cell_height, self.cell_width, self.cell_height)
                if self.game_state[x, y] == 1:
                    pygame.draw.rect(self.screen, self.black, cell)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.white)
            self.draw_grid()
            self.draw_cells()
            self.draw_button()
            self.draw_save_button()
            self.draw_load_button()
            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Toggle pause/resume on button click
                    if self.button_x <= event.pos[0] <= self.button_x + self.button_width and self.button_y <= event.pos[1] <= self.button_y + self.button_height:
                        self.paused = not self.paused
                    # "Save" button
                    elif self.save_button_x <= event.pos[0] <= self.save_button_x + self.button_width and self.save_button_y <= event.pos[1] <= self.save_button_y + self.button_height:
                        with open(self.save_file, "wb") as f:
                            pickle.dump(self.game_state, f)
                    # "Load" button
                    elif self.load_button_x <= event.pos[0] <= self.load_button_x + self.button_width and self.load_button_y <= event.pos[1] <= self.load_button_y + self.button_height:
                        try:
                            with open(self.save_file, "rb") as f:
                                self.game_state = pickle.load(f)
                        except FileNotFoundError:
                            print("File not found.")
                    else:
                        x, y = event.pos[0] // self.cell_width, event.pos[1] // self.cell_height
                        self.game_state[x, y] = not self.game_state[x, y]

            # Check for tick interval and update the grid if not paused
            if not self.paused:
                current_time = time.time()
                if current_time - self.last_tick_time >= self.tick_interval:
                    self.next_generation()
                    self.last_tick_time = current_time

        # Quit Pygame
        pygame.quit()

# Create a singleton instance
game_of_life = GameOfLife()
game_of_life.run()
