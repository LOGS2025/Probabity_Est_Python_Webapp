from math import *
import numpy as np

# VERY ACCURATE AT 0.00001 DX BUT TOO SLOW
def norm_dist_gen(delta_x : float, b : float):
    p_dist = []
    def p_std_prob_function(z : float)->float:
        z_float = float(z)
        p_value = (1*e**((-z**2)/2))/(sqrt(2*pi))

        return p_value
    
    a = -1000
    i = a
    
    while i < b:
        p_dist.append( p_std_prob_function(i) )
        i += delta_x
    
    # Get the area under the curve by rectangles
    prev = p_dist[0]
    total_area = 0
    for i in p_dist:
        #Heights
        right = i
        total_area += (right -  prev)*delta_x

    print(total_area)

#################################################################
######################  DISTRIBUTIONS   #########################
#################################################################

# FASTER VERSION WITH NUMPY C VECTORIZATION INTEGRATION
def normal_cdf(b : float)->float:
    z = np.arange(-1000,b,0.0001)
    pdf = (1*np.exp((-z**2)/2))/(np.sqrt(2*np.pi))
    return np.trapezoid(pdf,z)

# RETURNS GREATER THAN
def t_cdf(b : float,v : int)->float:
    t = np.arange(-10,b,0.0001)
    pdf = (  gamma( (v+1)/2 ) * (  (  1 + (t**2)/v  )**(-(v+1)/2)  )  )/(  sqrt(v*pi) * gamma(v/2)  )
    return 1 - np.trapezoid(pdf,t)

def xi2_cdf():
    pass

def fisher():
    pass

##########################################################
######################  STAT Z   #########################
##########################################################

def standarize_z(x : float ,mu : float ,sigma : float ,n : int)->float:
    return (x-mu)/(sigma/sqrt(n))

def normal_left(x : float ,mu : float ,sigma : float ,n : int)->float:
    z = standarize_z(x,mu,sigma,n)
    return 1 - normal_cdf(z)

def normal_right(x : float ,mu : float ,sigma : float ,n : int)->float:
    z = standarize_z(x,mu,sigma,n)
    return normal_cdf(z)

##########################################################
######################  STAT T   #########################
##########################################################

def Sp_c1(): 
    pass
def Sp_c2():
    pass
def T_c1():
    pass
def T_c2():
    pass

########################################################
######################  VARS   #########################
########################################################

# Population class
class Population :
    distribution : str
    size : int
    avg : float
    var : float
    std_dev : float

    def __init__(self, avg : float = None, dist : str = None, var : float = None, std_dev : float = None, size : int = None):
        self.avg = avg 
        self.distribution = dist 
        self.var = var
        self.std_dev = std_dev
        self.size = size

        if ( var ) : 
            self.std_dev = sqrt(var)
        if ( std_dev ) :
            self.var = std_dev**2

        pass


# Sample class
class Sample :
    from_population : Population

    distribution : str
    size : int
    samples_taken : int
    avg : float
    var : float
    std_dev : float
    fNn : float

    def __init__(self, n : int, samples_taken : int = None, dist : str = None, avg : float = None, var : float = None, std_dev : float = None, population : Population = None):
        self.from_population = population
        self.distribution = dist
        self.avg = avg
        self.size = n # SAMPLES SIZE
        self.var = var
        self.std_dev = std_dev
        self.samples_taken = samples_taken # NUMBER OF SAMPLES TAKEN

        if ( self.from_population ):
                # GRAB THE SAME PARAMETERS FROM POPULATION
            if ( not self.avg and self.from_population ) :
                self.avg = self.from_population.avg
                # GRAB THE SAME PARAMETERS FROM POPULATION
            if ( not self.var or self.std_dev and self.from_population ) :
                self.var = self.from_population.var
                self.std_dev = sqrt(self.var)

        if ( var and not std_dev ) : 
            self.std_dev = sqrt(var)
        if ( std_dev and not var ) :
            self.var = std_dev**2
        
        # WE ASSUME THAT IF THERE IS AN INPUT ON POPULATION, WE DO SAMPLING
        # WITTHOUT REPLACEMENT FOR SIMPLICITY 
        
        self.fNn = self.corr_factor()
        
        if ( self.fNn ):

            self.var = (self.from_population.var / self.size)*self.fNn
            self.std_dev = (self.from_population.std_dev/sqrt(self.size))*sqrt(self.fNn)

        if ( self.clt_check() ):
            print("Check made")

        pass

    def corr_factor( self ) :
        if ( self.from_population.size and self.size) :
            cocienteNn = self.size / self.from_population.size
            if ( cocienteNn < 0.05 ) :
                return ( self.from_population.size - self.size ) / ( self.from_population.size - 1 )
        else :
            return None

    def clt_check(self)->bool:
        if ( not self.distribution ):
            if ( self.size > 30):
                self.distribution = "normal"
                print("set dist to normal by clt")
                return True
            else :
                print("set dist to t of student")
                self.distribution = "t_student"
                return True
        elif ( self.distribution == 'normal' ) :
            return True
        else :
            return False
        
class Test :
    find = {
        'critical_values' : list,
        'tail' : str,
    }

    def __init__(self, critical_values : list , tail : str)->str:
        if (len(critical_values) > 0):
            self.find['critical_values'] = critical_values
            self.find['tail'] = tail

            # Validate when you use it
            if self.find['tail'] not in ['<', '>', '!=']:
                raise ValueError("tail must be '<', '>', or '!='")
        pass