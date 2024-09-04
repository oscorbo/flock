
import data
import random
from math import sqrt
import pyglet
from pyglet import shapes
import math

class boidsSystem():

    flocks = []

    def __init__(self) -> None:
        pass

    def addBoid(self, boid):
        self.flocks.append(boid)

    def update(self):
        for boid in self.flocks:
            boid.check_edges()
            boid.flock(self.flocks)
            boid.update()

class boid():
    def __init__(self, batch) -> None:
        self.sprite = pike(0, 0, 10, batch)

        self.position = vector(random.randrange(data.width), random.randrange(data.height))

        self.velocity = vector()
        self.velocity.setRandom(power=3)
        self.velocity.setMagnitude(random.randrange(2, 4))
        self.previus_velocity = self.velocity

        self.acceleration = vector()

        self.maxForce = 0.2
        self.maxSpeed = 5
        self.perceptionRadiusAlign = 25
        self.perceptionRadiusSeparation = 24
        self.perceptionRadiusCohesion = 50
        
    def check_edges(self):
        if self.position.x > data.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = data.width

        if self.position.y > data.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = data.height

    def alignment(self, boids):
        steering = vector()
        total = 0

        for other in boids:
            if other == self: continue
            distance = other.position.distance(self.position)
            if distance < self.perceptionRadiusAlign:
                steering.addV(other.velocity)
                total += 1
        
        if total > 0:
            steering.divide(total)
            steering.setMagnitude(self.maxSpeed)
            steering.sub(self.velocity)
            steering.limit(self.maxForce)

        return steering
    
    def separation(self, boids):
        steering = vector()
        total = 0

        for other in boids:
            if other == self: continue
            distance = other.position.distance(self.position)
            if distance < self.perceptionRadiusSeparation:
                diff = vector(self.position.x, self.position.y)
                diff.sub(other.position)
                diff.divide(distance * distance)
                steering.addV(diff)
                total += 1

        if total > 0:
            steering.divide(total)
            steering.setMagnitude(self.maxSpeed)
            steering.sub(self.velocity)
            steering.limit(self.maxForce)

        return steering
    
    def cohesion(self, boids):
        steering = vector()
        total = 0

        for other in boids:
            if other == self: continue
            distance = other.position.distance(self.position)
            if distance < self.perceptionRadiusCohesion:
                steering.addV(other.position)
                total += 1

        if total > 0:
            steering.divide(total)
            steering.sub(self.position)
            steering.setMagnitude(self.maxSpeed)
            steering.sub(self.velocity)
            steering.limit(self.maxForce)

        return steering
    
    def flock(self, boids):
        alignment = self.alignment(boids)  
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        alignment.multiply(data.align)
        cohesion.multiply(data.cohesion)
        separation.multiply(data.separation)

        self.acceleration.addV(alignment)
        self.acceleration.addV(cohesion)
        self.acceleration.addV(separation)

    def update(self):
        self.sprite.position.x = self.position.x
        self.sprite.position.y = self.position.y
        
        self.position.addV(self.velocity)
        self.velocity.addV(self.acceleration)
        self.velocity.limit(self.maxSpeed)
        self.acceleration.multiply(0)

        # y
        opp = (self.velocity.y + self.previus_velocity.y) / 1.5
        if opp < 0: opp * -1
        # x
        adj = (self.velocity.x + self.previus_velocity.x) / 1.5
        if adj < 0: adj * -1
        if adj == 0: adj += 1
        tan = opp / adj

        self.previus_velocity = self.velocity

        self.sprite.angle = math.tanh(tan)
        self.sprite.update()


class vector():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x += x
        self.y += y

    def addV(self, vector):
        self.x += vector.x
        self.y += vector.y

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def multiply(self, mult):
        self.x *= mult
        self.y *= mult

    def divide(self, div):
        if div == 0:
            self.setRandom(1)
            return
        self.x /= div
        self.y /= div

    def get_length(self):
        return sqrt(self.x * self.x + self.y * self.y)
    
    def setMagnitude(self, mag):
        self.normalize()
        self.multiply(mag)

    def normalize(self):
        vector_leng = sqrt(self.x * self.x + self.y * self.y)
        if vector_leng == 0:
            self.x = 0
            self.y = 0
            return
        self.x = self.x/vector_leng
        self.y = self.y/vector_leng

    def distance(self, vector):
        temp1 = (self.x - vector.x)
        temp2 = (self.y - vector.y)
        try:
            return sqrt(temp1 + temp2)
        except:
            return sqrt(-1 * (temp1 + temp2))
    
    def setRandom(self, power):
        self.x = random.randrange(-power, power)
        self.y =  random.randrange(-power, power)

    def limit(self, limited):
        if self.get_length() > limited:
            self.normalize()
            self.multiply(limited)
    
    def printVector(self):
        print('x: ' + str(self.x) + ' / y : ' + str(self.y))

class pike():
    def __init__(self, x, y, size, Batch) -> None:
        self.position = vector(x, y)
        self.size = size
        self.pointer = vector(x + size, y)
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
        direction = vector(self.towards_line.x2 - self.position.x, self.towards_line.y2 - self.position.y)
        to_perpendicular1 = [-direction.y * self.size / 30, direction.x * self.size / 30]
        to_perpendicular2 = [direction.y * self.size / 30, -direction.x * self.size / 30]

        self.pointer = vector(
            self.position.x + self.size * math.cos(self.angle), 
            self.position.y + self.size * math.sin(self.angle)
            )
        
        self.set_position(self.towards_line, self.position.x, self.position.y, 
                self.pointer.x, self.pointer.y)
        
        self.set_position(self.tail_line, self.position.x, self.position.y, 
                self.position.x - direction.x / 3, self.position.y - direction.y / 3)
        
        self.set_position(self.left_line, self.position.x, self.position.y, 
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