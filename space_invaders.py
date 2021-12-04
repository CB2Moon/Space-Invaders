from space_invader_support import *
import tkinter as tk
import random
from tkinter import messagebox
from tkinter import filedialog
from typing import Callable


class Entity(object):
    """Entity is an abstract class that is used to represent any element that
    can appear on the game’s grid. """

    def display(self) -> str:
        """(str) Return the character used to represent this entity in a
        text-based grid. """
        raise NotImplementedError

    def __repr__(self) -> str:
        """(str) Return a representation of this entity."""
        return f'{self.__class__.__name__}()'


class Player(Entity):
    """A subclass of Entity representing a Player within the game."""

    def display(self) -> str:
        """(str) Return the character representing a player"""
        return PLAYER


class Destroyable(Entity):
    """A subclass of Entity representing a Destroyable within the game. """

    def display(self) -> str:
        """(str) Return the character representing a destroyable"""
        return DESTROYABLE


class Collectable(Entity):
    """A subclass of Entity representing a Collectable within the game."""

    def display(self) -> str:
        """(str) Return the character representing a collectable"""
        return COLLECTABLE


class Blocker(Entity):
    """A subclass of Entity representing a Blocker within the game."""

    def display(self) -> str:
        """(str) Return the character representing a blocker"""
        return BLOCKER


class Bomb(Entity):
    """A subclass of Entity representing a Bomb within the game."""

    def display(self) -> str:
        """(str) Return the character representing a bomb"""
        return BOMB


class Grid(object):
    """The Grid class is used to represent the 2D grid of entities."""

    def __init__(self, size: int) -> None:
        """A grid is constructed with a size representing the number of rows
        (equal to the number of columns) in the grid.

        Parameters:
            size (int): representing the number of rows (equal to the number of
                        columns) in the grid
        """
        self._size = size
        self._entities = {}

    def get_size(self) -> int:
        """(int) Return the size of the grid"""
        return self._size

    def add_entity(self, position: Position, entity: Entity) -> None:
        """Add a given entity into the grid at a specified position.

        Parameters:
            position (Position): the position of the entity
            entity (Entity): the entity
        """
        if self.in_bounds(position):
            self._entities[position] = entity

    def get_entities(self) -> Dict[Position, Entity]:
        """(dict) Return the dictionary containing grid entities"""
        return self._entities.copy()

    def get_entity(self, position: Position) -> Optional[Entity]:
        """(Optional) Return a entity from the grid at a specific position

        Parameters:
            position (Position): the position of the entity
        """
        return self._entities.get(position)

    def remove_entity(self, position: Position) -> None:
        """Remove an entity from the grid at a specified position

        Parameters:
            position (Position): the position of the entity
        """
        self._entities.pop(position, None)

    def serialise(self) -> Dict[Tuple[int, int], str]:
        """(dict) Convert dictionary of Position and Entities into a
        simplified, serialised dictionary mapping tuples to characters,
        and return this serialised mapping. """
        return {(position.get_x(), position.get_y()): entity.display()
                for position, entity in self._entities.items()}

    def in_bounds(self, position: Position) -> bool:
        """(bool) Return a boolean based on whether the position is valid in
        terms of the dimensions of the grid

        Parameters:
            position (Position): the position of the entity
        """
        if position.get_x() < 0 or position.get_x() >= self._size:
            return False
        if position.get_y() < 1 or position.get_y() >= self._size:
            return False
        return True

    def __repr__(self) -> str:
        """(str) Return a representation of this Grid"""
        return f'{self.__class__.__name__}({self._size})'


