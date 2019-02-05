import random
import numpy as np

class MarkovComponent:
    # a Markov Chain.
    def __init__(self, transient_matrix, absorbing_matrix, outputs, start_index = 0):
        self.transient_matrix = transient_matrix
        # The transition matrix between transient nodes
        self.absorbing_matrix = absorbing_matrix
        # The transition matrix from transient to absorbing nodes
        self.outputs = outputs
        # What the component should output when it ends on each absorbing node
        self.start_index = start_index
        self.final_state_probs = self.calculate_final_state_probs()
        # Precompute the probabilities of reaching each final state

    def run_simulation(self):
        current_node = self.start_node
        while(not current_node.absorbing):
            current_node = current_node.next_node()
        return current_node.output

    def advance_timestep(self):
        num_absorbing = self.final_state_probs.size
        final_state_index = np.random.choice(num_absorbing, p=self.final_state_probs)
        self.current_output = self.outputs[final_state_index]


    def calculate_final_state_probs(self):
        num_transient, num_absorbing = self.absorbing_matrix.shape
        start_probabilies = np.zeros(num_transient)
        start_probabilies[self.start_index] = 1.0

        final_state_probs = self.absorbing_matrix.T @ np.linalg.solve(np.eye(num_transient) - self.transient_matrix.T, start_probabilies)

        return final_state_probs
