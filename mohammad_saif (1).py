# -*- coding: utf-8 -*-
"""Mohammad Saif.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-Fx1RXFcHWQw4mIt3u4CmYKBwYiiQB0J

# Objective function : 2ab+2bc+2ac-a-b-c+1
find value for a,b,c

#Installation
"""

pip install dimod

pip install dwave-neal

pip install dwave-ocean-sdk

"""#Method 1: Classical Solver"""

import dimod
from dimod import ExactSolver

Q = [[ -1, 2, 1, 0],
     [ 2, -1, 2, 0],
     [ 1, 2, -1, 0],
     [ 0, 0, 0, 0]]

# Q = {(0, 1): 2, (0, 2): 2, (1, 2): 2, (0, 0): -1, (1, 1): -1, (2, 2): -1}
exactsolver = dimod.ExactSolver()
response = exactsolver.sample_qubo(Q)

# Print the best sample and its energy
best_sample = response.first.sample
best_energy = response.first.energy
print("Best sample:", best_sample)
print("Best energy:", best_energy)
print("\n\n All possible solution")

# Print the all results
for sample, energy in response.data(['sample', 'energy']):
  print(sample,energy)

print(response)

"""#Method 2A: Simulated Annealing"""

import neal

# Define the objective function as (QUBO) problem
Q = {(0, 1): 2, (0, 2): 2, (1, 2): 2, (0, 0): -1, (1, 1): -1, (2, 2): -1}
offset = 1

# Solve the problem using the SimulatedAnnealingSampler solver
sampler = neal.SimulatedAnnealingSampler()
response = sampler.sample_qubo(Q, num_reads=1000)

# # Print the results
# for sample, energy in response.data(['sample', 'energy']):
#     a = sample[0]
#     b = sample[1]
#     c = sample[2]
#     if energy == response.first.energy:
#         print(a,b,c)
#         print(f'Energy: {energy + offset}')

best_sample = response.first.sample
best_energy = response.first.energy
print("Best sample:", best_sample)
print("Best energy:", best_energy)

"""#Method 2B: Simulated Annealing"""

from dwave.samplers import SimulatedAnnealingSampler

# Define the QUBO matrix
Q = {(0,1): 2, (0,2): 2, (1,2): 2, (0,0): -1, (1,1): -1, (2,2): -1, (3,3): 1}


# Create a SimulatedAnnealingSampler object
sampler = SimulatedAnnealingSampler()

# Solve the QUBO problem using simulated annealing
response = sampler.sample_qubo(Q, num_reads=1000)

# Print the best sample and its energy
best_sample = response.first.sample
best_energy = response.first.energy
print("Best sample:", best_sample)
print("Best energy:", best_energy)

"""#Method 3: Hybrid Solver"""

from dwave.system import  LeapHybridSampler

# Define the objective function as (QUBO) problem
Q = {(0, 1): 2, (0, 2): 2, (1, 2): 2, (0, 0): -1, (1, 1): -1, (2, 2): -1}

# Create a LeapHybridSampler object
sampler = LeapHybridSampler(token = "DEV-79b52af764c9cc6cefaf61d21dd2820ef46f5f72")

# Solve the QUBO problem using Hybrid Solver with Default time
response = sampler.sample_qubo(Q, time_limit   = 3)

# Print the best sample and its energy
best_sample = response.first.sample
best_energy = response.first.energy
print("Best sample:", best_sample)
print("Best energy:", best_energy)

import dwave 
import dimod
from dwave.system import LeapHybridSampler
import numpy as np

Q = {(0,1): 2, (0,2): 2, (1,2): 2, (0,0): -1, (1,1): -1, (2,2): -1, (3,3): 1}

bqm = dimod.BQM.from_qubo(Q)

result = LeapHybridSampler(token = "DEV-79b52af764c9cc6cefaf61d21dd2820ef46f5f72").sample(bqm, label='Notebook - Hybrid Computing 1')
print("Found solution with {} nodes at energy {}.".format(np.sum(result.record.sample), result.first.energy))

from dwave.system import DWaveSampler, EmbeddingComposite

Q = {(0,1): 2, (0,2): 2, (1,2): 2, (0,0): -1, (1,1): -1, (2,2): -1, (3,3): 1}
sampler = EmbeddingComposite(DWaveSampler(token = "DEV-79b52af764c9cc6cefaf61d21dd2820ef46f5f72"))
response = sampler.sample_qubo(Q, num_reads=1000)

sample = response.first.sample
energy = response.first.energy
print("Sample:", sample)
print("Energy:", energy)

"""#TSP Problem."""

!pip install pyqubo
!pip install dwave-system

# Commented out IPython magic to ensure Python compatibility.

# %matplotlib inline
from pyqubo import Array, Placeholder, Constraint
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

n_city = 4
x = Array.create('c', (n_city, n_city), 'BINARY')

# Constraint not to visit more than two cities at the same time.
time_const = 0.0
for i in range(n_city):
    # If you wrap the hamiltonian by Const(...), this part is recognized as constraint
    time_const += Constraint((sum(x[i, j] for j in range(n_city)) - 1)**2, label="time{}".format(i))

# Constraint not to visit the same city more than twice.
city_const = 0.0
for j in range(n_city):
    city_const += Constraint((sum(x[i, j] for i in range(n_city)) - 1)**2, label="city{}".format(j))

