"""
The :mod:`paddy.writer` module contains built in data display functions.

Module functions are used to print specific data to terminal, formating
output in a user friendly manner, and quickly generate plots via the
`matplotlib.pyplot` module.  Data is often passed via methods found in
:mod:`paddy.Paddy_Runner`.

Routine Listings
----------------
box(g_data, box_type)
    Function that produces box plots.
average_gen_plot(g_data)
    Function that plots the average fitness for each *generation*.
average_population_plot(g_data)
    Function that plots the average fitness for the *population*
    during each itteration.
preformace_plotter(info,verbose)
    Function that handles other module level functions for plotting.
clean_parameter_print(dirty_values)
    Function that prints information regarding the top evaluated seed for
    each iteration, including a list of parameter values on a single line.
single_param_print(dirty_values,value_key)
    Function that prints the parameters for a user specified seed.


See Also
--------

:meth:`paddy.Paddy_Runner.PFARunner.paddy_plot_and_print` : `PFARunner` method
    that handles data output functions.

matplotlib.pyplot : Plotting package dependancy.
    See more at `<https://matplotlib.org/>` for specifics.

Notes
-----
The `PFARunner` method `paddy_plot_and_print` calls `preformace_plotter`
when passed relevant arguments such as 'scatter'.  Refer to
`paddy_plot_and_print` documentation for information regarding how data is
generated and passed to `preformace_plotter`

"""
# Authors: Armen Beck & Jonathan Fine
# License: BSD

import numpy as np
import matplotlib.pyplot as plt

def box(g_data, box_type):
    """Plot boxplots via `preformance_plotter`.

    Function that plots the desired box plot type as specified by the user.

    Parameters
    ----------
    g_data : dictionary
        A dictionary with keys being the paddy iteration, with '0'
        representing the random initiation step, and values being a
        numpy-array containig parameter and gausian values.

    box_type : integer
        One of the integers: 1, 2, or 3.  The number is associated with a
        respective box plot type detailed in the notes section.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.paddy_plot_and_print` : `PFARunner`
        method that handles data output functions.

    preformance_plotter : Function that manages plotting arguments passed by
        `paddy.Paddy_Runner.PFARunner.paddy_plot_and_print`

    plt.boxplot : Function that generates boxplots as part of the
        `matplotlib.pyplot` module.

    Notes
    -----
    The `box_type` parameter is an integer assigned as a numeric
    representation of a string argument passed via the `verbose` parameter of
    the `preformance_plotter` function.  The numeric values are related to the
    string arguments as:

        * 1: equivalent to 'box'.
        * 2: equivalent to 'box_hidden'
        * 3: equivalent to 'box_notched'

    See documentation for `preformance_plotter` and `paddy_plot_and_print` for
    details on how `box` is called.
    """
    plot_data = []
    x_val = []
    counter = 0
    for i in g_data:
        temp = g_data['{0}'.format(counter)]
        x_val.append(counter)
        data = temp
        plot_data.append(data)
        counter += 1
    if box_type == 1:
        #default box plot
        return plt.boxplot(plot_data, positions=x_val)
    if box_type == 2:
        #box plot without scatter
        return plt.boxplot(plot_data, 0, '', positions=x_val)
    if box_type == 3:
        #box plot with indents
        return plt.boxplot(plot_data, 1, positions=x_val)

def average_gen_plot(g_data):
    """Plot average fitness for each generation.

    Function that plots the average fitness value for the seeds sown during
    each iteration.

    Parameters
    ----------
    g_data : dictionary
        A dictionary with keys being the paddy iteration, with '0'
        representing the random initiation step, and values being a
        numpy-array containig parameter and gausian values.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.paddy_plot_and_print` : `PFARunner`
        method that handles data output functions.

    preformance_plotter : Function that manages plotting arguments passed by
        `Paddy_Runner.PFARunner.paddy_plot_and_print`.

    plt.plot : Plotting function as part of the `matplotlib.pyplot` module.

    Notes
    -----
    `average_gen_plot` is typically called by `preformance_plotter` via the
    `PFARunner` method `paddy_plot_and_print`.  See respective documentation
    for detailes on how `average_gen_plot` is called.
    """
    ave = []
    counter = -1
    x_list = []
    counter_2 = 0
    for i in g_data:
        counter += 1
        x_list.append(counter)
        ave.append(np.average(g_data['{0}'.format(counter_2)]))
        counter_2 += 1
    return plt.plot(x_list, ave, color='orange',
                    label='Average Fitness of Iteration')


def average_population_plot(g_data):
    """Plot average fitness for the population during each iteration.

    Function that plots the average fitness value for the seeds within
    the population of evaluated seeds at each given interation.

    Parameters
    ----------
    g_data : dictionary
        A dictionary with keys being the paddy iteration, with '0'
        representing the random initiation step, and values being a
        numpy-array containig parameter and gausian values.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.paddy_plot_and_print` : `PFARunner`
        method that handles data output functions.

    preformance_plotter : Function that manages plotting arguments passed by
        `paddy.Paddy_Runner.PFARunner.paddy_plot_and_print`

    matplotlib.pyplot

    Notes
    -----
    `average_population_plot` is typically called by `preformance_plotter` via
    the `PFARunner` method `paddy_plot_and_print`.  See respective
    documentation for detailes on how `average_gen_plot` is called.
    """
    temp = []
    ave = []
    counter = -1
    x_list = []
    counter_2 = 0
    for i in g_data:
        counter += 1
        x_list.append(counter)
        temp.append(g_data['{0}'.format(counter_2)])
        ave.append(np.average(np.concatenate(temp)))
        counter_2 += 1
    return plt.plot(x_list, ave, color='green', label='Average Fitness of Population')

