class Maze:
    """
    Stores Maze data.
    """
    def __init__(self, w, h, data):
        self.w, self.h, self.data = w, h, data

    def get_point(self, p):
        """
        Get the state of a point on the maze.

        :param p: The point (x, y)
        :return: Boolean state of the point
        """
        x, y = p
        return self.data[(y * self.w) + x]


class Node:
    """
    Graph node on the maze
    """
    def __init__(self, parent_node_position, position, maze):
        self.x, self.y = position    # The position of this node
        self.visited = False

        adjacent_node_positions = [  # The positions of adjacent nodes
            (self.x, self.y - 1),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x - 1, self.y)
        ]

        # Clean the adjacent nodes list until all are valid, ie must be in bounds of the maze, and must be empty
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

        # Create the node objects adjacent to this one recursively
        self.adjacent_nodes = [Node(position, node_position, maze) for node_position in adjacent_node_positions]


class Solver:
    """
    Solves a given maze object from start to end
    """
    def __init__(self, size, m, start, end):
        w, h = size                                                    # Define the size of the maze
        self.__start = start                                           # Define the start of the maze
        self.__end = end                                               # Define the end of the maze
        self.__maze = Maze(w, h, m)                                    # Create the maze object
        self.__start_node = Node((-1, -1), self.__start, self.__maze)  # Recursively create the Node objects from the start node
        self.__current_path = []                                       # Stores the current path through the maze
        self.__solution_paths = []                                     # Stores paths from start to end

        self.__visit_node(self.__start_node)                           # Start recursively traversing the graph from the start node

    def __visit_node(self, node):
        # Visit a node and add it to the current path
        node.visited = True
        self.__current_path.append((node.x, node.y))

        # If the node is at the end point, add this path to the solution paths
        if (node.x, node.y) == self.__end:
            self.__solution_paths.append(self.__current_path)

        # Visit nodes adjacent to this one recursively
        for adjacent_node in node.adjacent_nodes:
            self.__visit_node(adjacent_node)

    def find_solution(self):
        """
        Get the shortest solution to the maze, or none if there is no solution
        :return: The shortest solution to the maze, or none
        """
        if len(self.__solution_paths) == 0:
            return None

        shortest_path_index = None
        shortest_path_length = 99999999999
        for i in range(len(self.__solution_paths)):
            if len(self.__solution_paths[i]) < shortest_path_length:
                shortest_path_index = i

        return self.__solution_paths[shortest_path_index]
