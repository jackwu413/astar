import os
import sys
import math
import heapq
from heapq import heappush
import myHeap
from myHeap import Heap
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
        if self.f==other.f:
            return self.g>other.g
        return self.f < other.f
    def __le__(self, other):
        if self.f==other.f:
            return self.g>=other.g
        return self.f <= other.f
    def __gt__(self, other):
        if self.f==other.f:
            return self.g<other.g
        return self.f > other.f 
    def __ge__(self, other):
        if self.f==other.f:
            return self.g<=other.g
        return self.f >= other.f
    def __eq__(self, other):
        if(other == 0):
            return False
        return (self.f == other.f) and (self.x == other.x) and (self.y == other.y) and (self.g == other.g) and (self.h == other.h) and (self.parent == other.parent) and (self.blocked == other.blocked) and (self.onPath == other.onPath)

    # def __cmp__(self, other):
    #     return cmp(self.f, other.f)


    # def __lt__(self, other): 
    #     return self.f < other.f
    # def __le__(self, other):
    #     return self.f <= other.f
    # def __gt__(self, other):
    #     return self.f > other.f 
    # def __ge__(self, other):
    #     return self.f >= other.f
    # def __eq__(self, other):
    #     return (self.f == other.f) and (self.x == other.x) and (self.y == other.y) and (self.g == other.g) and (self.h == other.h) and (self.parent == other.parent) and (self.blocked == other.blocked) and (self.onPath == other.onPath)    

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
        algo = raw_input("Enter F for FORWARD, B for BACKWARD, or A for ADAPTIVE.\n")
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
        curr = realArray[0][0]
        expandedCells = 0
        while(curr != goal):
            print("New Start is: " + '(' + str(curr.x) + ',' + str(curr.y) + ')')
            #Return a path from curr to goal
            path, expandedCells = aStar(curr,goal,agentArray, realArray, algo, expandedCells)

            if(len(path) == 0):
                print("No path found")
                print("Expanded Cells: " + str(expandedCells))
                return 
            else:
                curr = followPath(path,realArray)
        print("Expanded Cells: " + str(expandedCells))
        return
    elif algo == 'b':
        print("Executing Repeated Backward A*")
        goal = realArray[len(realArray)-1][len(realArray[0])-1]
        curr = realArray[0][0]
        expandedCells = 0
        while(curr != goal):
            print("New Start is: " + '(' + str(curr.x) + ',' + str(curr.y) + ')')
            #Return a path from curr to goal
            path, expandedCells = aStar(goal,curr,agentArray, realArray, algo, expandedCells)

            if(len(path) == 0):
                print("No path found")
                print("Expanded Cells: " + str(expandedCells))
                return 
            else:
                curr = followBackwardPath(path,realArray)
        print("Expanded Cells: " + str(expandedCells))
        return
    else: 
        print("Executing Adaptive A*")
        goal = realArray[len(realArray)-1][len(realArray[0])-1]
        curr = realArray[0][0]
        expandedCells = 0
        prevCloseList = []
        i = 0
        while(curr != goal):
            print("New Start is: " + '(' + str(curr.x) + ',' + str(curr.y) + ')')
            #Return a path from curr to goal
            path, prevCloseList, expandedCells = adaptiveAStar(curr,goal,agentArray, realArray, prevCloseList,i, expandedCells)
            i += 1
            if(len(path) == 0):
                print("No path found")
                print("Expanded Cells: " + str(expandedCells))
                return 
            else:
                curr = followPath(path,realArray)
        print("Expanded Cells: " + str(expandedCells))
        return


def adaptiveAStar(tempStart, tempGoal, agentArray, realArray, prevCloseList, i, expandedCells):
    openList = Heap()
    closeList = []
    #Hold onto this starting node so we can traverse the path later 
    start = agentArray[tempStart.x][tempStart.y]
    #Curr is used to actually perform the A Star search 
    curr = agentArray[tempStart.x][tempStart.y]
    #Goal is the goal node in the agent's world
    goal = agentArray[tempGoal.x][tempGoal.y]

    curr.g = 0

    if(i==0):   
        #Mark any immediate neighbors as blocked if they are blocked in the real Array 
        immediateNeighbors = getNeighbors(curr, agentArray)
        for cell in immediateNeighbors:
            if(realArray[cell.x][cell.y].blocked):
                cell.blocked = True
                closeList.append(cell)

        while(curr != goal):
            neighbors = getNeighbors(curr, agentArray)
            for cell in neighbors:
                if cell not in openList.heap and cell not in closeList:
                    if cell.blocked:
                        closeList.append(cell)
                    else: 
                        openList.push(cell)
                        #Update g, h, and fa values 
                        cell.g = curr.g + 1
                        cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                        cell.f = cell.g + cell.h 
                        #Set parent to curr
                        cell.parent = curr
                elif(cell in openList.heap):
                    #Update g, h, f values 
                    if(curr.g + 1 < cell.g):
                        cell.g = curr.g + 1
                        cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                        cell.f = cell.g + cell.h
                        #Set new parent because we found a better path to this cell 
                        cell.parent = curr
            #Done expanding curr
            closeList.append(curr)
            expandedCells += 1
            if(len(openList.heap) >= 2):
                curr = openList.heappop()
            else:
                noPath = []
                return noPath
    else:
        immediateNeighbors = getNeighbors(curr, agentArray)
        for cell in immediateNeighbors:
            if(realArray[cell.x][cell.y].blocked):
                cell.blocked = True
                closeList.append(cell)

        while(curr != goal):
            neighbors = getNeighbors(curr, agentArray)
            for cell in neighbors:
                if cell not in openList.heap and cell not in closeList:
                    if cell.blocked:
                        closeList.append(cell)
                    else: 
                        openList.push(cell)
                        if(cell not in prevCloseList):
                            cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                        else:
                            #Possible error
                            cell.h = prevCloseList[prevCloseList.index(goal)].g - prevCloseList[prevCloseList.index(cell)].g
                        cell.g = curr.g + 1
                        cell.f = cell.g + cell.h
                        cell.parent = curr
                elif(cell in openList.heap):
                    if(curr.g + 1 < cell.g):
                        if(cell not in prevCloseList):
                            cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                        else:
                            cell.h = prevCloseList[prevCloseList.index(goal)].g - prevCloseList[prevCloseList.index(cell)].g
                        cell.g = curr.g + 1
                        cell.f = cell.g + cell.h
                        cell.parent = curr
            closeList.append(curr)
            expandedCells += 1
            if(len(openList.heap) >= 2):
                curr = openList.heappop()
            else:
                noPath = []
                return noPath,closeList,expandedCells

    goal.g=curr.g
    closeList.append(goal)
    path=[]
    ptr2=goal
    while (ptr2 != start):
        path.insert(0,ptr2)
        ptr2 = ptr2.parent
    #adding start to the path
    path.insert(0,ptr2)
    #printList(path)
    return path, closeList, expandedCells



