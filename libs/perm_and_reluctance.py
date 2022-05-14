from math import pi

class Permeance_model:
  
    def __init__(self,core,material):
        self.core = core
        self.reluctances = Reluctance_model(core,material)
        self.leg_segments=self.reluctances.leg_segments
        
        self.leg_permeances = self.permeance_dicts(self.reluctances.leg_reluctances)
        self.fullturn_permeance = self.reluctances.parallel(self.leg_permeances['center'],
                                     self.leg_permeances['left']+self.leg_permeances['right'])
        
    def permeance(self,r):
        return 1/r
    
    def permeance_dicts(self,r):
        return {key: 1/value for key, value in r.items()}
    
    

class Reluctance_model:

  #valid for 3 leg EE/EI type core geometry (EE, EI, PQ, RM, etc.)
  
    def __init__(self,core,material):
      
        self.core=core
        self.u = material["u"]
        
        #create dictionary of core segment reluctances
        self.segment_reluctances = {key: self.reluctance(ur=self.u, length=value, area=self.core.segment_areas[key])  for key, value in self.core.core_segment_lengths.items()}
    
        #add gap reluctances to legs
        for key, value in self.core.gap_lengths.items():
            self.segment_reluctances[key]+=self.reluctance(ur=1, length=value, area=self.core.segment_areas[key])
        
        #each leg is made up of segments
        self.leg_segments={
            'left':   ['AB','EF','AF'],
            'right':  ['BC','CD','DE'],
            'center': ['BE']
        }
        
        #create dictionary of leg reluctances
        self.leg_reluctances = {leg: self.total_reluctance(segmentlist) for leg, segmentlist in self.leg_segments.items()}
        
        #create dictionary of reluctances seen by each winding.  note that center winding are full turns and left/right leg windings are half turns.
        self.winding_reluctances = {'left': self.leg_reluctances['left']  + self.parallel(self.leg_reluctances['center'],self.leg_reluctances['right']),
                                    'right': self.leg_reluctances['right'] + self.parallel(self.leg_reluctances['center'],self.leg_reluctances['left']),
                                    'center'        : self.leg_reluctances['center']+ self.parallel(self.leg_reluctances['left'],self.leg_reluctances['right'])}
    
        #create dictionary of parallel reluctances.  Used in superposition calculation
        self.parallel_reluctances = {'Rpc2': self.parallel(self.leg_reluctances['center'],self.leg_reluctances['right']),
                                     'Rpc1': self.parallel(self.leg_reluctances['center'],self.leg_reluctances['left']),
                                     'Rp12': self.parallel(self.leg_reluctances['left'],  self.leg_reluctances['right'])}
        
        
        
    def reluctance(self,ur,length,area): 
        uo = 4*pi*1e-7
        return length/(uo*ur*area)
      
    def total_reluctance(self,segmentlist):
        reluctance_list = [self.segment_reluctances[segment] for segment in segmentlist]
        return sum(reluctance_list)
    
    def parallel(self,a,b):
        return a*b/(a+b)
      
