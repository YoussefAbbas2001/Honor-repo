import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from matplotlib import pyplot as plt

class pidcont():
    def __init__(self,P,I,D,pmax,pmin):
        self.kp      = P         # Proportional Weight
        self.kd      = D         # Derviative Weight
        self.ki      = I         # Intergral Weight
        self.pidmax  = pmax      # Maximum Accumluation of Error signal
        self.pidmin  = pmin      # Minimum Accumluation of Error signal
        self.desired = 0.0       # Set Point of PID
        self.error   = 0.0       # Error = Setpoint - Current
        self.elast   = 0.0       # Previous Error
        self.esum    = 0.0       # Cummulative of Error
        self.eder    = 0.0       # Difference in Current and previous Error

    def update(self,current):
        self.error = self.desired - current
        self.eder  = self.error   - self.elast
        self.elast = self.error
        self.esum  = self.esum + self.error
        if self.esum>self.pidmax:
            self.esum=self.pidmax
        elif self.esum<self.pidmin:
            self.esum=self.pidmin

        self.P = self.kp * self.error
        self.D = self.kd * self.eder
        self.I = self.ki * self.esum
        pid    = self.P + self.I + self.D
        return pid
    
    def setDesired(self,d):
        self.desired = d

    def setGains(self,P,I,D):
        self.kp = P
        self.kd = D
        self.ki = I

    def setLimits(self,pmax,pmin):
        self.pidmax=pmax
        self.pidmin=pmin
        
plt.ion()
fig=plt.figure()

ferr = ctrl.Antecedent(np.arange(-150, 150, 1), 'ferr')
fder = ctrl.Antecedent(np.arange(-150, 150, 1), 'fder')
fout = ctrl.Consequent(np.arange(-1, 1, 0.01), 'fout')

ferr.automf(5)
fder.automf(5)
fout.automf(5)
fout['poor'] = fuzz.trimf(fout.universe, [-1, -1, -0.5])
fout['mediocre'] = fuzz.trimf(fout.universe, [-1, -0.5, 0])
fout['average'] = fuzz.trimf(fout.universe, [-0.1, 0, 0.1])
fout['decent'] = fuzz.trimf(fout.universe, [0, 0.5, 2])
fout['good'] = fuzz.trimf(fout.universe, [0.5, 1, 1])
fout.view()
ferr.view()
fder.view()
plt.show()
plt.pause(0.0001)

#'poor'; 'mediocre'; 'average'; 'decent', or 'good'
rules=[]
rules.append(ctrl.Rule(ferr['average'] | fder['average'] , fout['average']))
rules.append(ctrl.Rule(ferr['decent'] | fder['decent'] , fout['decent']))
rules.append(ctrl.Rule(ferr['good'] | fder['good'] , fout['good']))
rules.append(ctrl.Rule(ferr['mediocre'] | fder['mediocre'] , fout['mediocre']))
rules.append(ctrl.Rule(ferr['poor'] | fder['poor'] , fout['poor']))

fctrl = ctrl.ControlSystem(rules)
fpid = ctrl.ControlSystemSimulation(fctrl)

pid= pidcont(1.2,0.02,0.01,5,-5)

pid2= pidcont(1.2,0.02,0.01,5,-5)

d=np.zeros(10)
for i in range(10):
    d=np.append(d,np.ones(10)*np.random.uniform(-100,100,1))

print(len(d))
m=[]
m.append(0.0)
m2=[]
m2.append(0.0)
e=[]
de=[]
e2=[]
de2=[]

kp=pid.kp
kd=pid.kd
ki=pid.ki
for i in range(len(d)):
    pid.setDesired(d[i])
    print("e:",pid.error ,"\t de:", pid.eder)
    fpid.input['ferr'] = pid.error
    fpid.input['fder'] = pid.eder
    fpid.compute()
    newpid=np.abs(fpid.output['fout'])
    print("PID:", newpid*pid.kp,"\t",newpid*pid.ki,"\t",newpid*pid.kd)
    pid.setGains(newpid*kp,newpid*ki,newpid*kd)
    newm=pid.update(m[-1])
    newm=m[-1]+newm
    print(i,m[-1],newm)
    m.append(newm)
    e.append(pid.error)
    de.append(pid.eder)

    pid2.setDesired(d[i])
    newm2=pid2.update(m2[-1])
    newm2=m2[-1]+newm2
    m2.append(newm2)
    e2.append(pid2.error)
    de2.append(pid2.eder)

    ax1 =plt.subplot(2,1,1)
    ax1.set_xlim([0, len(d)])
    ax1.set_ylim([-200, 200])
    plt.grid()
    plt.plot(range(len(m)),m,linewidth=5.0)
    plt.plot(range(len(m2)),m2,linewidth=2.0)
    plt.plot(range(len(d)),d,'g--')

    plt.title('Status')
    ax2=plt.subplot(2,1,2)
    ax2.set_xlim([0, 50])
    ax2.set_ylim([-100, 100])
    plt.plot(range(len(e)),e,'r-',range(len(de)),de,'g-')
    plt.grid()
    plt.title('e and ed')
    #plt.draw()
    plt.show()
    plt.pause(0.0001)