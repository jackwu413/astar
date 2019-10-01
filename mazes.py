import random

maze_1=[]

for i in range(103):
    if i == 0 or i == 102:
	string = ""
	for j in range(103):
		string = string + "X"
	maze_1.append(string)
    else: 
	string = ""
	string = string + "X"
	for k in range (101):
	    temp = random.randint(1,100)
	    if temp > 70:
		string = string + "X"
	    else: 
		string = string + " "
	string = string + "X"
	maze_1.append(string)

print('\n'.join(maze_1)) 
