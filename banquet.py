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
#    X = truncated_normal(mean=0, sd=0.4, low=-0.5, upp=0.5)

def getCanvasDimensions(canvas):
    canvas.update()
    canvas_width=canvas.winfo_width()
    canvas_height=canvas.winf0_height()
    return canvas_width,canvas_height

    
class banquet():
    def addFood(self,position):
        self.population.append(tksnake.food(self.root,position,width=self.width))
    def __init__(self,root,max_number,width=5):
        self.population=[]
        self.root=root
        self.maxFood=max_number
        self.updateScreenInfo()
        for i in range(0,max_number):
            pos=[random.random()*self.canvasWidth,random.random()*self.canvasHeight]
            self.population.append(tksnake.food(root,pos,width=width))

    def updateScreenInfo(self):
        self.root.update()
        self.canvasWidth=self.root.winfo_width()
        self.canvasHeight=self.root.winfo_height()