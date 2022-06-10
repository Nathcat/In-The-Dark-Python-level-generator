class Maze:
    def __init__(self, w, h, data):
        self.w, self.h, self.data = w, h, data

    def get_point(self, p):
        x, y = p
        return self.data[(y * self.w) + x]


class Node:
    def __init__(self, parent_node_position, position, maze):
        self.x, self.y = position
        self.visited = False

        adjacent_node_positions = [
            (self.x, self.y - 1),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x - 1, self.y)
        ]

        empty_pass = False
        while not empty_pass:
            empty_pass = True
            for i in range(len(adjacent_node_positions)):
                if adjacent_node_positions[i] == parent_node_position:
                    del adjacent_node_positions[i]
                    empty_pass = False
                    break

                elif adjacent_node_positions[i][0] < 0 or adjacent_node_positions[i][0] >= maze.w:
                    del adjacent_node_positions[i]
                    empty_pass = False
                    break

                elif adjacent_node_positions[i][1] < 0 or adjacent_node_positions[i][1] >= maze.h:
                    del adjacent_node_positions[i]
                    empty_pass = False
                    break

                elif not maze.get_point(adjacent_node_positions[i]):
                    del adjacent_node_positions[i]
                    empty_pass = False
                    break

        self.adjacent_nodes = [Node(position, node_position, maze) for node_position in adjacent_node_positions]


class Solver:
    def __init__(self, size, m, start, end):
        w, h = size
        self.__start = start
        self.__end = end
        self.__maze = Maze(w, h, m)
        self.__start_node = Node((-1, -1), self.__start, self.__maze)
        self.__current_path = []
        self.__solution_paths = []

        self.__visit_node(self.__start_node)

    def __visit_node(self, node):
        node.visited = True
        self.__current_path.append((node.x, node.y))

        if (node.x, node.y) == self.__end:
            self.__solution_paths.append(self.__current_path)

        for adjacent_node in node.adjacent_nodes:
            self.__visit_node(adjacent_node)

    def find_solution(self):
        if len(self.__solution_paths) == 0:
            return None

        shortest_path_index = None
        shortest_path_length = 99999999999
        for i in range(len(self.__solution_paths)):
            if len(self.__solution_paths[i]) < shortest_path_length:
                shortest_path_index = i

        return self.__solution_paths[shortest_path_index]
