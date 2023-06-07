# Import packages.
import cvxpy as cp
import numpy as np

# Generate a  linear program.
n = 2                             # Variables Dimensional
x  = cp.Variable(n)               # Optimization variables
g  = [x>=0, x[0]+2*x[1]<=2]       # Constraints

# Solve the Problem
prob = cp.Problem(cp.Maximize(cp.sum(x)), g)
prob.solve()

# Print result.
print(f"Optimal Point : {x.value}")
print(f"Optimal Value : {prob.value}")

