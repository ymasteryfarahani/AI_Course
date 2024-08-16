# water sort! Color sorting game in Python
import pygame
import random
import copy
from ai_solution import GameSolution

# Constants for the game window
WIDTH = 850
HEIGHT = 600
fps = 60

# Color choices available for the game
color_choices = ['red', 'light blue', 'dark green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray',
                 'cyan', 'magenta', 'lime', 'olive', 'navy', 'gold', 'indigo']


class SpinBox:
    """A UI element for a SpinBox widget.

        Attributes:
            label (str): The label text displayed next to the SpinBox.
            x (int): The X-coordinate of the SpinBox.
            y (int): The Y-coordinate of the SpinBox.
            value (int): The current value of the SpinBox.
            min_value (int): The minimum allowed value.
            max_value (int): The maximum allowed value.
            font (pygame.Font): The font used for text rendering.
            increment_button_rect (pygame.Rect): The rectangle for the increment button.
            decrement_button_rect (pygame.Rect): The rectangle for the decrement button.
    """
    def __init__(self, x, y, label, initial_value, min_value, max_value):
        # Constructor initializes SpinBox attributes
        self.label = label
        self.x = x
        self.y = y
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.font = pygame.font.SysFont("Arial", 24)
        self.increment_button_rect = pygame.Rect(x + 30, y - 3, 20, 15)
        self.decrement_button_rect = pygame.Rect(x + 50, y - 3, 20, 15)

    def draw(self, display):
        """Draws the SpinBox widget on the display."""
        lbl_txt = pygame.font.SysFont("Arial", 20)
        label_text = lbl_txt.render(f"{self.label}:", True, 'teal')
        value_text = lbl_txt.render(f"{self.value}", True, 'teal')
        display.blit(label_text, (self.x - 50, self.y - 7))
        display.blit(value_text, (self.x - 48 + label_text.get_width(), self.y - 7))
        pygame.draw.rect(display, 'white', self.increment_button_rect, 2)
        pygame.draw.rect(display, 'white', self.decrement_button_rect, 2)

        # Render the increment and decrement signs
        increment_sign = self.font.render("+", True, 'green')
        decrement_sign = self.font.render("-", True, 'red')
        display.blit(increment_sign, (self.increment_button_rect.x + 5, self.increment_button_rect.y - 7))
        display.blit(decrement_sign, (self.decrement_button_rect.x + 7, self.decrement_button_rect.y - 9))

        pygame.draw.rect(display, 'teal', self.increment_button_rect, 2)
        pygame.draw.rect(display, 'teal', self.decrement_button_rect, 2)

    def update(self, evt):
        """Updates the SpinBox based on user input event.
                Args:
                    evt (pygame.event.Event): The user input event.
        """
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if self.increment_button_rect.collidepoint(evt.pos):
                self.value = min(self.value + 1, self.max_value)
            elif self.decrement_button_rect.collidepoint(evt.pos):
                self.value = max(self.value - 1, self.min_value)


