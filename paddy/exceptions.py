"""
The :mod:`paddy.exceptions` module contains the error classes
and custom warning messages used in paddy.

"""
# Authors: Armen Beck & Jonathan Fine
# License: BSD


RANGE_LIMIT_ERROR = 'param_range values must be within defined limits'

EQUAL_LIMIT_ERROR = 'limits cannot be equal to eachother'

LIMIT_ORDER_ERROR = 'limits must be listed in assending order'

PARAM_RANGE_ORDER_ERROR = 'param_range must be listed in assending order'

PARAM_TYPE_ERROR = (
    "param_type must be 'integer' or 'continuous',\n\
                                  {0} is not a valid input")

GAUSSIAN_TYPE_ERROR = (
    "gaussian must be 'default' or 'scaled',\n\
                                  {0} is not a valid input")

INF_NORM_ERROR = (
    'normalization cannot be True if limits contain infinity')

NONE_LIMITS_NORM_ERROR = 'normalization cannot be True if limits are None'

RANDOM_SEED_ERROR = (
    'paddy requires more than four random seeds during initiation')

INT_PARAM_ERROR = '{0} must be a positive integer, {1} is not a valid input'

RADIUS_ERROR = 'r must be a positive numeric value, {0} is not a valid input'

PADDY_TYPE_ERROR = (
    "paddy_type must be 'population' or 'generational' {0} is not valid")

CONTAINER_ERROR = '{0} cannot be a data structures with more than one element'

PADDY_FILE_ERROR = 'File handle defined by "file_name" must be a string'

NULL_BACKUP = 'no backup file present after failed recovery of initial path'

PFA_PATH_ERROR = (
    'no file was found for the paths: {0}.pickle & {0}_backup.pickle')

BAD_PICKLES = 'desired pickle and backup are non-readable or corrupt'

EXTENSION_ERROR = "A negative input for new iterations terminates the run,\
             value must be positive to extend parameters"

class PaddyParamError(Exception):
    """Exception raised when initializing a PaddyParameter class instance.

    """

class PaddyRunnerError(Exception):
    """Exception raised when initalizing a PaddyRunner class instance.

    """

class PaddyRecoveryError(Exception):
    """Exception raised when paddy recovery fails.

    """
