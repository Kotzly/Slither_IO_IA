from Tkinter import *
import time
import random
import numpy as np

import snake
import tksnake
import snakery
import banquet

mouseX,mouseY=1,0
canvas_width=600
canvas_height=600
master = Tk()

w = Canvas(master, width=canvas_width, height=canvas_height)
w.pack()


ball = w.create_oval(200,200,120,120)
master.update()
foods =banquet.banquet(w,50)
snakes=snakery.snakery(w,8,foods,lenght=5,width=8,segDis=2)


for snk in snakes.population:
    snk.body[0].direction=random.random()*2*np.pi
    

def moveball():
    global counter
    counter+=1
    w.move(ball,10*(random.random()*2-1),10*(random.random()*2-1))
    master.after(1000,moveball)

def setMousePos(event):
    global mouseX,mouseY,angle
    mouseX,mouseY=event.x,event.y

    w.move(ball,(mouseX-100)/100,(mouseY-100)/100)

    v=mysnake.body[0].vertex
    center=mysnake.body[0].center
    d=[v[2]-v[0],v[3]-v[1]]
    c=[mouseX-center[0],mouseY-center[1]]
    c=tksnake.vecAngle(d,c)*tksnake.vecDir(d,c)
         
    mysnake.turnHead(c)

def moveSnake():
    mysnake.moveSnake()
    snakes.moveAll()
    snakes.checkCollisions()
    snakes.checkFoodCollisions()
        
    master.after(50,moveSnake)

master.bind('<B1-Motion>',setMousePos)
mysnake=tksnake.snake(w,lenght=50,x=200,y=200)
master.after(1000,moveSnake)

mainloop()