# distance of route
dist = np.array([
    [0 , 10 , 40 , 30],
    [10 , 0  ,20 , 50],
    [40 ,20 ,  0 , 20],
    [30 ,50 , 20,   0]
])

flow = np.array([
    [0 , 30 , 5 , 10],
    [30 , 0 , 5 , 20],
    [5 , 5 , 0 , 50],
    [10 , 20 , 50 , 0]
])
n_city = 4

distance = 0.0
for i in range(n_city):
  for j in range(n_city):
          for k in range(n_city):
              for l in range(n_city):
                      distance += flow[i][j] * x[i][k] * dist[k][l] *x[j][l]

# Construct hamiltonian
A = Placeholder("A")
max_bound = np.max(dist) *  np.max(flow) + 1
print(max_bound)
H = distance + A * (time_const + city_const)

# Compile model
model = H.compile()

# Generate QUBO
feed_dict = {'A': max_bound}
bqm = model.to_bqm(feed_dict=feed_dict)
print(bqm)

"""#**1. Simulated Annealing Solver**"""

import neal
sa = neal.SimulatedAnnealingSampler()
sampleset = sa.sample(bqm, num_reads=100, num_sweeps=100)
# nums_read = Indicates the number of states (output solutions) to read from the solver.
# Must be a positive integer in the range given by the num_reads_range solver property.

# Decode solution
decoded_samples = model.decode_sampleset(sampleset, feed_dict=feed_dict)
best_sample = min(decoded_samples, key=lambda x: x.energy)
num_broken = len(best_sample.constraints(only_broken=True))
print("number of broken constarint = {}".format(num_broken))
print(best_sample)

#for trail only
sample = sampleset.first.sample
energy = sampleset.first.energy
print("Sample:", sample)
print("Energy:", energy)

# Optimal solution as a 2D matrix
opt = np.zeros((n_city, n_city))
for i in range(n_city):
    for j in range(n_city):
        if best_sample.array('c', (i, j)) == 1:
            opt[i][j] = 1

print(opt)
print("Energy:", energy)

"""#Correct Answer

The correct answer is 
x =

      [[0. 0. 0. 1.]
      [0. 0. 1. 0.]
      [1. 0. 0. 0.]
      [0. 1. 0. 0.]]
optimal solution (minimum of flow*dist possible): 4700.0

#**2. Hybrid Solver**
"""

from dwave.system import  LeapHybridSampler
sa = LeapHybridSampler(token = "DEV-79b52af764c9cc6cefaf61d21dd2820ef46f5f72")
sampleset = sa.sample(bqm,time_limit=3)

# Decode solution
decoded_samples = model.decode_sampleset(sampleset, feed_dict=feed_dict)
best_sample = min(decoded_samples, key=lambda x: x.energy)
num_broken = len(best_sample.constraints(only_broken=True))
print("number of broken constarint = {}".format(num_broken))
print(best_sample)
energy = sampleset.first.energy

# Optimal solution as a 2D matrix
opt = np.zeros((n_city, n_city))
for i in range(n_city):
    for j in range(n_city):
        if best_sample.array('c', (i, j)) == 1:
            opt[i][j] = 1

print(opt)
print("Energy:", energy)

"""#**3.Quantum Solver**"""

from dwave.system import DWaveSampler, EmbeddingComposite
sampler = EmbeddingComposite(DWaveSampler(token = "DEV-79b52af764c9cc6cefaf61d21dd2820ef46f5f72"))
sampleset = sampler.sample(bqm, num_reads=100)

# Decode solution
decoded_samples = model.decode_sampleset(sampleset, feed_dict=feed_dict)
best_sample = min(decoded_samples, key=lambda x: x.energy)
num_broken = len(best_sample.constraints(only_broken=True))
print("number of broken constarint = {}".format(num_broken))
print(best_sample)


#for trail only
sample = sampleset.first.sample
energy = sampleset.first.energy
print("Sample:", sample)
print("Energy:", energy)

# Optimal solution as a 2D matrix
opt = np.zeros((n_city, n_city))
for i in range(n_city):
    for j in range(n_city):
        if best_sample.array('c', (i, j)) == 1:
            opt[i][j] = 1

print(opt)
print("Energy:", energy)

?DWaveSampler.sample

?EmbeddingComposite.sample

"""#**4. Classical Solver**"""

import dimod
from dimod import ExactSolver

sampler = dimod.ExactSolver()
sampleset = sampler.sample(bqm)

# Decode solution
decoded_samples = model.decode_sampleset(sampleset, feed_dict=feed_dict)
best_sample = min(decoded_samples, key=lambda x: x.energy)
num_broken = len(best_sample.constraints(only_broken=True))
print("number of broken constarint = {}".format(num_broken))
print(best_sample)

#only for best trail 
#for trail only
sample = sampleset.first.sample
energy = sampleset.first.energy
print("Sample:", sample)
print("Energy:", energy)

# Optimal solution as a 2D matrix
opt = np.zeros((n_city, n_city))
for i in range(n_city):
    for j in range(n_city):
        if best_sample.array('c', (i, j)) == 1:
            opt[i][j] = 1

print(opt)
print("Energy:", energy)