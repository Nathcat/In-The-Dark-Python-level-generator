from PIL import Image as PILImage
import random
import MazeSolver


class CaveGenerator:
    def __init__(self, w, h, chanceToStartAlive, starvationLimit, overpopLimit, birthNumber):
        self.w = w
        self.h = h
        self.__starvationLimit = starvationLimit
        self.__overpopLimit = overpopLimit
        self.__birthNumber = birthNumber
        self.__cave = []
        self.__blobs = []
        self.__blob_colours = []

        self.init_cave(chanceToStartAlive)

    def cell_index(self, x, y):
        return (y * self.w) + x

    def cell_position(self, index):
        return index % self.w, index // self.w

    def __pixel_colour(self, cell):
        if cell:
            return (0, 0, 0, 255)

        else:
            return (255, 255, 255, 255)

    def generator_step(self):
        result_cave = [cell for cell in self.__cave]

        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                current_index = self.cell_index(x, y)

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

                alive_neighbours = 0
                for index in neighbour_indices:
                    if self.__cave[index]:
                        alive_neighbours += 1

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
        img = PILImage.new("RGBA", size=(self.w, self.h))
        pixel_data = [(255, 255, 255, 255) for i in range(len(self.__cave))]
        for i in range(len(self.__cave)):
            pixel_data[i] = self.__pixel_colour(self.__cave[i])

            for blob_array_index in range(len(self.__blobs)):
                if self.__blobs[blob_array_index][i]:
                    pixel_data[i] = self.__blob_colours[blob_array_index]

        img.putdata(pixel_data)
        return img

    def init_cave(self, chanceToStartAlive):
        self.__cave = []
        for cell in range(self.w * self.h):
            self.__cave.append(random.randint(0, 1000) <= chanceToStartAlive * 1000)

    def generate_blobs(self, colour, chance, appear_on_cell_state, max_number=None, min_number=None):
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
        solver = MazeSolver.Solver((self.w, self.h), self.__cave, start, end)
        path = solver.find_solution()
        return path


def create_cave():
    gen = CaveGenerator(11, 11, 0.1, 1, 3, 2)

    for i in range(20):
        gen.generator_step()

    gen.generate_blobs((0, 255, 0, 255), 0.05, False)
    gen.generate_blobs((255, 0, 0, 255), 0.2, True)
    gen.generate_blobs((255, 0, 255, 255), 0.2, False, 1, 1)
    gen.generate_blobs((0, 0, 255, 255), 0.2, False, 1, 1)

    return gen

if __name__ == "__main__":
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

    cave_img.save("Cave.png")