class Game(object):
    """ Handles the logic for controlling the actions of the entities within
    the grid. """

    def __init__(self, size: int) -> None:
        """A game is constructed with a size representing the dimensions of
        the playing grid

        Parameters:
            size (int): representing the number of rows (equal to the number of
                        columns) in the grid
        """
        self._grid = Grid(size)
        self._flag = None
        self._PLAYER_POSITION = Position(size // 2, 0)
        self._acquired_collectable = 0
        self._removed_destroyable = 0
        self._shots = 0
        self._life = 1

    def get_grid(self) -> Grid:
        """(Grid) Return the instance of the grid held by the game."""
        return self._grid

    def get_player_position(self) -> Position:
        """(Position) Return the position of the player in the grid"""
        return self._PLAYER_POSITION

    def get_num_collected(self) -> int:
        """(int) Return the total of Collectables acquired."""
        return self._acquired_collectable

    def set_num_collected(self, num: int) -> None:
        """Sets the collected number. Used when loading the game.

        Parameters:
            num (int): the number of collectables that the player has collected
        """
        self._acquired_collectable = num

    def get_num_destroyed(self) -> int:
        """(int) Return the total of Destroyables removed with a shot."""
        return self._removed_destroyable

    def set_num_destroyed(self, num: int) -> None:
        """Sets the destroyed number. Used when loading the game

        Parameters:
            num (int): the number of destroyables that the player has destroyed
        """
        self._removed_destroyable = num

    def get_total_shots(self) -> int:
        """(int) Return the total of shots taken."""
        return self._shots

    def set_total_shots(self, num: int) -> None:
        """Sets the total shots number. Used when loading the game

        Parameters:
            num (int): the number of shots that the player has shot
        """
        self._shots = num

    def get_life(self) -> int:
        """(int) Returns the life of the player"""
        return self._life

    def set_life(self, num: int) -> None:
        """Sets the life of the player

        Parameters:
            num (int): the number of lives that the player has
        """
        self._life = num

    def die(self) -> None:
        """Decrements the life of the player"""
        self._life -= 1

    def alive(self) -> bool:
        """(bool) Returns true iff the player still has lives"""
        return self.get_life() > 0

    def rotate_grid(self, direction: str) -> None:
        """Rotate the positions of the entities within the grid depending on
        the direction they are being rotated

        Parameters:
            direction (str): left or right in valid string form
        """
        if direction == LEFT:
            rotation_x, rotation_y = ROTATIONS[0]
            out_bound_x = self.get_grid().get_size() - 1
        else:
            rotation_x, rotation_y = ROTATIONS[1]
            out_bound_x = 0
        rotate = Position(rotation_x, rotation_y)
        rotated_entities = {}

        for position, entity in self._grid.get_entities().items():
            self._grid.remove_entity(position)
            new_position = position.add(rotate)
            if not self._grid.in_bounds(new_position):
                new_position = Position(out_bound_x, new_position.get_y())
            rotated_entities[new_position] = entity

        for pos, en in rotated_entities.items():
            self._grid.add_entity(pos, en)

    def load_entities(self, entities: Dict[tuple, str]) -> None:
        """Load the entities data

        Parameters:
            entities (dict): All the entities that need loading.
        """
        # clear all entities
        for pos, _ in self.get_grid().get_entities().items():
            self.get_grid().remove_entity(pos)

        # add entities
        for position, entity in entities.items():
            x, y = position
            pos = Position(int(x), int(y))
            if not self.get_grid().in_bounds(pos):
                continue
            entity = self._create_entity(entity)
            self.get_grid().add_entity(pos, entity)

    def _create_entity(self, display: str) -> Entity:
        """Uses a display character to create an Entity.

        Parameters:
            display (str): The entity type in string form
        """
        entity = {
            COLLECTABLE: Collectable(),
            DESTROYABLE: Destroyable(),
            BLOCKER: Blocker(),
            BOMB: Bomb()}
        if display not in entity:
            raise NotImplementedError
        else:
            return entity[display]

    def generate_entities(self) -> None:
        """
        Method given to the students to generate a random amount of entities to
        add into the game after each step
        """
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)

    def step(self) -> None:
        """Moves all entities on the board by an offset of (0, -1)"""
        move = Position(MOVE[0], MOVE[1])
        for position, entity in self._grid.get_entities().items():
            self._grid.remove_entity(position)
            new_position = position.add(move)
            if not self._grid.in_bounds(new_position):
                if entity.display() == DESTROYABLE:
                    self.die()
                    if not self.alive():
                        self._flag = False
                continue

            self._grid.add_entity(new_position, entity)

        self.generate_entities()

    def fire(self, shot_type: str) -> None:
        """Handles the firing/collecting actions of a player towards an
        entity within the grid

        Parameters:
            shot_type (str): collect or destroy.
        """
        self._shots += 1
        if shot_type not in SHOT_TYPES:
            return None

        fire_dir = Position(FIRE[0], FIRE[1])
        entity_pos = self.get_player_position()
        for _ in range(self.get_grid().get_size() - 1):
            entity_pos = entity_pos.add(fire_dir)
            entity = self.get_grid().get_entity(entity_pos)

            if entity is None:
                continue
            if entity.display() == BLOCKER:
                return None
            # collect type shot
            if shot_type == COLLECT:
                if entity.display() == COLLECTABLE:
                    self._acquired_collectable += 1
                    self.get_grid().remove_entity(entity_pos)
                    if self._acquired_collectable == COLLECTION_TARGET:
                        self._flag = True
                return None
            # destroy type shot
            else:
                if entity.display() == BOMB:
                    for x, y in SPLASH:
                        neighbour_pos = entity_pos.add(Position(x, y))
                        neighbour = self.get_grid().get_entity(neighbour_pos)
                        if neighbour is not None:
                            self.get_grid().remove_entity(neighbour_pos)
                elif entity.display() == DESTROYABLE:
                    self._removed_destroyable += 1
                self.get_grid().remove_entity(entity_pos)
                return None

    def has_won(self) -> bool:
        """(bool) Return True if the player has won the game"""
        return False if self._flag is None else self._flag

    def has_lost(self) -> bool:
        """(bool) Returns True if the game is lost"""
        return False if self._flag is None else not self._flag


