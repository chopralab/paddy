import paddy
from paddy import Paddy_Parameter
from paddy.Paddy_Parameter import *
from paddy import Paddy_Runner
from paddy import Default_Numerics
import math
import unittest
import itertools
import random


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
#file = open("/test_files/paddy_grid.txt","a")
pc=0
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
    runner.paddy_plot_and_print(['best_sown','average_population','average_gen'],
                                figure_name="paddy/tests/test_files/{0}".format(pc))
    runner.save_paddy("paddy/tests/test_files/{0}".format(pc))

print('paddy utils')


x_param = paddy.PaddyParameter(param_range=[0,1,.1],param_type='continuous',limits=[0,1,.1], gaussian='scaled',normalization = True)
y_param = paddy.PaddyParameter(param_range=[0,1,.1],param_type='continuous',limits=[0,1,.1], gaussian='scaled',normalization = True)
class space(object):
    def __init__(self):
	    self.xp = x_param
	    self.yp = y_param

test_space = space()
runner = paddy.PFARunner(space=test_space, eval_func=function_1,
                    paddy_type='generational', rand_seed_number=50,
                    yt=5,Qmax=5,r=.02,iterations =1000)
runner.run_paddy(verbose='all')

def function_z(input):
    if (input[0,0] > .5):
        return (1)
    else:
        return(0.1-input[0,0])

runner = paddy.PFARunner(space=test_space, eval_func=function_z,
                    paddy_type='generational', rand_seed_number=11,
                    yt=10,Qmax=5,r=.2,iterations =1)

print('final verbose')
runner.run_paddy(verbose='all')



#example paddy model class
class Mlp(object):
    def __init__(self):
        self.dropout_1 = paddy.PaddyParameter(param_range=[0,0.5,0.05],param_type='continious',limits=[0,1], gaussian='default', normalization = True)
        self.dropout_2 = paddy.PaddyParameter(param_range=[0,0.5,0.05],param_type='continious',limits=[0,1], gaussian='default',normalization=True)
        self.nl_1 = paddy.PaddyParameter(param_range=[5,50,2],param_type='integer',limits=[-12,150], gaussian='default', normalization=True)

'''
class RunFunc(object):
    def __init__(self):
        self.xs , self.ys = gramacy_lee()
    def eval(self,values):
        score = paddy.Default_Numerics.eval_gl(seed=values,x=self.xs,y=self.ys)
        return score
'''

class TestPaddyParameter(unittest.TestCase):
    
    def test_PaddyParameter_random_init(self):
        test_parameter = paddy.PaddyParameter(param_range=[0,0.5,0.05],param_type='continuous',limits=[0,1], gaussian='default', normalization=True )
        rand_value = test_parameter.random_init()
        print(rand_value)
        self.assertGreaterEqual(rand_value[0] , test_parameter.limits[0])
        self.assertLessEqual(rand_value[0] , test_parameter.limits[1])
    
    def test_new_seed_init(self):
        new_seed_args=[['scaled',True],['scaled',False],['default',True],['default',False]]
        for combination in new_seed_args:
            test_parameter = paddy.PaddyParameter(param_range=[0,0.5,0.05],
            param_type='continuous',limits=[0,1],
            gaussian=combination[0], normalization=combination[1] )
            rand_value = test_parameter.random_init()
            value = test_parameter.new_seed_init(rand_value)
            self.assertGreaterEqual(value[0] , test_parameter.limits[0])
            self.assertLessEqual(value[0] , test_parameter.limits[1])
    
    def test_get_ecludian_values(self):
        normalization_bool = [True,False]
        for boolean in normalization_bool:
            test_parameter = paddy.PaddyParameter(param_range=[0,0.5,0.05],param_type='continuous',limits=[0,1],
             gaussian='default', normalization=boolean )
            rand_val=test_parameter.random_init()
            ecludian_value=test_parameter.get_ecludian_values(rand_val)
            if boolean == False:
                self.assertEqual(ecludian_value,rand_val[0])
            if boolean == True:
                norm_rand=test_parameter.norm_p(rand_val[0])
                self.assertEqual(ecludian_value,norm_rand)
  
