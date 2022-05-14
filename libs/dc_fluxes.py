import numpy as np
class DC_fluxes:
  
    def __init__(self, permeances, windings):  #warning: an imbalance in leg currents could produce DC flux in the magnetizing 
        self.permeances=permeances
        self.windings=windings
        
        self.dc_MMFs=self.calculate_dc_MMFs()
        self.dc_flux={state:{leg:mmf*self.permeances.leg_permeances[leg] for leg,mmf in mmf_states.items()}for state,mmf_states in self.dc_MMFs.items()}
        
    def calculate_dc_MMFs(self):
        coefficients = np.array([
            [0,  1, 0],
            [1, -1, 0],
            [0, -1, 1]])
        
        legs = ['left','center','right'] #list order is important in solver so must explicitly declare rather than create from dict.keys()
        
        right_matrix = {state:np.array([mmf['center'][0]-mmf['center'][1],
                                        mmf['center'][1]-mmf['center'][0],
                                        mmf['center'][1]-mmf['center'][0]]) for state,mmf in self.windings.mmfs.items()}
        
        return  {state:dict(zip(legs,np.linalg.solve(coefficients,rightmatrix))) for state,rightmatrix in right_matrix.items()}