class AbstractField(tk.Canvas):
    """ An abstract view class which inherits from tk.Canvas and provides
    base functionality for other view classes """

    def __init__(
            self,
            master: tk.Frame,
            rows: int,
            cols: int,
            width: int,
            height: int,
            **kwargs
    ) -> None:
        """Construct an AbstractField

        Parameters:
            master (tk.Tk): the Tk object
            rows (int): the number of rows in the grid
            cols (int): the number of columns in the grid
            width (int): the width of this Canvas
            height (int): the height of this Canvas
        """
        super().__init__(master, width=width, height=height, **kwargs)
        self._cols = cols
        self._rows = rows
        self._width = width
        self._height = height
        self._box_width = width // cols
        self._box_height = height // rows

    def get_bbox(
            self, position: Position
    ) -> Tuple[int, int, int, int]:
        """Returns the bounding box for the position

        Parameters:
            position (Position): The (row, column) position

        Returns:
            (tuple): a tuple containing information about the pixel
                    positions of the edges of the shape
        """
        x, y = position.get_x(), position.get_y()
        return (x * self._box_width,
                y * self._box_height,
                (x + 1) * self._box_width,
                (y + 1) * self._box_height)

    def pixel_to_position(self, pixel: Tuple[int, int]) -> Tuple[int, int]:
        """ Converts the (x, y) pixel position (in graphics units) to a (row,
        column) position.

        Parameters:
            pixel (tuple): The (x, y) pixel position

        Returns:
            (tuple): The (row, column) position
        """
        return pixel[0] // self._box_width, pixel[1] // self._box_height

    def get_position_center(self, position: Position) -> Tuple[int, int]:
        """ Gets the graphics coordinates for the center of the cell at the
        given (row, column) position.

        Parameters:
            position (Position): The (row, column) position

        Returns:
            (tuple): The (x, y) pixel position
        """
        x, y = position.get_x(), position.get_y()
        return (int((x + 0.5) * self._box_width),
                int((y + 0.5) * self._box_height))

    def annotate_position(self, position: Position, text: str) -> int:
        """Annotates the center of the cell at the given (row, column) position
        with the provided text.

        Parameters:
            position (Position): The (row, column) position
            text (str): The text to annotate

        Returns:
            (int): the id of the thing drawn on the canvas
        """
        x, y = self.get_position_center(position)
        return self.create_text(x, y, text=text)


