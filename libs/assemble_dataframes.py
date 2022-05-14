
import pandas as pd

class Assemble_Dataframes:
  
    def __init__(self,fluxdensities,imagcurrents): 
    
        self.b=fluxdensities      
        self.imag=imagcurrents
        
        self.fluxrates=self.create_flatframe(fluxdensities.acfluxes.fluxrates,'Flux Rates')
        self.dcfluxes=self.create_flatframe(fluxdensities.dcfluxes.dc_flux,'DC Fluxes')
        self.bflat=self.create_bflat_dataframe()
        self.iflat=self.create_iflat_dataframe()
        
      
    def create_flatframe(self,dict,name):
        frame=pd.DataFrame.from_dict(dict)
        frame.index.names=['legs']
        frame.columns.names=['state']
        frame2=frame.T.stack()
        frame2.name=name
        flat=frame2.reset_index()
        return flat
  
    #def create_fluxrates(self):
        
    def create_bflat_dataframe(self):
        bacdcflat=self.create_flatframe(self.b.bpeak_max,'Bpeak')
        bacflat=self.create_flatframe(self.b.bac_max,'Bac')
        bdcflat=self.create_flatframe(self.b.bdc_max,'Bdc')
        bflat1=pd.merge(bacflat,bdcflat)
        bflat=pd.merge(bflat1,bacdcflat)
        return bflat
      
    def create_iflat_dataframe(self):   
        cacdcflat=self.create_flatframe(self.imag.peak_currents,'Imag peak')
        cacflat=self.create_flatframe(self.imag.ac_currents,'Imag ac')
        cdcflat=self.create_flatframe(self.imag.dc_currents,'Imag dc')
        cflat1=pd.merge(cacflat,cdcflat)
        cflat=pd.merge(cflat1,cacdcflat)
        return cflat