r"""
The :mod:`paddy.Paddy_Runner` module contains the
:class:`~paddy.Paddy_Runner.PFARunner` class and its associated methods.

Routine listings
----------------
PFARunner(object)
    Paddy class that runs the paddy field algorithm.

PFARunner.random_step()

PFARunner.run_paddy(self, file_name=None, verbose=None )

See Also
--------
:mod:`paddy.utils`

:mod:`paddy.Paddy_Parameter`

Notes
-----
The two user defined :class:`~paddy.Paddy_Runner.PFARunner` parameters
``space`` and ``eval_func`` must be defined such that they are consistent with
the internal operations of paddy.  Refer to their specific documentation
detailed in the **Parameters** section of
:class:`~paddy.Paddy_Runner.PFARunner` for more information.

Examples
--------
A generic example of using the :mod:`paddy.Paddy_Runner` module
:class:`~paddy.Paddy_Runner.PFARunner` and associated methods in a typical
manner.  In this case, we are setting up a `PFARunner` to optimize (x,y)
coordinates for a paraboloid of :math:`z=-\frac{x^2}{7}-\frac{y^2}{2}+1`.

>>> import paddy
>>> def parabola(input):
...     x = input[0][0]
...     y = input[1][0]
...     return(((x**2)/7)-((y**2)/2)+1)# The maximum is when x and y are 0
...
>>> # now we need to set our parameter space for x and y
>>> x_param = paddy.PaddyParameter(param_range=[-5,5,.2],
...                                param_type='continuous',
...                                limits=None, gaussian='scaled',
...                                normalization = False)
...
>>> y_param = paddy.PaddyParameter(param_range=[-7,3,.2],
...                                param_type='continuous',
...                                limits=None, gaussian='scaled',
...                                normalization = False)
...
>>> # now we make a class with the parameter spaces we defined
>>> class paraboloid_space(object):
...     def __init__(self):
...         self.xp = x_param
...         self.yp = y_param
...
>>> # now we need to initialize a `PFARunner`
>>> example_space = paraboloid_space() #the space parameter
>>> example_runner = paddy.PFARunner(space=example_space,
...                                  eval_func=parabola,
...                                  paddy_type='population',
...                                  rand_seed_number = 20,
...                                  yt = 10,
...                                  Qmax = 5,
...                                  r=.2,
...                                  iterations = 5)
...
>>> example_runner.run_paddy(file_name='paddy_example')
paddy is done!

Lets load the :mod:`~paddy.Paddy_Runner` and run it some more

>>> import paddy
>>> # we need to define the dependent evaluation function
>>> def parabola(input):
...     x = input[0][0]
...     y = input[1][0]
...     return(((-x**2)/7)-((y**2)/2)+1)# The maximum is when x and y are 0
...
>>> recovered_example = paddy.paddy_recover('paddy_example')
>>> recovered_example.recover_run()
recovered paddy run was already completed, use extend_paddy
>>> # woops! Wrong method, lets use `extend_paddy`!
>>> recovered_example.extend_paddy(5)
paddy is done!

Lets graph the results using
:meth:`~paddy.Paddy_Runner.PFARunner.paddy_plot_and_print`

>>> example_runner.paddy_plot_and_print(('scatter',
...                                      'average_gen',
...                                      'average_population'))
...

.. image:: example_figure.png

Looks good!  But what parameters do the top seed have?

>>> example_runner.get_top_seed()
['seed_116']
>>> example_runner.seed_fitness[116]
0.9961291072913099
>>> example_runner.seed_params[]
array([[-0.29531996, -0.02205951],
       [-0.25822639,  0.01529183]])

"""
import pickle
import math
import numpy as np
from scipy.spatial import distance
from paddy.exceptions import (RADIUS_ERROR, INT_PARAM_ERROR,
                              PADDY_TYPE_ERROR, CONTAINER_ERROR,
                              EXTENSION_ERROR, PaddyParamError,
                              PADDY_FILE_ERROR, RANDOM_SEED_ERROR,
                              PaddyRunnerError)
from paddy.utils import random_propogation, get_top_fitness, get_param_names
from paddy.writer import *

