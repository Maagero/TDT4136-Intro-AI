import math
import csv
from PIL import Image
import Map

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

def astar(map, start, end):
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
        # print(curr_node.position)

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
            if node_pos[0] >(len(map)-1) or node_pos[0]<0 or node_pos[1] > (len(map[len(map)-1]) -1) or node_pos[1] < 0:
                continue
            if map[node_pos[0]][node_pos[1]] != 0:
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
                if child==open_node and child.g >= open_node.g:
                    isInOpen = True
            if isInOpen:
                continue


            open.append(child)


def read_map(map_file):
    map = []
    with open(map_file) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=",")
        for row in csv_reader:
            map.append(row)
        for i in range(len(map)):
            for j in range(len(map[0])):
                # print(map[i][j])
                if map[i][j]=="1":
                    map[i][j]=0
                if map[i][j]=="-1":
                    map[i][j]=1
                if map[i][j]=="2":
                    map[i][j]=0
                if map[i][j]=="3":
                    map[i][j]=0
                if map[i][j]=="4":
                    map[i][j]=0
    return map

def main():
    task = 2
    mapper = Map.Map_Obj(task=task)
    start, end, end_goal_pos, path_to_map = mapper.fill_critical_positions(task)
    map = read_map(path_to_map)
    path = astar(map, tuple(start), tuple(end))

    for i in path:
        mapper.replace_map_values(i,7,end_goal_pos)
    mapper.show_map()

if __name__ == '__main__':
    main()
