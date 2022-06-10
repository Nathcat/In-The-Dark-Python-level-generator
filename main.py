from PIL import Image as PILImage
import random
import MazeSolver


class CaveGenerator:
    """
    Generates a random cave given a set of parameters using cellular automata.

    Starts by generating a list of boolean values (True for an alive cell, False for a dead cell), and then performing
    generation steps to refine the final map. Alive cells are black on the image, and dead cells are white.

    "Blobs" are then applied, these are pixels of a set colour, that will appear on the final image.
    """
    def __init__(self, w, h, chanceToStartAlive, starvationLimit, overpopLimit, birthNumber):
        self.w = w                                # The width of the final map
        self.h = h                                # The height of the final map
        self.__starvationLimit = starvationLimit  # The minimum alive neighbours for alive cells
        self.__overpopLimit = overpopLimit        # The maximum alive neighbours for alive cells
        self.__birthNumber = birthNumber          # The number of alive neighbours required for a dead cell to become alive
        self.__cave = []                          # The array containing cells
        self.__blobs = []                         # An array containing blob maps
        self.__blob_colours = []                  # An array containing colours for blob maps

        self.init_cave(chanceToStartAlive)

    def cell_index(self, x, y):
        """
        Return the array index of a cell from x/y coordinates.

        :param x: x ordinate
        :param y: y ordinate
        :return: The cell array index
        """
        return (y * self.w) + x

    def cell_position(self, index):
        """
        Return the x/y coordinates of a cell array index.

        :param index: The cell index
        :return: The x/y coordinates of the given cell index
        """
        return index % self.w, index // self.w

    def __pixel_colour(self, cell):
        """
        Return the colour of an alive/dead cell.

        :param cell: Cell state
        :return: The RGBA colour of the cell
        """
        if cell:
            return (0, 0, 0, 255)

        else:
            return (255, 255, 255, 255)

    def generator_step(self):
        """
        Perform a Cellular automata generator step.
        """
        result_cave = [cell for cell in self.__cave]

        # Iterate over cells in the array
        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                # Get the index of the current cell
                current_index = self.cell_index(x, y)

                # Get the indices of all the neighbour cells
                neighbour_indices = [
                    self.cell_index(x - 1, y),
                    self.cell_index(x + 1, y),
                    self.cell_index(x, y - 1),
                    self.cell_index(x, y + 1),
                    self.cell_index(x - 1, y - 1),
                    self.cell_index(x - 1, y + 1),
                    self.cell_index(x + 1, y + 1),
                    self.cell_index(x + 1, y - 1)
                ]

                # Determine the number of alive neighbour cells
                alive_neighbours = 0
                for index in neighbour_indices:
                    if self.__cave[index]:
                        alive_neighbours += 1

                # Change the result cell state based on parameters supplied to the generator
                if self.__cave[current_index]:
                    if alive_neighbours < self.__starvationLimit or alive_neighbours > self.__overpopLimit:
                        result_cave[current_index] = False

                    else:
                        result_cave[current_index] = True

                else:
                    if alive_neighbours == self.__birthNumber:
                        result_cave[current_index] = True

        self.__cave = result_cave

    def generate_cave_image(self):
        """
        Generate an RGBA image of the level.

        :return: PIL Image type
        """
        img = PILImage.new("RGBA", size=(self.w, self.h))
        pixel_data = [(255, 255, 255, 255) for i in range(len(self.__cave))]
        for i in range(len(self.__cave)):
            pixel_data[i] = self.__pixel_colour(self.__cave[i])

            # Add blobs
            for blob_array_index in range(len(self.__blobs)):
                if self.__blobs[blob_array_index][i]:
                    pixel_data[i] = self.__blob_colours[blob_array_index]

        img.putdata(pixel_data)
        return img

    def init_cave(self, chanceToStartAlive):
        """
        Initialize the level.

        :param chanceToStartAlive: The chance that any given cell will start alive
        """
        self.__cave = []
        for cell in range(self.w * self.h):
            self.__cave.append(random.randint(0, 1000) <= chanceToStartAlive * 1000)

    def generate_blobs(self, colour, chance, appear_on_cell_state, max_number=None, min_number=None):
        """
        Generate a random blob map.

        :param colour: The colour of blobs in this map
        :param chance: The chance that any given cell that meets the conditions will be painted with this blob
        :param appear_on_cell_state: The blobs will only appear on this cell state
        :param max_number: The maximum number of blobs in the map
        :param min_number: The minimum number of blobs in the map
        """
        blobs = []
        number = 0
        if min_number is not None:
            while number < min_number:
                blobs = []
                number = 0
                for cell in self.__cave:
                    state = cell == appear_on_cell_state and random.randint(0, 1000) <= chance * 1000
                    if max_number is not None:
                        state = state and (number < max_number)

                    blobs.append(state)
                    if state:
                        number += 1

        else:
            for cell in self.__cave:
                state = cell == appear_on_cell_state and random.randint(0, 1000) <= chance * 1000
                if max_number is not None:
                    state = state and (number < max_number)

                blobs.append(state)
                if state:
                    number += 1

        self.__blobs.append(blobs)
        self.__blob_colours.append(colour)

    def validate_cave(self, start, end):
        """
        Ensure that the level is solvable.

        :param start: The start position
        :param end: The end position
        :return: The path of the end solution
        """
        solver = MazeSolver.Solver((self.w, self.h), self.__cave, start, end)
        path = solver.find_solution()
        return path


def create_cave():
    """
    Create a level (cave)
    :return: The cave generator object
    """
    gen = CaveGenerator(11, 11, 0.1, 1, 3, 2)

    for i in range(20):
        gen.generator_step()

    gen.generate_blobs((0, 255, 0, 255), 0.05, False)         # Time increase blobs (green)
    gen.generate_blobs((255, 0, 0, 255), 0.2, True)           # Spike blobs (red)
    gen.generate_blobs((255, 0, 255, 255), 0.2, False, 1, 1)  # End blob (purple)
    gen.generate_blobs((0, 0, 255, 255), 0.2, False, 1, 1)    # Start blob (blue)

    return gen

if __name__ == "__main__":
    # Keep generating random caves until a solvable one is found
    cave = create_cave()
    cave_img = cave.generate_cave_image()
    cave_img_data = list(cave_img.getdata())
    start = (-1, -1)
    end = (-1, -1)
    for i in range(len(cave_img_data)):
        if cave_img_data[i] == (0, 0, 255, 255):
            start = cave.cell_position(i)

        if cave_img_data[i] == (255, 0, 255, 255):
            end = cave.cell_position(i)

    while cave.validate_cave(start, end):
        cave = create_cave()
        cave_img = cave.generate_cave_image()
        cave_img_data = list(cave_img.getdata())
        start = (-1, -1)
        end = (-1, -1)
        for i in range(len(cave_img_data)):
            if cave_img_data[i] == (0, 0, 255, 255):
                start = cave.cell_position(i)

            if cave_img_data[i] == (255, 0, 255, 255):
                end = cave.cell_position(i)

        print(cave.validate_cave(start, end))

    # Save the solvable cave image
    cave_img.save("Cave.png")
