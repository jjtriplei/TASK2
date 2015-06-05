from Tkinter import *
import random
import time

class DebugText:
    # This property (variable) is shared across all instances of the debugtext class
    debug_text_count = 0

    def __init__(self, canvas, initial_text=""):
        DebugText.debug_text_count += 1
        self.debug_text_id = DebugText.debug_text_count
        self.canvas = canvas
        self.x = 0 + 50
        self.y = 0 + DebugText.debug_text_count * 5
        self.id = self.canvas.create_text(self.x, self.y, text=initial_text, state="normal",
                                          font="Helvetica 10")
        self.canvas.move(self.id, self.x, self.y)

    def log(self, log_text):
        # Update text on the screen
        self.canvas.itemconfigure(self.id, text=str(log_text))


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    # Another method
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) is True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rectangle_width = 100
        self.color = color
        self.id = canvas.create_rectangle(0, 0, self.rectangle_width, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.y = 0
        self.maxSpeed = 10
        self.xSpeed = 0
        self.ySpeed = 0
        self.air_resistance = .25
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.accelerate_left)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop_left_acceleration)
        self.canvas.bind_all('<KeyPress-Right>', self.accelerate_right)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop_right_acceleration)

        self.left_pressed = FALSE
        self.right_pressed = FALSE

        # I'm going to be re-using the same debug text, so I'm just going to make it a class variable 
        # so I can easily use it and call format on it with the values
        self.debug_text = "{} Paddle: x: {} y: {}"
        self.my_debug_text_object = DebugText(self.canvas)

    def write_debug_text(self, text_to_write):
        self.my_debug_text_object.log(text_to_write)

    def animate(self):
        self.my_debug_text_object.log(self.debug_text.format(self.color.title(), self.x, self.y))
        will_go_off_screen = self.will_go_off_screen()

        if (self.right_pressed and not will_go_off_screen == "right"):
            if self.xSpeed < self.maxSpeed:
                self.xSpeed += .5
        if (self.left_pressed and not will_go_off_screen == "left"):
            if self.xSpeed > -self.maxSpeed:
                self.xSpeed -= .5

        # We should only be redrawing and moving the paddle when its in motion, if it's sitting still
        # don't touch it
        if self.xSpeed > 0 or self.xSpeed < 0:
            self.canvas.move(self.id, self.xSpeed, self.ySpeed)
            # If the paddle is moving gradually slow it down
            if self.xSpeed > 0:
                self.xSpeed -= self.air_resistance
            else:
                self.xSpeed += self.air_resistance

    def will_go_off_screen(self):
        self.x, self.y, bottom_right_x, bottom_right_y = self.canvas.coords(self.id)

        if self.x <= 0:
            self.xSpeed = 0
            return "left"

        if bottom_right_x >= self.canvas_width - 1:
            self.xSpeed = 0
            return "right"

        return False

    def accelerate_left(self, evt):
        self.left_pressed = True
    def stop_left_acceleration(self, evt):
        self.left_pressed = False
    def accelerate_right(self, evt):
        self.right_pressed = True
    def stop_right_acceleration(self, evt):
        self.right_pressed = False

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

def stop_the_program(evt):
    tk.destroy()
canvas.bind_all('<KeyPress-q>', stop_the_program)

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

while 1:
    try:
        if ball.hit_bottom == False:
                ball.draw()
                paddle.animate()
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
    except TclError:
        break
