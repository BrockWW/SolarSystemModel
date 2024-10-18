'''Script containing functions for solar system visualization.'''

import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go

def plot_2d(solar_system_object, axis_lims = (1,1,1,1), im_size = (10,10)):
    AU = 1.495978707e11   # m

    low_x, high_x, low_y, high_y = axis_lims

    plt.figure(figsize=im_size)

    for object in solar_system_object.objects:
        name = object.name
        plt.plot(solar_system_object.r_arrays[name][:,0]/AU, solar_system_object.r_arrays[name][:,1]/AU, label = " "+name)

    plt.title("Solar System Model")
    plt.xlabel("x (AU)")
    plt.ylabel("y (AU)")

    plt.legend()
    plt.axis('equal')
    plt.grid()
  
    plt.xlim(low_x, high_x)
    plt.ylim(low_y, high_y)

    plt.savefig("plot_outputs/2d_plot.pdf")

    return


def plot_3d(solar_system_object, axis_lims = (1,1,1,1,1,1)):
    AU = 1.495978707e11   # m

    low_x, high_x, low_y, high_y, low_z, high_z = axis_lims

    # Configure Plotly to be rendered inline in the notebook.
    #plotly.offline.init_notebook_mode()

    data = []

    for planet in solar_system_object.objects:
        name = planet.name

        # Configure the trace.
        trace = go.Scatter3d(
            x = solar_system_object.r_arrays[name][:,0]/AU,
            y = solar_system_object.r_arrays[name][:,1]/AU,
            z = solar_system_object.r_arrays[name][:,2]/AU,
            marker = {'size': 0.1},
            line = {'width': 2},
            name = name)

        data.append(trace)

    # Configure the layout.
    layout = go.Layout(margin = {'l': 0, 'r': 0, 'b': 0, 't': 0}, 
                    scene = dict(aspectmode = 'cube',
                                    xaxis={'range':[low_x,high_x]},
                                    yaxis={'range':[low_y,high_y]},
                                    zaxis={'range':[low_z,high_z]}))
    plot_figure = go.Figure(data = data, layout = layout)

    # Render the plot.
    #plotly.offline.plot(plot_figure)
    plot_figure.write_html("plot_outputs/3d_plot.html")

    return