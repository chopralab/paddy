"""
The :mod:`paddy.utils` module contains suporting functions for the
:mod:`paddy.Paddy_Runner` module.

Routine listings
----------------
get_param_names(p_space)

get_top_fitness(dirty_values)

random_propogation(rand_seed_number, p_space, seed_counter)

paddy_recover(file_name)

"""
# Authors: Armen Beck & Jonathan Fine
# License: BSD

import pickle
import os
import numpy as np
import random
from paddy.exceptions import (PADDY_FILE_ERROR, PFA_PATH_ERROR,
                              BAD_PICKLES, NULL_BACKUP,
                              PaddyRecoveryError)

def get_param_names(p_space):
    """Return list of parameter names.

    Parameters
    ----------
    p_space : class
        A class containing attributes exclusively of `PaddyParameter`
        instances.

    Returns
    -------
    param_name_list : list of strings
        A list of `PaddyParameter` instances as string types of the instance
        variable name.

    """
    param_name_list = []
    for i in vars(p_space):
        param_name_list.append(i)
    return param_name_list

def get_top_fitness(dirty_values):
    """Return top fitness value.

    Returns the top fitness values of a
    :class:`~paddy.Paddy_Runner.PFARunner`, solely, for each iteration as a
    list when passed a dictionary with the structure type of
    :attr:`~paddy.Paddy_Runner.PFARunner.top_values`.

    Parameters
    ----------
    dirty_values : dictionary
        A dictionary in the form of :attr:`~PFARunner.top_values`.

    Returns
    -------
    fitness_list : list of floats
        A list of the top fitness value evaluated for sowing during each
        itteration.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.run_paddy`

    Notes
    -----
    The top value evaluated for sowing when using 'population' for
    the `paddy_type` parameter of a `PFARunner` instance might not be the
    value of a seed generated during that itteration.  
    """
    fitness_list = []
    counter = 0
    for i in dirty_values:
        fitness_list.append(dirty_values['{0}'.format(counter)]['fitness'])
        counter += 1
    return fitness_list


def random_propogation(rand_seed_number, p_space, seed_counter):
    """Return updatad seed counter and random seed parameters.

    This function takes parameter space and generates random seeds as an array
    with length determined by the user parameter rand_seed_number and returns
    the array as well as an updated seed_counter.

    See Also
    --------
    :meth:`paddy.Paddy_Runner.PFARunner.run_paddy`

    """
    p_names = get_param_names(p_space)
    random_seeds = np.empty([rand_seed_number, len(p_names), 2])
    while seed_counter < rand_seed_number + 1:
        counter = 0
        for i in p_names:
            temp = getattr(p_space, i).random_init()
            random_seeds[seed_counter-1][counter] = temp
            counter += 1
        seed_counter += 1
    return(seed_counter-1, random_seeds)


def paddy_recover(file_name):
    """Recover pickled paddy file.

    Trys to recover the pickled `PFARunner` instance, and will
    then use the backup file if there is an issue recovering the
    original.

    Parameters
    ----------
    file_name : string or nonetype, optional (default : None)
        A user defined string that is used as the file handle for
        `PFARunner` instance pickling.

    Returns
    -------
    recovered_paddy : :class:`~paddy.Paddy_Runner.PFARunner`
        Depickled `PFARunner` class instance.

    Raises
    ------
    PaddyRecoveryError
        If the recovery of a previous `PFARunner` fails.

    See Also
    --------

    :meth:`paddy.Paddy_Runner.PFARunner.recover_run`

    :meth:`paddy.Paddy_Runner.PFARunner.run_paddy`

    :meth:`pickle.load`

    Warnings
    --------
    The |pickle|_ module is not secure against malicious data!

    .. |pickle| replace:: ``pickle``
    .. _pickle: https://docs.python.org/3.6/library/pickle.html

    Notes
    -----
    All functions, that the `PFARPaddyRecoveryErrorunner` instance being recoverd is dependant
    on, need to be defined for successfull depickling, namely the `eval_func`
    parameter input.

    Examples
    --------
    >>> import paddy
    >>> from paddy.Default_Numerics import *
    >>> recovered_PFARunner = paddy.paddy_recover('old_PFARunner')

    """
    if not isinstance(file_name, str):
        raise PaddyRecoveryError(PADDY_FILE_ERROR)
    bad_recovery = False
    if os.path.isfile('{0}.pickle'.format(file_name)):
        with open('{0}.pickle'.format(file_name), 'rb') as handle:
            pickle_binary = handle.readline()
            if pickle_binary.rfind(b'\x80') != 0:
                print('{0}.pickle is empty or corrupted\
                \n trying backup file'.format(file_name))
                bad_recovery = True
            else:
                #If the AttributeError for lack of PFARunner globals would
                #be raised here, the backup file will raise the same error
                handle.seek(0)
                bad_recovery = True
                recovered_paddy = pickle.load(handle)
                bad_recovery = False
                return recovered_paddy
    if bad_recovery:
        if os.path.isfile('{0}_backup.pickle'.format(file_name)):
            with open('{0}_backup.pickle'.format(file_name), 'rb') as handle:
                pickle_binary = handle.readline()
                if pickle_binary.rfind(b'\x80') != 0:
                    #Both pickles corrupt
                    raise PaddyRecoveryError(BAD_PICKLES)
                handle.seek(0)
                recovered_paddy = pickle.load(handle)
                return recovered_paddy
        else:
            #Could not recover origional and backup not present
            raise PaddyRecoveryError(NULL_BACKUP)
    else:
        #error for no path to origional file
        raise PaddyRecoveryError(PFA_PATH_ERROR.format(file_name))



