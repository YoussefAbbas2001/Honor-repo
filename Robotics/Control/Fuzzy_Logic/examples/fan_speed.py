'''
Determine The fan speed based on Current Temperature

'''
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl 
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# Define Input and Output
temp = ctrl.Antecedent(np.arange(101), 'temp')
speed= ctrl.Consequent(np.arange(101), 'speed')

# FUZZIFICATION
# Define Memberfunction 
temp['cold']   = fuzz.trimf(temp.universe, [0, 30, 50] )
temp['normal'] = fuzz.trimf(temp.universe, [40, 55, 75] )
temp['hot']    = fuzz.trimf(temp.universe, [65, 80, 100] )
temp.view()


speed['slow']    = fuzz.trimf(speed.universe, [0, 30, 50] )
speed['medium'] = fuzz.trimf(speed.universe, [40, 55, 75] )
speed['fast']   = fuzz.trimf(speed.universe, [60, 80, 100] )
speed.view()

# print(speed.universe)
# print(speed.terms)
# print(speed.label)
# print(dir(speed['low']))
# print(speed['low'].mf)




# FUZZY RULES
rule1 = ctrl.Rule(temp['cold']  , speed['slow'])
rule2 = ctrl.Rule(temp['normal'], speed['medium'])
rule3 = ctrl.Rule(temp['hot']   , speed['fast'])

rule1.view()

# CONTROL SYSTEM
fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
fan      = ctrl.ControlSystemSimulation(fan_ctrl)
fan.input['temp'] = 90
fan.compute()
print('Fan Speed :  ',fan.output['speed'])
speed.view(sim=fan)

plt.show()
