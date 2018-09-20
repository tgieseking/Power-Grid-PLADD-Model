import random

class Markov:
    # a Markov Chain.
    def __init__(self, start_node):
        self.start_node = start_node

    def run_simulation(self):
        current_node = self.start_node
        while(not current_node.final):
            current_node = current_node.next_node()
        return current_node.output

class MarkovNode:
    # a single node of a Markov chain
    def __init__(self, final, output = None):
        self.final = final
        # whether the simulation should stop when this node is reached
        self.output = output
        # the returned value if the simulation stops in this node
        self.transitions = []
        # a list of pairs (state, transition probability)
        self.previous_nodes = set([])

    def add_transition(self, next_node, probability):
        self.transitions.append((next_node, probability))
        next_node.previous_nodes.add(self)

    def next_node(self):
        # randomly selects a node to transition to from this node according to the supplied transition distribution
        rand_double = random.random()
        total = 0.0
        index = 0
        while total < rand_double:
            total += self.transitions[index][1]
            index += 1
        return self.transitions[index - 1][0]
