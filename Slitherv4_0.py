# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:50:14 2018

@author: PauloAugusto
"""

from tkinter import StringVar,IntVar,Canvas,Radiobutton,Button,W,E,S,N,Label,Entry,ALL,Tk,mainloop
import time
import random
import numpy as np
from PIL import ImageTk, Image
import os
import tksnake
import snakery
import banquet
import snkAgUtils
import threading
import snkbrain
#import population_control as pc


#sim_lock=threading.BoundedSemaphore(value=1)
#sim_lock.acquire()
#sim_ready=threading.BoundedSemaphore(value=1)
#sim_ready.acquire()

""" Slither IO Genetic algorithm"""

sim_lock=threading.Event()
sim_ready=threading.Event()
mod_lock=threading.Lock()
mod_ready=threading.Event()
gen_lock=threading.Lock()
snakes_lock=threading.Lock()
sim_lock.wait_clear=lambda:[sim_lock.wait(),sim_lock.clear()]
sim_ready.wait_clear=lambda:[sim_ready.wait(),sim_ready.clear()]
new_snakes_flag=False
first_run=True
max_time=7
pps=500
frame_period=30
food_score=2000
initial_pop=5
food_quantity=50
food_width=5
tam_pop=20
mutation_chance=38
mutation_rate=0.1
mutation_rate_mult=4
mutation_rate_max=1
mutation_rate_min=0.001
brain_config=([22,1,1],[1,1,0])
incremental_rate=25
mod_flag=False  
max_gen=1000
sim_on=True
mouseX,mouseY=1,0
canvas_width=600
canvas_height=400
input_number=10
frame_count=0
foods=None
snakes=None
player_on=False
temp=0
mysnake=None
for i in range(len(brain_config[0])-1):
    temp+=brain_config[0][i]*brain_config[0][i+1]
mutation_chance=10000/temp+1

snake_init={'lenght':3,
            'width':8,
            'segDis':6,
            'brain_config':brain_config,
            'vision_range':40,
            'max_heritage':5,
            'neuron_value':2}
#brain_init={'neuron_value':5,
#            'neuron_std':0.5}


#opt_window=Tk()
master = Tk()
w = Canvas(master,background='white' ,width=canvas_width, height=canvas_height)
w.grid(row=1,column=1,columnspan=30,rowspan=30)

def reset_simulation():
    global foods,snakes,new_snakes_flag,gen,player_on,mysnake,frame_count,food_width,best
    gen,frame_count=0,0
    w.delete(ALL)
    foods =banquet.banquet(w,food_quantity,width=food_width)
    snakes=snakery.snakery_class(w,initial_pop,foods,**snake_init)
    best=snakes[0]
    new_snakes_flag=False
    
    for snk in snakes.population:
        snk.body[0].direction=random.random()*2*np.pi
    if player_on:
        snakes.add_snake(tksnake.snake(w,x=random.randint(0,canvas_width),
                              y=random.randint(0,canvas_height),cpu=False,**snake_init))
        mysnake=snakes[-1]

def construct_gui():
    
    global info_var,pkev,noev,mhev,plrb,shev,slev,swev,ssev,sbev,svev,stev,bvev,fwev,ppev,pfev,psev,ipev,piev,fqev,mtev
    
    
    shl=Label(master,text="Snake opt.")    
    sll=Label(master,text="Lenght")
    swl=Label(master,text="Width")
    ssl=Label(master,text="Segment Distance")
    sbl=Label(master,text="Brain config.")
    svl=Label(master,text="Snake vision range")
    stl=Label(master,text="Snake max. turning")
    mhl=Label(master,text="Snake generations # heritage")
    nol=Label(master,text="Number of objects to parse")
    bvl=Label(master,text="Brain init value")
    fwl=Label(master,text="Food width")
    fql=Label(master,text="Food quantity")
    ppl=Label(master,text="Points per second")
    pfl=Label(master,text="Points per food")
    pkl=Label(master,text="Points per kill")
    psl=Label(master,text="Population size")
    ipl=Label(master,text="Initial pop. size")
    pil=Label(master,text="Pop. increment factor")
    mtl=Label(master,text="Max. Sim. time")
    pll=Label(master,text="Player on?")    

    shl.grid(row=1,column=31,columnspan=2)

#    shev=StringVar()
    slev=StringVar()
    swev=StringVar()
    ssev=StringVar()
    sbev=StringVar()
    svev=StringVar()
    stev=StringVar()
    mhev=StringVar()
    noev=StringVar()
    bvev=StringVar()
    fwev=StringVar()
    fqev=StringVar()
    ppev=StringVar()
    pfev=StringVar()
    pkev=StringVar()
    psev=StringVar()
    ipev=StringVar()
    piev=StringVar()
    mtev=StringVar()
    plrb=IntVar()
    info_var=StringVar()
    global entry_variables
    
#    she=Entry(master,textvariable=shev)    
    sle=Entry(master,textvariable=slev)
    swe=Entry(master,textvariable=swev)
    sse=Entry(master,textvariable=ssev)
    sbe=Entry(master,textvariable=sbev)
    sve=Entry(master,textvariable=svev)
    ste=Entry(master,textvariable=stev)
    mhe=Entry(master,textvariable=mhev)
    noe=Entry(master,textvariable=noev)
    bve=Entry(master,textvariable=bvev)
    fwe=Entry(master,textvariable=fwev)
    fqe=Entry(master,textvariable=fqev)
    ppe=Entry(master,textvariable=ppev)
    pfe=Entry(master,textvariable=pfev)
    pke=Entry(master,textvariable=pkev)
    pse=Entry(master,textvariable=psev)
    ipe=Entry(master,textvariable=ipev)
    pie=Entry(master,textvariable=piev)
    mte=Entry(master,textvariable=mtev)
    plb=Radiobutton(master,variable=plrb,value=True)
    

    lv=[sll,swl,ssl,sbl,svl,stl,mhl,nol,bvl,fwl,fql,ppl,pfl,pkl,psl,ipl,pil,mtl,pll]
    ev=[sle,swe,sse,sbe,sve,ste,mhe,noe,bve,fwe,fqe,ppe,pfe,pke,pse,ipe,pie,mte,plb]    
    entry_variables=[slev,swev,ssev,sbev,svev,stev,mhev,noev,bvev,fwev,fqev,ppev,pfev,pkev,psev,ipev,piev,mtev]
    
    row=2
    for label,entry in zip(lv,ev):
        label.grid(row=row,column=31)
        entry.grid(row=row,column=32)
        row+=1
        
    sttbtn=Button(master,text='Start/Reset')
    sttbtn.grid(row=row,column=31,columnspan=2,sticky=W+E)
    row+=1
    stpbtn=Button(master,text='Stop')
    stpbtn.grid(row=row,column=31,sticky=W+E)

    resbtn=Button(master,text='Resumo')
    resbtn.grid(row=row,column=32,sticky=W+E)
    row+=1
    
    info_label=Label(master,textvariable=info_var)    
    info_label.grid(row=row,column=31,columnspan=2,sticky=W+E)
    
    def stop_sim():
        global sim_on
        with snakes_lock:
            sim_on=False
    def start_sim():
        global sim_on
        with snakes_lock:
            sim_on=True
#        master.after(100,moveSnake)
            
    sttbtn.bind("<Button-1>",start_over)
    stpbtn.bind("<Button-1>",lambda e: stop_sim())
    resbtn.bind("<Button-1>",lambda e: start_sim())
def start_over(e):
    global mod_flag,sim_on,first_run,gen
    with snakes_lock:
        sim_on=False
    apply()
    mod_flag=True
    reset_simulation()
    
    if first_run:
        threading.Thread(target=genetic_alg).start()
        master.after(1000,moveSnake)
        first_run=False
    with snakes_lock:
        sim_on=True    
def apply():
    global mutation_chance,input_number,player_on,entry_variables,food_width,tam_pop,food_score,pps,initial_pop,food_quantity,frame_count,frame_period,max_time,incremental_rate,new_snakes_flag
#    mod_lock.set()
#    mod_ready.wait()
#    mod_ready.clear()
    try:    
#        if noev.get():
#            input_number=int(noev.get())
            
        if swev.get():  snake_init['width']=int(swev.get())
        if slev.get():  snake_init['lenght']=int(slev.get())
        if ssev.get():  snake_init['segDis']=int(ssev.get())
        if sbev.get() or noev.get():
            if noev.get():
                input_number=int(noev.get())
                snake_init['objs']=input_number
            config=[int(s) for s in sbev.get().split(' ') if s]
            biases=[1 for i in range(len(config)+1)]+[0]
            brain=[input_number*2+2]+config+[1]
            snake_init['brain_config']=[brain,biases]
            temp=0
            for i in range(len(brain)-1):
                temp+=brain[i]*brain[i+1]
            mutation_chance=10000./temp+1
    #        print(snake_init['brain_config'])
        if svev.get():  snake_init['vision_range']=int(svev.get())
        if stev.get():  snake_init['max_turning']=float(stev.get())
        if mhev.get():  snake_init['max_heritage']=int(mhev.get())
        if bvev.get():  snake_init['neuron_value']=int(bvev.get())
        if fwev.get():  food_width= int(fwev.get())
        if fqev.get():  food_quantity= int(fqev.get())
        if ppev.get():  pps=int(ppev.get())
        if pfev.get():  food_score=int(pfev.get())
        if pkev.get():  snake_init['kill_score']=int(pkev.get())
        if psev.get():  tam_pop=int(psev.get())
        if piev.get():  incremental_rate=int(piev.get())
        if ipev.get():  initial_pop=int(ipev.get())
        if mtev.get():  max_time=int(mtev.get())
        if plrb.get():  
            player_on=True
        else:
            player_on=False
    except:
        print('problema')
    finally:
        new_snakes_flag=True

    
def setMousePos(event):
    global mouseX,mouseY,angle,mysnake
    mouseX,mouseY=event.x,event.y

    if player_on:
        v=mysnake.body[0].vertex
        center=mysnake.body[0].center
        d=[v[2]-v[0],v[3]-v[1]]
        c=[mouseX-center[0],mouseY-center[1]]
        c=tksnake.vecAngle(d,c)*tksnake.vecDir(d,c)
    
        mysnake.turnHead(c)

def moveSnake():
    global sim_on,frame_count,food_score,max_time,frame_count,pps,frame_period,gen,max_gen,best,snakes
    if sim_on:
        snakes.moveAll()
        frame_count+=1
    gen_lock.acquire()
    if gen<max_gen:
        gen_lock.release()
        sim_lock.wait()
        for snake in snakes.population:
            if snake.isAlive:
                snake.fit+=pps*frame_period/1000
        if len(snakes.checkAlive()) > 1 and not frame_count//(1000./frame_period)>max_time:
            pass
        else:
            for snk in snakes.population:
                snk.fit+=len(snk.body)*food_score
            frame_count=0
            snakes.reset()
            sim_lock.clear()
            sim_ready.set()
    else:
        if gen_lock.locked():
            gen_lock.release()
    master.after(frame_period,moveSnake)

#        w.delete(aurea)
#            master.destroy()
    
def remove_suckers(n):
    def get_fit(indiv):
        return indiv.get_fit()
    snakes.population.sort(reverse=False,key=get_fit)
    for i in range(0,n):
#        snakes[i].brain=snkbrain.brain([21, 12, 1],[1,1,0])
        snakes[i].new_brain()
        snakes[i].heritage=[0]

def get_best():
    valid_snakes=[snk for snk in snakes if not snk==mysnake]
    fits=[snk.get_fit() for snk in valid_snakes]
    best=np.argmax(fits)
    return valid_snakes[best]

def gen_new_pop(best):

    for i in range(len(snakes)):
        if not snakes[i]==best:
            if snakes[i].heritage[-1]<best.heritage[-1]:
#                snakes[i].brain=snkbrain.brain([21,12,1],[1,1,0])#brain([])best.brain.transa(snakes[i].brain,mutation_chance,mutation_rate)
                snakes[i].brain=best.brain.transa(snakes[i].brain,mutation_chance,mutation_rate)

def evaluate_all():
    global mod_flag,new_snakes_flag
    [w.itemconfig(seg,fill='DeepPink2',outline='DeepPink3') for seg in [pos.shape for pos in best.body]]
    info_var.set('Gen:'+str(gen)+','+'Best fit='+str(best.get_fit()))
#    print(best.brain.brainMatrixes,best.id)
    if mod_flag:
        apply()
        mod_flag=False
    sim_lock.set()
    sim_ready.wait()
    sim_ready.clear()
    [snk.add_fit(snk.fit) for snk in snakes]
    for snk in snakes:
        snk.fit=0
#    print([(snk.heritage,snk.id) for snk in snakes])

def genetic_alg():
    
    global  best,last,tam_pop,mutation_rate,mutation_chance,gen,brain_config,gen_max,best,incremental_rate
   
    gen=0
    counter=0
    best=last=snakes[0]
    mutation_rate=0.1
    controller=ag_controller()
    while gen<max_gen:
        if len(snakes)<tam_pop and (gen+1)%incremental_rate==0:
            snakes.add_snake(tksnake.snake(w,**snake_init))
        with gen_lock:
            gen+=1
        evaluate_all()
        remove_suckers(max(1,len(snakes)//4))
        best=get_best()                 
        print(gen,best.get_fit(),best.id,':',tam_pop,mutation_rate,mutation_chance,max_gen)#,':', [p.fit for p in population]
        gen_new_pop(best)
        controller.control(gen,counter,best,last)
        last=best
   
#    plotGens(bestVec,meanVec)
#    plotGens(bestVec,taxaVec)
    print([p.get_fit() for p in snakes])

class ag_controller():
    global  tam_pop,\
            mutation_rate,\
            mutation_chance,\
            max_gen,\
            mutation_rate_max,\
            mutation_chance,\
            binaryCrossChance,\
            mutation_rate_mult,\
            mutation_rate_min

    def __init__(self):
        self._tam_pop=tam_pop
        self._mutation_rate=mutation_rate
        self._mutation_chance=mutation_chance
        self._max_gen=max_gen
        self._tam_pop=tam_pop            
        self._mutation_rate_min=mutation_rate_min
        self._mutation_rate_max=mutation_rate_max
        self._mutation_chance=mutation_chance
        self._mutation_rate_mult=mutation_rate_mult
        self._counter=0
        self._expansion=False
  
    def control(self,gen,counter,best,last):
        global mutation_rate
#        mutation_rate=self._mutation_rate_max
        ascending_counter=0
        if gen>25:
            if best.get_fit()<=last.get_fit()*1.1: #If the fitness doesnt grow by 0.1%
                self._counter+=1
            else:
    #            mutation_rate=self._mutation_rate
                mutation_chance=self._mutation_chance
                self._expansion=False
                self._counter=0
                ascendingCounter=0
                
            
            if self._counter==5:    # If the fitness doesnt grow in n generations
                if self._expansion: # If it the mutation_rate is increasing 
                    if mutation_rate<self._mutation_rate_max:    # If mutation_rate is less than the maximum
                        mutation_rate*=self._mutation_rate_mult
                    else:           # If mutation_rate bigger than the maximum
                        self._expansion=False
    
                else:               # If mutation_rate is decreasing
                    if mutation_rate>self._mutation_rate_min:    # If it is bigger than the minimum
                        mutation_rate/=self._mutation_rate_mult
                    else:                           # If it is less than the minimum
                        self._expansion=True    
                
                self._counter=0   

master.update()
master.bind('<B1-Motion>',setMousePos)

#snakes.spawn.append([300,300])                
construct_gui()
mainloop()
