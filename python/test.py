import random
import turtle

def tree(branchLen, t):
    if branchLen > 3:
        if 8 <= branchLen <= 12:
            if random.randint(0, 2) == 0:
                t.pencolor('snow')
            else:
                t.pencolor('lightcoral')
            t.pensize(branchLen / 3)
        elif branchLen < 8:
            if random.randint(0, 1) == 0:
                t.pencolor('snow')
            else:
                t.pencolor('lightcoral')
            t.pensize(branchLen / 2)
        else:
            t.pencolor('sienna')
            t.pensize(branchLen / 10)
        t.forward(branchLen)
        a = 1.5 * random.random()
        t.right(20 * a)
        b = 1.5 * random.random()
        tree(branchLen - 10 * b, t)
        t.left(40 * a)
        tree(branchLen - 10 * b, t)
        t.right(20 * a)
        t.penup()
        t.backward(branchLen)
        t.pendown()

def petal(m, t):
    for i in range(m):
        a = 200 - 400 * random.random()
        b = 10 - 20 * random.random()
        t.penup()
        t.forward(b)
        t.left(90)
        t.forward(a)
        t.pendown()
        t.pencolor('lightcoral')
        t.circle(1)
        t.penup()
        t.backward(a)
        t.right(90)
        t.backward(b)

def draw():
    try:
        t = turtle.Pen()
        t.hideturtle()
        t.speed(0)
        # turtle.tracer(0, 0)  # 禁用自动刷新
        turtle.bgcolor('wheat')
        t.left(90)
        t.penup()
        t.backward(150)
        t.pendown()
        t.pencolor('sienna')
        tree(60, t)
        petal(100, t)
        # turtle.update()  # 手动刷新屏幕
        turtle.done()
    except turtle.Terminator:
        print("The turtle graphics window was closed.")

if __name__ == '__main__':
    draw()
