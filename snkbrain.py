# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:02:56 2018

@author: Paulo Augusto
"""
import numpy as np
import random
from scipy.stats import truncnorm

def truncated_normal(mean=0, sd=1, low=-10, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
#    X = truncated_normal(mean=0, sd=0.4, low=-0.5, upp=0.5)
#   matrix = X.rvs(m,n)
def sigma(t,x):
    return 1/(1+np.exp(-x/t))
def feature_scaling(v):
    mean = np.mean(v)
    temp = [a-mean for a in v]
    return temp/desvio_padrao(v)

class brain():


    
    def __init__(self,
                 nInputs,
                 nOutputs,
                 numberOfLayers,
                 numberOfIntermediaryNeurons):

        self.brainMatrixes=self.gen_neural_network(nInputs,
                                                   nOutputs,
                                                   numberOfLayers,
                                                   numberOfIntermediaryNeurons)#[[random.random() for i in range(0,nNeuron)] for i in range(0,nNeuron)]

    
    def gen_neural_network(self,nInputs,nOutputs,numberOfLayers,numberOfIntermediaryNeurons):
        mat=[]
        rad = 1 / np.sqrt(nInputs)
        X = truncated_normal(mean=2, sd=1, low=-rad, upp=rad)
        
        neuronVec=[nInputs]
        [ neuronVec.append(a) for a in numberOfIntermediaryNeurons ]
        neuronVec.append(nOutputs)
        
        for i in range(0,numberOfLayers-1):
            mat.append(X.rvs((neuronVec[i],neuronVec[i+1])))
        return np.array(mat)
    
    def run(self,inpt):
        vecIn=np.matrix(feature_scaling(inpt))
        saida=vecIn
        for i in range(0, len(self.brainMatrixes)):
            
            saida=sigma(1,saida*self.brainMatrixes[i])
        return saida.A1