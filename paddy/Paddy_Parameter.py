# -*- coding: UTF-8 -*-

"""
The :mod:`paddy.Paddy_Parameter` module contains the
:class:`~paddy.Paddy_Parameter.PaddyParameter` class and its associated
methods.

The `PaddyParameter` class is used to manage the generation of numeric values
associated with parameters that are being optomized paddy.  Specific
operations are detailed in the methods section of `PaddyParameter`.

Routine Listings
----------------
PaddyParameter(object)
    Stores information regarding a parameter being optimized, and handles
    operations on associated values.

See Also
--------
:mod:`paddy.Paddy_Runner`

"""
# Authors: Armen Beck & Jonathan Fine
# License: BSD

import random
import numpy as np

from paddy.exceptions import (PaddyParamError,
                              PARAM_RANGE_ORDER_ERROR,
                              LIMIT_ORDER_ERROR,
                              EQUAL_LIMIT_ERROR,
                              RANGE_LIMIT_ERROR,
                              NONE_LIMITS_NORM_ERROR,
                              INF_NORM_ERROR,
                              GAUSSIAN_TYPE_ERROR,
                              PARAM_TYPE_ERROR)

class PaddyParameter(object):
    r"""The class that handles operations and atributes used for
    generating random and new seed parameters.

    Parameters
    ----------
    param_range : list of integer or float
        A list of three numeric values used to define what
        random seed value is possible for the specific `PaddyParameter`
        where the first position (a) is the lowest possible value, the
        second position (b) is the highest possible value, and the
        third position (c) is the incremental unit used to develop a
        range between a & b to generate a random value in said range.

    param_type : string
        A string that, unless using a custom class in place of
        `PaddyParameter`, should be either: ‘integer’ or ‘continuous’.
        This allows the algorithm to either pass integer or float
        class instances.

    limits : None or list of integer or float
        A list of two values used to define if a new seed’s
        respective parameter value is permitted.  Additionally, these
        values are used to normalize values if the normalization
        argument is set as `True`.  The fist value in the limits list is
        the minimum value, and the second value is the maximum value
        permitted as defined by user.  If `None` is used in the list,
        possible values are unbound in that direction.  If a unbound
        limit term exists, normalization is defined as `False` internally,
        overriding a user input.

    gaussian : string
        A string that, unless using a custom class in place of
        `PaddyParameter`, should be either: ‘default’ or ‘scaled’.
        This allows the algorithm to determine if scaling of the standard
        deviation, used by the gaussian distribution that new paddy
        parameter values are generated along, is desired by the user.

    normalization : bool
        A boolean to determine if min-max normalization is used when using the
        methods `random_init`, `new_seed_init`, and `get_ecludian_values`.
        The minimum and maximum values for normalization are defined by the
        limits argument, and cannont contain inf for normalization to be
        `True`.  If limits is `None` normalization again must be `False`.

    Methods
    -------
    random_init()
        Generates random new values defined by `param_range`.

    new_seed_init(values)
        Generates new values for the parameter and gaussian.

    norm_p(p_val)
        Normalizes a seed parameter.

    inverse_norm_p(ip_val)
        Returns a denormalized seed parameter.

    get_ecludian_values(p_vals)
        Returns apropriate value for euclidean evaluation.

    Raises
    ------
    PaddyParamError
        If parameter value(s) used to initialize an instance of
        `PaddyParameter` would raise an exception when calling
        methods of `PaddyParameter`.
    """

    def __init__(self, param_range, param_type, limits,
                 gaussian, normalization):
        self.param_range = param_range
        self.param_type = param_type
        self.limits = limits
        self.gaussian = gaussian
        self.normalization = normalization
        if param_range[0] > param_range[1]:
            raise PaddyParamError(PARAM_RANGE_ORDER_ERROR)
        if limits is not None:
            if limits[0] > limits[1] or limits[1] < limits[0]:
                raise PaddyParamError(LIMIT_ORDER_ERROR)
            if limits[0] == limits[1]:
                raise PaddyParamError(EQUAL_LIMIT_ERROR)
            if param_range[0] < limits[0] or param_range[1] > limits[1]:
                raise PaddyParamError(RANGE_LIMIT_ERROR)
        if limits is None and normalization:
            raise PaddyParamError(NONE_LIMITS_NORM_ERROR)
        if isinstance(limits, list) and (
                float('inf') in limits or -float('inf') in limits):
            if normalization:
                raise PaddyParamError(INF_NORM_ERROR)
        if gaussian not in ('default', 'scaled'):
            error = GAUSSIAN_TYPE_ERROR.format(gaussian)
            raise PaddyParamError(error)
        if param_type not in ('integer', 'continuous'):
            error = PARAM_TYPE_ERROR.format(param_type)
            raise PaddyParamError(error)

    def norm_p(self, p_val):
        """Return normalized paddy value via min-max feature scaling.

        Parameters
        ----------
        p_val : integer or float
            Single seed parameter value from previous itteration.

        Returns
        -------
        np_val : integer or float
            Normalized parameter value used to generate a new seed
            or undergo euclidean evaluation.
        """
        np_val = (p_val - self.limits[0]) / float(self.limits[1]-self.limits[0])
        return np_val

    def inverse_norm_p(self, ip_val):
        """Inverses min-max feature scaling.

        See Also
        --------
        :meth:`norm_p`

        """
        return (ip_val * (self.limits[1]-self.limits[0])) + self.limits[0]

    def random_init(self):
        """Generates and returns random value for seeds.

        This is used to generate random values during the random propogation
        step when initializing the paddy algorithm.  The param_range parameter
        of `PaddyParameter` is used to define a range of posible values from
        which the new seed uses during evaluation.

        Returns
        -------
        value : integer or float
            New numeric value for a parameter evaluated by paddy.

        See Also
        --------
        :meth:`paddy.PaddyRunner.random_step`
        """
        range_v = np.arange(
            self.param_range[0], self.param_range[1]
            +self.param_range[2], self.param_range[2])
        value = [random.choice(range_v)]
        if self.param_type == 'integer':
            value[0] = int(round(value[0]))
        value.append(0)
        return value

    def new_seed_init(self, values):
        """Return values for a new seed.

        Takes values from previous seed and generates seeds for a new paddy
        iteration.

        Parameters
        ----------
        values : list, shape (2)

        Returns
        -------
        b : list, shape (2)
            A list containing the numeric values for the parameter and
            associated gaussian of a new seed.

        See Also
        --------
        :meth:`paddy.PaddyRunner.new_propogation`
        """
        b = [None, 0]
        if not self.normalization:
            b[0] = np.random.normal(
                loc=values[0], scale=0.2 **(10**values[1]))
            if self.limits is None:
                if self.gaussian == 'scaled':
                    b[1] = np.random.normal(loc=values[1], scale=0.2)
            elif self.limits is not None:
                b[0] = np.clip(b[0], self.limits[0], self.limits[1])
                if self.gaussian == 'scaled':
                    b[1] = np.random.normal(loc=values[1], scale=0.2)
        else:
            b[0] = np.random.normal(
                loc=self.norm_p(values[0]),
                scale=0.2 **(10**values[1]))
            g = self.inverse_norm_p(b[0])
            b[0] = np.clip(g, self.limits[0], self.limits[1])
            if self.gaussian == 'scaled':
                b[1] = np.random.normal(loc=values[1], scale=0.2)
        if self.param_type == 'integer':
            b[0] = int(round(b[0]))
        return b

    def get_ecludian_values(self, p_vals):
        """Return the ecludian value for a paddy parameter.

        This allows normalization of a parameter to be considered during
        neighbor counting, prior to returning the apropriate ecludian value.

        Parameters
        ----------
        p_vals : list, shape (2)

        Returns
        -------
        e_val : integer, float
            A numeric value that is used during neighbor counting.

        See Also
        --------
        :meth:`paddy.PaddyRunner.neighbor_counter`
        """
        if not self.normalization:
            e_val = p_vals[0]
            return e_val
        e_val = self.norm_p(p_vals[0])
        return e_val
