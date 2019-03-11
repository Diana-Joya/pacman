from vector import Vector
from settings import Settings
from stacks import Stack
from numpy import loadtxt
from maze_assets import *


class Node(object):
    def __init__(self, screen, row, column, depth):
        self.row, self.column, self.depth = row, column, depth
        self.settings = Settings()
        self.screen = screen
        self.maze_offset = 16
        self.position = Vector(self.maze_offset+column*self.settings.node_width,
                               self.maze_offset+row*self.settings.node_height, self.depth)
        self.neighbors = {}

    def render(self):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(self.screen, (255, 255, 255), self.position.toTuple(),
                                 self.neighbors[n].position.toTuple(), 4)
                pygame.draw.circle(self.screen, (255, 0, 0), self.position.toTuple(), 12)


class NodeGroup(object):
    def __init__(self, screen, level):
        self.settings = Settings()
        self.screen = screen
        self.level = level

        self.type_of_node = ["+", "n", "N", "o"]
        self.ghost_node = ["v"]
        self.type_of_path = ["p", "P"]

        self.nodeList = []
        self.ghostList = []

        self.grid = None
        self.nodeStack = Stack()
        self.create_node_list()

    def create_node_list(self):
        self.grid = loadtxt(self.level, dtype=str)
        self.num_rows, self.num_columns = len(self.grid), len(self.grid[0])
        startNode = self.find_first_node(self.num_rows, self.num_columns)
        self.nodeStack.push(startNode)
        while not self.nodeStack.is_empty():
            node = self.nodeStack.pop()
            self.addNode(node, self.nodeList)
            leftNode = self.get_path_node(self.settings.left, node.row, node.column-1, self.nodeList)
            rightNode = self.get_path_node(self.settings.right, node.row, node.column+1, self.nodeList)
            upNode = self.get_path_node(self.settings.up, node.row-1, node.column, self.nodeList)
            downNode = self.get_path_node(self.settings.down, node.row+1, node.column, self.nodeList)
            node.neighbors[self.settings.up] = upNode
            node.neighbors[self.settings.down] = downNode
            node.neighbors[self.settings.left] = leftNode
            node.neighbors[self.settings.right] = rightNode
            self.add_node_to_stack(leftNode, self.nodeList)
            self.add_node_to_stack(rightNode, self.nodeList)
            self.add_node_to_stack(upNode, self.nodeList)
            self.add_node_to_stack(downNode, self.nodeList)

    def find_first_node(self, rows, columns):
        nodeFound = False
        for row in range(rows):
            for column in range(columns):
                if self.grid[row][column] in self.type_of_node:
                    return Node(self.screen, row, column, 0)
                if self.grid[row][column] in self.ghost_node:
                    return Node(self.screen, row, column, 0)
        return None

    def addNode(self, node, nodeList):
        nodeInList = self.nodeInList(node, nodeList)
        if not nodeInList:
            nodeList.append(node)

    def add_ghost_Node(self, node, ghostList):
        nodeInList = self.nodeInList(node, ghostList)
        if not nodeInList:
            ghostList.append(node)

    def get_node(self, x, y, z, nodeList=[]):
        for node in nodeList:
            if node.position.x == x and node.position.y == y and node.position.z == z:
                return node
        return None

    def get_node_from_node(self, node, nodeList):
        if node is not None:
            for inode in nodeList:
                if node.row == inode.row and node.column == inode.column and node.depth == inode.depth:
                    return inode
            return node

    def get_path_node(self, direction, row, column, nodeList):
        tempNode = self.followPath(direction, row, column)
        return self.get_node_from_node(tempNode, nodeList)

    def add_node_to_stack(self, node, nodeList):
        if node is not None and not self.nodeInList(node, nodeList):
            self.nodeStack.push(node)

    def nodeInList(self, node, nodeList):
        for inode in nodeList:
            if node.position.x == inode.position.x and node.position.y == inode.position.y and node.position.z == inode.position.z:
                return True
        return False

    def followPath(self, direction, row, column):
        if direction == self.settings.left and column >= 0:
            return self.pathToFollow(self.settings.left, row, column, "-")
        elif (direction == (self.settings.right)) and column < self.num_columns:
            return self.pathToFollow(self.settings.right, row, column, "-")
        elif direction == self.settings.up and row >= 0:
            return self.pathToFollow(self.settings.up, row, column, "|")
        elif direction == self.settings.down and row < self.num_rows:
            return self.pathToFollow(self.settings.down, row, column, "|")
        else:
            return None

    def pathToFollow(self, direction, row, col, path):
        tempSymbols = [path] + self.type_of_node + self.type_of_path + self.ghost_node
        if self.grid[row][col] in tempSymbols:
            while self.grid[row][col] not in self.type_of_node:
                if direction is self.settings.left:
                    col -= 1
                elif direction is self.settings.right:
                    col += 1
                elif direction is self.settings.up:
                    row -= 1
                elif direction is self.settings.down:
                    row += 1
            node = Node(self.screen, row, col, 0)
            if self.grid[row][col] in self.ghost_node:
                self.ghostList.append(self.grid[row][col])
            return node
        else:
            return None

    def render(self):
        for node in self.nodeList:
            node.render()
