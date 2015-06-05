from tkinter import *
import random
import time

class Joe:
  def __init__(self):
    # If we're gonna do it let's just make a class instead :)
    self.name = "Joseph"
    self.coolness = 8  # Out of 10




# Here he's just defining the actual class name - you get this
class Ball:
    def __init__(self, canvas, paddle, color):    # So in his init declaration he's accepting canvas/paddle/ and color as a parameter
        # Canvas does not come from this class, it is passed into this class when he creates it.  It's a tkinter thing, jump down to way below with me                
        # Any time  you create an instance of this class the init method is run first and automatically
        # The other methods in the class like - hit_paddle and draw are not run until they're specifically called        So I get this              
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
        # When you see him use 'self' and then follow it with a name he's creating a member variable, so all of these things here
        # are just him making variables that are going to exist on the new class object he created 
        # - I think I get this. The variables only exist to the instance of the object right? Correct
                # So if I made two ball objects, they would each have their own variables, same variables but 2 seperate instances, and ball1 can't touch ball2's variables       
        
        # This is just a function created in a class (which is called a method) - I get this
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    # Another method
    def draw(self):
        # Here he's using the canvas object that he passed in, the tkinter canvas object has a method called 'move'                
        # So the move function takes three parameters (Object ID, x coord, y coord)        
        # I want you to document the paddle class now                # K
            self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

class Paddle:
  # Defines class
    def __init__(self, canvas, color):
      # when the object is created this block of code is applied to it. It also takes the three parameters. Question though. Why does it take self as a 
      # parameter? The answer to this is ... it's just the syntax (for now, don't worry about it - you won't need to dig into it for years prolly)
      # 
      # Acquiring the currently initialized tkinter canvas
      # So this is creating a variable that will make coding easier to do in the following lines. I can type "canvas" instead of "self.canvas" each time
      self.canvas = canvas
      # here I'm doing two things. I'm creating a rectange and saving the shape id output to the self.id variable
      self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
      # Here I'm using Tkinters Canvas' move() method to place the rectange at the coords that I want it
      self.canvas.move(self.id, 200, 300)
      # the object (rectangle) is going to be user controlled, and is only going to move on the x-axis so I create a variable for the 
      # x coord that will allow me to change the the position of the object relativly easily
      self.x = 0
      # So this is a variable that olds the method that's designed to output the width of the canvas object
      # Small disctinction - this doesn't hold the method, it gets the returned value from it - so it actually executes the method and gets the number that is the width back from it
      # And stores that value      - gotcha
      self.y = 0
      self.canvas_width = self.canvas.winfo_width()
      # These two are events / key bindings
      self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
      self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
      # so all of this happens when I create an object in the paddle class
      # paddle1 = Paddle(canvas, "purple")
      # Good

    def draw(self):
      """      
      This method will move the object on the canvas
      """
      # It takes three params the ID of the shape, coords for the x axis, coords for the y axis
      # he enters the variable created at __init__ for the shape ID as the first param. He enters the variable created for the position on the X axis and enters 0 
      # as the param for y because when we call the draw method, we're not going to want to move the object on the y axis. So this param will never be anything
      # but 0. The number in this method is only the amount of pixels we're moving the object
                                        
      self.canvas.move(self.id, self.x, self.y)            
      # this creates a variable called 'pos'. The variable returns the results of the coords method of the canvas class. The coords method takes a single param
      # the id of the object that it's returning the coords for         
      # This method returns a tuple of four numbers ... The x,y coord of the top left (x1,y1) of the shape and the X,y coord of the bottom right of the shape (x2,y2)
      pos = self.canvas.coords(self.id)      
      # This prevents the paddle from going off of the left or right side of the screen      
      if pos[0] <= 0:        
          self.x = 0
      elif pos[2] >= self.canvas_width:
          self.x = 0

    # These methods handle movement for the paddle, they are bound to keypress events in __init__
    def turn_left(self, evt):
        self.x = -2      
    
    def turn_right(self, evt):
        self.x = 2                  

        

# Ok so here he initializes the tkinter environment
tk = Tk()
# Here he sets the window title for a window that'll pop up
tk.title("Game")
tk.resizable(0, 0)
# So the window is on the top. I get most of this stuff He explains most of it
# ok back to SHH - shhhhhhhhhhhhhhhhhhhhhhhhhhhh
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# When he creates an instance of the paddle class he is passing in that screen object from above as the first parameter
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')
# He's doing the same with ball, so he creates the screen once, then passes it as a parameter to his class so the class can use the 

while 1:
    if ball.hit_bottom == False:
            ball.draw()
            paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
    