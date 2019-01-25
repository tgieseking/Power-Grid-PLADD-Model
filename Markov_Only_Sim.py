from PLADD.Markov import *
import numpy as np
from matplotlib.pyplot import plot, show, hist, legend, xlabel, ylabel, title

# Initializing Markov Model
start_node = TransientNode()
grid_data_node = TransientNode()
vulerability_report_node = TransientNode()
ip_node = TransientNode()
substation_node = TransientNode()
injected_node = TransientNode()
avoided_detection_node = TransientNode()
success_node = AbsorbingNode("SUCCESS")
captured_node = AbsorbingNode("CAPTURED")

start_node.set_transitions({start_node: 0.65, grid_data_node: 0.25, captured_node: 0.1})

grid_data_node.set_transitions({grid_data_node: 0.5, vulerability_report_node: 0.25, start_node: 0.15, captured_node: 0.1})

vulerability_report_node.set_transitions({vulerability_report_node: 0.5, ip_node: 0.25, grid_data_node: 0.15, captured_node: 0.1})

ip_node.set_transitions({ip_node: 0.5, substation_node: 0.25, vulerability_report_node: 0.15, captured_node: 0.1})

substation_node.set_transitions({substation_node: 0.5, injected_node: 0.25, ip_node: 0.15, captured_node: 0.1})

injected_node.set_transitions({injected_node: 0.5, avoided_detection_node: 0.25, substation_node: 0.15, captured_node: 0.1})

avoided_detection_node.set_transitions({avoided_detection_node: 0.5, success_node: 0.25, injected_node: 0.15, captured_node: 0.1})


# To save time, we precalculate the Markov model result distribution
model = Markov([start_node, grid_data_node, vulerability_report_node, ip_node, substation_node, injected_node, avoided_detection_node], [success_node, captured_node], start_node)
markov_dist = model.calculate_output_probs()
print(markov_dist)

probabilities = model.calculate_state_probabilities(25)

plot(probabilities)
legend(("Start", "Grid data obtained", "Vulnerability report", "IP address obtained", "Substation breached", "Data injected", "Avoided detection", "Attack succeeded", "Attacker captured"))
xlabel("Step Number")
ylabel("State Probability")
title("Probabilities Attacker is in Each State Over Time")
show()

final_probabilities = np.zeros((25, 3))
final_probabilities[:,0] = np.sum(probabilities[:, :7], axis=1)
final_probabilities[:,1:] = probabilities[:, -2:]
plot(final_probabilities)
legend(("Attack ongoing", "Attacker captured", "Attack succeded"))
xlabel("Step Number")
ylabel("State Probability")
title("Probabilities of Outomes Over Time: Markov Model")
show()
