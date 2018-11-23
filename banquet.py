# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 01:32:52 2018

@author: Paulo Augusto
"""
import numpy as np
from scipy.stats import truncnorm
import tksnake
import random

def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def getCanvasDimensions(canvas):
    canvas.update()
    canvas_width=canvas.winfo_width()
    canvas_height=canvas.winf0_height()
    return canvas_width,canvas_height

    
class banquet():
    def clean(self,food):
        food.clean()
        self.population.remove(food)
#        if len(self.population)<self.maxFood:
        self.addFood_random()

    def addFood_random(self):
        self.updateScreenInfo()
        pos=[random.random()*self.canvasWidth,random.random()*self.canvasHeight]
        self.population.append(tksnake.food(self.root,self,pos,width=self.foodWidth))

    def addFood(self,position):
        self.population.append(tksnake.food(self.root,self,position,width=self.foodWidth))
    def __init__(self,root,max_number,width=5):
        self.population=[]
        self.root=root
        self.maxFood=max_number
        self.foodWidth=width
        for i in range(0,max_number):
            self.addFood_random()
#        self.updateScreenInfo()
#        for i in range(0,max_number):
#            pos=[random.random()*self.canvasWidth,random.random()*self.canvasHeight]
#            self.population.append(tksnake.food(root,self,pos,width=width))

    def updateScreenInfo(self):
        self.root.update()
        self.canvasWidth=self.root.winfo_width()
        self.canvasHeight=self.root.winfo_height()
    
    def clean_all(self):
        for food in self.population:
            food.clean()
        self=self.__init__(self.root,
                           self.maxFood,
                           width=self.foodWidth)
    def explode(self):
        shapes=[seg.shape for seg in self.population]
        for obj in shapes:
            self.root.delete(obj)
        