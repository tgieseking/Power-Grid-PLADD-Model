from PLADD.Markov import *
import numpy as np

transient_matrix = np.asarray([
[0.2, 0.5, 0.3],
[0.0, 0.0, 0.0],
[0.0, 0.0, 0.0]
])
absorbing_matrix = np.asarray([
[0.0, 0.0],
[0.5, 0.5],
[0.0, 1.0]
])
markov_component = MarkovComponent(transient_matrix, absorbing_matrix, ['A', 'B'])

print(markov_component.final_state_probs)

outs = {'A':0, 'B':0}
for i in range(1000):
    markov_component.advance_timestep()
    outs[markov_component.current_output] += 1
print(outs)
