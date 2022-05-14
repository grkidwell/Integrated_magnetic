class Time_states:  
  
#should be able to solve for time-states based on ac flux balance.
#can also try to play with asymmetrical time periods
  
    def __init__(self,fs,duty):
        self.fs = fs*2
        self.ts = 1/fs
        self.duty = duty
        self.four_states=self.calculate_4state(fs=self.fs,duty=self.duty)
        
    def calculate_4state(self,fs,duty):
        ts = 1/self.fs
        t1 = self.duty*ts
        t3 = t1
        t2 = (ts-t1-t3)/2
        t4 = t2
        return {'state1':t1,
                'state2':t2,
                'state3':t3,
                'state4':t4}