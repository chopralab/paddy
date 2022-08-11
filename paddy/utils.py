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
