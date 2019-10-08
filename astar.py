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

        openList = []
        closeList = []

        goal = array[len(array)-1][len(array[0])-1]
        curr = array[4][2]
        while(curr != goal):
            computePath(curr, goal, array, openList, closeList)
            return
            closeList.append(curr)
            curr = heapq.heappop(openList)
            #printMaze(curr,array)
        #End while

    elif algo == 'b':
        print("Executing Repeated Backward A*")
    else: 
        print("Executing Adaptive A*")

#Function that takes in "starting" point and computes best path to goal without regard for blocked cells 
def computePath(curr, goal, array, openList, closeList):
    curr.g = 0
    curr.h = manDis(curr.x, curr.y, goal.x, goal.y)
    curr.f = curr.g + curr.h
    print("closeList size: " + str(len(closeList)))
    #Mark initial neighbors as visited 
    initialNeighbors = getNeighbors(curr, array)
    for cell in initialNeighbors:
        print("Checking: " + str(cell.x) + ',' + str(cell.y))
        sys.stdout.write("closeList: ")
        printList(closeList)
        if cell not in openList and cell not in closeList:
            print("Entered If Statement")
            cell.visited = True
            if cell.blocked:
                closeList.append(cell)
            else:
                heapq.heappush(openList, cell)
        else: 
            if(cell in openList):
                print("cell in openList")
            else: 
                print("cell in closeList")
    
    while(curr != goal):
        neighbors = getNeighbors(curr, array)
        for cell in neighbors:
            if(cell not in closeList and cell not in openList):
                if(cell.blocked):
                    closeList.append(cell)
                else:
                    heapq.heappush(openList, cell)
                    cell.g = curr.g + 1
                    cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                    f = cell.g + cell.h 
                    if(f < cell.f):
                        cell.f = f
                        cell.parent = curr
        if(len(openList) != 0):
            curr = heapq.heappop(openList)
            print("Curr: " + '(' + str(curr.x) + ',' + str(curr.y) + ')') 
        else: 
            print("Path does not exist.")
            break
        #End if else 
    #End while
    listPath(goal,array)
#End computePath


def inList(somelist, element):
    return element in somelist


#List coordinates taken
def listPath(goal, array):
    print("Path: \n")
    print("***GOAL***")
    while(goal.parent != None):
        print('(' + str(goal.x) + ',' + str(goal.y) + ')')
        goal = goal.parent
    print('(' + str(goal.x) + ',' + str(goal.y) + ')')
    print("***START***\n")



def printList(nodelist):
    for item in nodelist:
        print('(' + str(item.x) + ',' + str(item.y) +')')



#Print maze with path
def printMaze(start,array):
    print("Maze:" + '\n' + "----------")
    for line in array:
        for item in line:
            if(item.x == start.x and item.y == start.y):
                sys.stdout.write('S')
            elif(item.x == len(array)-1 and item.y == len(array[0])-1):
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