def preformance_plotter(info, verbose, figure_name=None):
    """Plot preformance as specified.

    Function that plots the results from a completed paddy run.  The type of
    plot argument string is typically passed through the `PFARunner` method
    `paddy_plot_and_print`.

    Parameters
    ----------
    info : list
        A list containing a list generated by `get_top_fitness`, and a
        dictionary of the form `PFARunner.generation_fitness`.

    verbose : set of strings
        A set of string comand(s), typically passed by `paddy_plot_and_print`.
        See the notes section for a full list of valid strings.

    figure_name : string
        A string passed by `paddy_plot_and_print` that provides a file
        handle for the figure being saved.

    See Also
    --------
    paddy.utils.get_top_fitness : Function that returns a list of fitness
        values.

    :meth:`paddy.Paddy_Runner.PFARunner.paddy_plot_and_print` : `PFARunner`
        method that handles data output functions.

    average_gen_plot

    average_population_plot

    box

    matplotlib.pyplot

    Notes
    -----
    `preformance_plotter` is typically called by the `PFARunner` method
    `paddy_plot_and_print` when valid string arguments are passed by the
    user.  Valid strings that will call `preformace_plotter` from the
    `paddy_plot_and_print` method are:

    * 'best_sown'
        A line plot of the best seed sown during each iteration.
    * 'average_gen'
        A line plot of the average fitness of the seeds sown during each
        iteration.
    * 'average_population'
        A line plot of the average fitness value of all seeds at the end of
        each iteration.
    * 'scatter'
        A scatter plot of each seeds fitness value for each iteration.
    * 'box'
        A box plot of the sown seeds for each iteration.
    * 'box_notched'
        Same as box, but with notched boxes.
    * 'box_hidden'
        Same as box, but with outliers ommited.

    Refer to `<https://matplotlib.org/>`_ for specifics regarding plotting.
    """
    plotter_types = {'best_sown', 'average_population',
                     'average_gen', 'scatter', 'box',
                     'box_notched', 'box_hidden'}

    if len(plotter_types.intersection(verbose)) > 0:
        plt.figure()
        x_1 = list(range(len(info[0])))
        plt.ylabel("Error")
        plt.xlabel("Iteration")
        plt.title("Fitness Throughout Paddy Iterations")
        if 'best_sown' in verbose:
            plt.plot(x_1, info[0], color='blue',
                     label='Best Seed During Sowing')
        g_data = info[1]
        counter = 0
        y_s = []
        x_2 = []
        for i in g_data:
            for j in g_data[str(counter)]:
                y_s.append(j)
                x_2.append(counter)
            counter += 1
        if 'average_gen' in verbose:
            average_gen_plot(g_data)
        if 'average_population' in verbose:
            average_population_plot(g_data)
        if "scatter" in verbose:
            plt.scatter(y=y_s, x=x_2)
        if 'box' in verbose:
            box(g_data, 1)
        if 'box_notched' in verbose:
            box(g_data, 3)
        if 'box_hidden' in verbose:
            box(g_data, 2)
        plt.tight_layout()
        plt.legend()
        if figure_name is not None:
            plt.savefig(figure_name, dpi=300)
        else:
            plt.show()
        plt.close()
    else:
        print('preformance_ploter was not provided verbose containing valid argument')


def clean_parameter_print(dirty_values):
    """Prints parameter values of `PFARunner` atribute ``top_values``.

    Function that prints information regarding the top seed evaluated for
    sowing during each iteration of paddy.

    Parameters
    ----------
    dirty_values : dictionary
        Dictionary with the same structure of `PFARunner.top_values`.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.run_paddy`

    :meth:`paddy.Paddy_Runner.PFARunner.paddy_plot_and_print`

    Notes
    -----
    This function prints two lines for each iteration, where the first line
    contains details on what seed was most fit during the selection step and
    the second line consists of a list of parameter values.  Be mindfull of
    this when using this function as it is intended for low iteration
    implementations of paddy, such as deep learning, and a high iteration run
    will result in a proportionaly long print time.

    The function is typically called by `PFARunner.paddy_plot_and_print`
    when passed the argument 'final_results'.
    """
    counter = 0
    for i in dirty_values:
        temp = []
        for j in dirty_values[str(counter)]['parameters']:
            temp.append(j[0])
        print(str(counter)+':seed_'+str(dirty_values[str(counter)]['seed'])
              +':Fitness:'+str(dirty_values[str(counter)]['fitness'])+'  Parameters:')
        print(temp)
        counter += 1

def single_param_print(dirty_values, value_key):
    """Prints the parameters for a specific seed.

    Function that typically prints parameter values stored in
    `PFARunner.seed_params` when called throughout a paddy run.

    Parameters
    ----------
    dirty_values : list of array-like, shape = (seed_counter,parameters,2)
        A list of numpy-arrays containing the parameter and gaussian values
        for each `PaddyParameter` instance in `PFARunner.space` of a given
        paddy run.  Typically the `PFARunner.seed_params` atribute.

    value_key : integer
        A integer that represents the seed number that the parameters are to
        be printed for.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.run_paddy` : method that excecutes the
        paddy field algorithm.

    Notes
    -----
    This function is natively called when 'top_gen' or 'pop' are passed via
    `paddy.Paddy_Runner.PFARunner.run_paddy` when listed as an element in the
    `verbose` parameter. The list that is printed contains strictly the
    parameter values of the `PFARunner.space` atributes of a given seed,
    rather than the associated gaussian values.
    """
    temp = []
    for i in dirty_values[value_key]:
        temp.append(i[0])
    print(temp)