class GameField(AbstractField):
    """A visual representation of the game grid"""

    def __init__(
            self,
            master: tk.Frame,
            size: int,
            width: int,
            height: int,
            **kwargs
    ) -> None:
        """Construct a GameField

        Parameters:
            master (tk.Tk): the Tk object
            size (int): the number of rows and columns in the grid
            width (int): the width of this Canvas
            height (int): the height of this Canvas
        """
        super().__init__(
            master, rows=size, cols=size, width=width, height=height, **kwargs)

    def draw_grid(self, entities: Dict[Position, Entity]) -> None:
        """Draws the entities in the game grid at their given position using a
        coloured rectangle with superimposed text identifying the entity

        Parameters:
            entities (dict): A dict of current entities, including the player
        """
        for pos, entity in entities.items():
            entity_type = entity.display()
            color = COLOURS[entity_type]
            x_min, y_min, x_max, y_max = self.get_bbox(pos)

            self.create_rectangle(x_min, y_min, x_max, y_max, fill=color)
            self.annotate_position(pos, entity_type)

    def draw_player_area(self) -> None:
        """Draws the grey area the player is placed on"""
        self.create_rectangle(
            0, 0, self._width, self._box_height, fill=PLAYER_AREA
        )

    def draw_field_area(self) -> None:
        """Draws the dark grey area the grid is placed on"""
        self.create_rectangle(
            0, self._box_height, self._width, self._height, fill=FIELD_COLOUR
        )


class ScoreBar(AbstractField):
    """A visual representation of shot statistics from the player"""

    def __init__(self, master: tk.Frame, rows: int, **kwargs):
        """Construct an ScoreBar

        Parameters:
            master (tk.Tk): the Tk object this ScoreBar in
            rows (int): the number of rows in the grid
        """
        super().__init__(
            master,
            rows=rows,
            cols=2,
            width=SCORE_WIDTH,
            height=MAP_HEIGHT,
            **kwargs
        )

    def draw_static_stuff(self, task: int) -> None:
        """Draws score area and the text

        Parameters:
            task (int): the current TASK
        """

        self.create_rectangle(
            0, 0, self._width, self._height, fill=SCORE_COLOUR
        )

        x, y = self._width // 2, self._box_height // 2
        self.create_text(
            x, y, text='Score', font=('Arial', 20), fill='white'
        )

        collected, destroyed, lives = (
            Position(0, 1), Position(0, 2), Position(0, 3)
        )
        self.annotate_position(collected, 'Collected:')
        self.annotate_position(destroyed, 'Destroyed:')
        if task == 3:
            self.annotate_position(lives, 'Lives')

    def annotate_position(self, position: Position, text: str) -> int:
        """Annotates the center of the cell at the given (row, column) position
        with the provided text.

        Parameters:
            position (Position): The (row, column) position
            text (str): The text to annotate

        Returns:
            (int): the id of the thing drawn on the canvas
        """
        x, y = self.get_position_center(position)
        return self.create_text(x, y, text=text, fill='white')