class Numeric_Assistant(object):
    """
    Sampling assistant that manages numeric space.
    Repeats if false will remove observations after
    a set of observations

    Parameters
    ----------
    observations : array_like, shape(N+1,M)
        A rank-2 array of M observations where rows contain
        the cordinates in N-dimensional parameter space, with
        the last row being the response value.

    repeats : bool (default: True)
        Boolean to determine if observations can be repeatedly
        sampled.

    raw_responce : bool (default: False)
        Boolean to determine if the responce is normalized
        when an observation is sampled.


    Attributes
    ----------
    obs_clone : array_like, shape(,2)
        Array that is initially a clone of the observation
        parameter, and has observations removed by the 
        `obs_cloner` method.

    norm_clone : array_like, shape(,2)


    Methods
    ------- 
    sample(inputs)

    norm_cloner()
        Clones 

    obs_cloner()
        Uses `black_list` to ommit observations before
        cloning to `obs_clone`.

    min_max(x, minV, maxV)
        Used for normalizing rows in `observations` or 
        `obs_clone` if `repeats` is False.

    """
    def __init__(self,observations,repeats=True,raw_responce=False):
        self.observations = observations
        self.repeats = repeats
        self.obs_clone = np.array(copy.deepcopy(observations))
        self.black_list = []
        self.norm_cloner()
        self.raw_responce = raw_responce

    def sample(self,inputs):
        temp = []
        for i in inputs:
            temp.append(i[0])
        inputs = temp
        distance_list = []
        distance_vectors = []
        c = 0
        for i in range(len(self.obs_clone[0])):#get distances for every param combo
            distance_vectors.append(np.linalg.norm(self.norm_clone[:-1,c] - inputs))
            c += 1
        distance_list.append(distance_vectors)#append distances for each domain/param
        score_list = []
        if not self.repeats:#doesnt have error handling for equal distances
            self.black_list = []
            #print("distance list:",distance_list)
            #print("norm clone", self.norm_clone)
            #print("distance list len:",len(distance_list[0]))
            if len(distance_list[0]) > 1:
                for i in distance_list:
                    repeats = i.count(min(i))
                    if repeats == 1:
                        if self.raw_responce:
                            print(self.obs_clone[:-1,np.argmin(i)])
                            score_list.append(self.obs_clone[-1][np.argmin(i)])
                        else:
                            score_list.append(self.norm_clone[-1][np.argmin(i)])
                        self.black_list.append(np.argmin(i))
                    if repeats > 1:
                        d = 0
                        r_list = []
                        for j in i:
                            if j == min(i):
                                r_list.append(d)
                            d +=1
                        rc = random.choice(r_list)
                        if self.raw_responce:
                            score_list.append(self.obs_clone[-1][rc])
                        else:
                            score_list.append(self.norm_clone[-1][rc])
                        self.black_list.append(rc)
            if len(distance_list[0]) == 1:
                if self.raw_responce:
                    score_list.append(self.obs_clone[-1][0])
                else:
                    score_list.append(self.norm_clone[-1][0])
                self.black_list.append(0)

            self.norm_cloner()#renormalizes after sampling and removes observations
            #distance_list is values of selection out of vector of posibilites
            #print("Black list len:", len(self.black_list))
            #print("# Observations:", len(self.obs_clone[0]))
        else:
            for i in distance_list:
                if self.raw_responce:
                    score_list.append(self.obs_clone[-1][np.argmin(i)])
                else:
                    score_list.append(self.norm_clone[-1][np.argmin(i)])
        #print(score_list)
        return(score_list)

    def min_max(self, x, minV, maxV):
        if minV != maxV:
            x = x
            minV = minV
            maxV = maxV
            return((x-minV)/(maxV-minV))
        else:
            return(1)

    def norm_cloner(self):
        #clones observations with normalized values between 0 and 1
        self.norm_clone =[]
        if self.repeats:
            for row in self.observations:
                minV, maxV = min(row), max(row)
                temp =[]
                for value in row:
                    normed = self.min_max(value, minV, maxV)
                    temp.append(normed)
                self.norm_clone.append(temp)
        else: 
            self.obs_cloner()
            if len(self.obs_clone[0]) > 0: 
                for row in self.obs_clone:
                    minV, maxV = min(row), max(row)
                    temp =[]
                    for value in row:
                        normed = self.min_max(value, minV, maxV)
                        temp.append(normed)
                    self.norm_clone.append(temp)
        self.norm_clone = np.array(self.norm_clone)    

    def obs_cloner(self):
        #uses black list to ommit prior observations
        obs_clone2 = []
        c2 = 0
        for i in self.obs_clone:
            obs_clone2.append([])
            c = 0
            for j in i:
                if c in self.black_list:
                    pass
                else:
                    obs_clone2[c2].append(j)
                c += 1
            c2 += 1
        self.obs_clone = np.array(obs_clone2)
