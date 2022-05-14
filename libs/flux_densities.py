class Flux_densities:
  
    def __init__(self,acfluxes,dcfluxes):
      
        self.acfluxes = acfluxes
        self.dcfluxes = dcfluxes
        
        self.leg_segments  = self.acfluxes.permeances.leg_segments
        self.segment_areas = self.acfluxes.permeances.core.segment_areas
        self.time_states   = self.acfluxes.time_states
        
        self.deltaflux     = self.acfluxes.deltaflux
        self.bac_offset    = self.acfluxes.offset
      
        self.bac   = {state:{leg:{segment:deltaflux_leg/self.segment_areas[segment] for segment in self.leg_segments[leg]} 
                             for leg,deltaflux_leg in deltaflux_state.items()} 
                      for state,deltaflux_state in self.deltaflux.items()}
        self.bdc   = {state:{leg:{segment:dcflux_leg/self.segment_areas[segment] for segment in self.leg_segments[leg]} 
                             for leg,dcflux_leg in dcflux_state.items()} 
                      for state,dcflux_state in self.dcfluxes.dc_flux.items()}
        self.bpeak = {state:{leg:{segment:bdc_segment+self.bac[state][leg][segment]/2 for segment,bdc_segment in bdc_leg.items()} 
                             for leg,bdc_leg in bdc_state.items()} 
                      for state,bdc_state in self.bdc.items()}
        
        self.bac_max_with_key,   self.bac_max   = self.max_by_leg(self.bac)
        self.bdc_max_with_key,   self.bdc_max   = self.max_by_leg(self.bdc)
        self.bpeak_max_with_key, self.bpeak_max = self.max_by_leg(self.bpeak)
        
    def max_by_leg(self,bdict):
        def absmax(b_dict):
            absv=[abs(val) for val in b_dict.values()]
            k=list(b_dict.keys())
            m=max(absv)
            mkey=k[absv.index(m)]
            return {mkey:b_dict[mkey]}         
        withkey    = {state:{leg: absmax(b_legs) for leg,b_legs in b_state.items()} 
                      for state,b_state in bdict.items()}
        withoutkey = {state:{leg: list(absmax(b_legs).values())[0] for leg,b_legs in b_state.items()} 
                      for state,b_state in bdict.items()}       
        return withkey,withoutkey