import paddy

def parabola(input):
    x = input[0][0]
    y = input[1][0]
    return(((x**2)/7)-((y**2)/2)+1)# The maximum is when x and y are 0

# now we need to set our parameter space for x and y
x_param = paddy.PaddyParameter(param_range=[-5,5,.2],
                               param_type='continuous',
                               limits=None, gaussian='scaled',
                               normalization = False)
y_param = paddy.PaddyParameter(param_range=[-7,3,.2],
                               param_type='continuous',
                               limits=None, gaussian='scaled',
                               normalization = False)
# now we make a class with the parameter spaces we defined
class paraboloid_space(object):
    def __init__(self):
        self.xp = x_param
        self.yp = y_param
# now we need to initialize a `PFARunner`
example_space = paraboloid_space() #the space parameter
example_runner = paddy.PFARunner(space=example_space,
                                 eval_func=parabola,
                                 paddy_type='population',
                                 rand_seed_number = 20,
                                 yt = 10,
                                 Qmax = 5,
                                 r=.2,
                                 iterations = 1)

example_runner.run_paddy()
print(example_runner.S)
print(len(example_runner.seed_fitness))
print(example_runner.generation_data)
print(example_runner.seed_fitness)

