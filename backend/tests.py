from normal import *

##########################################################
######################  NORMAL   #########################
##########################################################

# 2. Una máquina automática llena botellas con cervezas de raíz con un promedio de
# 16 onzas por botella y desviación estándar de 0.5 onzas. Si la población tiene
# distribución normal, ¿Cuál es la probabilidad de que una muestra de 35 botellas
# tenga una media de llenado:
# a) Mayor que 16.1 onzas?
# b) Entre 15.9 y 16.1 onzas?

avg_pop = 16
var_pop = 0.5**2
distribution = "normal"

size_s = 35

#    PROBABILITY
#   P( Mu_x > 16.1 )
population_1 = Population(avg=avg_pop,dist='normal',var=var_pop)
sample_1 = Sample(size_s,population=population_1)

p = normal_left(   16.1,  population_1.avg,   population_1.std_dev,   sample_1.size   )

print("p = ",p)

##########################################################
######################  FINITE POP   #####################
##########################################################

# 1. Las estaturas de 1000 estudiantes están distribuidas aproximadamente en forma
# normal con una media de 174.5 centímetros y una desviación estándar de 6.9
# centímetros. Si se extraen 200 muestras aleatorias de tamaño 25 sin reemplazo de
# esta población, determine el número de medias muestrales que caen entre 172.5 y
# 175.8 centímetros.

population_2 = Population(avg=174.5,dist='normal',size=1000,std_dev=6.9)
sample_2 = Sample(25,population=population_2,samples_taken=200)

z1 = (172.5 - population_2.avg)/(sample_2.std_dev)
z2 = (175.8 - population_2.avg)/(sample_2.std_dev)

p = normal_cdf(z2) - normal_cdf(z1)
# p = normal_left(175.8,sample_2.avg,sample_2.std_dev,sample_2.size) - normal_left(172.5,sample_2.avg,sample_2.std_dev,sample_2.size)

print("p = ",p)

#####################################################
######################  C L T   #####################
#####################################################

# 2. La resistencia a la ruptura de un remache tiene una media de 10000lb/in2
# y una desviación estándar de 500 lb/in2.

# a) ¿Cuál es la probabilidad de que la resistencia media a la ruptura de la muestra, para
# una muestra aleatoria de 40 remaches, sea entre 9900 y 10200?

# b) Si el tamaño muestral hubiera sido 15 en lugar de 40, ¿podría calcularse la
# probabilidad pedida en el inciso a)?

population_3 = Population(avg=10_000, std_dev=500)
sample_3_1 = Sample(40,population=population_3)
sample_3_2 = Sample(15,population=population_3)

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
    
test = Test([9900,10200],'<')

def probability_switch( params : Test, *samples : Sample, population : Population = None )->float:
    sample_arr = []
    z = None

    # Fill z array for critical values and order them in any case
    if len(params.find['critical_values']) > 1:
        # Always sort in descending order (largest to smallest)
        z = sorted(params.find['critical_values'], reverse=True)
    else:
        z = params.find['critical_values']

    # Fill our sample array with the input samples
    if ( samples ) :
        for sample in samples :
            sample_arr.append(sample)

    # FIX: Check distribution from sample or population
    distribution = None
    if sample_arr and hasattr(sample_arr[0], 'distribution'):
        distribution = sample_arr[0].distribution
    elif population and hasattr(population, 'distribution'):
        distribution = population.distribution

    if ( distribution == 'normal' ) :
        if (  len(z) == 1  ) :
            if ( params.find['tail'] == '<' ) :
                z = standarize_z(z[0],sample_arr[0].avg,sample_arr[0].std_dev ,sample_arr[0].size)
                return normal_cdf(z)
            if ( params.find['tail'] == '>' ) :
                z = standarize_z(z[0],sample_arr[0].avg,sample_arr[0].std_dev ,sample_arr[0].size)
                return 1 - normal_cdf(z)
        else :
            
            # z_sup = (z[0] - sample_arr[0].avg)/(sample_arr[0].std_dev/sqrt(sample_arr[0].size))
            z_sup = (z[0] - sample_arr[0].avg)/(sample_arr[0].std_dev/sqrt(sample_arr[0].size))
            # z_inf = (z[1] - sample_arr[0].avg)/(sample_arr[0].std_dev/sqrt(sample_arr[0].size))
            z_inf = (z[1] - sample_arr[0].avg)/(sample_arr[0].std_dev/sqrt(sample_arr[0].size))
            return normal_cdf(z_sup) - normal_cdf(z_inf)
    return 0

p = probability_switch(test, sample_3_1, population=population_3)
print(p)