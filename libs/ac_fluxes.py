
import numpy as np

class AC_fluxes:   #only for Vout=<Vin/4
    
    def __init__(self, permeances, windings,time_states): 
      
        self.permeances       = permeances
        self.windings         = windings
        self.time_states      = time_states.four_states
        self.ts               = time_states.ts
        
        self.legs        = self.windings.turns.keys()
        
        self.fluxrates   = self.calculate_fluxrates()
        self.deltaflux   = {state:{leg:self.time_states[state]*fluxrate for leg,fluxrate in fluxrate_legs.items()} for state,fluxrate_legs in self.fluxrates.items()} 
        
        self.fluxbalance = self.confirm_flux_balance()
        self.offset      = self.calculate_offset()
        
        self.Lmag        = round(self.windings.turns['center'][0]**2*self.permeances.fullturn_permeance,7)
        
    def calculate_fluxrates(self):
        #3 equations, 3 unknowns to solve for flux rates.  
        #'up' = positive for 2 legs and down = positive for center post
        coefficients = np.array([
                        [ 0,             self.windings.turns['center'][0],     0],
                        [ 1,                         -1,                       1],
                        [ 1,                          0,                      -1]])
        
        legs         = ['left','center','right'] #list order is important in solver so must explicitly declare rather than create from dict.keys()
        right_matrix = {state:np.array([voltages['center'][0],
                                           0,
                                           0]) for state,voltages in self.windings.voltages.items()}
        return  {state:dict(zip(legs,np.linalg.solve(coefficients,rightmatrix))) for state,rightmatrix in right_matrix.items()}
    
    def confirm_flux_balance(self):
        deltafluxsum={'left':0,'center':0,'right':0}
        for state, leg_deltaflux in self.deltaflux.items():
            for leg, deltaflux in leg_deltaflux.items():
                deltafluxsum[leg]+=deltaflux
        return deltafluxsum
        
    def calculate_offset(self):
        offset={'left':0,'center':0,'right':0}
        for state, leg_deltaflux in self.deltaflux.items():
            for leg, deltaflux in leg_deltaflux.items():
                offset[leg]+=deltaflux*self.time_states[state]/2/self.ts
        return offset
    
