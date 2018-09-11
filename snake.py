# -*- coding: utf-8 -*-
"""
Created on Wed Sep 05 19:18:35 2018

@author: Paulo Augusto
"""
import numpy as np
from Tkinter import *

def getAngle(a,b):      #between vectors
    
    def ab(v):
        return np.sqrt(np.power(v[0],2)+np.power(v[1],2))
#    print a,b
    theta=a[0]*b[0]+a[1]*b[1]
    theta/=float(ab(a)*ab(b))
    
    mat=np.matrix([[a[0],a[1],0],[b[0],b[1],0],[1,1,1]])
    det = np.linalg.det(mat)
    sig=1
    if det<0:
        sig=-1
    return float(sig*np.arccos(theta))

def dist(seg1,seg2):
    return np.sqrt(np.power(seg1,2)+np.power(seg2,2))  

def segDis(seg1,seg2):
    a,b = seg1.x-seg2.x , seg1.y-seg2.y
    a2,b2= np.power(a,2) , np.power(b,2)
    return np.sqrt(a2+b2)

def pointAngle(p1,p2):
    x,y = p2[0]-p1[0], p2[1]-p1[1]
    
    if x<0:
        x*=-1
        c=float(y)/float(x) 
        sig=-1
        if y>0:
            sig=1
        return np.arctan(c)+(np.pi/2)*sig
    elif x>0:
        c=float(y)/float(x)   
        return np.arctan(c)
    else:
        if y>0:
            return np.pi/2
        elif y<0:
            return -np.pi/2
        else:
            return 1
def segAngle(seg1,seg2):
    
    x,y = seg2.x-seg1.x , seg2.y-seg1.y
    
    if x<0:
        x*=-1
        c=float(y)/float(x)   
        return np.arctan(c)+(np.pi/2)*y/abs(y)
    elif x>0:
        c=float(y)/float(x)   
        return np.arctan(c)
    else:
        if y>0:
            return np.pi/2
        elif y<0:
            return -np.pi/2
        else:
            return 1
#    return getAngle([float(a),float(b)],[1.0,-1])  

class snake():
    segVec=[]
    _maxV=10
    _initialWidth=50
    _initialLenght=5
    
    class segment():    
        def __init__(self,x,y):
            self.x,self.y=float(x),float(y)
        def move(self,distance,direction):
            self.x+=distance*np.cos(direction)
            self.y+=distance*np.sin(direction)

    class head(segment):
        def __init__(self,x,y):
            self.x,self.y=float(x),float(y)
            self._maxTurn=np.pi/12
            self.direction=np.pi/2
        def turn(self,angle=None,x=None,y=None):
            if not angle==None:
                sig=0
                if angle<0:
                    sig=-1
                else:
                    sig=1
                if abs(angle)<=self._maxTurn:
                    self.direction+=angle
                else:
                    self.direction+=self._maxTurn*sig
            else:
                self.turn(angle=getAngle([self.x,self.y],[x,y]))
                


    
    def initSnake(self,lenght=1,x=1,y=1):
        self.segVec.append(self.head(x,y))
        for i in range(0,lenght):
            self.segVec.append(self.segment(x,y+(i+1)*self._preferedDistance))
        self.width=self._initialWidth
        self.head=self.segVec[0]
        self.body=self.segVec[1:999999]
        
    
    def moveSnake(self):
        direction=0
        for i in range(0,self.lenght):
            if i ==0:
                direction=self.segVec[0].direction
                self.segVec[i].move(self.velocity,direction)
            else:
                if segDis(self.segVec[i],self.segVec[i-1]) >=self._preferedDistance :
#                    v1=self.segVec[i]
#                    v2=self.segVec[i-1]
#                    v3=self.segVec[i-2]
#                    p1=[v1.x-v2.x,v1.y-v2.y]
#                    p2=[v2.x-v3.x,v2.y-v3.y]
                    direction=segAngle(self.segVec[i],self.segVec[i-1])
#                    direction=pointAngle(p1,p2)
                    self.segVec[i].move(segDis(self.segVec[i],self.segVec[i-1])-self._preferedDistance,direction)
        
    
    def __init__(self,lenght=_initialLenght,x=0,y=0):
        self.lenght=lenght+1
        self.velocity=5
        self._preferedDistance=10.0
        self.score=0
        self.initSnake(lenght=lenght,x=x,y=y)
