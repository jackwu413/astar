import os
import random 


def execute():

	counter = 1


	while(counter < 51):
		file = open(os.getcwd() + "/mazes/" + "maze" + str(counter) + ".txt", "w")
		file.write('S')
		for i in range(100):
			temp = random.randint(1,100)
			if temp > 70:
				file.write('X')
			else: 
				file.write(' ')
		file.write('\n')

		for j in range(99):
			for k in range(101):
				temp2 = random.randint(1,100)
				if temp2 > 90:
					file.write('X')
				else: 
					file.write(' ')
			file.write('\n')

		for l in range (100):
			temp3 = random.randint(1,100)
			if (temp3 > 90):
				file.write('X')
			else:
				file.write(' ')
		file.write('E')

		file.close()
		counter += 1


execute()