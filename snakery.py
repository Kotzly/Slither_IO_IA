# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:33:57 2018

@author: Paulo Augusto
"""
import tksnake

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
    def distToHead(point,snk):
        distances= [ dist(point,snk.body[i].center)+snk.width for i in range(0,len(snk.body))]
        return min(distances)
    def snakeDist(snk1,snk2):
        distances= [ 
                    dist(snk1.body[0].center,snk2.body[i].center+snk1.width+snk2.width) 
                    for i in range(0,len(snk2.body))
                   ]
        return min(distances)
    def getSnake(self,i):
        return self.population[i]

    def __init__(self,root,tamPop,lenght=10,width=10,segDis=3):
        self.population=[]
        self.root=root
        self.lenght=10
        self.width=10
        self.segDis=3
        self.tamPop=tamPop
        root.update()
        cols=root.winfo_width()
        rows=root.winfo_height()
        
        for i in range(0,tamPop):
#            print tamPop,root.winfo_width(),root.winfo_height()

            n=getDim(tamPop,cols,rows)

            self.population.append(tksnake.snake(root,lenght=50,x=n[i][0],y=n[i][1]))
            
    def checkCollisions(self):
        for snk in self.population:
            if snakeDist<2*snk.width:
                snk.isAlive=False
        
        
