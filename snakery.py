# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:33:57 2018

@author: Paulo Augusto
"""
import tksnake
import numpy as np
import random


def dist(p1,p2):
    return np.sqrt(np.power(p1[0]-p2[0],2)+
                   np.power(p1[1]-p2[1],2))

def sqrdist(p1,p2):
    return np.power(p1[0]-p2[0],2)+np.power(p1[1]-p2[1],2)


def getDim(tam,width,height):
    
    i=round(np.sqrt(tam))
#    i=i-1
    m=width/i
    n=height/(i+1)
#    print(m,n)
    pos=[]
    x,y = m/2-m,n/2-n
    
    while y <= height-n and len(pos)<tam:
        y+=n
        x=m/2-m
        while x <= width-m and len(pos)<tam:
            x+=m
            pos.append([x,y])
    return pos
           
class snakery_class():
    
    """This class implements methods to deal with a large number of snakes."""
    
    def reassemblyAll(self,w):
        for snk in self.population:
            snk.reassembly(w)
    
    def reset(self):
        self.root.update()
        cols=self.root.winfo_width()
        rows=self.root.winfo_height()
        self.banquet.clean_all()
        self.spawn=getDim(len(self.population),self.canvasWidth,self.canvasHeight)
        random.shuffle(self.spawn)
#        print(self.spawn)
#        print('')
        for i in range(0,len(self.population)):
            ind=self.population[i]
            ind.respawn(self.lenght,x=self.spawn[i][0],y=self.spawn[i][1])
#            ind.body=ind.body[0:ind.lenght]
#            ind.moveToPosition([self.spawn[i][0],self.spawn[i][1]])
#        for i in range(len(self.population)):
#            self.population[i].isAlive=True
            
            
    def parseCollision(self,snk):
        lookAround=self.root.find_overlapping(snk.body[0].center[0]-snk.width/2,
                                              snk.body[0].center[1]-snk.width/2,
                                              snk.body[0].center[0]+snk.width/2,
                                              snk.body[0].center[1]+snk.width/2)
        for obj in lookAround:            
            for somesnk in self.population:
                if (not somesnk==snk) and somesnk.isAlive:
                    if obj in [seg.shape for seg in somesnk.body]:
                        p=somesnk.root.coords(obj)
                        p=[p[0],p[1]]#[(p[2]+p[0])/2,(p[3]+p[1])/2]
                        if sqrdist(p,snk.body[0].center)<= pow(somesnk.width,2):
                            snk.die(self.banquet)
                            
                            if obj == somesnk.body[0].shape:
                                somesnk.die(self.banquet)
                            else:
                                if hasattr(somesnk,'fit'):
                                    somesnk.fit+=somesnk.kill_score
        return False

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

    def __init__(self,root,tamPop,banquet,lenght=10,width=10,segDis=3,neuron_value=2,brain_config=([21,12,1],[1,1,0]),vision_range=40,max_turning=np.pi/24,max_heritage=5,objs=10,kill_score=2000):
        self.population=[]
        self.root=root
        self.lenght=lenght
        self.width=width
        self.segDis=segDis
        self.tamPop=tamPop
        self.banquet=banquet
        self.snakeCount=0
        root.update()
        cols=root.winfo_width()
        rows=root.winfo_height()
        n=getDim(tamPop,cols,rows)
        self.spawn=n

        for i in range(0,tamPop):
            self.population.append(tksnake.snake(root,max_turning=max_turning,lenght=lenght,width=width,segDis=segDis,x=n[i][0],y=n[i][1],brain_config=brain_config,vision_range=vision_range,objs=objs,kill_score=kill_score,neuron_value=neuron_value))
            self.population[i].id=self.snakeCount
            self.snakeCount+=1
    def add_snake(self,snk):
        snk.id=self.snakeCount
        self.snakeCount+=1
        self.population.append(snk)
        
    def updateScreenInfo(self):
        self.root.update()
        try:
            self.canvasWidth=self.root.winfo_width()
            self.canvasHeight=self.root.winfo_height()
        except:
            pass
    def __getitem__(self,i):
        return self.population[i]
    def __len__(self):
        return len(self.population)
    def checkCollisions(self):

        for me_snk in self.population:            
            ######################3
            if me_snk.isAlive:
                self.updateScreenInfo()
        
#                if me_snk.body[0].center[0]> self.canvasWidth or me_snk.body[0].center[1]> self.canvasHeight or me_snk.body[0].center[0]<0 or me_snk.body[0].center[1]<0:
#                    me_snk.die(self.banquet)

                self.parseCollision(me_snk)

            #########################
    def checkFoodCollisions(self):
        for ind in self.population:
            v=ind.body[0].vertex
            pos=[(v[0]+v[2])/2+self.width/2,(v[1]+v[3])/2+self.width/2]
#            pos=ind.body[0].center
            if ind.isAlive:
                for food in self.banquet.population:
                    min_dist=food.width+ind.width
                    if pos[0]-min_dist<food.pos[0]<pos[0]+min_dist and pos[1]-min_dist<food.pos[1]<pos[1]+min_dist:
                        if dist(pos,food.pos) <= (ind.width+food.width)/2:
                            ind.eat(food)
    
    def checkAlive(self):
        temp=[]
        for snk in self.population:
            if snk.isAlive:
                temp.append(snk)
        return temp
                    
                    
                    
    def moveAll(self):        
        self.updateScreenInfo()
        for snk in self.population:
            if snk.isAlive:
                snk.moveSnake(self.canvasWidth,self.canvasHeight)
        
        self.checkCollisions()
        self.checkFoodCollisions()
        
    def explode(self):
        shapes=[[seg.shape for seg in bd.body] for bd in self.population]
        for obj in [val for sublist in shapes for val in sublist]:
            self.root.delete(obj)
        