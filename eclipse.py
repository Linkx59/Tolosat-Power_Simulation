import constante as cs

import pandas as pd

class Eclipse:
    def __init__(self,start,end):
        self.start = start
        self.end = end

    def in_progress(self,time):
        if self.start <= time <= self.end :
            return True
        return False
    
    def after(self,time):
        if self.end < time:
            return True
        return False

class Eclipses:
    def __init__(self):
        self.remaining = []

    def in_shadow(self,time):
        if self.remaining[0].after(time):
            self.remaining.pop()
        return self.remaining[0].in_progress(time)
    
    def get_data(self,filename): # Convert the data of the csv into an object Eclipses
        df = pd.read_csv(filename, index_col = False)
        for i in range(0,df.shape[0]): # Iteration on the row
            startDate = pd.to_datetime(df["start"][i].split("+")[0],format="%Y-%m-%d %H:%M:%S")
            endDate = pd.to_datetime(df["end"][i].split("+")[0],format="%Y-%m-%d %H:%M:%S")
            start = (startDate - cs.SimulationStartDate).seconds
            end = (endDate - cs.SimulationStartDate).seconds
            self.remaining.append(Eclipse(start,end))
            if i<10:
                print(startDate)
                print(start)


#####
e = Eclipses()
sim_start = pd.Timestamp(year=2024, month=1, day=2, hour=12)
e.get_data("Eclipse_data.csv")