def aStar(tempStart, tempGoal, agentArray, realArray, algo, expandedCells):
    openList = Heap()
    closeList = []

    #Hold onto this starting node so we can traverse the path later 
    start = agentArray[tempStart.x][tempStart.y]

    #Curr is used to actually perform the A Star search 
    curr = agentArray[start.x][start.y]

    #Goal is the goal node in the agent's world
    goal = agentArray[tempGoal.x][tempGoal.y]

    curr.g = 0
    curr.h = manDis(curr.x, curr.y, goal.x, goal.y)

    #Discover and record any immediate blocked neighbors going forward 
    if(algo == 'f'):
        immediateNeighbors = getNeighbors(curr, agentArray)
        for cell in immediateNeighbors:
            if(realArray[cell.x][cell.y].blocked):
                cell.blocked = True
                closeList.append(cell)
    else:
    #Discover and record any immediate neighbors going backward
        immediateNeighbors = getNeighbors(goal, agentArray)
        for cell in immediateNeighbors:
            if(realArray[cell.x][cell.y].blocked):
                cell.blocked = True
                closeList.append(cell)

    while(curr != goal):
        
        neighbors = getNeighbors(curr, agentArray)
        for cell in neighbors:
            if cell not in openList.heap and cell not in closeList: 
                if cell.blocked:
                    closeList.append(cell)
                else: 
                    openList.push(cell)
                    cell.g = curr.g + 1
                    cell.h = manDis(cell.x, cell.y, goal.x, goal.y)
                    cell.f = cell.g + cell.h
                    cell.parent = curr
            elif(cell in openList.heap):
                if(curr.g + 1 < cell.g):
                    cell.g = curr.g + 1 
                    cell.f = cell.g + cell.h
                    cell.parent = curr
        closeList.append(curr)
        expandedCells += 1
        if(len(openList.heap) >= 2):
            curr = openList.heappop()
        else:
            noPath = []
            return noPath, expandedCells

    #Return the path from start to tempGoal
    path=[]
    ptr2=goal
    while (ptr2 != start):
        path.insert(0,ptr2)
        ptr2 = ptr2.parent
    #adding start to the path
    path.insert(0,ptr2)
    #printList(path)
    return path, expandedCells


def followPath(path, realArray):
    i=0
    #This list needs to be traversed backwards in backwards
    for item in path:
        if (realArray[item.x][item.y].blocked):
            printMaze(0,0,realArray,[],realArray[item.x][item.y])
            return realArray[item.parent.x][item.parent.y]
        else:
            realArray[item.x][item.y].onPath = True

            # #Print everything like normal using print maze, but there is a current we also send in and that is the 
            # if(i == 0):
            #     i+=1
            #     #Do nothing
            # else:
            #     realArray[item.x][item.y].onPath = True
    printMaze(0,0,realArray,[],realArray[item.x][item.y])
    return realArray[item.x][item.y]


def followBackwardPath(path, realArray):
    i=0

    ptr1 = path[0]
    #This list needs to be traversed backwards in backwards
    for item in reversed(path):
        if (realArray[item.x][item.y].blocked):
            printMaze(0,0,realArray,[],realArray[item.x][item.y])
            return realArray[ptr1.x][ptr1.y]
            #return realArray[item.parent.x][item.parent.y]
        else:
            realArray[item.x][item.y].onPath = True
            #Print everything like normal using print maze, but there is a current we also send in and that is the 
            if(i == 0):
                i+=1
                #Do nothing
            else:
                realArray[item.x][item.y].onPath = True
        ptr1 = item
    printMaze(0,0,realArray,[],realArray[item.x][item.y])
    print("GOAL")
    return realArray[len(realArray)-1][len(realArray[0])-1]


#Get the new starting point for computePath
def getNewStart(start, goal, array):
    result = goal
    while(goal != None and goal != start):
        if(goal.blocked):
            result = goal.parent
        goal = goal.parent
    print('New start: (' + str(result.x) + ',' + str(result.y) + ')')
    return result.x, result.y


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
            elif(item.blocked):
                sys.stdout.write('X')
            elif(item.onPath):
                sys.stdout.write('.')
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







