import pyglet
from pyglet import shapes
from pyglet.window import key
from pyglet.window import mouse
import math

window = pyglet.window.Window()

window.set_size(400, 400)

Batch = pyglet.graphics.Batch()

class vector():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class pike():
    def __init__(self, x, y, size) -> None:
        self.position = vector(x, y)
        self.size = size
        self.pointer = vector(x + size, y)
        self.velocity = vector(x=20,y=50)
        self.previus_velocity = self.velocity
        self.angle = 0
        direction = vector(self.pointer.x - self.position.x, self.pointer.y - self.position.y)

        to_perpendicular1 = [-direction.y * size / 30, direction.x * size / 30]
        to_perpendicular2 = [direction.y * size / 30, -direction.x * size / 30]

        self.center = shapes.Circle(x, y, radius=2, color=(50, 225, 30), batch=Batch)

        self.towards_line = shapes.Line(
            x=self.position.x, y=self.position.y, 
            x2=self.pointer.x, y2=self.pointer.y, 
            width=1, batch=Batch)
        
        self.tail_line = shapes.Line(
            x=self.position.x, y=self.position.y, 
            x2=self.position.x - direction.x / 3 , y2=self.position.y - direction.y / 3, 
            width=1, batch=Batch)
        
        self.left_line = shapes.Line(
            x=self.position.x, y=self.position.y, 
            x2=to_perpendicular1[0] + self.position.x, y2=to_perpendicular1[1] + self.position.y, 
            width=1, batch=Batch)

        self.rigth_line = shapes.Line(
            x=self.position.x, y=self.position.y, 
            x2=to_perpendicular2[0] + self.position.x, y2=to_perpendicular2[1] + self.position.y, 
            width=1, batch=Batch)
        
        self.help_line1= shapes.Line(
            x=self.rigth_line.x2, y=self.rigth_line.y2,
            x2=self.towards_line.x2, y2=self.towards_line.y2,
            width=1, batch=Batch)

        self.help_line2= shapes.Line(
            x=self.left_line.x2, y=self.left_line.y2,
            x2=self.towards_line.x2, y2=self.towards_line.y2,
            width=1, batch=Batch)
        
        self.help_line3= shapes.Line(
            x=self.tail_line.x2, y=self.tail_line.y2,
            x2=self.towards_line.x2, y2=self.towards_line.y2,
            width=1, batch=Batch)
        
        self.help_line4= shapes.Line(
            x=self.left_line.x2, y=self.left_line.y2,
            x2=self.towards_line.x2, y2=self.towards_line.y2,
            width=1, batch=Batch)

    def set_position(self, line, x, y, x2, y2):
        line.x = x
        line.y = y
        line.x2 = x2
        line.y2 = y2

    def update(self):

        self.center.x = self.position.x + self.velocity.x
        self.center.y = self.position.y + self.velocity.y


        opp = self.velocity.y
        adj = self.velocity.x
        # print(f"opp : {opp} | adj: {adj}")
        if adj == 0: adj += 1

        tan = opp / adj

        self.angle = math.atan(tan)

        # print(self.angle)

        self.previus_velocity = self.velocity

        self.pointer = vector(
            self.position.x + (self.size * math.cos(self.angle)),
            self.position.y + (self.size * math.sin(self.angle))
            )

        direction = vector(self.towards_line.x2 - self.position.x, self.towards_line.y2 - self.position.y)
        to_perpendicular1 = [-direction.y * self.size / 30, direction.x * self.size / 30]
        to_perpendicular2 = [direction.y * self.size / 30, -direction.x * self.size / 30]
        
        self.set_position(self.towards_line, self.position.x, self.position.y, 
                self.pointer.x, self.pointer.y)
        
        self.set_position(self.tail_line, self.position.x, self.position.y, 
                self.position.x - direction.x / 3, self.position.y - direction.y / 3)
        
        self.set_position(self.left_line, self.position.x, self.position.x, 
                self.position.x + to_perpendicular1[0], self.position.y + to_perpendicular1[1])
    
        self.set_position(self.rigth_line, self.position.x, self.position.y, 
                self.position.x + to_perpendicular2[0], self.position.y + to_perpendicular2[1])
    
        self.set_position(self.help_line1, self.left_line.x2, self.left_line.y2, 
                self.towards_line.x2, self.towards_line.y2)
        self.set_position(self.help_line2, self.rigth_line.x2, self.rigth_line.y2, 
                self.towards_line.x2, self.towards_line.y2)
        
        self.set_position(self.help_line3, self.tail_line.x2, self.tail_line.y2, 
                self.left_line.x2, self.left_line.y2)
        self.set_position(self.help_line4, self.tail_line.x2, self.tail_line.y2, 
                self.rigth_line.x2, self.rigth_line.y2)

pike1 = pike(100, 100, 13)

@window.event
def on_mouse_press(x, y, button, modifiers):
    pike1.velocity.x = x 
    pike1.velocity.y = y

@window.event
def on_draw():
    window.clear()
    Batch.draw()

def update(dt):
    # pike1.angle += dt
    # 😁
    # pike1.angle = 90
    print(pike1.angle)
    pike1.update()
    # towards_line.rotation += dt * 10


pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()