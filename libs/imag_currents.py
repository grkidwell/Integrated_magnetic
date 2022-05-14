import numpy as np
class Imag_currents:
    
    def __init__(self,acfluxes,dcfluxes):
        
        self.acfluxes=acfluxes
        self.dcfluxes=dcfluxes
        
        self.permeances=self.acfluxes.permeances 
        self.time_states=self.acfluxes.time_states
        self.windings=self.acfluxes.windings #self.turns=self.acfluxes.nturns
        self.deltaflux=self.acfluxes.deltaflux 
        
        self.deltaMMF=self.calculate_deltaMMFs_fullturns()
        self.ac_currents = {state:{leg:np.round(dMMF/self.windings.turns[leg][0],3) for leg,dMMF in dMMFs.items()} 
                            for state,dMMFs in self.deltaMMF.items()}
        
        self.dc_currents = {state:{leg:np.round(MMF/self.windings.turns[leg][0],3) for leg,MMF in MMFs.items() if self.windings.turns[leg][0]} 
                            for state,MMFs in self.dcfluxes.dc_MMFs.items()}
        
        self.peak_currents = {state:{leg:self.dc_currents[state][leg]+ac/2 for leg,ac in ac_leg.items()}
                             for state,ac_leg in self.ac_currents.items()}
        
    def par(self,a,b):
        return a*b/(a+b)
    
    def calculate_deltaMMFs_fullturns(self):
        return {state:{'center':dflux['center']/self.permeances.fullturn_permeance} for state,dflux in self.deltaflux.items()}
        
    def calculate_deltaMMFs_include_halfturns(self):
        p1 = self.permeances.leg_permeances['left']
        pc = self.permeances.leg_permeances['center']
        p2 = self.permeances.leg_permeances['right']
      
        coefficients = np.array([
            [1,                     1,         0],
            [0,                     1,         1],
            [p1/(pc+p2)-1, -pc/(p1+p2), p2/(p1+pc)]])
        
        legs = ['left','center','right']
        #create dictionary of dictionaries of deltaMMFs[state][leg]
        deltaMMFdictofdict={}
        for state in self.time_states:
            right_matrix = np.array([ self.deltaflux[state]['left']/p1  + self.deltaflux[state]['center']/pc,
                                      self.deltaflux[state]['right']/p2 + self.deltaflux[state]['center']/pc,
                                     -self.deltaflux[state]['left']/p1])
            deltaMMFdictofdict[state]=dict(zip(legs,np.linalg.solve(coefficients,right_matrix)))
        return deltaMMFdictofdict
      
    
      

   