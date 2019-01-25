import random
import numpy as np

class Markov:
    # a Markov Chain.
    def __init__(self, transient_nodes, absorbing_nodes, start_node):
        self.transient_nodes = transient_nodes
        self.absorbing_nodes = absorbing_nodes
        self.start_node = start_node

        for index, node in enumerate(transient_nodes):
            node.transient_index = index
        for index, node in enumerate(absorbing_nodes):
            node.absorbing_index = index

    def run_simulation(self):
        current_node = self.start_node
        while(not current_node.absorbing):
            current_node = current_node.next_node()
        return current_node.output

    def calculate_state_probabilities(self, num_steps):
        num_transient = len(self.transient_nodes)
        num_absorbing = len(self.absorbing_nodes)
        num_nodes = num_transient + num_absorbing

        transient_matrix = np.zeros((num_transient, num_transient))
        absorbing_matrix = np.zeros((num_transient, num_absorbing))


        for node in self.transient_nodes:
            for next_node in node.transitions:
                if next_node.absorbing:
                    absorbing_matrix[node.transient_index, next_node.absorbing_index] = node.transitions[next_node]
                else:
                    transient_matrix[node.transient_index, next_node.transient_index] = node.transitions[next_node]

        transition_matrix = np.zeros((num_nodes, num_nodes))
        transition_matrix[:num_transient, :num_transient] = transient_matrix
        transition_matrix[:num_transient, num_transient:] = absorbing_matrix
        transition_matrix[num_transient:, num_transient:] = np.eye(num_absorbing)
        print(transition_matrix)

        current_probabilies = np.zeros(num_nodes)
        current_probabilies[self.start_node.transient_index] = 1.0

        probabilities = np.zeros((num_steps, num_nodes))

        for i in range(num_steps):
            probabilities[i] = np.copy(current_probabilies)
            current_probabilies = current_probabilies @ transition_matrix
        return probabilities




    def calculate_output_probs(self):
        num_transient = len(self.transient_nodes)
        num_absorbing = len(self.absorbing_nodes)

        transient_matrix = np.zeros((num_transient, num_transient))
        absorbing_matrix = np.zeros((num_transient, num_absorbing))

        for node in self.transient_nodes:
            for next_node in node.transitions:
                if next_node.absorbing:
                    absorbing_matrix[node.transient_index, next_node.absorbing_index] = node.transitions[next_node]
                else:
                    transient_matrix[node.transient_index, next_node.transient_index] = node.transitions[next_node]

        start_probabilies = np.zeros(num_transient)
        start_probabilies[self.start_node.transient_index] = 1.0
        final_probabilities = absorbing_matrix.T @ np.linalg.solve(np.eye(num_transient) - transient_matrix.T, start_probabilies)

        output_probabilities = {}
        for i in range(num_absorbing):
            output = self.absorbing_nodes[i].output
            if output in output_probabilities:
                output_probabilities[output] += final_probabilities[i]
            else:
                output_probabilities[output] = final_probabilities[i]

        return output_probabilities

class TransientNode:
    def __init__(self):
        self.absorbing = False

    def set_transitions(self, transitions):]
        total_probability = sum(transitions.values())
        epsilon = 10**-6
        if abs(1.0 - total_probability) > epsilon:
            raise ProbabilitySumError()

        self.transitions = transitions

    def next_node(self):
        return select_from_dist(self.transitions)

class AbsorbingNode:
    def __init__(self, output):
        self.absorbing = True
        self.output = output

def select_from_dist(distribution):
    rand_double = random.random()
    total = 0.0
    for key in distribution:
        total += distribution[key]
        if total >= rand_double:
            return key

class ProbabilitySumError(Exception):
    pass