class HackerController(object):
    """Acts as the controller for the Hacker game"""

    def __init__(self, master: tk.Tk, size: int) -> None:
        """The constructor of the HackerController

        Parameters:
            master (tk.Tk): the master window
            size (int): the number of rows (= number of columns)
        """
        self._master = master
        self._size = size
        self._scores = []
        self._wait = None
        self._time = 0
        self._game = self.initialize_game()
        self._title_frame = None
        self._title = None
        self._game_frame = None
        self._game_field = None
        self._score_bar = None

        self.initialize_frames()
        self.initialize_fields()

        self._master.bind('<Key>', self.handle_keypress)
        self.draw(self._game)
        self.wait()

    def initialize_game(self) -> Game:
        """(Game) Initializes the Game and return"""
        return Game(self._size)

    def initialize_frames(self) -> None:
        """Initializes the tk frames of the game"""
        self._title_frame = tk.Frame(self._master)
        self._title_frame.pack(side=tk.TOP, fill=tk.X)
        self._title = tk.Label(
            self._title_frame, text=TITLE,
            bg=TITLE_BG, fg='white', font=TITLE_FONT
        )
        self._title.pack(expand=True, fill=tk.X)

        self._game_frame = tk.Frame(self._master)
        self._game_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def initialize_fields(self) -> None:
        """Initializes the tk fields of the game"""
        self._game_field = GameField(
            self._game_frame, self._size, MAP_WIDTH, MAP_HEIGHT
        )
        self._game_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._score_bar = ScoreBar(self._game_frame, self._size)
        self._score_bar.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self._score_bar.draw_static_stuff(1)

    def handle_keypress(self, event: tk.Event) -> None:
        """Called when the user presses any key during the game

        Parameters:
            event (tk.Event): <Key> event
        """
        key = event.keysym.upper()
        if key in DIRECTIONS:
            self.handle_rotate(key)
        elif key in SHOT_TYPES:
            self.handle_fire(key)
            self.check_won_lost()

    def draw(self, game: Game) -> None:
        """Clears and redraws the view based on the current game state

        Parameters:
            game (Game): the current game
        """
        # draw game field
        self._game_field.delete(tk.ALL)
        self._game_field.draw_player_area()
        self._game_field.draw_field_area()
        entities = game.get_grid().get_entities()
        entities[game.get_player_position()] = Player()
        self._game_field.draw_grid(entities)

        # draw score num
        for score in self._scores:
            self._score_bar.delete(score)

        self._scores.append(
            self._score_bar.annotate_position(
                Position(1, 1), str(game.get_num_collected())
            )
        )
        self._scores.append(
            self._score_bar.annotate_position(
                Position(1, 2), str(game.get_num_destroyed())
            )
        )

    def handle_rotate(self, direction: str) -> None:
        """Handles rotation of the entities and redrawing the game.

        Parameters:
            direction (str): the direction to rotate
        """
        self._game.rotate_grid(direction)
        self.draw(self._game)

    def handle_fire(self, shot_type: str) -> None:
        """Handles the firing of the specified shot type and redrawing of
        the game.

        Parameters:
            shot_type (str): the shot type the player fired
         """
        self._game.fire(shot_type)
        self.draw(self._game)

    def wait(self) -> None:
        """Waits for some time."""
        self._wait = self._master.after(2000, self.step)

    def step(self) -> None:
        """Called every 2 seconds. Triggers the step method for the game and
        updates the view accordingly """
        self._game.step()
        self.draw(self._game)
        self.check_won_lost()
        self.wait()

    def check_won_lost(self) -> None:
        """Check if the game has won or lost and end the game"""
        msg = ''
        if self._game.has_won():
            msg = 'won!'
        elif self._game.has_lost():
            msg = 'lost!'
        if msg:
            self._master.after_cancel(self._wait)
            if messagebox.showwarning(
                    title='Game Over', message=f'You {msg}'
            ) == 'ok':
                self._master.destroy()


