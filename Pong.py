import turtle
from playsound import playsound


class Ball(turtle.Turtle):
    dx: float
    dy: float

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def reflect_x(self):
        self.dx *= -1

    def reflect_y(self):
        self.dy *= -1
        playsound("bounce.wav")


class ScoreBoard(turtle.Turtle):
    a: int
    b: int

    def __init__(self):
        super().__init__()
        self.a = 0
        self.b = 0

    def increase_a(self):
        self.a += 1
        self.reload()

    def increase_b(self):
        self.b += 1
        self.reload()

    def reload(self):
        self.clear()
        self.write("Player A: {} Player B: {}".format(self.a, self.b), align="center", font=("Courier", 24, "normal"))


def create_paddle(stretch_wid=5, stretch_len=1, color="white", x=0, y=0):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(color)
    paddle.shapesize(stretch_wid=stretch_wid, stretch_len=stretch_len)
    paddle.penup()
    paddle.goto(x, y)
    return paddle


def create_screen(title):
    screen = turtle.Screen()
    screen.title(title)
    screen.bgcolor("black")
    screen.setup(width=800, height=600)
    screen.tracer(0)
    return screen


def create_score_board():
    board = ScoreBoard()
    board.speed(0)
    board.color("white")
    board.penup()
    board.hideturtle()
    board.goto(0, 260)
    board.reload()
    return board


def create_ball(color="white", x=0, y=0, dx=0.0, dy=0.0):
    ball = Ball()
    ball.speed(0)
    ball.shape("square")
    ball.color(color)
    ball.penup()
    ball.goto(x, y)
    ball.dx = dx
    ball.dy = dy
    return ball


class Pong:
    screen: turtle.Screen
    score_board: ScoreBoard
    paddle_a: turtle.Turtle
    paddle_b: turtle.Turtle
    ball: Ball

    def __init__(self, title="Pong", speeds=0.25):
        self.score_a = 0
        self.score_b = 0
        self.screen = create_screen(title)
        self.paddle_a = create_paddle(x=-350, y=0)
        self.paddle_b = create_paddle(x=350, y=0)
        self.ball = create_ball(dx=speeds, dy=speeds)
        self.score_board = create_score_board()

    def paddle_a_up(self):
        self.paddle_a.sety(self.paddle_a.ycor() + 30)

    def paddle_a_down(self):
        self.paddle_a.sety(self.paddle_a.ycor() - 30)

    def paddle_b_up(self):
        self.paddle_b.sety(self.paddle_b.ycor() + 30)

    def paddle_b_down(self):
        self.paddle_b.sety(self.paddle_b.ycor() - 30)

    def listen(self):
        self.screen.listen()
        self.screen.onkeypress(self.paddle_a_up, "w")
        self.screen.onkeypress(self.paddle_a_down, "s")
        self.screen.onkeypress(self.paddle_b_up, "Up")
        self.screen.onkeypress(self.paddle_b_down, "Down")

    def play(self):
        while True:
            self.screen.update()
            self.ball.move()

            # Border checking
            if self.ball.ycor() > 290:
                self.ball.sety(290)
                self.ball.reflect_y()

            if self.ball.ycor() < -290:
                self.ball.sety(-290)
                self.ball.reflect_y()

            if self.ball.xcor() > 390:
                self.ball.goto(0, 0)
                self.ball.reflect_x()
                self.score_board.increase_a()

            if self.ball.xcor() < -390:
                self.ball.goto(0, 0)
                self.ball.reflect_x()
                self.score_board.increase_b()

            # Paddle and ball collisions
            if 340 < self.ball.xcor() < 350 and (self.ball.ycor() < self.paddle_b.ycor() + 50) and (
                    self.ball.ycor() > self.paddle_b.ycor() - 50):
                self.ball.setx(340)
                self.ball.reflect_x()

            if -350 < self.ball.xcor() < -340 and (self.ball.ycor() < self.paddle_a.ycor() + 50) and (
                    self.ball.ycor() > self.paddle_a.ycor() - 50):
                self.ball.setx(-340)
                self.ball.reflect_x()
