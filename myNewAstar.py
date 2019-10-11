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
        self.g = 99999
        self.h = 99999
        self.f = 99999
        self.parent = None
        self.blocked = blocked
        self.onPath =  False


    def __lt__(self, other): 
        return self.f < other.f
    def __le__(self, other):
        return self.f <= other.f
    def __gt__(self, other):
        return self.f > other.f 
    def __ge__(self, other):
        return self.f >= other.f
    def __eq__(self, other):
        return (self.f == other.f) and (self.x == other.x) and (self.y == other.y) and (self.g == other.g) and (self.h == other.h) and (self.parent == other.parent) and (self.blocked == other.blocked)    

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
    realArray, agentArray = loadMazes(mazeNum)
    execute(agentArray, realArray, algo)

#Take in maze number and return 2D array
def loadMazes(mazeNum):
    realArray = []
    agentArray = []
    for f in listdir("mazes"):
        if f == "maze" + str(mazeNum) + ".txt":
            file = open(os.getcwd() + "/mazes/" + f)
            temp = file.read().splitlines()
            i = 0
            for item in temp:
                realSubArray = []
                agentSubArray = []
                j = 0 
                for index in item:
                    if index == 'X':
                        realSubArray.append(Node(i,j,True))
                        agentSubArray.append(Node(i,j,False))
                    elif index == 'S':
                        realSubArray.append(Node(i,j,False))
                        agentSubArray.append(Node(i, j, False))
                    else:
                        realSubArray.append(Node(i,j,False))
                        agentSubArray.append(Node(i,j,False))
                    j += 1
                realArray.append(realSubArray)
                agentArray.append(agentSubArray)
                i += 1
    return realArray, agentArray

def execute(agentArray, realArray, algo):
    if algo == 'f':
        print("Executing Repeated Forward A*")
        goal = realArray[len(realArray)-1][len(realArray[0])-1]
        curr = realArray[4][2]
        while(curr != goal):
            print("New Start is: " + '(' + str(curr.x) + ',' + str(curr.y) + ')')
            #Return a path from 
            path = aStar(curr,goal,agentArray, realArray)
            if(len(path) == 0):
                print("No path found")
                return 
            else:
                curr = followPath(path,realArray,True)

        return
    elif algo == 'b':
        print("Executing Repeated Backward A*")
    else: 
        print("Executing Adaptive A*")


def aStar(tempStart, tempGoal, agentArray, realArray):
    openList = []
    closeList = []
    start = agentArray[tempStart.x][tempStart.y]
    curr = agentArray[start.x][start.y]
    goal = agentArray[tempGoal.x][tempGoal.y]
    curr.g = 0
    curr.h = manDis(curr.x, curr.y, goal.x, goal.y)

    #Discover and record any immediate blocked neighbors
    immediateNeighbors = getNeighbors(curr, agentArray)
    for cell in immediateNeighbors:
        if(realArray[cell.x][cell.y].blocked):
            cell.blocked = True
            closeList.append(cell)


    while(curr != goal):
        neighbors = getNeighbors(curr, agentArray)
        for cell in neighbors:
            if cell not in openList and cell not in closeList: 
                if cell.blocked:
                    closeList.append(cell)
                else: 
                    heapq.heappush(openList, cell)
                    cell.g = curr.g + 1
                    cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                    cell.f = cell.g + cell.h
                    cell.parent = curr 
        closeList.append(curr)
        if(len(openList) >= 1):
            curr = heapq.heappop(openList)
        else:
            noPath = []
            return noPath

    #Return the path from start to tempGoal
    path=[]
    ptr2=goal
    while (ptr2 != start):
        path.insert(0, ptr2)
        ptr2 = ptr2.parent
    #adding start to the path
    path.insert(0,ptr2)
    return path


def followPath(path, realArray, new):
    i=0
    for item in path:
        if (realArray[item.x][item.y].blocked):
            return realArray[item.parent.x][item.parent.y]
        else:
            #print everything llike normal using print maze, but there is a currnt we also send in and that is the 
            if(new and i==0):
                i+=1
                #do nothing
            else:
                printMaze(4,2,realArray,[],realArray[item.x][item.y])
    return realArray[item.x][item.y]


#Get the new starting point for computePath
def getNewStart(start, goal, array):
    result = goal
    while(goal != None and goal != start):
        if(goal.blocked):
            result = goal.parent
        goal = goal.parent
    print('New start: (' + str(result.x) + ',' + str(result.y) + ')')
    return result.x, result.y

#List coordinates taken
def listPath(holder ,goal, array):
    
    print("***GOAL***")
    while(goal.parent != holder and goal.parent != None):
        print('(' + str(goal.x) + ',' + str(goal.y) + ')')
        goal = goal.parent
        goal.onPath = True
    print('(' + str(goal.x) + ',' + str(goal.y) + ')')
    print("***START***\n")

#Print the values in a given list
def printList(nodelist):
    for item in nodelist:
        print('(' + str(item.x) + ',' + str(item.y) +')' + "f-value: " + str(item.f))

#Print maze with path
def printMaze(startx, starty,array,closeList, curr):
    print("Maze:" + '\n' + "----------")
    for line in array:
        for item in line:
            if(item.x == startx and item.y == starty):
                sys.stdout.write('S')
            elif(item.x == len(array)-1 and item.y == len(array[0])-1):
                sys.stdout.write('E')
            elif(item.onPath):
                sys.stdout.write('.')
                item.onPath = False
            elif(item.blocked):
                sys.stdout.write('X')
            elif(item==curr):
                sys.stdout.write('A')
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







