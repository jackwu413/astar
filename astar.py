import turtle 

window = turtle.Screen()
window.bgcolor("white")
window.title("A*")
window.setup(1130,1130)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("black")
        self.penup()
        self.speed(0)

mazes = [""]

maze_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXX",
"X XXXXXXXXXXXXXXXXXXXXXX",
"X    XXXXX     XXXXXXXXX",
"XXXX XXXXXXXXXXXXXXXXXXX",
"XXXX XXXXXXXXXXXXXXXXXXX",
"XXXX XXXXXXXXXXXXXXXXXXX",
"XXXX XXXXXXXXXXXXXXXXXXX",
"XXXX       XXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXX XXXXXXXXX",
"XXXX     XXXXX XXXXXXXXX",
"XXXXXXXXXXXXXX XXXXXXXXX",
"XXXXXXXXXXXXXX XXXXXXXXX",
"XXXXXXX XXXXXXXXXXXXXXXX",
"XXXXXXX XXXXXXXXXXXXXXXX",
"XXXXXXX XXXXXXXXXXXXXXXX",
"XXXXXXX XXXXXXXXXXXXXXXX",
"XXXXXXX        XXXXXXXXX",
"XXXXXXXXXXXXXX XXXXXXXXX",
"XX  XXXXXXXXXX    XXXXXX",
"XX  XXXXXXXXXX    XXXXXX",
"XX  XXXXXXXXXXXXXXXXXXXX",
"XX  XXXXXXXXXXXXXXXXXXXX",
"XX  XXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXX",
]


mazes.append(maze_1)


def setup_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            character = maze[y][x]
            screen_x = -288 + (x*24)
            screen_y = 288 - (y*24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()


pen = Pen()


setup_maze(mazes[1])

while True:
    pass







