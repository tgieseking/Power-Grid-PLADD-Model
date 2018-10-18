from PLADD.PLADD import *
from PLADD.Markov import *

timesteps_per_unit = 100

grid_data_attack = lambda: ExponentialAttack(0.5, timesteps_per_unit)
grid_data = Resource(grid_data_attack, grid_data_attack, lambda: True)

vulerability_report_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
vulerability_report = Resource(vulerability_report_attack, vulerability_report_attack, lambda: True)

ip_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
ip = Resource(ip_attack, ip_attack, lambda: True)

rtu_attack = lambda: ExponentialAttack(0.6, timesteps_per_unit)
rtu = Resource(rtu_attack, rtu_attack, lambda: True)

start_node = MarkovNode(False)
substation_node = MarkovNode(False)
injected_node = MarkovNode(False)
incorrect_state_node = MarkovNode(False)
success_node = MarkovNode(True, "SUCCESS")
failure_node = MarkovNode(True, "FAILURE")
captured_node = MarkovNode(True, "CAPTURED")

start_node.add_transition(substation_node, 0.5)
start_node.add_transition(failure_node, 0.25)
start_node.add_transition(captured_node, 0.25)
substation_node.add_transition(injected_node, 0.5)
substation_node.add_transition(failure_node, 0.25)
substation_node.add_transition(captured_node, 0.25)
injected_node.add_transition(incorrect_state_node, 0.9)
injected_node.add_transition(failure_node, 0.05)
injected_node.add_transition(captured_node, 0.05)
incorrect_state_node.add_transition(success_node, 0.85)
incorrect_state_node.add_transition(failure_node, 0.075)
incorrect_state_node.add_transition(captured_node, 0.075)

model = Markov(start_node)
markov_dist = model.calculate_output_probs()
print(markov_dist)
# 
# pladd_game.run_game()
