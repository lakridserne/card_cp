import turtle
import time

turtle = turtle.Turtle()
turtle.screen.setup(800,600)

def plade():
    turtle.hideturtle()
    turtle.clear()
    turtle.penup()
    turtle.goto(-150,50)
    turtle.pendown()
    turtle.setheading(0)
    for i in range(4):
        turtle.forward(300)
        turtle.right(180)
        turtle.forward(100)
        turtle.right(90)
        turtle.forward(100)
        turtle.right(180)


def kryds(x,y):
    turtle.pencolor('blue')
    turtle.penup()
    turtle.goto(-140 + x*100, -60 + y*100)
    turtle.pendown()
    turtle.goto(turtle.position()[0] + 80, turtle.position()[1] - 80)
    turtle.goto(-140 + x*100, -140 + y*100)
    turtle.pendown()
    turtle.goto(turtle.position()[0] + 80, turtle.position()[1] + 80)