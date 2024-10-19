'''Script for running the solar system model and saving/visualizing output.'''

import numpy as np
from pathlib import Path

from solar_system_classes import *
from plotting_functions import *

# Data path entry

#######################
# work on asking again if given directory does not exist
#######################
flag = True
while flag:
    data_path = input("Please input the local path to directory containing all object data files:")
    try:
        pathlist = Path(data_path).glob('*')
        flag = False
    except:
        input("Path must be a string.\n\nPress ENTER to continue.\n")

# Model method selection
flag = True
while flag:
    method = input("Please select the numerical method to run the model with:\nVelocity Verlet (VV)\n4th Order Runge-Kutta (RK4):")
    method = method.lower()
    if method == "vv" or method == "rk4":
        flag = False
    else:
        input("Invalid method, please use 'VV' for Velocity Verlet or 'RK4' for 4th Order Ruge-Kutta.\n\nPress ENTER to continue.\n")

# Output plot selection
flag = True
while flag:
    plot_type = input("Please select the plot outputs:\n2d - Creates plot of x and y data\n3d - Creates plot of x, y, and z data in interactive HTML\nboth - Creates both the 2d and 3d plot")
    plot_type = plot_type.lower()

    size_2d: set = (0.,0.)
    dim_2d: set = (0.,0.,0.,0.)
    dim_3d: set = (0.,0.,0.,0.,0.,0.)

    if plot_type == "2d":
        dim_2d = input("Please enter axis boundaries in the following format: (x_min, x_max, y_min, y_max)")
    elif plot_type == "3d":
        dim_3d = input("Please enter axis boundaries in the following format: (x_min, x_max, y_min, y_max, z_min, z_max)")
    elif plot_type == "both":
        dim_2d = input("Please enter 2D axis boundaries in the following format: (x_min, x_max, y_min, y_max)")
        dim_3d = input("Please enter 3D axis boundaries in the following format: (x_min, x_max, y_min, y_max, z_min, z_max)")
    else:
        input("Invalid plot type, please use '2d' for x and y data, and '3d' for x, y, and z data.\n\nPress ENTER to continue.\n")

object_dict = {}


for path in pathlist:
    path_str = str(path)
    object = Celestial_Object(path_str)  
    object_dict[object.name] = object
    print(object.name, object.mass)

sorted_objects = dict(sorted(object_dict.items(), key = lambda item: np.linalg.norm(item[1].r_0)))

object_arr = np.array(list((sorted_objects.values())))

'''The following simulates solar system starting on Jan 1st 2000'''

# Creating the Solar System object
SolarSys = Solar_System(object_arr, t_0 = 0, t_f = (10)*(365*24*3600), delta_t = 2*(3600*24))

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