class PFARunner(object):
    """Class that runs PFA.

    `PFARunner` handles the user defined parameters, and exicutes
    the paddy field algorithm for a defined amount of iterations.

    Parameters
    ----------
    space : class
        A user defined class that is comprised of `PaddyParameter`
        instances for attributes.

    eval_func : function, or method
        A function or method that returns a value to be maximized.
        The function must accept an array-type input where
        shape = (parameters,2) and reads the zeroth index of every
        two index lenght slice as a the parameter value where the
        first index position is the gaussian value which should be
        ignored.

    paddy_type: string
        The string 'population' or 'generational' to specify which
        method is used during the selection step.

    rand_seed : integer
        A numeric that defines the number of random seeds generated.

    yt : integer
        A numeric that defines the threshold operator for the
        evaluation step.

    Qmax : integer
        A numeric that defines the maximum number of seeds posible
        that a plant can produce.

    iterations : integer
        A numeric that defines the amount of iterations that paddy
        will run.

    error_handling : bool, optional (default: True)
        A boolean that allows the user to bypass built in error
        handlings.


    Attributes
    ----------
    yt_prime : integer or float
        A numeric that is defined by the origional `yt` parameter
        and is called to reset `yt` if `yt` is modified otherwise
        while running paddy.

    seed_counter : integer
        A numeric that tracks the number of seeds generated.

    paddy_counter : integer
        A numeric that tracks the number of iteration run.

    seed_params : list
        A list of seed parameters generated while running paddy.

    seed_fitness: list
        A list of seed fitness values.

    generation_data : dictionary
        A dictionary that documents the seed indexes per paddy
        iteration.

    generation_fitness : dictionary
        A dictionary of iterations and the fitness values of
        their respective seeds.

    top_values : dictionary
        A dictionary of the top seed per iteration, and their
        respective fitness value and parameters.

    s : array-like, shape = (yt, 2)
        A numpy array containing seed indexes and the number of
        unpolinated seeds.

    Un : array-like, shape = (yt, 2)
        A numpy array containing seed indexes and neighbor count
        values.

    S : array-like, shape = (yt, 2)
        A numpy array containing seed indexes and the number of
        polinated seeds.

    recover : bool (default : False)
        A boolean that determines if the instance of `PFARunner` has been
        recovered.

    Methods
    -------
    run_paddy(file_name=None, verbose=None)
        Executes the paddy field algorithm.  `PFARunner` methods utilized by
        `run_paddy` are described in the respective note section per method.

    paddy_plot_and_print(verbose=None)
        Used to print, and or graph, results.

    save_paddy(new_file_name=None)
        Saves the given instance of `PFARunner`.

    recover_run(new_verbose=None)
        Resumes the paddy field algorithm if otherwise
        interupted or recovered.

    extend_paddy(new_iterations, new_file_name=None, new_verbose=None)
        Extends the iterations of a previously completed
        instance of `PFARunner`.

    get_top_seed()
        Provides the seed of greatest fitness in population.

    get_generation_top_seed(counter=None, verbose=False)
        Provides the seed of greatest fitness in a generation.

    Raises
    ------
    PaddyRunnerError
        If parameter value(s) used to initialize an instance of `PFARunner`
        would raise an exception when calling methods of `PFARunner`.

    """
    def __init__(self, space, eval_func, rand_seed_number,
                 yt, Qmax, paddy_type, r, iterations,
                 error_handling=True):
        if error_handling:
            _int_params = [rand_seed_number, yt, Qmax, iterations]
            ipn = ['rand_seed_number', 'yt', 'Qmax', 'iterations']
            for i in range(len(_int_params)):
                if isinstance(
                        _int_params[i],
                        (list, tuple, set, dict, np.ndarray)):
                    if len(_int_params[i]) > 1:
                        error = CONTAINER_ERROR.format(ipn[i])
                        raise PaddyParamError(error)
                    _int_params[i] = _int_params[i][0]
                if isinstance(_int_params[i], str):
                    if not _int_params[i].isdigit():
                        error = INT_PARAM_ERROR.format(ipn[i], _int_params[i])
                        raise PaddyParamError(error)
                    _int_params[i] = float(_int_params[i])
                if isinstance(_int_params[i], float):
                    if not _int_params[i] % 1 == 0:
                        error = INT_PARAM_ERROR.format(ipn[i], _int_params[i])
                        raise PaddyParamError(error)
                    _int_params[i] = int(_int_params[i])
                if isinstance(_int_params[i], int):
                    if _int_params[i] < 1:
                        error = INT_PARAM_ERROR.format(ipn[i], _int_params[i])
                        raise PaddyParamError(error)
            if isinstance(r, (list, tuple, set, dict, np.ndarray)):
                if len(r) > 1:
                    error = CONTAINER_ERROR.format('r')
                    raise PaddyParamError(error)
                r = r[0]
            if isinstance(r, str):
                try:
                    r = float(r)
                except:
                    error = RADIUS_ERROR.format(r)
                    raise PaddyParamError(error)
            if r < 0:
                error = RADIUS_ERROR.format(r)
                raise PaddyParamError(error)
            if isinstance(paddy_type, (list, tuple, set, dict, np.ndarray)):
                if len(paddy_type) > 1:
                    error = CONTAINER_ERROR.format('paddy_type')
                    raise PaddyParamError(error)
                paddy_type = paddy_type[0]
            if paddy_type not in ('generational','population'):
                error = PADDY_TYPE_ERROR.format(paddy_type)
                raise PaddyParamError(error)
            (rand_seed_number, yt, Qmax, iterations) = (_int_params[0],
                                                        _int_params[1],
                                                        _int_params[2],
                                                        _int_params[3])

            if rand_seed_number < 4:
                raise PaddyParamError(RANDOM_SEED_ERROR)
        self.Qmax = Qmax
        self.yt = yt
        self.yt_prime = yt
        self.rand_seed_number = rand_seed_number
        if yt > rand_seed_number:
            print('threshold operatior is greater than seeds in\
             random initiation, Yt is set to 3/4ths the random seed number')
            self.yt = int(np.round(rand_seed_number * .75))
        self.eval_func = eval_func
        self.r = r
        self.space = space #must be a class made of PaddyParameter instances
        self.seed_counter = 1
        self.seed_params = []
        self.seed_fitness = []
        self.paddy_type = paddy_type
        self.paddy_counter = 0
        self.s = np.array([])
        self.S = np.array([])
        self.Un = np.array([])
        self.iterations = iterations
        self.generation_data = {}
        self.generation_fitness = {}
        self.top_values = {}
        self.recover = False
        self.verbose = None
        self.file_name = None

    def random_step(self):
        """Generate random seeds.

        Excecutes the initialization step of the paddy field algorithm via
        random propogation of `PaddyParameter` attributes in provided space.

        See Also
        ----------
        :func:`paddy.utils.random_propogation` : function that generates
            random seeds and an updated seed counter.

        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.
        """
        self.seed_counter, rand_seeds = random_propogation(
                                    rand_seed_number=self.rand_seed_number,
                                    p_space=self.space,
                                    seed_counter=self.seed_counter)
        c = 1
        for i in rand_seeds:
            self.seed_params.append(i)
            self.seed_fitness.append(self.eval_func(i))
            if self.verbose is not None:
                if 'status' in self.verbose:
                    print(str(c)+" of "+str(len(rand_seeds))+" seeds", "  complete\r",)
                    c += 1
        self.generation_data['0'] = [0, int(self.rand_seed_number)-1]
        ############Top Gen Seed###########
        if self.verbose is not None:
            if 'top_gen' in self.verbose:
                best_rand_seed = self.get_top_seed()
                print("Best seed(s) during random initiation was:\
                "+str(best_rand_seed))
        ##################################

    def sowing_function(self):
        r"""Generate unpolinated seeds.

        Applies the threshold operator `yt` on the seeds to be considered,
        defined by the paddy type, and calculates the number of unpolinated
        seeds for the subsequent steps in the paddy field algorithm.

        See Also
        --------
        run_paddy : `PFARunner` method that excecutes the paddy field
            algorithm.

        Notes
        -----
        The user defined threshold operator `yt` is used to select seeds
        to be subsequently considered for the remaining steps of the current
        paddy itteration, where `yt` is an integer that represents the nth
        fittest seed.  However, if `yt` is greater than the number of seeds
        being considered, `yt` is redefined as:

        .. math:: y_{t}\simeq 0.75 \ast y_{considered}

        New seeds (`s`) are then generated for evaluated seeds of fitness
        greater than `yt` using min-max feature scalling to the form of:

        .. math:: s=Q_{max^{\ast}}[{y-y_{t}\over y_{max}-y_{t}}]
        """
        seed_key_numbers = self.generation_data[str(self.paddy_counter)]
        temp_gen_fit = []
        for i in range(seed_key_numbers[0], seed_key_numbers[1]+1):
            temp_gen_fit.append(self.seed_fitness[i])
        self.generation_fitness[str(self.paddy_counter)] = temp_gen_fit
        if self.verbose is not None:
            ###########Top Gen Seed###########
            if 'top_gen' in self.verbose:
                print('Top seed in generation:')
                ts = self.get_generation_top_seed()
                if len(ts) > 1:
                    print(ts, 'fitness:',
                          self.seed_fitness[int((ts[0]).split('_')[1])])
                if len(ts) == 1:
                    print(ts[0], 'fitness:',
                          self.seed_fitness[int((ts[0]).split('_')[1])])
                for i in ts:
                    if len(ts) > 1:
                        print(int((i).split('_')[1]))
                    single_param_print(self.seed_params,
                                       int((i).split('_')[1]))
            #########Top in Population########
            if 'pop' in self.verbose:
                print('Top seed in population:')
                tp = self.get_top_seed()
                if len(tp) > 1:
                    print(tp, 'fitness:',
                          self.seed_fitness[int((tp[0]).split('_')[1])])
                if len(tp) == 1:
                    print(tp[0], 'fitness:',
                          self.seed_fitness[int((tp[0]).split('_')[1])])
                for i in tp:
                    if len(tp) > 1:
                        print(int((i).split('_')[1]))
                    single_param_print(self.seed_params,
                                       int((i).split('_')[1]))
            ##################################
        if self.paddy_type == 'generational':
            if self.yt > seed_key_numbers[1]+1 - seed_key_numbers[0]:
                self.yt = int(np.round((seed_key_numbers[1]+1 -
                                        seed_key_numbers[0])*.75))
            gen_clone = []
            for i in range(seed_key_numbers[0], seed_key_numbers[1]+1):
                gen_clone.append([i, self.seed_fitness[i]])
            gen_clone = np.array(gen_clone)
            gen_clone = gen_clone[gen_clone[:, 1].argsort()]
            y_max = gen_clone[-1][1]
            self.top_values[str(self.paddy_counter)] = {}
            self.top_values[str(self.paddy_counter)]['fitness'] = y_max
            self.top_values[str(self.paddy_counter)]['parameters'] = self.seed_params[
                int(gen_clone[-1][0])]
            self.top_values[str(self.paddy_counter)]['seed'] = 'seed_{0}'.format(
                int(gen_clone[-1][0]))
            yt_val = [gen_clone[-self.yt][1]]
            counter = 1
            self.s = []
            while counter != self.yt +1:
                if yt_val != y_max:
                    self.s.append([int(gen_clone[-counter][0]),
                                   (self.Qmax * ((gen_clone[-counter][1] - yt_val)/
                                                 float(y_max - yt_val)))])
                counter += 1
            self.s = np.array(self.s,dtype='object')
        if self.paddy_type == 'population':
            pop_clone = []
            pop_clone.append([])
            population_fitness_keys = sorted(self.seed_fitness)
            ###the above does not consider the case
            ###where multiple top values are the exact same
            y_max = self.seed_fitness[np.argmax(self.seed_fitness)]
            self.top_values[str(self.paddy_counter)] = {}
            self.top_values[str(self.paddy_counter)]['fitness'] = y_max
            self.top_values[str(self.paddy_counter)]['parameters'] = self.seed_params[
                np.argmax(self.seed_fitness)]
            self.top_values[str(self.paddy_counter)]['seed'] = np.argsort(
                np.array(self.seed_fitness,dtype='object'))[-1]
            yt_val = population_fitness_keys[-self.yt]
            counter = 1
            self.s = []
            while counter != self.yt + 1:
                if yt_val != y_max:
                    self.s.append([np.argsort(np.array(self.seed_fitness,dtype='object'))[-counter],
                                   (self.Qmax * ((population_fitness_keys[-counter] -
                                                  yt_val) / float(y_max - yt_val)))])
                counter += 1
            self.s = np.array(self.s,dtype='object')


    def neighbor_counter(self):
        r"""Generate neighbor counts and polinated seeds.

        Calculates the amount of neighbors per seed, and then uses the
        neighbor counts to calculate the polination factor per seed. Polinated
        seed values are defined as the rounded integer resulting from the
        product of the unpolinated seed term and polination term.

        See Also
        --------
        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.

        :meth:`paddy.Paddy_Parameter.PaddyParameter.get_ecludian_values` :
            Function that retrieves values for calculating ecludian distance
            of parameters.

        Notes
        -----
        Polinated seeds are calculated as the product of unpolinated seed
        numbers (`s`) and the polination factor (`U`).  The polination factor
        is varient and defined by the number of 'neighbors' within the
        population of seeds being evaluated.  Neighbors (`u`) are defined as
        seeds falling within the radius (`r`) of a multi-dimensional euclidean
        space as such:

         .. math::   u(x_{j},x_{k})=\left \| x_{j}-x_{k} \right \|-r<0

        After calculating the number of neighbors per seed in the evaluated
        population, a polination factor is then calculated and assigned as a
        normalized value falling between zero and one via the expression:

        .. math:: U=e^{[{u\over u_{max}}-1]}

        If the radius parameter provided by the user fails to generate any
        neighbors for the evaluated seeds, an initial quantile cutoff of 0.75
        is applied to an internal list of euclidean distances to generate a
        new radius term for neighbor counting.  This corrective procedure
        itterates untill the evaluated population contains seeds with
        neighbors, with the quantile cutoff decreasing by 0.05 untill a cutoff
        of 0.05 is applied.  In the case that this fails, the number of
        neighbors per seed is simply assigned as one, effectively dropping the
        polination factor in the current iteration.
        """
        p_names = get_param_names(self.space)
        if len(self.s) < self.yt:
            n_values = np.empty([len(self.s), len(p_names)+1])
        else:
            n_values = np.empty([self.yt, len(p_names)+1])
        c = 0
        for i in self.s[:, 0]:
            n_values[c][0] = i
            c2 = 1
            for parameter in p_names:
                temp = getattr(self.space, parameter).get_ecludian_values(
                    self.seed_params[int(i)][c2-1])
                n_values[c][c2] = temp
                c2 += 1
            c += 1
        neighbors = []
        d_list = []
        for i in n_values:
            n_count = 0
            for j in n_values:
                if i[0] != j[0]:
                    d_list.append(distance.euclidean(i[1:], j[1:]))
                    if distance.euclidean(i[1:], j[1:])-self.r < 0:
                        n_count += 1
            neighbors.append([i[0], n_count])
        neighbors = np.array(neighbors,dtype='object')
        quantile_value = 0.75
        #this will let the paddy run even if there are no neighbors
        while all(x < 1 for x in neighbors[:, 1]):
            if quantile_value < 0.05:
                neighbors[:, 1] = 1
                print('you might want to tweek your paddy parameters,\
                 new seeds did not have neighbors')
                break
            neighbors = []
            for i in n_values:
                n_count = 0
                for j in n_values:
                    if i[0] != j[0]:
                        if (distance.euclidean(i[1:], j[1:])-np.quantile(
                                d_list, quantile_value) < 0):
                            n_count += 1
                neighbors.append([i[0], n_count])
            neighbors = np.array(neighbors,dtype='object')
            quantile_value -= 0.05
        n_max = max(neighbors[:, 1])
        self.Un = []
        for i in neighbors:
            self.Un.append([i[0], math.exp((i[1]/float(n_max))-1)])
        self.Un = np.array(self.Un,dtype='object')
        self.S = []
        c = 0
        while c < len(neighbors):
            self.S.append([neighbors[c, 0],
                           np.round(self.Un[c, 1]*self.s[c, 1])])
            c += 1
        self.S = np.array(self.S,dtype='object')

    def new_propogation(self):
        """Generate new seeds and evaluate.

        Assignes parameters to new seeds, and evaluates them to generate
        respective fitness values.

        See Also
        --------
        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.

        :meth:`paddy.Paddy_Parameter.PaddyParameter.new_seed_init` :
            `PaddyParameter` method that generates new seed parameters.
        """
        p_names = get_param_names(self.space)
        S_len = int(sum(self.S[:, 1]))
        iteration_seed_limits = [self.seed_counter, self.seed_counter+S_len-1]
        S_len_counter = 1
        #Status#
        if self.verbose is not None:
            if 'status' in self.verbose:
                print("Starting Iteration " +str(self.paddy_counter)+" of "
                      +str(self.iterations))
        ########
        #for each seed id in S
        for i in self.S:
            counter = 0
            while counter != i[1]:
                c = 0
                temp = np.empty([len(p_names), 2])
                for j in p_names:
                    temp[c] = getattr(self.space, j).new_seed_init(
                        self.seed_params[int(i[0])][c])
                    c += 1
                self.seed_params.append(temp)
                counter += 1
                self.seed_fitness.append(self.eval_func(
                    self.seed_params[self.seed_counter]))
                #Status#
                if self.verbose is not None:
                    if 'status' in self.verbose:
                        print(str(S_len_counter)+" of "+str(S_len)
                              +" seeds", "  complete\r",)
                ########
                S_len_counter += 1
                self.seed_counter += 1
        self.generation_data[str(self.paddy_counter)] = iteration_seed_limits

    def run_paddy(self, file_name=None, verbose=None):
        """Excecute paddy field algorithm :func:'run_paddy'.

        This method is used to run the paddy field algorithm.  A thorough
        explination of how the method works can be found in the notes section
        of the :mod:`paddy.Paddy_Runner` module.

        Parameters
        ----------
        file_name : string or nonetype, optional (default : None)
            A user defined string that is used as the file handle for
            `PFARunner` instance pickling.

        verbose : string or sequence of string, optional (default : None)
            String comand(s) that handle printing of values generated during
            paddy runs.  Valid strings include:
            ``('status','top_gen','pop','all')``.

        See Also
        --------
        :meth:`random_step` : Method that excecutes the random initiation
            step.

        :meth:`sowing_function` : Method that calculates unpolinated seed
            values.

        :meth:`neighbor_counter` : Method that calculates neighbor terms and
            the resulting polination term.

        :meth:`new_propogation` : Method that generates new seeds and
            evaluates them.

        :class:`paddy.Paddy_Parameter.PaddyParameter` : Class that handles
             calculations for specific parameters being optimized by paddy and
            communicates with `PFARunner` methods.

        Notes
        -----
        For specifics regarding the dependant methods and
        :class:`PaddyParameter`, refer to their respective documentation.

        Examples
        --------
        Setting up a paddy run using default `Polynomial` parameter space
        generator function to optimize parameters for trigonometric polynomial
        interpolation of the Gramacy & Lee function.

        >>> import paddy
        >>> from paddy.Default_Numerics import *

        The default polynomial class is used to set up parameter space:

        >>> polly_space = Polynomial(length=15, scope=1,
        ...                          gaussian_type='scaled',
        ...                          normalization=False)

        A class instance with an evaluation method for optimization:

        >>> class RunFunc(object):
        ...     def __init__(self):
        ...         self.xs , self.ys = gramacy_lee()
        ...     def eval(self,values):
        ...         score = eval_gl(seed=values,x=self.xs,y=self.ys)
        ...         return score
        >>> rf = RunFunc()

        A `PFARunner` instance is generated and run using run_paddy:

        >>> runner = paddy.PFARunner(space=polly_space,
        ...                            eval_func=rf.eval,
        ...                            rand_seed_number = 50,
        ...                            yt = 10, paddy_type='population',
        ...                            Qmax=50, r=0.75, iterations=10)

        `PFARunner` parameters can be changed before and after runs:

        >>> runner.Qmax = 10
        >>> runner.Qmax
        10

        The `PFARunner` instance can then run the paddy field algorithm:

        >>> runner.run_paddy()
        paddy is done!
        """
        self.file_name = file_name
        self.verbose = verbose
        #needs error handling for verbose
        if self.verbose == 'all':
            self.verbose = {'status', 'top_gen', 'pop'}
        if self.verbose is None:
            self.verbose = {}
        #needs error handling for file_name
        if file_name is not None:
            if not isinstance(file_name, str):
                raise PaddyRunnerError(PADDY_FILE_ERROR)
        if not self.recover:
            self.random_step()
            if self.file_name is not None:
                self.save_paddy()
        while self.paddy_counter < self.iterations:
            self.sowing_function()
            s_len = len(self.s)
            if s_len == 0:
                print('paddy has converged')
                return
            self.yt = self.yt_prime
            self.neighbor_counter()
            self.paddy_counter += 1
            self.new_propogation()
            if self.file_name is not None:
                self.save_paddy()
        self.top_values[str(self.paddy_counter)] = {}
        seed_key_numbers = self.generation_data[str(self.paddy_counter)]
        temp_gen_fit = []
        for i in range(seed_key_numbers[0], seed_key_numbers[1]+1):
            temp_gen_fit.append(self.seed_fitness[i])
        self.generation_fitness[str(self.paddy_counter)] = temp_gen_fit
        if self.paddy_type == 'generational':
            gen_clone = []
            for i in range(seed_key_numbers[0], seed_key_numbers[1]+1):
                gen_clone.append([i, self.seed_fitness[i]])
            gen_clone = np.array(gen_clone,dtype='object')
            gen_clone = gen_clone[gen_clone[:, 1].argsort()]
            y_max = gen_clone[-1][1]
            self.top_values[str(self.paddy_counter)] = {}
            self.top_values[str(self.paddy_counter)]['fitness'] = y_max
            self.top_values[str(self.paddy_counter)]['parameters'] = (
                self.seed_params[int(gen_clone[-1][0])])
            self.top_values[str(self.paddy_counter)]['seed'] = (
                'seed_{0}'.format(int(gen_clone[-1][0])))
        if self.paddy_type == 'population':
            y_max = self.seed_fitness[np.argmax(self.seed_fitness)]
            self.top_values[str(self.paddy_counter)] = {}
            self.top_values[str(self.paddy_counter)]['fitness'] = y_max
            self.top_values[str(self.paddy_counter)]['parameters'] = (
                self.seed_params[(np.argmax(self.seed_fitness))])
            self.top_values[str(self.paddy_counter)]['seed'] = (
                np.argsort(np.array(self.seed_fitness,dtype='object'))[-1])
        ###########Top Gen Seed###########
        #this prints the seed(s) id's and their fitness followed by parameters
        if 'top_gen' in self.verbose:
            print('Top seed in generation:')
            ts = self.get_generation_top_seed()
            if len(ts) > 1:
                print(ts, 'fitness:', self.seed_fitness[int((ts[0]).split('_')[1])])
            if len(ts) == 1:
                print(ts[0], 'fitness:', self.seed_fitness[int((ts[0]).split('_')[1])])
            for i in ts:
                if len(ts) > 1:
                    print(int((i).split('_')[1]))
                single_param_print(self.seed_params, int((i).split('_')[1]))
        #########Top in Population########
        if 'pop' in self.verbose:
            print('Top seed in population:')
            tp = self.get_top_seed()
            if len(tp) > 1:
                print(tp, 'fitness:',
                      self.seed_fitness[int((tp[0]).split('_')[1])])
            if len(tp) == 1:
                print(tp[0], 'fitness:',
                      self.seed_fitness[int((tp[0]).split('_')[1])])
            for i in tp:
                if len(tp) > 1:
                    print(int((i).split('_')[1]))
                single_param_print(self.seed_params, int((i).split('_')[1]))
        ##################################
        print("paddy is done!")
        if self.file_name is not None:
            self.save_paddy()

    def paddy_plot_and_print(self, verbose=None, figure_name=None):
        """Plot and print results.

        This method is used to generate results as either printed or plotted
        results.  The type of output is dictated by passed strings via the
        `verbose` parameter.

        Parameters
        ----------
        verbose : string or sequence of string, optional (default : None)
            String comand(s) that handle printing of values generated after
            completion of a paddy run.  Details regarding valid strings are
            discussed in the notes section below.

        figure_name : string, (default : None)
            A string that is passed to `writer.preformance_plotter` that
            is used to save generated plots.

        See Also
        --------
        :meth:`paddy.writer.preformance_plotter`

        :meth:`paddy.writer.clean_parameter_print`

        :meth:`paddy.utils.get_top_fitness`

        Notes
        -----
        `paddy_plot_and_print` coordinates with `writer.preformance_plotter`
        to generate desired representations of results via string arguments
        initially introduced via `verbose`.  Valid strings that will generate
        output without calling `writer.preformance_plotter` are:

        * 'generation'
            Simply prints the `PFARunner` attribute ``generation_data``.
        * 'final_results'
            Prints results via `clean_parameter_print` with the `PFARunner`
            attribute ``top_values`` as input.
        * 'pop_fitness'
            Prints the list returned by `get_top_fitness` using the
            `PFARunner` attribute ``top_values`` as input.
        * 'gen_fitness'
            Prints the `PFARunner` attribute ``generation_fitness``.

        Valid comands are passed to `writer.preformance_plotter` as described
        in detail in the notes section for
        :meth:`paddy.writer.preformance_plotter`.
        """
        is_running = False
        if verbose is None:
            print("plot and print requires a string argument\
             or list containing valid string arguments")
            return
        if isinstance(verbose, bool):
            print('plot and print does not accept bool objects')
            return
        #print(verbose)
        paddy_plot_and_write_comands = {'generation', 'final_results',
                                        'pop_fitness', 'gen_fitness',
                                        'best_sown', 'average_population',
                                        'scatter', 'box', 'box_notched',
                                        'box_hidden', 'average_gen'}
        plotter_types = {'best_sown', 'average_population', 'scatter', 'box',
                         'box_notched', 'box_hidden', 'average_gen'}
        if isinstance(verbose, str):
            verbose = {verbose}
        for comand in verbose:
            if paddy_plot_and_write_comands.issuperset({comand}):
                is_running = True
            else:
                print(str(comand)+' is not a valid input for plot and print')
                return
        verbose = set(verbose)
        ###Generation Seed ID's###
        if 'generation' in verbose:
            print(self.generation_data)
        #######Final Results######
        if 'final_results' in verbose:
            clean_parameter_print(self.top_values)
        #########Fitness Array of Population##########
        fitness_list = get_top_fitness(self.top_values)
        if 'pop_fitness' in verbose:
            print("List of fitness values:")
            print(fitness_list)
        ####All Fitness In Gens####
        gf = self.generation_fitness
        if 'gen_fitness' in verbose:
            print(gf)
        ###########################
        info = [fitness_list, gf]
        print_len = len(plotter_types.intersection(verbose))
        if print_len > 0:
            preformance_plotter(info, verbose, figure_name)
        else:
            if is_running:
                pass

    def save_paddy(self, new_file_name=None):
        """Save :class:`PFARunner` as a pickled file.

        This method uses the python pickle serialization module to store class
        iterances of `PFARunner` to be recovered as needed by the user.

        Parameters
        ----------
        new_file_name : string, (default : None)
            A string that is used for the file handle.  The same string is
            also used for generating the file handle of the backup pickle with
            the trailing '_backup.pickle' added, and replaces the former file
            name used.

        See Also
        --------
        :func:`paddy.utils.paddy_recover` : `utils` function that depickles a
            given pickled `PFARunner` instance.

        Notes
        -----
        The backup pickle is saved every other iteration of paddy after the
        primary pickle handle.
        """
        if new_file_name is None:
            if self.file_name is None:
                error = 'a file name must be provided prior to saving'
                PaddyRunnerError(error)
        else:
            self.file_name = new_file_name
        with open('{0}.pickle'.format(self.file_name), 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()
        if self.paddy_counter % 2 == 0:
            with open('{0}_backup.pickle'.format(
                self.file_name), 'wb') as handle:
                pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)
                handle.close()

    def recover_run(self, new_verbose=None):
        """Run paddy after recovering a pickled run.

        This method runs a recovered depickled `PFARunner` instance, by
        resuming where the algorithm was functioning last.

        Parameters
        ----------
        new_verbose : string or sequence of strings, optional (default : None)
            See `verbose` parameter description for `run_paddy`.

        See Also
        --------
        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.

        :func:`paddy.utils.paddy_recover` : `utils` function that depickles a
            given pickled `PFARunner` instance.

        Notes
        -----
        If a recovered `PFARunner` is unable to excicute :meth:`recover_run`,
        it may be needed to manualy decrease the `paddy_counter` attribute.
        """
        if new_verbose is None:
            new_verbose = self.verbose
        if isinstance(new_verbose, str):
            new_verbose = {new_verbose}
        self.verbose = new_verbose
        self.recover = True
        if self.paddy_counter != self.iterations:
            print('Recovering at iteration ' + str(self.paddy_counter) + ' out of '
                  + str(self.iterations))
            self.run_paddy(verbose=self.verbose, file_name=self.file_name)
        else:
            print(
                "recovered paddy run was already completed, use extend_paddy")

    def extend_paddy(self, new_iterations,
                     new_file_name=None, new_verbose=None):
        """Extend the iterations of a completed paddy runner.

        This method runs a `PFARunner` instance that has completed the amount
        of iterations set as its attribute.

        Parameters
        ----------
        new_iterations : integer
            Integer to extend the iterations of the `PFARunner` by.

        new_file_name : string, optional (default : None)
            A string that is used for the file handle.  The same string is
            also used for generating the file handle of the backup pickle with
            the trailing '_backup.pickle' added, and replaces the former file
            name used.

        new_verbose : string or sequence of strings, optional (default : None)
            See `verbose` parameter description for `run_paddy`.

        Raises
        ------
        PaddyRunnerError
            If parameter value(s) used to initialize an instance of
            `PFARunner` would raise an exception when calling methods of
            `PFARunner`.

        See Also
        --------
        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.

        :meth:`recover_run` : `PFARunner` method that runs a recovered pickle
            run.

        Notes
        -----
        This method can be used to extend the `iterations` of a `PFARunner`
        while changing the `file_name` and `verbose` atributes as well in
        one line rather than manualy for each and calling :meth:`run_paddy`.
        """
        if new_iterations < 1 or new_iterations % 1 != 0:
            raise PaddyRunnerError(EXTENSION_ERROR)
        self.recover = True
        if new_verbose is not None:
            self.verbose = new_verbose
        if isinstance(new_file_name, (str, int)):
            self.file_name = new_file_name
        self.iterations = self.iterations + new_iterations
        self.run_paddy(verbose=self.verbose, file_name=self.file_name)

    def get_top_seed(self):
        """Return the seed with the greatest fitness in the paddy runner.

        This method returns the top seed number when called internally, though
        a user can simply call the method directly to print to terminal.

        Returns
        -------
        temp_names : list of strings
            A list of seed number string(s) in the form `'seed_#'`

        See Also
        --------
        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.

        Notes
        -----
        When running paddy via :meth:`run_paddy`, the ``verbose`` parameter
        will call :meth:`get_top_seed` if the string command `'pop'` is
        passed.

        In the case that multiple seeds are tied for having the greatest
        fitness value, they are appended to `temp_names`.
        """
        fit_list = list(self.seed_fitness)
        max_fit = max(fit_list)
        if fit_list.count(max_fit) > 1:
            print('multiple seeds of maximum fitness value:'+str(max_fit))
        temp_names = []
        c = 0
        for i in self.seed_fitness:
            if i == max_fit:
                temp_names.append('seed_{0}'.format(c))
            c += 1
        return temp_names

    def get_generation_top_seed(self, counter=None, verbose=False):
        """Return the max value of fitness in the generation.

        This method returns the top seed number of a given generation
        of a paddy run when called internally, though a user can call the
        method directly to print to terminal.  If called directly, a `counter`
        parameter value can be passed to specify which generation is acessed,
        where the default generation analyzed is the last evaluated.

        Parameters
        ----------
        counter : integer, (default : None)
            An integer that specifies which generation is analyzed.

        verbose : bool, (default : False)

        Returns
        -------
        temp_names : list of strings
            A list of seed number string(s) in the form `'seed_#'`

        See Also
        --------
        :meth:`run_paddy` : `PFARunner` method that excecutes the paddy field
            algorithm.

        Notes
        -----
        When running paddy via :meth:`run_paddy`, the ``verbose`` parameter
        will call :meth:`get_generation_top_seed` if the string command
        `'top_gen'` is passed.

        In the case that multiple seeds are tied for having the greatest
        fitness value, they are appended to `temp_names`.
        """
        if counter is None:
            fit_list = self.generation_fitness[str(self.paddy_counter)]
        else:
            try:
                counter = int(counter)
                fit_list = self.generation_fitness[str(counter)]
            except:
                print('counter needs to be an integer or string of integer')
                return
        max_fit = max(fit_list)
        if verbose:
            print(max_fit)
        if fit_list.count(max_fit) > 1:
            print('multiple seeds of maximum fitness value:'+str(max_fit))
        temp_names = []
        if counter is None:
            gen_seeds = self.generation_data[str(self.paddy_counter)]
        else:
            gen_seeds = self.generation_data[str(counter)]
        for i in np.arange(gen_seeds[0], gen_seeds[1]+1):
            if self.seed_fitness[i] == max_fit:
                if verbose:
                    print('seed_{0}'.format(i))
                temp_names.append('seed_{0}'.format(i))
        return temp_names
