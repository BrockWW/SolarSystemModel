'''Script for running the solar system model and saving/visualizing output.'''

import numpy as np
from pathlib import Path

from solar_system_classes import *
from plotting_functions import *

object_dict = {}

pathlist = Path("object_data/major_planets").glob('*')
for path in pathlist:
    path_str = str(path)
    object = Celestial_Object(path_str)  
    object_dict[object.name] = object
    print(object.name, object.mass)

sorted_objects = dict(sorted(object_dict.items(), key = lambda item: np.linalg.norm(item[1].r_0)))

object_arr = np.array(list((sorted_objects.values())))

'''The following simulates solar system starting on Jan 1st 2000'''

#Creating the Solar System object
SolarSys = Solar_System(object_arr, t_0 = 0, t_f = (10)*(365*24*3600), delta_t = 2*(3600*24))

#Runs Velocity Verlet Numerical Method
#SolarSys.Velocity_Verlet()
SolarSys.RK4()

plot_2d(SolarSys, (-5,5,-5,5), (10,10))
plot_3d(SolarSys, (-5,5,-5,5, -1, 1))