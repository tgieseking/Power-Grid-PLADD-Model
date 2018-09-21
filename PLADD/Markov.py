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

    def calculate_output_probs(self):
        # if this object is a Markov chain that is a DAG where the start node is the only chain with no inputs, this function calculates the probabilites of the chain getting each possible output

        # all three of these function track probabilites that the Markov chain eventually is in a given node
        output_probs = {}# all three of these function track probabilites that the Marko
        # final probabilies of output nodes
        in_progress_probs = {self.start_node:1}
        # probabilies of nodes that we have not finished calculating yet
        final_probs = {}
        # probabilies of nodes that we are done calculating with

        while(in_progress_probs):
            for node in dict(in_progress_probs):
                # we copy in_progress_probs here because we are modifying in_progress_probs inside the loop
                if all([(prev in final_probs) for prev in node.previous_nodes]):
                    # we have finished calculating the probabilies of all previous nodes, so this node is done
                    if node.final:
                        if node.output in output_probs:
                            output_probs[node.output] += in_progress_probs.pop(node)
                        else:
                            output_probs[node.output] = in_progress_probs.pop(node)
                    else:
                        final_probs[node] = in_progress_probs.pop(node)
                        for next_node, transition_prob in node.transitions:
                            if next_node in in_progress_probs:
                                in_progress_probs[next_node] += transition_prob * final_probs[node]
                            else:
                                in_progress_probs[next_node] = transition_prob * final_probs[node]
        return output_probs

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