class AdvancedHackerController(HackerController):
    """A new interface class that extends the functionality of the
    HackerController class """

    def __init__(self, master: tk.Tk, size: int) -> None:
        """The constructor of the AdvancedHackerController

        Parameters:
            master (tk.Tk): the master window
            size (int):  the number of rows (= number of columns)
        """
        self._playing = True
        self._status_frame = None

        # adding menu
        self._menu = tk.Menu(master)
        master.config(menu=self._menu)
        self._file_menu = tk.Menu(self._menu)
        self._menu.add_cascade(label='File', menu=self._file_menu)
        self._file_menu.add_command(label='New game', command=self.new_game)
        self._file_menu.add_command(label='Save game', command=self.save_game)
        self._file_menu.add_command(label='Load game', command=self.load_game)
        self._file_menu.add_command(label='Quit', command=self.quit)

        super().__init__(master, size)

    def initialize_fields(self) -> None:
        """Initializes the tk fields of the game"""
        self._game_field = ImagesGameField(
            self._game_frame, self._size, MAP_WIDTH, MAP_HEIGHT
        )
        self._game_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._score_bar = ScoreBar(self._game_frame, self._size)
        self._score_bar.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self._score_bar.draw_static_stuff(2)

        self._status_frame = StatusBar(self._master)
        self._status_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._status_frame.draw_grid()
        self._status_frame.set_button(self.pause_resume)

    def handle_fire(self, shot_type: str) -> None:
        """Handles the firing of the specified shot type and redrawing of
        the game.

        Parameters:
            shot_type (str): the shot type the player fired
         """
        super().handle_fire(shot_type)
        self._status_frame.update_shot(self._game.get_total_shots())

    def wait(self) -> None:
        """Waits for some time."""
        self._wait = self._master.after(1000, self.step)

    def step(self) -> None:
        """Steps every 1 seconds. Also counts the time."""
        self._time += 1
        self._status_frame.update_time(self._time)

        # step every 2s
        if not self._time % 2:
            self._game.step()
            self.draw(self._game)
            self.check_won_lost()
        self.wait()

    def pause_resume(self) -> None:
        """Stops the game or resumes the game when the button is hit"""
        if self._playing:
            self.pause()
        else:
            self.resume()

    def pause(self) -> None:
        """Pauses the game"""
        self._status_frame.get_btn().config(text='Resume')
        self._master.after_cancel(self._wait)
        self._master.unbind('<Key>')
        self._playing = False

    def resume(self) -> None:
        """Resumes the game"""
        self._playing = True
        self._status_frame.get_btn().config(text='Pause')
        self._master.bind('<Key>', self.handle_keypress)
        self.wait()

    def new_game(self) -> None:
        """Starts the game from scratch."""
        self.pause()
        self._time = 0
        self._status_frame.update_time(0)
        self._game.set_num_destroyed(0)
        self._game.set_num_collected(0)
        self._game.set_total_shots(0)
        self._status_frame.update_shot(0)
        self._game.set_life(1)
        self._game.load_entities({})
        self.draw(self._game)
        self.resume()

    def save_game(self) -> None:
        """Saves the game"""
        self.pause()
        pos = '|'.join(map(str, self._game.get_grid().serialise().keys()))
        entity = '|'.join(self._game.get_grid().serialise().values())
        try:
            file = filedialog.asksaveasfile(
                initialdir='./',
                filetypes=(('txt files', '*.txt'), ('all files', '*.*')),
                defaultextension='.txt',
                mode='w'
            )
            file.writelines([
                f'Time: {self._time}\n',
                f'Life: {self._game.get_life()}\n',
                f'Shots: {self._game.get_total_shots()}\n',
                f'Collected: {self._game.get_num_collected()}\n',
                f'Destroyed: {self._game.get_num_destroyed()}\n',
                f'Positions: {pos}\n',
                f'Entities: {entity}'
            ])
            file.close()

        # cancel saving
        except AttributeError:
            self.resume()

    def load_game(self) -> None:
        """Load a played game"""
        self.pause()
        data_format = [
            (6, 'Time: '),
            (6, 'Life: '),
            (7, 'Shots: '),
            (11, 'Collected: '),
            (11, 'Destroyed: '),
            (11, 'Positions: '),
            (10, 'Entities: ')
        ]
        restored_data = []
        try:
            with filedialog.askopenfile(mode='r') as game_data:
                for line_num, data in enumerate(game_data):
                    to, value = data_format[line_num]
                    if data[:to] == value:
                        restored_data.append(data[to:])
                    else:
                        raise ValueError
        # cancel loading
        except AttributeError:
            self.resume()
            return None
        # file includes wrong game data
        except ValueError:
            messagebox.showerror(
                title='Invalid File!',
                message='This is not a valid file!')
            self.resume()
            return None

        self._time = int(restored_data[0])
        self._status_frame.update_time(int(restored_data[0]))

        self._game.set_life(int(restored_data[1]))

        self._game.set_total_shots(int(restored_data[2]))
        self._status_frame.update_shot(int(restored_data[2]))

        self._game.set_num_collected(int(restored_data[3]))
        self._game.set_num_destroyed(int(restored_data[4]))

        positions = restored_data[5].split("|")
        positions = list(
            map(lambda x: tuple(x.strip()[1:-1].split(', ')), positions)
        )
        entities = restored_data[6].split("|")
        self._game.load_entities(
            dict(zip(positions, entities))
        )

        self.draw(self._game)
        self.resume()

    def quit(self):
        """Asks if the player really want to quit the game.
        Resumes the game or ends the game as they wish"""
        self.pause()
        if messagebox.askyesno(title='Quit', message='Are you sure?'):
            self._master.destroy()
        else:
            self.resume()


