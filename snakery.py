# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:33:57 2018

@author: Paulo Augusto
"""
import tksnake
import numpy as np

def dist(p1,p2):
    return np.sqrt(np.power(p1[0]-p2[0],2)+
                   np.power(p1[1]-p2[1],2))

def getDim(tam,width,height):
    a=0.0
    i=1.0
    while a < tam:
        a=i*(i+1)
        i+=1
    m=width/i
    n=height/(i+1)
    
    pos=[]
    x,y = 0,0
    while y <= height and len(pos)<tam:
        y+=n
        x=0
        while x <= width and len(pos)<tam:
            x+=m
            pos.append([x-m/2,y-n/2])
    return pos
           
class snakery():
    def distToHead(self,point,snk):
        distances= [ dist(point,snk.body[i].center)+snk.width for i in range(0,len(snk.body))]
        return min(distances)
    def snakeDist(self,snk1,snk2):
        distances= [ 
                    dist(snk1.body[0].center,snk2.body[i].center) -snk2.width
                    for i in range(0,len(snk2.body)) 
                    if snk2.isAlive
                   ]
        return min(distances)
    def getSnake(self,i):
        return self.population[i]

    def __init__(self,root,tamPop,banquet,lenght=10,width=10,segDis=3):
        self.population=[]
        self.root=root
        self.lenght=10
        self.width=10
        self.segDis=3
        self.tamPop=tamPop
        self.banquet=banquet
        self.snakeCount=0
        root.update()
        cols=root.winfo_width()
        rows=root.winfo_height()
        
        for i in range(0,tamPop):
#            print tamPop,root.winfo_width(),root.winfo_height()

            n=getDim(tamPop,cols,rows)

            self.population.append(tksnake.snake(root,lenght=self.lenght,x=n[i][0],y=n[i][1]))
            self.population[i].id=self.snakeCount
    
    def updateScreenInfo(self):
        self.root.update()
        self.canvasWidth=self.root.winfo_width()
        self.canvasHeight=self.root.winfo_height()
        
    def checkCollisions(self):
        for me_snk in self.population:
            me_snk.see(10)

            ######################3
            if me_snk.isAlive:
                self.updateScreenInfo()
        
                if me_snk.body[0].center[0]> self.canvasWidth or me_snk.body[0].center[1]> self.canvasHeight or me_snk.body[0].center[0]<0 or me_snk.body[0].center[1]<0:
                    me_snk.die(self.banquet)
                for other_snk in self.population:
                    if (not me_snk == other_snk) and other_snk.isAlive and self.snakeDist(me_snk,other_snk) < 0:
                        me_snk.die(self.banquet)
                        me_snk.see(10)
            #########################
    def checkFoodCollisions(self):
        for ind in self.population:
            if ind.isAlive:
                for food in self.banquet.population:
                    if dist(ind.body[0].center,food.pos) < ind.width:
                        ind.eat(food)
    
                    
                    
                    
    def moveAll(self):        
        for snk in self.population:
            if snk.isAlive:
                snk.moveSnake()
        
        self.checkCollisions()
        self.checkFoodCollisions()
        