import math
import csv
from PIL import Image
import Map

#The node with posision, g, h, f and a parent (for finding the shortest path)
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    #When comparing nodes, only compare the position, so the g, h and f can be different
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

        #Choose the most promising node in open list
        for index, node in enumerate(open):
            if node.f < curr_node.f:
                curr_node = node
                curr_index = index

        open.pop(curr_index)
        closed.append(curr_node)

        #Check if you found the end node
        if curr_node==end_node:
            path = []
            curr = curr_node
            #Return a representation of the shortes path
            while curr is not None:
                path.append(curr.position)
                curr = curr.parent
            return path[::-1]

        #Finding the children to the most promesning node
        children = []
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_pos = (curr_node.position[0] + new_pos[0], curr_node.position[1] + new_pos[1])
            #If it is "out of bounds" then don't follow up on this child
            if node_pos[0] >(len(map)-1) or node_pos[0]<0 or node_pos[1] > (len(map[len(map)-1]) -1) or node_pos[1] < 0:
                continue
            #If it is a wall then dont follow up on the child.
            if map[node_pos[0]][node_pos[1]] == -1:
                continue

            new_node = Node(curr_node,node_pos)
            children.append(new_node)

        for child in children:
            isClosed = False
            #make sure the children aint closed already
            for closed_child in closed:
                if child==closed_child:
                    isClosed = True
            if isClosed:
                continue

            #Calculate the g, h and f of the children node
            child.g = curr_node.g + map[child.position[0]][child.position[1]]
            child.h = (abs(child.position[0] - end_node.position[0])) + (abs(child.position[1] - end_node.position[1]))
            child.f = child.g + child.h

            #Don't add it to open if open allready contains a better or equally good way to get to this node
            isInOpen = False
            for open_node in open:
                if child==open_node and child.g >= open_node.g:
                    isInOpen = True
            if isInOpen:
                continue

            #add the child to open
            open.append(child)

#Function to read the map from a cvs file to an two dimentional array
def read_map(map_file):
    txMap = []
    map = []

    with open(map_file) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=",")
        for row in csv_reader:
            txMap.append(row)
        for i in range(len(txMap)):
            mapLine = []
            for j in range(len(txMap[0])):
                mapLine.append(int(txMap[i][j]))
            map.append(mapLine)
    return map

def main():
    # set task to any task in map.py to test different tasks
    # PARAMETER task: Choose which task to test
    task = 2
    mapper = Map.Map_Obj(task=task)
    start, end, end_goal_pos, path_to_map = mapper.fill_critical_positions(task)
    map = read_map(path_to_map)
    # Set path using the astar algorithm
    path = astar(map, tuple(start), tuple(end))
    # Replace each point on the path
    for i in path:
        mapper.replace_map_values(i,7,end_goal_pos)
    # Show map
    mapper.show_map()

if __name__ == '__main__':
    main()
