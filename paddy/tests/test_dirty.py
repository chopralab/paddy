import math
import paddy
import itertools

def function_1(input):
    x=input[0,0]
    y=input[1,0]
    r = (((x-0.5)**2)+((y-0.5)**2))**.5
    result = math.cos(9*math.pi*r)*math.exp(-(((((x-0.5)**2)+((y-0.5)**2)))/(0.15**2)))
    #maximum at (0.5,0.5)
    return (result)

def function_2(input):
    x=input[0,0]
    y=input[1,0]
    r1=((x-0.5)**2)+((y-0.5)**2)
    r2=((x-0.6)**2)+((y-0.1)**2)
    result = (0.80*math.exp(-(r1)/(0.3**2))) + (0.88*math.exp(-(r2)/0.03**2))
    #global maximum at (0.6,0.1) with local at (0.5,0.5)
    return (result)

def function_3(input):
    x=input[0,0]
    y=input[1,0]
    result = -3*( (x-0.5)**2 + (y-0.5)**2 ) - 0.3*(math.cos(2*math.pi*3*x)+math.cos(2*math.pi*3*y))
    #maximum at (0.5,0.5) with 8 local maxima, Rastigrin function adaptation
    return (result)


def function_4(input):
    x=input[0,0]
    y=input[1,0]
    result = -((x-0.5)**2)-((x-y*y)**2)+1
    #maximum at (0.5,0.25), Rosenbrock function adaptation
    return (result)



pt = ['population','generational']
gausian = ['default','scaled']
rand_seed = [5,10,20,50,100]
max_seeds = [5,10,20,50,100]
iterations = [5,10,20,50,100,200]
norm = [True,False]

grid = [pt,gausian,rand_seed,max_seeds,iterations,norm]
gl = list(itertools.product(*grid))
gl2 = gl[0:58]
gl2.append(gl[82])

pc=0
def test_runner():
	for i in gl2:
	    x_param = paddy.PaddyParameter(param_range=[0,1,.1],param_type='continuous',limits=[0,1,.1], gaussian=i[1],normalization = i[5])
	    y_param = paddy.PaddyParameter(param_range=[0,1,.1],param_type='continuous',limits=[0,1,.1], gaussian=i[1],normalization = i[5])
	    class space(object):
		    def __init__(self):
			    self.xp = x_param
			    self.yp = y_param
	    test_space = space()
	    runner = paddy.PFARunner(space=test_space, eval_func=function_2,
		                    paddy_type=i[0], rand_seed_number=i[2],
		                    yt=i[2],Qmax=i[3],r=.02,iterations =i[4])
	    runner.run_paddy()
	    assert (runner.paddy_counter == i[4])
