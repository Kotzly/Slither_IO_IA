# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 20:49:53 2018

@author: Paulo Augusto
"""
from tkinter import *
import numpy as np
import random
import time
import math
import itertools
from snkbrain import *
from behaviors import *

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

def sqrdist(p1,p2):
    return np.power(p1[0]-p2[0],2)+np.power(p1[1]-p2[1],2)

def dist(p1,p2):
    return np.sqrt(np.power(p1[0]-p2[0],2)+
                   np.power(p1[1]-p2[1],2))


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def vecAngle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def vecAngle_d(v1,v2):
    return vecAngle(v1,v2)*vecDir(v1,v2)

def absAngle(p1,p2):
    x,y = p2[0]-p1[0], p2[1]-p1[1]
    return vecAngle([1,0],[x,y])
def absAngle_d(p1,p2):
    if p1==p2:
        return 0
    x,y = p2[0]-p1[0], p2[1]-p1[1]
    return vecAngle_d([1,0],[x,y])

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
def get_obj_center(obj):
    return [(obj[2]+obj[0])/2,(obj[3]+obj[1])/2]

class snake():
    
    class segment():
        def recalculate(self):
            self.center=[(self.vertex[0]+ self.vertex[2])/2,
                         (self.vertex[1]+self.vertex[3])/2]
            self.diameter=dist(self.vertex[0:2],self.vertex[2:4])
#            self.father.coords(bd[i].shape,bd[i].center[0],bd[i].center[1],
#                               bd[i].center[0]+self.width,bd[i].center[1]+self.width)
        def __init__(self,father,vertex):
            tag=''
            color_options=['green','blue','yellow','red','black','gray']
            self.color=random.choice(color_options)#''
            tag='segment'
            if isinstance(self,snake.head):
                self.direction=(random.random()-0.5)*2*np.pi
                self.color='red'
                tag=('head','segment')
            self.vertex=vertex
            self.father=father
            self.center=[(vertex[0]+vertex[2])/2,(vertex[1]+vertex[3])/2]
            self.diameter=dist(vertex[0:2],vertex[2:4])
            self.shape=father.root.create_oval(self.center[0]-father.width/2,
                                               self.center[1]-father.width/2,
                                               self.center[0]+father.width/2,
                                               self.center[1]+father.width/2,
                                               fill=self.color,
                                               outline=self.color,
                                               tags=tag)

    class head(segment):
        1        

    def reassembly(self,w):
        for seg in self.body:
            seg.father.root=w
            seg.shape=seg.father.root.create_oval(seg.center[0],
                                               seg.center[1],
                                               seg.center[0]+father.width,
                                               seg.center[1]+father.width,
                                               fill=seg.color,
                                               outline=seg.color)
    
    def respawn(self,initial_size,x=None,y=None,brain_config=None):

        if x==None:
            x=self.x
        if y==None:
            y=self.y
        
#        if brain_config:
#            self.brain_reset()
        for i in range(len(self.body)):
            self.root.delete(self.body[i].shape)
        old_heritage=[i for i in self.heritage]
        old_brain=self.brain
        self.__init__(self.root,
                       x=x,
                       y=y,
                       lenght=self.lenght,
                       width=self.width,
                       segDis=self.segmentDistance,
                       cpu=self.cpu,
                       brain_config=self.brain_config,
                       fit=self.fit,
                       vision_range=self.vision_range,
                       max_heritage=self.max_heritage,
                       max_turning=self.max_turning,
                       objs=self.objs_to_see,
                       neuron_value=self.neuron_value,
                       kill_score=self.kill_score)
        self.brain=old_brain
        self.set_heritage(old_heritage)
        self.body[0].direction=(random.random()-0.5)*2*np.pi
    def set_heritage(self,her):
        self.heritage=her
    def moveToPosition(self,pos):
        for i in range(0,len(self.body)):
            x=pos[0]
            y=pos[1]
            new_coords=[x,y+i*self.segmentDistance,x,y+(i+1)*self.segmentDistance]
            self.body[i].vertex=new_coords
            self.body[i].recalculate()
            self.root.coords(self.body[i].shape,*new_coords)
        
    def new_brain(self,new_config=None):
        if not new_config:
            new_config=self.brain_config
        self.brain.reset_brain(new_config)
    def __init__(self,root,x=0,y=0,lenght=10,width=10,segDis=3,cpu=True,fit=0,vision_range=40,brain_config=([21,15,6,1],[1,1,0]),max_turning=np.pi/24,max_heritage=5,objs=10,kill_score=2000,neuron_value=2):

        self.lenght=lenght
        self.heritage=[0]
        self.cpu=cpu
        self.x,self.y = x,y
        self.width=width
        self.brain_config=brain_config
        self.brain=brain(*brain_config,neuron_value=neuron_value)
        self.root=root
        self.body=[]
        self.max_heritage=max_heritage
        self.objs_to_see=objs
        self.fit=fit
        self.max_turning=max_turning
        self.neuron_value=neuron_value
        self.segmentDistance=segDis
        self.kill_score=kill_score
        self.direction=random.random()*2*np.pi
        self.isAlive=True
        self.body.append(self.head(self,[x,y,x,y+segDis]))
        self.vision_range=vision_range
        for i in range(1,self.lenght+1):
            self.body.append(self.segment(self,[x,y+i*segDis,x,y+(i+1)*segDis]))
    
    def setHeadDirection(self,direction):
        self.body[0].direction=direction

    def add_fit(self,score):
        max_heritage=self.max_heritage
        if len(self.heritage)<max_heritage:
            self.heritage.append(score)
        else:
            self.heritage.remove(self.heritage[0])
            self.heritage.append(score)
            
    def get_fit(self):
        return np.mean(self.heritage)
        
    def turnHead(self,direction):

        d=0
        if abs(direction)>=self.max_turning:
           d = self.max_turning
           if direction<0:
               d*=-1
        else:
            d=direction
        self.setHeadDirection(d+self.body[0].direction)
         
    def moveSnake(self,side_limit,upper_limit):
#        self.think()
        bd=self.body
        if not self.isAlive:
            return
        if self.cpu:
            self.think()
        for i in range(len(bd)-1,-1,-1):
            if i==0:
                bd[0].vertex[0:2] = bd[0].vertex[2:4]
                bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[2:4],self.segmentDistance,bd[0].direction)

                if bd[0].vertex[0:2][0]>side_limit:
                    bd[0].vertex[0:2]=[bd[0].vertex[0]-side_limit,bd[0].vertex[1]]
                    bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[0:2],self.segmentDistance,bd[0].direction)
                if bd[0].vertex[0:2][0]<0:
                    bd[0].vertex[0:2]=[bd[0].vertex[0]+side_limit,bd[0].vertex[1]]
                    bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[0:2],self.segmentDistance,bd[0].direction)
                if bd[0].vertex[0:2][1]>upper_limit:
                    bd[0].vertex[0:2]=[bd[0].vertex[0],bd[0].vertex[1]-upper_limit]
                    bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[0:2],self.segmentDistance,bd[0].direction)
                if bd[0].vertex[0:2][1]<0:
                    bd[0].vertex[0:2]=[bd[0].vertex[0],bd[0].vertex[1]+upper_limit]
                    bd[0].vertex[2:4] = movePoint_d(bd[0].vertex[0:2],self.segmentDistance,bd[0].direction)


            else:
                if not bd[i].vertex[0:4]==bd[i-1].vertex[0:4]:
                    bd[i].vertex[0:4]=bd[i-1].vertex[0:4]
            bd[i].recalculate()
        for i in range(0,len(bd)):
            newCoords=(bd[i].center[0],bd[i].center[1],
                       bd[i].center[0]+self.width,bd[i].center[1]+self.width)
            self.root.coords(bd[i].shape,*newCoords)

            
    def see_around(self,distance):
        snks=[]
        fds=[]
        vision=[]
        mp=self.body[0].center
        i,j=0,0
        x0=mp[0]-1.5*distance
        y0=mp[1]-1.5*distance
        thought=[]
        k=0
        my_shapes=[seg.shape for seg in self.body]
        thought=[[] for i in range(9)]#1
        for j in range(0,3):
            for i in range(0,3):
#1                thought.append([])    
                vision=self.root.find_overlapping(x0+i*distance,y0+j*distance,x0+(i+1)*distance,y0+(j+1)*distance)
                for obj in vision:
                    if not obj in my_shapes:
                        thought[k].append(obj)
                k+=1
            
        return thought
    

    def dist2head(self,p):
        p=[p[2]-p[0],p[3]-p[1]]
        return dist(p,self.body[0].center)

    
    def see_closest(self,distance):
        mp=self.body[0].center
        x0,y0=mp[0]-.5*distance,mp[1]-.5*distance
        thought=[]
        my_shapes=(seg.shape for seg in self.body)
        vision=self.root.find_overlapping(x0,y0,x0+distance,y0+distance)
        for obj in vision:
            if not obj in my_shapes:
                thought.append(obj)                
        coords=[self.root.coords(obj) for obj in thought]
        temp=coords.copy()
        temp.sort(reverse=False,key=self.dist2head)
        closest=temp[:self.objs_to_see]    
        indexes=(coords.index(coord) for coord in closest)
        thought=[thought[i] for i in indexes]

        obj_dists=[]
        obj_angles=[]
        
        for obj in thought:
            coords=self.root.coords(obj)
            dist_value=np.sqrt(self.dist2head(coords))
#            obj_size=round(dist(coords[0:2],coords[2:4])/np.sqrt(2),3)
#            if obj_size==self.width:
#                obj_dists.append(dist_value*(-1))
#            else:
#                obj_dists.append(dist_value)
            
#            print(self.root.gettags(obj))
            if 'segment' in self.root.gettags(obj):
                obj_dists.append(dist_value*(-1))
            else:
                obj_dists.append(dist_value)

            obj_angles.append(absAngle_d(self.body[0].center,get_obj_center(coords)))
        while len(obj_dists)<self.objs_to_see:
            obj_dists.append(0)
            obj_angles.append(0)
        return obj_dists,obj_angles

    def parse_vision(self,v):
        vision=[]
        segCounter,foodCounter=0,0
        for rec in v:
            segCounter=0
            foodCounter=0        
            for obj in rec:
#                coords=self.root.coords(obj)
#                if dist(coords[0:2],coords[2:4])==self.width:
#                    segCounter+=1
#                else:
#                    foodCounter+=1
                if 'segment' in self.root.gettags(obj):
                    segCounter+=1
                else:
                    foodCounter+=1
            vision.append(segCounter)
            vision.append(foodCounter)
        return vision

    
    def think(self):
#        vision = self.parse_vision(self.see_around(self.vision_range))      
        vision,angles=self.see_closest(self.vision_range)
        
        pos=vision
#        print(vision)
        pos.extend(angles)
        pos.extend([self.body[0].direction,len(self.body)])
        l,out=self.brain.run(pos)
        self.turnHead((out[0]-0.5)*2.2*self.max_turning)
        
    def grow(self):
#        tam=len(self.body)
        self.body.append(self.segment(self,self.body[-1].vertex[0:4]))
        
    def die(self,banquet):
        for seg in self.body:
            pos=seg.center[0:2]
            banquet.addFood(pos)
            self.root.delete(seg.shape)
#            self.body.remove(seg)
        self.isAlive=False
        
    def eat(self,food):
        food.father.clean(food)
        self.grow()
        
    def get_size(self):
        return len(self.body)
    def __len__(self):
        return len(self.body)

    def init_behaviors(self):
        self.cromo=cromo()
        def foo(mode='count'):
            return objs_in_angle(self,mode=mode)
        self.objs_in_angle=foo
        
    
class food():
    def clean(self):
        self.root.delete(self.shape)

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
                         outline='yellow',
                         tags='food')