class ag_controller():
    global  tam_pop,\
            mutation_rate,\
            mutation_chance,\
            bestAll,\
            bias,\
            max_gen,\
            tam_pop,\
            mutation_rate,\
            mutation_rate_max,\
            mutation_chance,\
            continuous,\
            binaryFit,\
            mult_fac,\
            binaryCrossChance,\
            mutation_rate_mult,\
            mutation_rate_min

    def __init__(self):
        self._tam_pop=tam_pop
        self._mutation_rate=mutation_rate
        self._mutation_chance=mutation_chance
        self._bias=bias
        self._max_gen=max_gen
        self._tam_pop=tam_pop            
        self._mutation_rate_min=mutation_rate_min
        self._mutation_rate_max=mutation_rate_max
        self._mutation_chance=mutation_chance
        self._mult_fac=mult_fac
        self._mutation_rate_mult=mutation_rate_mult
        self._counter=0
        self._expansion=False
  
    def control(self,gen,counter,best,last):
        global mutation_rate
#        mutation_rate=self._mutation_rate_max
        ascending_counter=0
        if gen>25:
            if best.get_fit()<=last.get_fit()*1.001: #If the fitness doesnt grow by 0.1%
                self._counter+=1
            else:
    #            mutation_rate=self._mutation_rate
                mutation_chance=self._mutation_chance
                self._expansion=False
                self._counter=0
                ascendingCounter=0
                
            
            if self._counter==10:    # If the fitness doesnt grow in n generations
                if self._expansion: # If it the mutation_rate is increasing 
                    if mutation_rate<self._mutation_rate_max:    # If mutation_rate is less than the maximum
                        mutation_rate*=self._mutation_rate_mult
                    else:           # If mutation_rate bigger than the maximum
                        self._expansion=False
    
                else:               # If mutation_rate is decreasing
                    if mutation_rate>self._mutation_rateMin:    # If it is bigger than the minimum
                        mutation_rate/=self._mutation_rate_mult
                    else:                           # If it is less than the minimum
                        self._expansion=True    
                
                self._counter=0  
                