class test_PaddyRunner(unittest.TestCase):

    def test_each_function_during_run(self):
        
        gausians = ['default','scaled']
        normalization_bool =[True,False]
        param_types = ['continuous','integer']

        iterables = [ gausians,normalization_bool,param_types ]

        iterable_combinations = []
        for i in itertools.product(*iterables):
            iterable_combinations.append(i)

        PaddyParameters = []
        for i in iterable_combinations:
            temp_param =  paddy.PaddyParameter(param_range=[1,50,2],
             param_type=i[2],limits=[1,59], gaussian=i[0], normalization=i[1] )
            PaddyParameters.append(temp_param)
    
        class test_runner_space(object):
            def __init__(self, PaddyParameters):
                c = 0
                for parameter in PaddyParameters:
                    vars(self)['param_{0}'.format(c)] = parameter
                    c += 1
        
        def mock_run(mock_input):
            return(random.randrange(0,10))

        runner_space = test_runner_space(PaddyParameters)

        test_runner = paddy.PFARunner( space= runner_space , eval_func = mock_run , 
        rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = .75 , iterations = 15)        

        test_runner.random_step()
        rand_seed_amount=len(test_runner.seed_fitness)
        self.assertEqual(rand_seed_amount,50)

        test_runner.sowing_function()
        self.assertEqual(test_runner.yt,len(test_runner.s),'yt sets the amount of s values, should be equal')
        test_runner.yt = test_runner.yt_prime
        test_runner.neighbor_counter()
        self.assertEqual(test_runner.yt,len(test_runner.S) and len(test_runner.Un))
        test_runner.paddy_counter += 1
        test_runner.new_propogation()
        S = test_runner.S
        S_vals = []
        gen_data = test_runner.generation_data['1']
        print(gen_data)
        print(test_runner.S)
        for i in S:
            S_vals.append(i[1])
        print(S_vals)
        self.assertEqual(sum(S_vals),gen_data[1]+1-gen_data[0])





class test_Eval(unittest.TestCase):
    run_func = paddy.Default_Numerics.EvalNumeric()
    #tests recovery and extend paddy function
    test_polly_space = paddy.Default_Numerics.Polynomial(length=45,scope=10,gausian_type='scaled',normalization=False)
    test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
    rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = .75 , iterations = 3)
    test_runner.run_paddy(file_name='paddy/tests/test_files/paddy_test',verbose=None)
    val =test_runner.generation_fitness
    recovered_runner = paddy.utils.paddy_recover(file_name='paddy/tests/test_files/paddy_test')
    recovered_runner.extend_paddy(new_iterations = 3)
    assert(recovered_runner.paddy_counter == 6)

    def test_sowing_function_exceptions(self):
        pass

run_func = paddy.Default_Numerics.EvalNumeric(f_func=paddy.Default_Numerics.poly)
test_polly_space = paddy.Default_Numerics.Polynomial(length=5,scope=10,gausian_type='scaled',normalization=False)
test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = .75 , iterations = 5)
test_runner.run_paddy(verbose='all')
test_runner.paddy_plot_and_print(verbose=['scatter','box'])
test_runner.paddy_plot_and_print(verbose='box_notched')
test_runner.paddy_plot_and_print(verbose='box_hidden')
test_runner.paddy_plot_and_print(verbose=['pop_fitness','final_results','generation','gen_fitness'])
test_runner.paddy_plot_and_print(verbose=['madness'])

try:
	test_runner.paddy_plot_and_print(verbose=['box','madness'])
except:
	print('oopsies')

test_runner.get_generation_top_seed()
test_runner.get_generation_top_seed(counter=2)
test_runner.get_generation_top_seed(verbose = True)
test_runner.get_top_seed()
paddy.writer.single_param_print(test_runner.seed_params,5)
paddy.writer.clean_parameter_print(test_runner.top_values)



try:
	test_runner.extend_paddy(new_iterations='five')
except:
	print('this should not print, line 258')

try:
	test_runner.extend_paddy(new_iterations=5,new_verbose='all')
except:
	print('this should not print, line 263')

try:
	test_runner.save_paddy('paddy/tests/test_files/a_test')
except:
	print('this should not print, line 268')

try:
	test_runner.get_generation_top_seed(counter='beep')
except:
	print('this should not print, line 273')

try:
	test_runner.extend_paddy(new_iterations=0)
except:
	print('this should not print, line 278')


try:
	test_runner.extend_paddy(new_iterations='nine')
except:
	print('this should not print, line 284')


try:
	test_runner.extend_paddy(new_iterations=1,new_file_name='paddy/tests/test_files/new_handel')
except:
	print('this should not print, line 290')


try:
	test_runner.extend_paddy(new_iterations=1,verbose='status')
except:
	print('this should not print, line 296')

print("testing #######")
try:
	test_runner.recover_run(new_verbose='status')
except:
	print('this should not print, line 302')

###recovers an incomplete run###
try:
	ic = paddy.utils.paddy_recover("paddy/tests/test_files/incomplete")
	ic.recover_run()
except:
	print('this should not print, line 309')
###recovery errors

try:
	will_recover_backup = paddy.utils.paddy_recover("paddy/tests/test_files/only_backup")
	will_recover_backup.recover_run()
except:
	print('this should not print, line 316')


try:
	will_recover_backup = paddy.utils.paddy_recover("paddy/tests/test_files/only_backup")
except:
	print('this should not print, line 322')

try:
	no_backup = paddy.utils.paddy_recover("paddy/tests/test_files/no_backup")
except:
	print('this should not print, line 327')

try:
	why = paddy.utils.paddy_recover(8675309)
except:
	print('this should print, line 332')

try:
	this_wont_work = paddy.utils.paddy_recover("this is not a path")
except:
	print('this should print, line 337')

try:
	this_also_wont_work = paddy.utils.paddy_recover("paddy/tests/test_files/bad")
except:
	print('this should print, line 342')


try:
	again_these_pickles_are_garbage = paddy.utils.paddy_recover("paddy/tests/test_files/also_bad")
