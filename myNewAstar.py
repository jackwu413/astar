import os
import sys
import math
import heapq
from heapq import heappush
from os import listdir

class Node:
    def __init__(self, x, y, blocked, start):
        self.x = x
        self.y = y
        self.g = 99999
        self.h = 99999
        self.f = 99999
        self.parent = None
        self.blocked = blocked
        self.visited = False
        self.onPath =  False
        self.isStart = start


    def __lt__(self, other): 
        return self.f < other.f
    def __le__(self, other):
        return self.f <= other.f
    def __gt__(self, other):
        return self.f > other.f 
    def __ge__(self, other):
        return self.f >= other.f
    def __eq__(self, other):
        return (self.f == other.f) and (self.x == other.x) and (self.y == other.y) and (self.g == other.g) and (self.h == other.h) and (self.parent == other.parent) and (self.blocked == other.blocked) and (self.visited == other.visited) and (self.isStart == other.isStart)      

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
                        realSubArray.append(Node(i,j,True, False))
                        agentSubArray.append(Node(i,j,False, False))
                    elif index == 'S':
                        realSubArray.append(Node(i,j,False, True))
                        agentSubArray.append(Node(i, j, False, True))
                    else:
                        realSubArray.append(Node(i,j,False, False))
                        agentSubArray.append(Node(i,j,False, False))
                    j += 1
                realArray.append(realSubArray)
                agentArray.append(agentSubArray)
                i += 1
    return realArray, agentArray

def aStar(start, goal, agentArray, realArray):
    openList = []
    closeList = []
    curr = start
    curr.g = 0
    curr.h = manDis(curr.x, curr.y, goal.x, goal.y)


    #Discover and record any immediate blocked neighbors
    immediateNeighbors = getNeighbors(curr, agentArray)
    for cell in immediateNeighbors:
        if(realArray[cell.x][cell.y].blocked):
            cell.blocked = True
            closeList.append(cell)


    while(curr != goal):
        print("Curr is: " + '(' + str(curr.x) + ',' + str(curr.y) + ')')
        neighbors = getNeighbors(curr, agentArray)
        for cell in neighbors:
            print("\tChecking neighbor: " + '(' + str(cell.x) + ',' + str(cell.y) + ')')
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
        curr = heapq.heappop(openList)
    #Print the path 
    print("********GOAL********")
    while(goal != start and goal != None):
        print('(' + str(goal.x) + ',' + str(goal.y) + ')')
        goal = goal.parent
    print("********START********")



def execute(agentArray, array, algo):
    if algo == 'f':
        print("Executing Repeated Forward A*")

        openList = []
        closeList = []

        goal = array[len(array)-1][len(array[0])-1]
        curr = array[4][2]
        aStar(curr,goal,agentArray, array)
        return
        i = 0
        while(curr != goal):
            i += 1
            curr = computePath(curr, goal, array, openList, closeList)
            print("gCL size: " + str(len(closeList)))
            if(i == 2):
                return
            #return
            # closeList.append(curr)
            # curr = heapq.heappop(openList)
            #printMaze(curr,array)
        #End while
    #End if
    elif algo == 'b':
        print("Executing Repeated Backward A*")
    else: 
        print("Executing Adaptive A*")

#Function that takes in "starting" point and computes best path to goal without regard for blocked cells 
def computePath(start, goal, array, openList, closeList):
    print("Start: " + '(' + str(start.x) + ',' + str(start.y) + ')')

    startx = start.x
    starty = start.y
    privateCloseList = list(closeList)

    print("privateCloseList: ")
    printList(privateCloseList)
    print("openList: ")
    printList(openList)
    print("closeList: ")
    printList(closeList)

    curr = start
    curr.g = 0
    curr.h = manDis(curr.x, curr.y, goal.x, goal.y)
    curr.f = curr.g + curr.h
    #Mark initial neighbors as visited 
    initialNeighbors = getNeighbors(curr, array)
    for cell in initialNeighbors:
        print("Neighbor: " + '(' + str(cell.x) + ',' + str(cell.y) + ') ')
        if cell not in closeList: #and cell not in openList
            cell.visited = True
            if cell.blocked:
                print("Cell: " + '(' + str(cell.x) + ',' + str(cell.y) + ')')
                print("\tCell added to privateCloseList and closeList")
                if(cell.x == 2 and cell.y == 1):
                    print("Problem Curr: " + '(' + str(curr.x) + ',' + str(curr.y) + ') ')

                closeList.append(cell)
                privateCloseList.append(cell)
            else:
                print("\tCell added to openList")
                heapq.heappush(openList, cell)
    closeList.append(curr)
    while(curr != goal):
        curr.visited = True
        print("Curr: " + '(' + str(cell.x) + ',' + str(cell.y) + ')')
        print("\tCell added to privateCloseList")
        privateCloseList.append(curr)
        neighbors = getNeighbors(curr, array)
        for cell in neighbors:
            if not cell.visited:
                cell.visited = True
                cell.g = curr.g + 1
                cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                cell.f = cell.g + cell.h
                cell.parent = curr
                print("Cell: " + '(' + str(cell.x) + ',' + str(cell.y) + ')')
                print("\tCell added to openList")
                heapq.heappush(openList, cell)
        if(len(openList) != 0):
            temp = curr
            curr = heapq.heappop(openList)
            if(curr == goal):
                curr.parent = temp
                break
        else: 
            print("Path does not exist.")
            break
        #End if else 
    #End while


    newX, newY = getNewStart(start, goal, array)

    listPath(start,goal,array)

    appendCloseList(start, newX, newY, array, closeList)

    #Print the path computed from this iteration
    printMaze(startx, starty,array, closeList)

    # print("privateCloseList: ")
    # printList(privateCloseList)
    # print("openList: ")
    # printList(openList)
    # print("closeList: ")
    # printList(closeList)
    # print("New curr: (" + str(newX) + ',' + str(newY) + ')')
    #Return new curr (the parent of the last blocked cell going backwards from the goal)

    return array[newX][newY]

#End computePath


#Get the new starting point for computePath
def getNewStart(start, goal, array):
    result = goal
    while(goal != None and goal != start):
        if(goal.blocked):
            result = goal.parent
        goal = goal.parent
    print('New start: (' + str(result.x) + ',' + str(result.y) + ')')
    return result.x, result.y

def appendCloseList(start, newX, newY, array, closeList):
    temp = array[newX][newY]
    while(temp != start and temp != None):
        closeList.append(temp)
        temp = temp.parent



#List coordinates taken
def listPath(holder ,goal, array):
    
    print("***GOAL***")
    while(goal.parent != holder and goal.parent != None):
        print('(' + str(goal.x) + ',' + str(goal.y) + ')')
        goal = goal.parent
        goal.onPath = True
    print('(' + str(goal.x) + ',' + str(goal.y) + ')')
    print("***START***\n")



def printList(nodelist):
    for item in nodelist:
        print('(' + str(item.x) + ',' + str(item.y) +')' + "f-value: " + str(item.f))



#Print maze with path
def printMaze(startx, starty,array,closeList):
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
            elif(item.blocked and item in closeList):
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