class MoreAdvancedHackerController(AdvancedHackerController):
    """Extends the AdvancedHackerController to fit TASK 3"""

    def initialize_game(self) -> Game:
        """(Game) Initializes the Game and return"""
        return MoreAdvancedGame(self._size)

    def initialize_fields(self) -> None:
        """Initializes the tk fields of the game"""
        self._game_field = ImagesGameField(
            self._game_frame, self._size, MAP_WIDTH, MAP_HEIGHT
        )
        self._game_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self._score_bar = ScoreBar(self._game_frame, self._size)
        self._score_bar.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self._score_bar.draw_static_stuff(3)

        self._status_frame = StatusBar(self._master)
        self._status_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._status_frame.draw_grid()
        self._status_frame.set_button(self.pause_resume)

    def draw(self, game: Game) -> None:
        """Clears and redraws the view based on the current game state

        Parameters:
            game (Game): the current game
        """
        super().draw(game)
        self._scores.append(
            self._score_bar.annotate_position(
                Position(1, 3), str(game.get_life())
            )
        )

    def new_game(self) -> None:
        """Starts the game from scratch."""
        self.pause()
        self._time = 0
        self._status_frame.update_time(0)
        self._game.set_num_destroyed(0)
        self._game.set_num_collected(0)
        self._game.set_total_shots(0)
        self._status_frame.update_shot(0)
        self._game.set_life(2)
        self._game.load_entities({})
        self.draw(self._game)
        self.resume()


class MoreAdvancedGame(Game):
    """Extends the Game to fit TASK 3"""
    def __init__(self, size: int) -> None:
        """A game is constructed with a size representing the dimensions of
        the playing grid

        Parameters:
            size (int): representing the number of rows (equal to the number of
                        columns) in the grid
        """
        super().__init__(size)
        self.set_life(2)

    def generate_entities(self) -> None:
        """
        Method given to the students to generate a random amount of entities to
        add into the game after each step
        """
        # Generate amount
        entity_count = random.randint(0, self.get_grid().get_size() - 3)
        entities = random.choices(ENTITY_TYPES, k=entity_count)

        # Blocker in a 1 in 4 chance
        blocker = random.randint(1, 4) % 4 == 0

        bomb = False
        if not blocker:
            bomb = random.randint(1, 4) % 4 == 0

        total_count = entity_count
        if blocker:
            total_count += 1
            entities.append(BLOCKER)

        if bomb:
            total_count += 1
            entities.append(BOMB)

        entity_index = random.sample(range(self.get_grid().get_size()),
                                     total_count)

        # Add entities into grid
        for pos, entity in zip(entity_index, entities):
            position = Position(pos, self.get_grid().get_size() - 1)
            new_entity = self._create_entity(entity)
            self.get_grid().add_entity(position, new_entity)


