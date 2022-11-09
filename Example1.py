# -*- coding: utf-8 -*-
#############################   Code description   ############################


## This code shows an example on how to use the library defines a library 
## Probabilistic_Load_Profile_Generator to create a synthetic load profile 
## for electric power consumed byhouseholds, based on their probability of 
## being activated at a certain momemnt. In this case, the load profile is
## generated for six apartments and then is added to get the building's load
## profile.
## Created by: Joel Alpízar Castillo.
## TU Delft
## Version: 1.0



###############################################################################
###########################   Imported modules   ##############################

from numpy import array, arange
import matplotlib.pyplot as plt
from csv import writer

from Probabilistic_Load_Profile_Generator import HouseholdDevice, SetBackgroundLoad, SetVariableLoad
###############################################################################


## Some examlpe devices are loaded from the library.
Fridge = HouseholdDevice.Fridge()
Router = HouseholdDevice.Router()
Dishwasher = HouseholdDevice.Dishwasher()
Lights = HouseholdDevice.Lights()
TV = HouseholdDevice.TV()
Cell_charger = HouseholdDevice.Cell_charger()
Laptop = HouseholdDevice.Laptop()
Screen = HouseholdDevice.Screen()
Kitchen = HouseholdDevice.Kitchen()
Microwave = HouseholdDevice.Microwave()
Kettle = HouseholdDevice.Kettle()

## A list of devices is created for the background profile.
BackgroundDevices = [Fridge, Router, Dishwasher]

## A list of devices is created for the variable load profile.
VariableDevices = [Lights, TV, Cell_charger, Laptop, Screen, Kitchen, Microwave, Kettle]

## The simulation time is set
EndTime = 24
StartTime = 0

## Number of apartments in the building.
n_houses = 6

## Base load for the building.
BuildingLoad = array([0]*60*int((EndTime-StartTime)))


## For each house, the background load and the total load is calculated, and
## then added to the building's load.
for i in range(n_houses):

    BackgroundLoad = SetBackgroundLoad(BackgroundDevices, 24)
    TotalLoad = SetVariableLoad(VariableDevices, BackgroundLoad, 24)

    BuildingLoad = [a + b for a, b in zip(BuildingLoad, TotalLoad)]

## The load is sampled every 15 min, as the load is samplead every 1 min.
Load_15min = [BuildingLoad[15*i] for i in range(96)]

## A .csv file is created to store the resulting load profile.
file = open('Load_Profile_15min.csv', 'w')
writer = writer(file)
writer.writerow(Load_15min)
file.close()

## A figure shows the complete load profile.
plt.figure(1)
plt.plot(BuildingLoad, 'b')
plt.xlim([1, len(BuildingLoad)])
l1 = arange(0, len(BuildingLoad)+1, step=60)
l2 = [int(i/60) for i in l1]
plt.xticks(l1, l2)  # Set label locations. 
plt.xlabel('Time [h]')
plt.ylabel('Power [kW]')
plt.title('Load profile of the building')
plt.grid()

## A figure shows the load profile sampled every 15 min.
plt.figure(2)
plt.plot(Load_15min, 'b')
plt.xlim([1, len(Load_15min)])
l1 = arange(0, len(Load_15min)+1, step=4)
l2 = [int(i/4) for i in l1]
plt.xticks(l1, l2)  # Set label locations. 
plt.xlabel('Time [h]')
plt.ylabel('Power [kW]')
plt.title('Load profile of the building sampled every 15 min')
plt.grid()

## The total energy of the building is calculated. Note that, as the output is
## on kWh, and the load profile is sampled every min, the conversion to get
## kW-min to kWh is 1/60.
TotalEnergy = sum(BuildingLoad)
TotalEnergy /= 60                       # In kWh

print('The total energy consumed per day by the building is: ', TotalEnergy, ' kWh')
print('The average energy consumed per apartment in the building is: ', TotalEnergy/n_houses, ' kWh')
