import pyglet
from pyglet.window import key
from pyglet.window import mouse
import boid
import data

window = pyglet.window.Window()

window.set_size(data.width, data.height)

Batch = pyglet.graphics.Batch()

boidsSystem = boid.boidsSystem()

for i in range(20):
    boidsSystem.addBoid(boid.boid(batch=Batch))

@window.event
def on_key_press(symbol, modifiers):
    pass

@window.event
def on_mouse_press(x, y, button, modifiers):
    pass

@window.event
def on_draw():
    window.clear()
    Batch.draw()

time_elapse = 0

def update(dt):
    global time_elapse
    
    time_elapse += dt
    boidsSystem.update()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()