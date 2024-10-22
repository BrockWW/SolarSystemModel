'''Script for running the solar system model and saving/visualizing output.'''

import numpy as np
from pathlib import Path
import os
import time

from solar_system_classes import *
from plotting_functions import *

# Data path entry
flag = True
while flag:
    data_path = input("\nPlease input the local path to directory containing all object data files:\n")
    if os.path.isdir(data_path):
        pathlist = Path(data_path).glob('*')
        flag = False
    else:
        input("\nInvalid directory path.\n\nPress ENTER to continue.\n")

# Model method selection
flag = True
while flag:
    method = input("\nPlease select the numerical method to run the model with:\nVelocity Verlet (VV)\n4th Order Runge-Kutta (RK4):\n")
    method = method.lower()
    if method == "vv" or method == "rk4":
        flag = False
    else:
        input("\nInvalid method, please use 'VV' for Velocity Verlet or 'RK4' for 4th Order Ruge-Kutta.\n\nPress ENTER to continue.\n")

# Model runtime constraints
flag = True
while flag:
    try:
        time_end = float(input("\nPlease enter the ending time of the simulation in years:\n"))
        delta_t = float(input("\nPlease enter the timestep for the model in days:\n"))

    except:
        input("\nInvalid parameters, please enter the time limits as a set (t_0, t_f) and enter the time step as a float or integer.\n\nPress ENTER to continue.\n")

    if 0 < time_end and time_end%delta_t == 0:
        flag = False
    elif 0 >= time_end:
        input("\nInvalid ending time, must be a value greater than zero.\n\nPress ENTER to continue.\n")
    elif time_end%delta_t != 0:
        input("\nInvalid time step. The ending time must be divisible by the time step.\n\nPress ENTER to continue.\n")

# Output plot selection
flag = True
while flag:
    plot_type = input("\nPlease select the plot outputs.\n2d - Creates plot of x and y data\n3d - Creates plot of x, y, and z data in interactive HTML\nboth - Creates both the 2d and 3d plot:\n")
    plot_type = plot_type.lower()

    size_2d = [0.,0.]
    dim_2d = [0.,0.,0.,0.]
    dim_3d = [0.,0.,0.,0.,0.,0.]

    if plot_type == "2d":
        dim_2d[0] = float(input("\nPlease enter axis boundaries in AU:\nx_min: "))
        dim_2d[1] = float(input("x_max: "))
        dim_2d[2] = float(input("y_min: "))
        dim_2d[3] = float(input("y_max: "))

        size_2d[0] = float(input("\nPlease enter the output figure size in inches:\nWidth: "))
        size_2d[1] = float(input("Height: "))
        flag = False
    elif plot_type == "3d":
        dim_3d[0] = float(input("\nPlease enter axis boundaries in AU:\nx_min: "))
        dim_3d[1] = float(input("x_max: "))
        dim_3d[2] = float(input("y_min: "))
        dim_3d[3] = float(input("y_max: "))
        dim_3d[4] = float(input("z_min: "))
        dim_3d[5] = float(input("z_max: "))
        flag = False
    elif plot_type == "both":
        dim_2d[0] = float(input("\nPlease enter axis boundaries in AU:\nx_min: "))
        dim_2d[1] = float(input("x_max: "))
        dim_2d[2] = float(input("y_min: "))
        dim_2d[3] = float(input("y_max: "))

        size_2d[0] = float(input("\nPlease enter the output figure size in inches:\nWidth: "))
        size_2d[1] = float(input("Height: "))

        dim_3d[0] = float(input("\nPlease enter axis boundaries in AU:\nx_min: "))
        dim_3d[1] = float(input("x_max: "))
        dim_3d[2] = float(input("y_min: "))
        dim_3d[3] = float(input("y_max: "))
        dim_3d[4] = float(input("z_min: "))
        dim_3d[5] = float(input("z_max: "))
        flag = False
    else:
        input("\nInvalid plot type, please use '2d' for x and y data, and '3d' for x, y, and z data.\n\nPress ENTER to continue.\n")

object_dict = {}

print("\nLoaded objects:")
for path in pathlist:
    path_str = str(path)
    object = Celestial_Object(path_str)  
    object_dict[object.name] = object
    print(object.name)

sorted_objects = dict(sorted(object_dict.items(), key = lambda item: np.linalg.norm(item[1].r_0)))
object_arr = np.array(list((sorted_objects.values())))

'''The following simulates solar system starting on Jan 1st 2000'''

print("\nRunning model...")
model_time_start = time.time()
# Creating the Solar System object
SolarSys = Solar_System(object_arr,0,time_end*(365*24*3600),delta_t*(3600*24))
print("Total model runtime", time.time()-model_time_start, "seconds.")

# Runs chosen method
if method == "vv":
    SolarSys.Velocity_Verlet()
elif method == "rk4":
    SolarSys.RK4()

# Creating plots
if plot_type == "2d":
    plot_2d(SolarSys, dim_2d, size_2d)
elif plot_type == "3d":
    plot_3d(SolarSys, dim_3d)
elif plot_type == "both":
    plot_2d(SolarSys, dim_2d, size_2d)
    plot_3d(SolarSys, dim_3d)

print("Script complete.")