except:
	print('this should print, line 348')

try:
	only_backup = paddy.utils.paddy_recover("paddy/tests/test_files/bo")
except:
	print('this should not print, line 353')

try:
	test_runner.paddy_plot_and_print()
except:
	print('this should not print, line 358')

try:
	test_runner.paddy_plot_and_print(verbose=True)
except:
	print('this should not print, line 363')

###testing errors

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = .75 , iterations = 5)
	test_runner.run_paddy(verbose=None,file_name=5)
except:
	print('this should not print, line 372')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = '.75' , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 379')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = [.75,.5] , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 386')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = 'one' , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 393')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = -.75 , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 400')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = '.75' , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 407')


###r[0]
try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = [.75] , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 416')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = 'nonsense.75' , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 423')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 8, yt = 10, paddy_type = ['generational','madness'] , Qmax = 50  , r = .75 , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 430')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 8, yt = 10, paddy_type = 'generational' , Qmax = 50  , r = .75 , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 437')


try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = 50  , r = .75 , iterations = 5)
	test_runner.run_paddy(verbose=None)
except:
	print('this should not print, line 445')


try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'not valid' , Qmax = 50  , r = .75 , iterations = 5)
except:
	print('this should not print, line 452')


try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = [50,7]  , r = .75 , iterations = 5)
except:
	print('this should not print, line 459')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = '50'  , r = .75 , iterations = 5)
except:
	print('this should not print, line 465')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = 50.7  , r = .75 , iterations = 5)
except:
	print('this should not print, line 471')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = -50  , r = .75 , iterations = 5)
except:
	print('this should not print, line 477')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = [50]  , r = .75 , iterations = 5)
except:
	print('this should not print, line 483')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = 'generational' , Qmax = ['fifty']  , r = .75 , iterations = 5)
except:
	print('this should not print, line 489')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 50, yt = 2, paddy_type = ['generational'] , Qmax = -50  , r = .75 , iterations = 5)
except:
	print('this should not print, line 495')

try:
	test_runner = paddy.PFARunner( space= test_polly_space , eval_func = run_func.eval , 
	rand_seed_number = 3, yt = 2, paddy_type = ['generational'] , Qmax = 50  , r = .75 , iterations = 5)
except:
	print('this should not print, line 501')


###paddy parameter error testing

#range limit error
try:
	temp_param =  paddy.PaddyParameter(param_range=[5,1,2], param_type='integer',limits=[1,10], gaussian='default', normalization=True)
except:
	print('this should print, line 510')

#range limit error
try:
	temp_param =  paddy.PaddyParameter(param_range=[0,5,1], param_type='integer',limits=[1,4], gaussian='default', normalization=True)
except:
	print('this should print, line 516')

#equal limit error
try:
	temp_param =  paddy.PaddyParameter(param_range=[3,5,1], param_type='integer',limits=[5,5], gaussian='default', normalization=True)
except:
	print('this should print, line 522')


#limit order error
try:
	temp_param =  paddy.PaddyParameter(param_range=[0,5,1], param_type='integer',limits=[5,1], gaussian='default', normalization=True)
except:
	print('this should print, line 529')


#none limits norm error
try:
	temp_param =  paddy.PaddyParameter(param_range=[5,5,1], param_type='integer',limits=None, gaussian='default', normalization=True)
except:
	print('this should print, line 536')

#gausian error
try:
	temp_param =  paddy.PaddyParameter(param_range=[5,5,1], param_type='integer',limits=None, gaussian='madness', normalization=False)
except:
	print('this should print, line 542')

#param type error
try:
	temp_param =  paddy.PaddyParameter(param_range=[5,5,1], param_type='madness',limits=None, gaussian='default', normalization=False)
except:
	print('this should print, line 548')

#inf norm error 
try:
	temp_param =  paddy.PaddyParameter(param_range=[-100,10,1], param_type='integer',limits=[-math.inf,10], gaussian='default', normalization=True)
except:
	print('this should print, line 554')

try:
	temp_param =  paddy.PaddyParameter(param_range=[-10,10,1], param_type='integer',limits=None, gaussian='scaled', normalization=False)
	temp_param.new_seed_init([2,0])

except:
	print('this should print, line 561')

try:
	temp_param =  paddy.PaddyParameter(param_range=[-10,10,.1], param_type='integer',limits=None, gaussian='scaled', normalization=False)
	temp_param.new_seed_init([2,0])
	temp_param.random_init()

except:
	print('this should not print, line 569')

try:
	temp_param =  paddy.PaddyParameter(param_range=[-10,10,.1], param_type='integer',limits=[-10,10], gaussian='scaled', normalization=True)
	temp_param.new_seed_init([2,0])

except:
	print('this should not print, line 576')

###numeric test extensions###
paddy.Default_Numerics.trig_inter(x_list=[1,2,3,4,5],seed=[[1,2],[1,3]])
paddy.Default_Numerics.Polynomial(length=11,scope=10,gausian_type='default',normalization= False, limits=False)

###writer test###
paddy.writer.preformance_plotter(info=[],verbose='madness',figure_name=None)
