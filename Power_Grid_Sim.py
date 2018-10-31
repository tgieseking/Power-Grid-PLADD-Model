from PLADD.PLADD import *
from PLADD.Markov import *
import numpy as np
from matplotlib.pyplot import plot, show, hist

# Experiment parameters
timesteps_per_unit = 100
total_time = 120
num_trials = 200

# Result data
success_times = []
failure_times = []
attacker_cost = 0
defender_cost = 0

# Initializing Markov Model
start_node = TransientNode()
substation_node = TransientNode()
injected_node = TransientNode()
incorrect_state_node = TransientNode()
success_node = AbsorbingNode("SUCCESS")
failure_node = AbsorbingNode("FAILURE")
captured_node = AbsorbingNode("CAPTURED")

start_node.set_transitions({substation_node: 0.5, failure_node: 0.25, captured_node: 0.25})
substation_node.set_transitions({injected_node: 0.5, failure_node: 0.25, captured_node: 0.25})
injected_node.set_transitions({incorrect_state_node: 0.9, failure_node: 0.05, captured_node: 0.05})
incorrect_state_node.set_transitions({success_node: 0.85, failure_node: 0.075, captured_node: 0.075})

# To save time, we precalculate the Markov model result distribution
model = Markov([start_node, substation_node, injected_node, incorrect_state_node], [success_node, failure_node, captured_node], start_node)
markov_dist = model.calculate_output_probs()
print(markov_dist)

for run in range(num_trials):
    #initialize the PLADD model
    grid_data_attack = lambda: ExponentialAttack(0.5, timesteps_per_unit)
    grid_data = Resource(grid_data_attack, grid_data_attack, lambda: True, 10, 10, 10, 1000, timesteps_per_unit)

    vulerability_report_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
    vulerability_report = Resource(vulerability_report_attack, vulerability_report_attack, lambda: True, 10, 5, 5, 20, timesteps_per_unit)

    ip_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
    ip = Resource(ip_attack, ip_attack, lambda: True, 10, 5, 5, 20, timesteps_per_unit)

    rtu_attack = lambda: ExponentialAttack(0.6, timesteps_per_unit)
    rtu = Resource(rtu_attack, rtu_attack, lambda: True, 50, 0, 10, 40, timesteps_per_unit)

    resources = [grid_data, vulerability_report, ip, rtu]
    attacker = GreedyAttacker(resources)
    defender = PeriodicDefender(resources, timesteps_per_unit, [2, 2.5, 2.5, 1.667])

    pladd_game = PLADD(resources, attacker, defender, total_time*timesteps_per_unit)

    # Run the model
    for time in range(pladd_game.total_timesteps):
        pladd_game.advance_timestep()
        if all(resource.compromised for resource in pladd_game.resources):
            outcome = select_from_dist(markov_dist)
            if outcome == "SUCCESS":
                success_times.append(time / timesteps_per_unit)
                break
            elif outcome == "CAPTURED":
                failure_times.append(time / timesteps_per_unit)
                break
            elif outcome == "FAILURE":
                for resource in pladd_game.resources:
                    resource.compromised = False
    attacker_cost += attacker.calculate_total_cost()
    defender_cost += defender.calculate_total_cost()

# Summarize results
print(f"Successes: {len(success_times)}")
print(f"Failures: {len(failure_times)}")
print(f"Attacker Cost: {attacker_cost / num_trials}")
print(f"Defender Cost: {defender_cost / num_trials}")

times = np.asarray(success_times + failure_times)
print(np.average(times))
hist(times, bins=100)
show()
