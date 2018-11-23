# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 14:02:56 2018

@author: Paulo Augusto
"""
import random
from scipy.stats import truncnorm
import numpy as np
import snkbrain

def truncated_normal(mean=0, sd=1, low=-10, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
#    X = truncated_normal(mean=0, sd=0.4, low=-0.5, upp=0.5)
#   matrix = X.rvs(m,n)
def feature_scaling(v):
    mean = np.mean(v)
    temp = [a-mean for a in v]
    return temp/np.std(v)

def randomMatrix(m,n,cap):
    mat=[]
    for i in range(0,m):
        mat.append([])
        for i in range(0,n):
            mat[-1].append((random.random()*2-1)*cap)
    return mat
def gen_brain_flags(m,n):
    mat=[]
    for i in range(0,m):
        mat.append([])
        for i in range(0,n):
            mat[-1].append(False)
    return mat


def sigma(x):
    return 1/(1+np.exp(-x))
def dsigma(x):
    return np.exp(-x)/(pow(1+np.exp(-x),2))
def dtanh(x):
    return 1/pow(np.cosh(x),2)
    
    
class brain():
    
    def __init__(self,
                 neurons,
                 biases,
                 neuron_value=1,
                 neuron_std=0.5):

        self.neurons=neurons
        self.brainMatrixes=self.gen_neural_network(neurons,
                                                   biases,
                                                   neuron_value=neuron_value,
                                                   neuron_std=0.5)#[[random.random() for i in range(0,nNeuron)] for i in range(0,nNeuron)]
        self.biases=biases
    def train(self,input_vector,target_vector,learning_rate):

        target=np.array(target_vector,ndmin=2).T
        inpt=np.array(input_vector,ndmin=2).T
        logging,output=self.run(input_vector)
        global tw
        tw=logging
        error=target-logging[-1]
        for i in range(0,len(logging)-1):
#            print i
            tmp=np.multiply(error , logging[-1-i])
            tmp=np.multiply( tmp, (1.0 - logging[-1-i] ))
            tmp=learning_rate*np.dot(tmp,(logging[-2-i]).T)
            tmp=tmp[0:len(tmp)-self.biases[-i-1]]
#            print tmp,error
            self.brainMatrixes[-i-1]+=tmp
            error=np.dot(self.brainMatrixes[-1-i].T,error[0:len(error)-self.biases[-1-i]])
            

    def gen_bias_matrix(self,vec):
        m=[]
        for i in range(0,len(vec)):
            m.append([])
            for j in range(0,vec[i]):
                m[i].append(random.random()*2-1)
        return m
            
    
    def gen_neural_network(self,
                           neurons,
                           biases,
                           neuron_value=1,
                           neuron_std=0.5):
        mat=[]
        flags=[]
#        rad = 1 / np.sqrt(neurons[0])
        rad=neuron_value
        X = truncated_normal(mean=0, sd=neuron_std, low=-rad, upp=rad)        
        neuronVec=[]
        [ neuronVec.append(a+bias) for a,bias in zip(neurons,biases[0:len(biases)]) ]
       
        numberOfLayers=len(neurons)
        
        self.biasMatrix=self.gen_bias_matrix(neuronVec)
        self.biases=biases
        
        for i in range(0,numberOfLayers-1):     
#            m=X.rvs((neuronVec[i+1]-biases[i+1],neuronVec[i]))
            m=randomMatrix(neuronVec[i+1]-biases[i+1],neuronVec[i],neuron_value)
            n=gen_brain_flags(neuronVec[i+1]-biases[i+1],neuronVec[i])
            flags.append(n)
            mat.append(np.matrix(m))
        self.brain_flags=flags
        return mat
    
    def gen_new_flags(self):
        numberOfLayers=len(self.neurons)
        neuronVec=[]
        flags=[]
        [ neuronVec.append(a+bias) for a,bias in zip(self.neurons,self.biases[0:len(self.biases)]) ]
        for i in range(0,numberOfLayers-1):     
            n=gen_brain_flags(neuronVec[i+1]-self.biases[i+1],neuronVec[i])
            flags.append(n)
        self.brain_flags=flags
    
    def run(self,inpt):
        import numpy
        global sigma
        def relu(v):
            for i in range(0,len(v)):
                if v[i]<-1:
                    v[i]=-1
                if v[i]>1:
                    v[i]= 1
        sigma=np.tanh
        logging=[]
        vecIn = np.matrix(inpt)
        saida=vecIn.T
#        print saida
        logging.append(saida)
        for i in range(0, len(self.brainMatrixes)):


            prox=[c for c in saida.A1]
            if self.biases[i]:
                prox.append(1)
                logging[i]=np.concatenate((logging[i],np.array([1],ndmin=2)))
            prox=np.matrix(prox)
            prox=prox.T
            saida=sigma(self.brainMatrixes[i]*prox)#+np.matrix(self.biasMatrix[i+1]).T)
            logging.append(saida)

#            saida=np.tanh(self.brainMatrixes[i]*prox)#+np.matrix(self.biasMatrix[i+1]).T)

        return logging,saida.A1
    
    def transa(self,b,chance,tax):
        temp_brain=[a.copy() for a in self.brainMatrixes]
        other_brain=[a.copy() for a in b.brainMatrixes]
        new_brain=[(a+b)/2 for (a,b) in zip(temp_brain,other_brain)]
        new_ind=brain(self.neurons,self.biases)
        new_ind.brainMatrixes=new_brain
        new_ind.brain_flags=b.brain_flags.copy()
        new_ind.check_trues()
        mutate(new_ind,chance,tax)
        return new_ind
    def reset_brain(self,new_config=None):
        if not new_config:
            new_config=(self.neurons,self.biases)
        self=self.__init__(*new_config)
    def check_trues(self):
        count=0.
        total=0.
        for m in self.brain_flags:
            for line in m:
                for row in line:
                    if row:
                        count+=1
                    total+=1
        if count/total>=0.60:
            self.gen_new_flags()
        return count,total

def mutate(b,chance,tax):
    actual_chance=chance
    for i in range(len(b.brainMatrixes)):
        for j in range(len(b.brainMatrixes[i])):
            for k in range(len(b.brainMatrixes[i][j].A[0])):
                if random.random()<0.5:
                    tax*=-1
                if random.random()*10000<actual_chance:
                    if not b.brain_flags[i][j][k]:
                        b.brainMatrixes[i][j].A[0][k]+=tax
                        b.brain_flags[i][j][k]=True
                        actual_chance=chance
                    else:
                        actual_chance*=1.2

            
            