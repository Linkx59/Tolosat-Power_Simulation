import pandas as pd

##### Simulation Parameters
SimulationStartDate = pd.Timestamp(year=2024, month=1, day=2, hour=12)


##### Design Parameters

# Solar Panel
SolarPanelNumber = 12
SolarPanelBranch = 4                #Not used
SolarPanelOptimalVoltage = 4.74     #Not used
SolarPanelOptimalCurrent = 0.499    #Not used


# Battery
BatteryCapacity_StartOfMission = 4 * 3.7 * 2.6 * 3600 # (Ws)  n * U * Ah * hourToSecondsConvertion