class Button:
    """A UI element for a Button widget.

        Attributes:
            rect (pygame.Rect): The rectangle defining the button's position and size.
            text (str): The text displayed on the button.
            color (tuple): The color of the button.
            font (pygame.Font): The font used for text rendering.
    """
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, display):
        """Draws the Button widget on the display.
                Args:
                    display: The pygame display surface.
        """
        pygame.draw.rect(display, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        display.blit(text_surface, text_rect)


class Game:
    """The main class for the Water Sort game.
        This class manages the game's logic, display, and user interactions.
        Attributes:
            clock (pygame.time.Clock): The game clock.
            font (pygame.Font): The font used for text rendering.
            screen (pygame.Surface): The game window surface.
            tubes (int): The total number of tubes in the game.
            NColorInTube (int): The maximum number of colors in a single tube.
            NEmptyTubes (int): The number of initially empty tubes.
            NColor (int): The number of unique colors available in the game.
            color_count (int): The current number of colors in the game.
            empty_tubes_count (int): The current number of empty tubes in the game.
            colors_in_tube_count (int): The current number of colors in each tube.
            new_game (bool): True if a new game is started.
            run (bool): True while the game is running.
            tube_colors (list): The colors in each tube.
            tube_rects (list): Rectangles representing each tube for rendering.
            game_state_history (list): A history of game states for undo functionality.
            selected (bool): True if a tube is selected for moving colors.
            win (bool): True if the player has won the game.
            move_count (int): The number of moves made by the player.
            selected_tube (int): The index of the currently selected tube.
            destination_tube (int): The index of the destination tube for moving colors.
            undo_button (Button): The "Undo" button.
            new_board_button (Button): The "New Game" button.
            solve_game_button (Button): The "Solve" button.
            optimal_solve_button (Button): The "Opt. Solve" button.
            color_spinner (SpinBox): The SpinBox for selecting the number of colors.
            empty_tubes_spinner (SpinBox): The SpinBox for selecting the number of empty tubes.
            colors_in_tube_spinner (SpinBox): The SpinBox for selecting the number of colors in each tube.
    """
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 27)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Water Sort!")
        self.tubes = 0
        self.NColorInTube = 2
        self.NEmptyTubes = 1
        self.NColor = 3
        self.color_count = self.NColor
        self.empty_tubes_count = self.NEmptyTubes
        self.colors_in_tube_count = self.NColorInTube
        self.new_game = True
        self.run = True
        self.tube_colors = []
        self.tube_rects = []
        self.game_state_history = []
        self.initial_colors = []
        self.selected = False
        self.win = False
        self.move_count = 0
        self.move_text = ""
        self.selected_tube = 100
        self.destination_tube = 100
        self.undo_button = Button(15, 550, 100, 30, "Undo", (33, 104, 105))
        self.new_board_button = Button(125, 550, 100, 30, "New Game", (33, 104, 105))
        self.solve_game_button = Button(235, 550, 50, 30, "Solve", (33, 104, 105))
        self.optimal_solve_button = Button(295, 550, 90, 30, "Opt. Solve", (33, 104, 105))
        self.reset_button = Button(750, 12, 70, 30, "Reset", (33, 104, 105))
        self.color_spinner = SpinBox(440, 560, "NColor", self.color_count, 2, 15)
        self.empty_tubes_spinner = SpinBox(590, 560, "ETube", self.empty_tubes_count, 1, 3)
        self.colors_in_tube_spinner = SpinBox(740, 560, "CTube", self.colors_in_tube_count, 2, 20)

    def generate_start(self):
        """Generate the initial configuration of tubes with colors.
                Returns:
                    Tuple[int, List[List[int]]]: A tuple containing the total number of tubes
                    and a list of lists representing the colors in each tube.
        """
        global tubes_number, tubes_colors
        check_win = True
        while check_win:
            tubes_number = self.NEmptyTubes + self.NColor
            tubes_colors = []
            available_colors = []
            for i in range(tubes_number):
                tubes_colors.append([])
                if i < tubes_number - self.NEmptyTubes:
                    for j in range(self.NColorInTube):
                        available_colors.append(i)
            for i in range(tubes_number - self.NEmptyTubes):
                for j in range(self.NColorInTube):
                    color = random.choice(available_colors)
                    tubes_colors[i].append(color)
                    available_colors.remove(color)
            check_win = self.check_victory(tubes_colors)

        print(tubes_colors, tubes_number)
        return tubes_number, tubes_colors

    def draw_tubes(self, tubes_num, tube_cols):
        """Draw the tubes and their colors on the game screen.
                Args:
                    tubes_num (int): The total number of tubes in the game.
                    tube_cols (List[List[int]]): A list of lists representing the colors in each tube.

                Returns:
                    List[pygame.Rect]: A list of pygame.Rect objects representing the rectangles
                    of the drawn tubes for user interaction.
        """
        tube_boxes = []
        if tubes_num % 2 == 0:
            tubes_per_row = tubes_num // 2
            offset = False
        else:
            tubes_per_row = tubes_num // 2 + 1
            offset = True
        spacing = WIDTH // tubes_per_row
        color_height = 200 // self.NColorInTube
        for k in range(tubes_per_row):
            for j in range(len(tube_cols[k])):
                pygame.draw.rect(self.screen, color_choices[tube_cols[k][j]],
                                 (k * spacing + spacing // 4, 250 - (color_height * (j + 1))
                                  , 65, color_height), 0, 5)
            box = pygame.draw.rect(self.screen, 'teal', [spacing // 4 + spacing * k, 50, 65, 200], 3, 5)
            if k == self.selected_tube:
                pygame.draw.rect(self.screen, 'white', [spacing // 4 + spacing * k, 50, 65, 200], 3, 5)
            tube_boxes.append(box)
        if offset:
            for k in range(tubes_per_row - 1):
                for j in range(len(tube_cols[k + tubes_per_row])):
                    pygame.draw.rect(self.screen, color_choices[tube_cols[k + tubes_per_row][j]],
                                     (k * spacing + spacing // 4,
                                      500 - (color_height * (j + 1))
                                      , 65, color_height), 0, 5)
                box = pygame.draw.rect(self.screen, 'teal', [spacing // 4 + spacing * k, 300, 65, 200], 3, 5)
                if self.selected_tube == k + tubes_per_row:
                    pygame.draw.rect(self.screen, 'white', [spacing // 4 + spacing * k, 300, 65, 200], 3, 5)
                tube_boxes.append(box)
        else:
            for k in range(tubes_per_row):
                for j in range(len(tube_cols[k + tubes_per_row])):
                    pygame.draw.rect(self.screen, color_choices[tube_cols[k + tubes_per_row][j]],
                                     (k * spacing + spacing // 4,
                                      500 - (color_height * (j + 1))
                                      , 65, color_height), 0, 5)
                box = pygame.draw.rect(self.screen, 'teal', [spacing // 4 + spacing * k, 300, 65, 200], 3, 5)
                if self.selected_tube == k + tubes_per_row:
                    pygame.draw.rect(self.screen, 'white', [spacing // 4 + spacing * k, 300, 65, 200], 3, 5)
                tube_boxes.append(box)
        return tube_boxes

    def move_logic(self, tube_cols, sel_tube, dest_tube):
        """Handle the logic for moving colors between tubes.
                Args:
                    tube_cols (List[List[int]]): A list of lists representing the colors in each tube.
                    sel_tube (int): The index of the selected tube.
                    dest_tube (int): The index of the destination tube.

                Returns:
                    List[List[int]]: Updated tube colors after the move.
        """
        chain = True
        length = 1
        color_on_top = 100
        color_to_move = 100
        if len(tube_cols[sel_tube]) > 0:
            color_to_move = tube_cols[sel_tube][-1]
            for col in range(1, len(tube_cols[sel_tube])):
                if chain:
                    if tube_cols[sel_tube][-1 - col] == color_to_move:
                        length += 1
                    else:
                        chain = False
        if len(tube_cols[dest_tube]) < self.NColorInTube:
            if len(tube_cols[dest_tube]) == 0:
                color_on_top = color_to_move
            else:
                color_on_top = tube_cols[dest_tube][-1]
        if color_on_top == color_to_move and len(tube_cols[sel_tube]) > 0:
            if sel_tube != dest_tube:
                self.game_state_history.append(copy.deepcopy(tube_cols))
                self.move_count += 1
            for i in range(length):
                if len(tube_cols[dest_tube]) < self.NColorInTube and len(tube_cols[sel_tube]) > 0:
                    tube_cols[dest_tube].append(color_to_move)
                    tube_cols[sel_tube].pop(-1)

        return tube_cols

    def check_victory(self, tube_cols):
        """Check if the player has won the game.
                Args:
                    tube_cols (List[List[int]]): A list of lists representing the colors in each tube.

                Returns:
                    bool: True if the player has won, False otherwise.
        """
        won = True
        for i in range(len(tube_cols)):
            if len(tube_cols[i]) > 0:
                if len(tube_cols[i]) != self.NColorInTube:
                    won = False
                else:
                    main_color = tube_cols[i][-1]
                    for j in range(len(tube_cols[i])):
                        if tube_cols[i][j] != main_color:
                            won = False
        return won

    def reset_game(self, colors_count, color_tube_count, empty_tubes):
        """Reset the game with new settings.
                Args:
                    colors_count (int): The number of unique colors in the game.
                    color_tube_count (int): The number of colors in each tube.
                    empty_tubes (int): The number of initially empty tubes.
        """
        self.NColor = colors_count
        self.NColorInTube = color_tube_count
        self.NEmptyTubes = empty_tubes
        self.tubes, self.tube_colors = self.generate_start()
        self.initial_colors = copy.deepcopy(self.tube_colors)
        self.game_state_history = []
        self.selected_tube = 100
        self.destination_tube = 100
        self.selected = False
        self.win = False
        self.move_count = 0
        self.move_text = ""

    def auto_move(self, founded_solution, m_font):
        """Move the colors automatically based on the solution found by the AI.
                Args:
                    founded_solution (List[Tuple[int, int]]): A list of tuples representing
                    the source and destination tubes for each move.
                    :param founded_solution:
                    :param m_font:
        """
        for move in founded_solution:
            self.screen.fill((0, 0, 0))
            self.clock.tick(fps)
            self.undo_button.draw(self.screen)
            self.new_board_button.draw(self.screen)
            self.solve_game_button.draw(self.screen)
            self.optimal_solve_button.draw(self.screen)
            self.reset_button.draw(self.screen)

            self.color_spinner.draw(self.screen)
            self.empty_tubes_spinner.draw(self.screen)
            self.colors_in_tube_spinner.draw(self.screen)

            sel_tube, dest_tube = move  # Extract the source and destination tubes from the AI's solution
            self.tube_colors = self.move_logic(self.tube_colors, sel_tube, dest_tube)
            self.move_text = m_font.render(f"Move: {self.move_count}", True, 'white')
            self.screen.blit(self.move_text, (10, 10))
            self.draw_tubes(self.tubes, self.tube_colors)
            pygame.display.flip()
            pygame.time.delay(500)  # Add a delay to slow down the automatic moves for better visualization

    def run_game(self):
        """Run the main game loop."""
        while self.run:
            self.screen.fill((0, 0, 0))
            self.clock.tick(fps)
            self.undo_button.draw(self.screen)
            self.new_board_button.draw(self.screen)
            self.solve_game_button.draw(self.screen)
            self.optimal_solve_button.draw(self.screen)
            self.reset_button.draw(self.screen)

            self.color_spinner.draw(self.screen)
            self.empty_tubes_spinner.draw(self.screen)
            self.colors_in_tube_spinner.draw(self.screen)

            move_font = pygame.font.SysFont("Arial", 24)
            self.move_text = move_font.render(f"Move: {self.move_count}", True, 'teal')
            self.screen.blit(self.move_text, (10, 10))

            if self.new_game:
                self.tubes, self.tube_colors = self.generate_start()
                self.initial_colors = copy.deepcopy(self.tube_colors)
                self.new_game = False
            else:
                self.tube_rects = self.draw_tubes(self.tubes, self.tube_colors)
            self.win = self.check_victory(self.tube_colors)
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if self.win:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.reset_game(self.color_spinner.value, self.colors_in_tube_spinner.value,
                                            self.empty_tubes_spinner.value)
                        if event.key == pygame.K_SPACE:
                            self.tube_colors = copy.deepcopy(self.initial_colors)
                            self.win = False
                            self.new_game = False
                            self.move_count = 0
                            self.game_state_history = []
                if not self.win or self.move_count == 0:
                    self.color_spinner.update(event)
                    self.empty_tubes_spinner.update(event)
                    self.colors_in_tube_spinner.update(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.selected:
                            for i in range(len(self.tube_rects)):
                                if self.tube_rects[i].collidepoint(event.pos):
                                    self.selected = True
                                    self.selected_tube = i
                        else:
                            for i in range(len(self.tube_rects)):
                                if self.tube_rects[i].collidepoint(event.pos):
                                    self.destination_tube = i
                                    # Save the current game state before moving
                                    self.tube_colors = self.move_logic(self.tube_colors, self.selected_tube,
                                                                       self.destination_tube)
                                    self.selected = False
                                    self.selected_tube = 100
                        if self.undo_button.rect.collidepoint(event.pos):
                            # Handle the "Undo" button click
                            if self.game_state_history:
                                self.tube_colors = self.game_state_history.pop()
                                self.move_count -= 1
                        if self.new_board_button.rect.collidepoint(event.pos):
                            # Handle the "New Game" button click
                            self.tube_colors.pop()
                            self.reset_game(self.color_spinner.value, self.colors_in_tube_spinner.value,
                                            self.empty_tubes_spinner.value)
                        if self.solve_game_button.rect.collidepoint(event.pos):
                            print("solving...")
                            solution = GameSolution(self)
                            solution.solve(self.tube_colors)
                            print(solution.solution_found, solution.moves)
                            print("move count:", len(solution.moves))
                            if solution.solution_found:
                                self.auto_move(solution.moves, move_font)
                        if self.optimal_solve_button.rect.collidepoint(event.pos):
                            print("optimal solving...")
                            solution = GameSolution(self)
                            solution.optimal_solve(self.tube_colors)
                            print(solution.solution_found, solution.moves)
                            print("optimal move count:", len(solution.moves))
                            if solution.solution_found:
                                self.auto_move(solution.moves, move_font)
                        if self.reset_button.rect.collidepoint(event.pos):
                            self.tube_colors = copy.deepcopy(self.initial_colors)
                            self.win = False
                            self.new_game = False
                            self.move_count = 0
                            self.game_state_history = []

            if self.win:
                victory_text = self.font.render('You win! press <Enter> to new game or press <Space> to reset!', True
                                                , 'yellow')
                self.screen.blit(victory_text, (110, 0))
            pygame.display.flip()

        pygame.quit()
