import math
import pandas as pd
import matplotlib.pyplot as plt


#######################################################################
# Input efficiency

Solar_converter_efficiency_0W = 97.5/100
Solar_converter_efficiency_55W = 91/100

def input_efficiency(solar_power_in):
    solar_converter_efficiency = Solar_converter_efficiency_0W + (Solar_converter_efficiency_55W - Solar_converter_efficiency_0W) / 55 * solar_power_in
    return solar_converter_efficiency

#######################################################################
# Output efficiency

Output_efficiency_0A = 0.92
Output_efficiency_5_3A = 0.77

def output_efficiency(output_current):
    return Output_efficiency_0A + (Output_efficiency_5_3A - Output_efficiency_0A) / 5.3 * output_current

#######################################################################
# Solar generation


Number_of_Solar_Panel = 12 # module
Solar_Panel_branch_OptiVoltage = 4.74 * 3 # (+/- 0.1) V
Solar_Panel_branch_OptiCurrent = 0.499 # (+/- 9mA) A
Solar_Panel_efficiency_BOL = 0.3
Solar_Panel_surface = 0.006036 # m² per module

Solar_irradiance = 1361 # W/m²


def solar_panel_efficiency(time): # Power in Joule
    return Solar_Panel_efficiency_BOL - 0.009 * (1.43 * 10**13) / (2.5 * 10**14) * (t / 31556926)

def solar_panels_power_average(t):
    panels_surface = Number_of_Solar_Panel * Solar_Panel_surface
    power_average_before_efficiency = Solar_irradiance * panels_surface * (math.pi / 2) / 4 #Calculated for uncontrolled sattelite
    power_average_with_efficiency = power_average_before_efficiency * solar_panel_efficiency(t)
    return power_average_with_efficiency

#####################################
#####################################


def importation(file_link):
    df = pd.read_csv(file_link, index_col = False)
    return df

#####################################
class Eclipse:
    def __init__(self,number,start,duration):
        Eclipse.number = number
        Eclipse.start = start
        Eclipse.end = start + duration
        Eclipse.duration = duration

def eclipse_duration_converter(text):
    l = text.split()
    hms = l[2].split(":")
    return (int(hms[0]) * 60 + int(hms[1])) * 60 + int(hms[2])

def get_eclipse(df,eclipse_number):
    return Eclipse(eclipse_number,int(df_eclipse["seconds"][eclipse_number]),eclipse_duration_converter(df_eclipse["duration"][eclipse_number]))

###############
Battery_capacity_max = 4 * 3.7 * 2.6 * 3600 # in Ws


###############
Start_battery_level = 1 # In percent
Run_time = 35000000 # in seconds
df_eclipse = importation("Eclipse_data.csv")


current_eclipse = get_eclipse(df_eclipse, 0)
battery_charge = Start_battery_level * Battery_capacity_max

time = range(Run_time)
Bat_charge = [battery_charge]


for t in time[1:]:
    print(t)
    ### Battery input 
    # Solar power
    if t > current_eclipse.end: # Update the eclipse if it has ended
        current_eclipse = get_eclipse(df_eclipse, current_eclipse.number+1)
    if t > current_eclipse.start and t < current_eclipse.end:
        solar_power = 0
    else:
        solar_power= solar_panels_power_average(t)
    
    # Battery input
    battery_Input = solar_power * input_efficiency(solar_power)

    ### Battery Output
    # Load power need
    # TODO real load calculation
    load_power_need = 7.55

    # Battery Output
    battery_Output = load_power_need / output_efficiency(load_power_need / 5) # We assume that the load use only 5V for max efficiency
    battery_Output += 0.115 # Power consumption of the P31u

    ### Battery state
    # TODO simulate loss of capacity and battery management considering degradation
    battery_change = battery_Input - battery_Output
    if battery_charge < -battery_change :
        raise Exception(f"Flat battery at {t}")
    battery_charge = min(battery_charge + battery_change , Battery_capacity_max)

    ###
    Bat_charge.append(battery_charge)

    if t == 10000000 or t == 20000000:
        plt.plot(range(len(Bat_charge)),Bat_charge)
        plt.show()


fig = plt.figure()
plt.subplot(2,1,1)
plt.plot(time,Bat_charge)
plt.title("Battery charge over time")
plt.xlabel("time (in second)")
plt.ylabel("Battery charge")
plt.ylim(0,Battery_capacity_max)
plt.show()