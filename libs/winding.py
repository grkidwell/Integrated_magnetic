

class Winding:
    def __init__(self, turns):
        self.turns=turns #[leg][n]-note-use a list for multiple windings on the same core leg
        
    def calculate_mmf(self,turnlist,currentlist):
        return [turnlist[i]*currentlist[i] for i in range(0,len(turnlist))]
        
    def add_v_i_and_calc_dcmmfs(self,v_windings,i_windings):
        self.voltages=v_windings
        self.dc_currents=i_windings
        self.mmfs={state:{leg:self.calculate_mmf(self.turns[leg],current) for leg,current in currents_state.items()} for state,currents_state in self.dc_currents.items()}
        