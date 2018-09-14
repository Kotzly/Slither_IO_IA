# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 20:49:53 2018

@author: Paulo Augusto
"""
from Tkinter import *
import numpy as np
import random
import time
import math
import itertools
from snkbrain import *

# from itertools recipes: https://docs.python.org/2/library/itertools.html
def vecDir(v1,v2):
    t1,t2=v1,v2
    t1.append(0),t2.append(0)
    a=np.matrix([t1,t2,[1,1,1]])
    det=np.linalg.det(a)
    if det <0:
        return -1
    else:
        return 1
    
def flatten(list_of_lists):
    return itertools.chain.from_iterable(list_of_lists)


def dist(p1,p2):
    return np.sqrt(np.power(p1[0]-p2[0],2)+
                   np.power(p1[1]-p2[1],2))

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def vecAngle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def absAngle(p1,p2):
    x,y = p2[0]-p1[0], p2[1]-p1[1]
    return vecAngle([1,0],[x,y])

def segAngle(seg):
    return absAngle(seg.vertex[0:2],seg.vertex[2:4])

def movePoint_d(point,distance,direction):
    p=point
    p[0]+=distance*np.cos(direction)
    p[1]+=distance*np.sin(direction)
    return p

def movePoint_v(point,vector):
    p=point
    p[0]+=vector[0]
    p[1]+=vector[1]
    return p
    
class snake():
    
    class segment():
        def recalculate(self):
            self.center=[(self.vertex[0]+ self.vertex[2])/2,
                         (self.vertex[1]+self.vertex[3])/2]
            self.diameter=dist(self.vertex[0:2],self.vertex[2:4])
#            self.father.coords(bd[i].shape,bd[i].center[0],bd[i].center[1],
#                               bd[i].center[0]+self.width,bd[i].center[1]+self.width)
        def __init__(self,father,vertex):
            a=['green','blue','yellow','red','black','white']
            self.color=random.choice(a)#''
            if isinstance(self,snake.head):
                self.direction=-0
                self.color='red'
            self.vertex=vertex
            self.father=father
            self.center=[(vertex[0]+vertex[2])/2,(vertex[1]+vertex[3])/2]
            self.diameter=dist(vertex[0:2],vertex[2:4])
            self.shape=father.root.create_oval(self.center[0],
                                               self.center[1],
                                               self.center[0]+father.width,
                                               self.center[1]+father.width,
                                               fill=self.color,
                                               outline=self.color)

    class head(segment):
        1        

    
    def __init__(self,root,x=0,y=0,lenght=10,width=10,segDis=3):
    
        self.lenght=lenght
        self.x,self.y = x,y
        self.width=width
        self.brain=brain(21,1,4,[12,4])
        self.root=root
        self.body=[]
        self.maxTurning=np.pi/24
        self.segmentDistance=segDis
        self.isAlive=True
        self.body.append(self.head(self,[x,y,x,y+segDis]))
        for i in range(1,self.lenght+1):
            self.body.append(self.segment(self,[x,y+i*segDis,x,y+(i+1)*segDis]))
    
    def setHeadDirection(self,direction):
        self.body[0].direction=direction

        
    def turnHead(self,direction):

        d=0
        if abs(direction)>=self.maxTurning:
           d = self.maxTurning
           if direction<0:
               d*=-1
        else:
            d=direction
        self.setHeadDirection(d+self.body[0].direction)
         
    def moveSnake(self):
        self.think()
        bd=self.body
        for i in range(len(bd)-1,-1,-1):
            if i==0:
#                bd[0].vertex[0:2] = movePoint_d(bd[0].vertex[0:2],self.segmentDistance,bd[0].direction)
#                bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[2:4],self.segmentDistance,bd[0].direction)
                bd[0].vertex[0:2] = bd[0].vertex[2:4]
                bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[2:4],self.segmentDistance,bd[0].direction)
                
            else:
                if not bd[i].vertex[0:4]==bd[i-1].vertex[0:4]:
                    bd[i].vertex[0:4]=bd[i-1].vertex[0:4]
            bd[i].recalculate()
        for i in range(0,len(bd)):
            newCoords=(bd[i].center[0],bd[i].center[1],
                       bd[i].center[0]+self.width,bd[i].center[1]+self.width)
            self.root.coords(bd[i].shape,*newCoords)
#        self.turnHead(np.pi/3)
#        bd[0].direction=bd[0].direction+np.pi/6
            
    def see(self,distance):
        snks=[]
        fds=[]
        vision=[]
        mp=self.body[0].center
        i,j=0,0
        x0=mp[0]-1.5*distance
        y0=mp[1]-1.5*distance
        thought=[]
        k=0
        for j in range(0,3):
            for i in range(0,3):
                thought.append([])    
                vision=self.root.find_overlapping(x0+i*distance,y0+j*distance,x0+(i+1)*distance,y0+(j+1)*distance)
                my_shapes=[seg.shape for seg in self.body]
                for obj in vision:
                    if not obj in my_shapes:
                        thought[k].append(obj)
                k+=1
            
        return thought
    
    def think(self):
        def parseVision(v):
            vision=[]
            segCounter,foodCounter=0,0
            for rec in v:
                segCounter=0
                foodCounter=0        
                for obj in rec:
                    coords=self.root.coords(obj)
                    if dist(coords[0:2],coords[2:4])==self.width:
                        segCounter+=1
                    else:
                        foodCounter+=1
                vision.append(segCounter)
                vision.append(foodCounter)
            return vision
        vision = parseVision(self.see(30))       
        pos=self.body[0].center[0:2]
        pos.extend(vision)
        pos.extend([1])
        self.turnHead(self.brain.run(pos)[0])
        
    def grow(self):
        tam=len(self.body)
        self.body.append(self.segment(self,self.body[tam-1].vertex[0:4]))
        
    def die(self,banquet):
        for seg in self.body:
            pos=seg.center[0:2]
            banquet.addFood(pos)
#            self.root.itemconfig(seg.shape,fill='',outline='')
       
            self.root.delete(seg.shape)
     
            self.body.remove(seg)
        self.isAlive=False
        
            
    def eat(self,food):
        food.father.clean(food)
        self.grow()

class food():
    def clean(self):
        self.root.delete(self.shape)
        print 'caralho'

    def __init__(self,root,father,foodPos,width=5):
        self.width=width
        self.pos=foodPos
        self.father=father
        self.root=root
        self.shape=root.create_oval(foodPos[0],
                         foodPos[1],
                         foodPos[0]+width,
                         foodPos[1]+width,
                         fill='yellow',
                         outline='yellow')