class ImagesGameField(GameField):
    """A new view class that extends the existing GameField class"""

    def __init__(
            self,
            master: tk.Frame,
            size: int,
            width: int,
            height: int,
            **kwargs
    ) -> None:
        """Construct an GameField

        Parameters:
            master (tk.Frame): the frame this canvas in
            size (int): the number of rows and columns in the grid
            width (int): the width of this Canvas
            height (int): the height of this Canvas
        """
        super().__init__(
            master, size=size, width=width, height=height, **kwargs)
        self._img = []
        self._pos = []

    def draw_grid(self, entities: Dict[Position, Entity]) -> None:
        """Draws the entities in the game grid at their given position using an
        image identifying the entity

        Parameters:
            entities (dict): A dict of current entities, including the player
        """
        self._img = []
        self._pos = []

        for pos, entity in entities.items():
            entity_type = entity.display()
            self._img.append(
                tk.PhotoImage(file=f'images/{IMAGES[entity_type]}')
            )
            self._pos.append(self.get_position_center(pos))

        for i, img in enumerate(self._img):
            self.create_image(self._pos[i], image=img, anchor=tk.CENTER)


class StatusBar(tk.Frame):
    """A class extends the tk.Frame class"""

    def __init__(self, master: tk.Tk) -> None:
        """Construct a StatusBar object

        Parameters:
            master (tk.Tk): the Tk object this frame is in
        """
        super().__init__(master)
        self._master = master
        self._total_shots_num = None
        self._time_num = None
        self._btn = None

    def draw_grid(self) -> None:
        """Draws the Total Shots, Timer"""
        total_shots_lbl = tk.Label(self, text='Total Shots')
        total_shots_lbl.grid(row=0, column=0)

        self._total_shots_num = tk.Label(self, text='0')
        self._total_shots_num.grid(row=1, column=0)

        timer_lbl = tk.Label(self, text='Timer')
        timer_lbl.grid(row=0, column=1)

        self._time_num = tk.Label(self, text='0m 0s')
        self._time_num.grid(row=1, column=1)

        for col in range(3):
            self.columnconfigure(col, weight=1)
        for row in range(2):
            self.rowconfigure(row, weight=1)

    def set_button(self, callback: Callable) -> None:
        """Creates the pause/resume button for the StatusBar

        Parameters:
            callback (Callable): the function implemented when the button is
                                pressed

        Returns:
            (tk.Button): the button created
        """
        self._btn = tk.Button(self, text='Pause', command=callback)
        self._btn.grid(row=0, column=2, rowspan=2)

    def get_btn(self) -> tk.Button:
        """(tk.Button) Returns the pause/resume button of the StatusBar"""
        return self._btn

    def update_shot(self, shots: int) -> None:
        """Updates the total shots number

        Parameters:
            shots (int): the latest total shots
        """
        self._total_shots_num.config(text=str(shots))

    def update_time(self, time: int) -> None:
        """Updates the time that has passed

        Parameters:
            time (int): the time that has passed
        """
        self._time_num.config(text=f'{time // 60}m {time % 60}s')


def start_game(root, TASK=3):
    controller = HackerController

    if TASK != 1:
        controller = AdvancedHackerController
        if TASK == 3:
            controller = MoreAdvancedHackerController

    app = controller(root, GRID_SIZE)
    return app


def main():
    root = tk.Tk()
    root.title(TITLE)
    app = start_game(root)
    root.mainloop()


if __name__ == '__main__':
    main()
