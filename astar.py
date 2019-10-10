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
    def __le__(self, other):
        return self.f <= other.f
    def __gt__(self, other):
        return self.f > other.f 
    def __ge__(self, other):
        return self.f >= other.f
    def __eq__(self, other):
        return (self.f == other.f) and (self.x == other.x) and (self.y == other.y) and (self.g == other.g) and (self.h == other.h) and (self.parent == other.parent) and (self.blocked == other.blocked) and (self.visited == other.visited)        

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

        goal = array[4][4]
        curr = array[4][2]
        curr.g = 0
        curr.h = manDis(curr.x, curr.y, goal.x, goal.y)
        curr.f = curr.g + curr.h
        while(curr != goal):

            path=computePath(curr, goal,array,closeList)
            #return
            curr=followPath(path,array,closeList)
            # curr = computePath(curr, goal, array, openList, closeList) #Returns a list
            # #Get first blocked cell in path and the parent of this is the new curr 
            # print("Curr: " + '(' + str(curr.x) + ',' + str(curr.y) + ')')
            printMaze(curr,array)
        #End while

    elif algo == 'b':
        print("Executing Repeated Backward A*")
    else: 
        print("Executing Adaptive A*")

#im at the start of the path and i just keep going and adding to closed list
def followPath(path, array, closeList):
    for item in path:
        if (item.blocked):
            closeList.append(item)
            return item.parent
        closeList.append(item)
    return item

#Function that takes in "starting" point and computes best path to goal without regard for blocked cells 
def computePath(start, goal, array, closeList):
    #so the way this function works is 
    pol = []
    pcl = list(closeList)
    pArray = list(array)
    curr = start
    curr.g = 0
    curr.h = manDis(curr.x, curr.y, goal.x, goal.y)
    curr.f = curr.g + curr.h
    curr.visited = True
    neighbors = getNeighbors(curr,array)
    for cell in neighbors:
        cell.visited = True
        if(cell.blocked):
            pcl.append(cell)
            closeList.append(cell)
        else: 
            heapq.heappush(pol, cell)
    pcl.append(curr)
    closeList.append(curr)

    print("Goal: (" +str(goal.x) +","+str(goal.y)+")")
    while(curr != goal):
        print("Current: (" +str(curr.x) +","+str(curr.y)+")")
        neighbors=getNeighbors(curr, pArray)
        for item in neighbors:
            #print("in neighbors for")
            print("\tlooking at neighbor: "+ "(" +str(item.x) +","+str(item.y)+")")
            if (not item.visited): #item not in pol and
                item.visited = True
                print("\tputting into heap")
                heapq.heappush(pol, item)
                heapq.heapify(pol)
                item.g = item.g + 1
                item.h = manDis(item.x, item.y, goal.x, goal.y)
                item.f = item.g + item.h 
                item.parent = curr
            else:
                print("\tCell "+ "(" +str(item.x) +","+str(item.y)+") already visited")
        #End for
        pcl.append(curr)

        #get next curr
        curr = heapq.heappop(pol) #can be literally anything THIS SHOULD NEVER HAVE AN "ITS EMPTY" ERROR BC IT SOHULD EVENTUALLY BE FUCKING GOAL AND BREAK OUT 
    #End while
    listPath(goal,pArray)
    return pathMaker(goal,start,pArray)
    #call function that makes the path

#End computepath
    
def pathMaker(goal, start, array):
    path=[]
    ptr=goal
    while (ptr != start):
        path.insert(0, ptr)
        ptr = ptr.parent
    #adding start to the path
    path.insert(0,ptr)
    return path



#List coordinates taken
def listPath(goal, array):
    print("Path: \n")
    print("***GOAL***")
    while(goal.parent != None):
        print('(' + str(goal.x) + ',' + str(goal.y) + ')')
        goal = goal.parent
    print('(' + str(goal.x) + ',' + str(goal.y) + ')')
    print("***START***\n")

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




'''
EXECTUE:
    


    execute runs a loop where we have a closed list and an open list--do we even need a global open list--idts
    
    initialize 
    
    i never populate closed list in compute path

    after compute path gives me the path i tke that path and send it into the path follower,
    it takes everything in it and follows the path adding eveything on the way to closed list. it adds the neighbors to to global open list??? idts dont think we need a global open list
    it adds the last blocked guy to the closed list and returns its parrent--in this fucntion im updating the g h f and partent values of array 
    in the other function i was just updating the vlaues for the clone, but i need them in the big actual guy--dont even know if inactaully ened this, lets just put it in for now and see if it works


    

Computue Path:
    compute path is going to get the best path to goal taking into account the things in closed list. the things in closed list is not changed in compute path

    first i initialize a start
    while the start is not the goal:
        get neighbors:
            initialize g valus and add to privateopenlist
        add curr to private closed list
        pop off best next and set curr to it

    call the fucntion that makes the path get an array of the path from start to goal

    return the path in an array

PathMaker:
    givin the goal and start and array
    declare an array for the path
    loop backward through the paretns getting the coordinates
    save each item to the front till i reach start.

'''
