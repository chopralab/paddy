"""
Parameter optimization package for Python
=========================================

Paddy is a Python package developed as an extension of the
Paddy Field Algorithm, a geneteic, plant based, global
optimization algorithm proposed by Premaratne et al. (2009)

Paddy was developed with the intention of being used to
optimize hyperparameters of machine learning algorithms and
as a general metaheuristic.

Routine listings
----------------
Paddy_Runner
    Module providing `paddy.Paddy_Runner.PaddyRunner` class that runs paddy.
Paddy_Parameter
    Module providing :mod:`paddy.Paddy_Parameter.PaddyParameter` class that
    handles parameter specific operations.
writer
    Module providing functions involved with the printing and plotting of
    results.
utils
    Module providing functions that suport :mod:`paddy.Paddy_Runner`

References
----------
Upeka Premaratne, Jagath Samarabandu, and Tarlochan Sidhu,
A New Biologically Inspired Optimization Algorithm
International Conference on Industrial and Information Systems
28-31 Dec. 2009
DOI: 10.1109/ICIINFS.2009.5429852
Print ISSN: 2164-7011

"""
# Authors: Armen Beck & Jonathan Fine
# License: BSD



from paddy import utils
from paddy import writer
from paddy.Paddy_Parameter import PaddyParameter
from paddy.Paddy_Runner import PFARunner
from paddy import Default_Numerics




__version__ = '0.2'
