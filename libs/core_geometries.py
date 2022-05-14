
from math import pi

class EEcore:   

    def __init__(self, outer_dim,backwall,leg,cp,gaps):
        self.outer_dim   = outer_dim  #{'length','width'}
        self.backwall    = backwall   #{'thickness','depth'}
        self.leg         = leg        #{'thickness','depth'}
        self.cp          = cp         #{'width','depth'}
        self.gap_lengths = gaps
        
        self.calculate_core_parameters(self.outer_dim,self.backwall,self.leg,self.cp)
        
    def eighth_turn(self,diameter):
        return diameter/2*2*pi/8
    
    def total_path_length(self,segmentlist):      
        pathlength_list = [self.core_segment_lengths[segment] for segment in segmentlist]
        return sum(pathlength_list)
     
    def core_volume(self,segmentlist):
        corevolume_list = [self.core_segment_lengths[segment]*self.segment_areas[segment]/2**(segment=='BE') for segment in segmentlist]
        return sum(corevolume_list)
        
    def find_amin(self,segmentlist):
        return min([self.segment_areas[segment]/2**(segment=='BE')for segment in segmentlist])
        
        
    def calculate_core_parameters(self,outer_dim,backwall,leg,cp):
        self.flux_loops = {'left' :['AB','BE','EF','AF'],
                      'right':['BC','CD','DE','BE']}
                      #'outer':['AB','CD','DF','AF']}
        
        window = {'width' : (outer_dim['length']-cp['width']-2*leg['thickness'])/2, 
                  'height':  outer_dim['width']-2*backwall['thickness']}
        
        self.segment_areas = {segment:backwall['thickness']*backwall['depth'] for segment in ['AB','BC','DE','EF','AC','DF']}
        self.segment_areas.update({segment:leg['thickness']*leg['depth'] for segment in ['CD','AF']})
        self.segment_areas.update({'BE':cp['width']*cp['depth']})
        
        self.core_segment_lengths = {segment:2*self.eighth_turn(backwall['thickness'])+window['width'] for segment in ['AB','BC','DE','EF','AC','DF']}
        self.core_segment_lengths.update({segment:2*self.eighth_turn(leg['thickness'])+window['height']-self.gap_lengths[segment] for segment in ['CD','AF']})
        self.core_segment_lengths.update({'BE':2*self.eighth_turn(cp['width']/2)+window['height']-self.gap_lengths['BE']})
         
        self.core_segment_volumes = {segment:self.segment_areas[segment]*self.core_segment_lengths[segment]
                                    for segment in self.segment_areas.keys()}
        
        self.le     = {loop: self.total_path_length(segmentlist) for loop,segmentlist in self.flux_loops.items()}
        self.volume = {loop: self.core_volume(segmentlist) for loop,segmentlist in self.flux_loops.items()}
        self.ae     = {loop: self.volume[loop]/self.le[loop] for loop in self.flux_loops.keys()}
        self.amin   = {loop: self.find_amin(segmentlist) for loop,segmentlist in self.flux_loops.items()}
          