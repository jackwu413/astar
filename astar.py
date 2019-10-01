import turtle
import random 

window = turtle.Screen()
window.bgcolor("white")
window.title("A*")
window.setup(1030,1030)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)

mazes = [""]

maze_1 = []

for i in range(103):
    if (i == 0 or i == 102):
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
mazes.append(maze_1)


def setup_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            character = maze[y][x]
            screen_x = -510 + (x*10)
            screen_y = 510 - (y*10)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()


pen = Pen()


setup_maze(mazes[1])

while True:
    pass







