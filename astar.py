import os
import sys
from os import listdir

class Node:
    def __init__(self, x, y, blocked):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.blocked = blocked
        self.visited = False 
        


    

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
        algo = raw_input('''Enter "f" for RFA*, "b" for RBA*, or "a" for AA*.\n''')
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
    print('\n')
    #Preconceived start and goal nodes 
    startx = 4
    starty = 2
    goalx = 4
    goaly = 4

    print(array[0][0].x)
    print(array[0][0].y)
    print(array[0][0].blocked)


    if algo == 'f':
        print("Executing Repeated Forward A*")
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
    

#Compute Manhattan Distance between 2 nodes
def manDis(x1,y1,x2,y2):
    return(abs(x2-x1)+abs(y2-y1)) 



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







