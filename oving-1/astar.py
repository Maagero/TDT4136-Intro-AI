import math

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):

    closed = []
    open = []
    print("Start")
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open.append(start_node)

    while len(open) > 0:
        curr_node = open[0]
        curr_index = 0
        for index, node in enumerate(open):
            if node.f < curr_node.f:
                curr_node = node
                curr_index = index

        open.pop(curr_index)
        closed.append(curr_node)
        print(curr_node.position)

        if curr_node==end_node:
            path = []
            curr = curr_node
            while curr is not None:
                path.append(curr.position)
                curr = curr.parent
            return path[::-1]


        children = []
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_pos = (curr_node.position[0] + new_pos[0], curr_node.position[1] + new_pos[1])
            if node_pos[0] >(len(maze)-1) or node_pos[0]<0 or node_pos[1] > (len(maze[len(maze)-1]) -1) or node_pos[1] < 0:
                continue
            if maze[node_pos[0]][node_pos[1]] != 0:
                continue

            new_node = Node(curr_node,node_pos)
            children.append(new_node)

        for child in children:
            isClosed = False
            for closed_child in closed:
                if child==closed_child:
                    isClosed = True
            if isClosed:
                continue

            child.g = curr_node.g + 1
            child.h = (abs(child.position[0] - end_node.position[0])) + (abs(child.position[1] - end_node.position[1]))
            child.f = child.g + child.h

            isInOpen = False
            for open_node in open:
                if child==open_node and child.g > open_node.g:
                    isInOpen = True
            if isInOpen:
                continue


            open.append(child)






def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (0, 9)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()
