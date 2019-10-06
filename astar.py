import os
import sys
import math
import heapq
from heapq import heappush
from os import listdir

class Node:
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")
        self.parent = None
        self.blocked = blocked
        self.visited = False 

    def __lt__(self, other): 
        return self.f < other.f
    def __gt__(self, other):
        return self.f > other.f 
    def __eq__(self, other):
        return self.f == other.f
        

def promptUser():
    #Prompt user for maze number 
    while True: 
        mazeNum = input("Enter a maze number between 1 and 50 (inclusive).\n")
        if(mazeNum > 50 or mazeNum < 1):
            print("Improper input. Try again.\n")
        else:
            break

    #Pompt user for algorithm
    while True: 
        algo = raw_input('''Enter F for FORWARD, B for BACKWARD, or A for ADAPTIVE.\n''')
        if(algo != 'f' and algo != 'b' and algo != 'a'):
            print("Improper input. Try again.\n")
        else: 
            break

    #Parse maze number to get txt file and convert to 2D array
    array = loadMaze(mazeNum)
    execute(array,algo)

#Take in maze number and return 2D array
def loadMaze(mazeNum):
    array = []
    for f in listdir("mazes"):
        if f == "maze" + str(mazeNum) + ".txt":
            file = open(os.getcwd() + "/mazes/" + f)
            
            temp = file.read().splitlines()
            i = 0
            for item in temp:
                subArray = []
                j = 0 
                for index in item:
                    if index == 'X':
                        subArray.append(Node(i,j,True))
                    else:
                        subArray.append(Node(i,j,False))
                    j += 1
                array.append(subArray)
                i += 1
    return array


def execute(array, algo):
    if algo == 'f':
        print("Executing Repeated Forward A*")

        openlist = []
        closelist = []
        goal = array[len(array)-1][len(array[0])-1]

        #Calculate and set h-value for starting point
        array[4][2].g = 0
        array[4][2].h = manDis(array[4][2].x,array[4][2].y,goal.x,goal.y)
        array[4][2].f = array[4][2].g + array[4][2].h
        curr = array[4][2]
        heapq.heappush(openlist,curr)
        while(curr != goal):
            neighbors = getNeighbors(curr,array)
            for node in neighbors:
                if (node not in openlist and node not in closelist and node.blocked == False):
                    heapq.heappush(openlist,node)
                    heapq.heapify(openlist)
                    node.g = curr.g + 1
                    node.h = manDis(curr.x,curr.y,goal.x,goal.y)
                    f = node.g + node.h
                    if (f < node.f):
                        node.f = f
                        node.parent = curr
            closelist.append(curr)
            curr = heapq.heappop(openlist)
        print("Finished Forward")
        printPath(goal,array)

    elif algo == 'b':
        print("Executing Repeated Backward A*")
    else: 
        print("Executing Adaptive A*")

    print("Maze:" + '\n' + "----------")
    for line in array:
        for item in line:
            if(item.x == 0 and item.y == 0):
                sys.stdout.write('S')
            elif(item.x == 4 and item.y == 4):
                sys.stdout.write('E')
            elif(item.blocked):
                sys.stdout.write('X')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
    print("----------")
    

def printPath(goal, array):
    while(goal.parent != None):
        print('(' + str(goal.x) + ',' + str(goal.y) + ')')
        goal = goal.parent
    print('(' + str(goal.x) + ',' + str(goal.y) + ')')


#Compute Manhattan Distance between 2 nodes
def manDis(x1,y1,x2,y2):
    return(abs(x2-x1)+abs(y2-y1)) 



#Get the neighbors of a node and return them in an array 
def getNeighbors(curr, array):
    neighbors = []
    if(curr.x == 0 and curr.y == 0):                             #Top left corner 
        neighbors.append(array[curr.x][curr.y+1])
        neighbors.append(array[curr.x+1][curr.y])
        return neighbors
    elif (curr.x == 0 and curr.y == len(array)-1):               #Top right corner
        neighbors.append(array[curr.x+1][curr.y])
        neighbors.append(array[curr.x][curr.y-1])
        return neighbors
    elif (curr.x == len(array[0])-1 and curr.y == 0):            #Bottom left corner
        neighbors.append(array[curr.x-1][curr.y])
        neighbors.append(array[curr.x][curr.y+1])
        return neighbors
    elif (curr.x == len(array[0])-1 and curr.y == len(array)-1): #Bottom right corner
        neighbors.append(array[curr.x][curr.y-1])
        neighbors.append(array[curr.x-1][curr.y])
        return neighbors
    elif(curr.x == 0):                                           #Top edge
        neighbors.append(array[curr.x+1][curr.y])
        neighbors.append(array[curr.x][curr.y+1])
        neighbors.append(array[curr.x][curr.y-1])
        return neighbors
    elif(curr.x == len(array)-1):                                #Bottom edge
        neighbors.append(array[curr.x-1][curr.y])
        neighbors.append(array[curr.x][curr.y+1])
        neighbors.append(array[curr.x][curr.y-1])
        return neighbors
    elif(curr.y == 0):                                            #Left edge
        neighbors.append(array[curr.x][curr.y+1])
        neighbors.append(array[curr.x+1][curr.y])
        neighbors.append(array[curr.x-1][curr.y])
        return neighbors   
    elif(curr.y == len(array[0])-1):                             #Right edge
        neighbors.append(array[curr.x][curr.y-1])
        neighbors.append(array[curr.x+1][curr.y])
        neighbors.append(array[curr.x-1][curr.y])
        return neighbors       
    else:                                                        #Center node returns 4 neighbors
        neighbors.append(array[curr.x+1][curr.y])
        neighbors.append(array[curr.x-1][curr.y])
        neighbors.append(array[curr.x][curr.y+1])
        neighbors.append(array[curr.x][curr.y-1])
        return neighbors




promptUser()










# import turtle
# import random 

# window = turtle.Screen()
# window.bgcolor("white")
# window.title("A*")
# window.setup(1030,1030)

# class Pen(turtle.Turtle):
#     def __init__(self):
#         turtle.Turtle.__init__(self)
#         self.shape("square")
#         self.color("black")
#         self.penup()
#         self.speed(0)

# mazes = [""]

# maze_1 = []

# for i in range(103):
#     if (i == 0 or i == 102):
#         string = ""
#         for j in range(103):
#             string = string + "X"
#         maze_1.append(string)
#     else:
#         string = ""
#         string = string + "X"
#         for k in range (101):
#             temp = random.randint(1,100)
#             if temp > 70:
#                 string = string + "X"
#             else:
#                 string = string + " "
#         string = string + "X"
#         maze_1.append(string)

# print('\n'.join(maze_1))
# mazes.append(maze_1)


# def setup_maze(maze):
#     for y in range(len(maze)):
#         for x in range(len(maze[y])):
#             character = maze[y][x]
#             screen_x = -510 + (x*10)
#             screen_y = 510 - (y*10)

#             if character == "X":
#                 pen.goto(screen_x, screen_y)
#                 pen.stamp()


# pen = Pen()


# setup_maze(mazes[1])

# while True:
#     pass







