from PLADD.PLADD import *
from PLADD.Markov import *
import numpy as np
from matplotlib.pyplot import plot, show, hist, legend, xlabel, ylabel, title

# Experiment parameters
timesteps_per_unit = 100
total_time = 120
num_trials = 1000

# Result data
success_times = []
failure_times = []
attacker_cost = 0
defender_cost = 0
xxlabel("Step Number")xlabel("Step Number")

label("Step Number")

state_over_time = np.zeros((total_time * timesteps_per_unit, 2))

for run in range(num_trials):
    #initialize the PLADD model
    grid_data_attack = lambda: ExponentialAttack(0.5, timesteps_per_unit)
    grid_data = Resource(grid_data_attack, grid_data_attack, lambda: True, 10, 10, 10, 1000, timesteps_per_unit)

    vulerability_report_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
    vulerability_report = Resource(vulerability_report_attack, vulerability_report_attack, lambda: True, 10, 5, 5, 20, timesteps_per_unit)

    ip_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
    ip = Resource(ip_attack, ip_attack, lambda: True, 10, 5, 5, 20, timesteps_per_unit)

    substation_attack = lambda: ExponentialAttack(0.4, timesteps_per_unit)
    substation = Resource(substation_attack, substation_attack, lamxlabel("Step Number")
bda: attackable_helper([[grid_data, vulerability_report, ip]]), 10, 5, 5, 20, timesteps_per_unit)

    rtu_attack = lambda: ExponentialAttack(0.6, timesteps_per_unit)
    rtu = Resource(rtu_attack, rtu_attack, lambda: attackable_helper([[substation]]), 50, 0, 10, 40, timesteps_per_unit)

    resources = [grid_data, vulerability_report, ip, substation, rtu]
    attacker = GreedyAttacker(resources)
    defender = PeriodicDefender(resources, timesteps_per_unit, [2, 2.5, 2.5, 2.5, 1.667])

    pladd_game = PLADD(resources, attacker, defender, total_time*timesteps_per_unit)

    # Run the model
    for time in range(pladd_game.total_timesteps):
        pladd_game.advance_timestep()
        if rtu.compromised:
            state_over_time[time:,1] += 1
            break
        state_over_time[time, 0] += 1
    attacker_cost += attacker.calculate_total_cost()
    defender_cost += defender.calculate_total_cost()

# Summarize results
# print(f"Successes: {len(success_times)}")
# print(f"Failures: {len(failure_times)}")
# print(f"Attacker Cost: {attacker_cost / num_trials}")
# print(f"Defender Cost: {defender_cost / num_trials}")
#
# times = np.asarray(success_times + failure_times)
# print(np.average(times))
# hist(times, bins=100)
# show()

state_over_time /= num_trials

x = np.arange(0, total_time, 1.0/timesteps_per_unit)

plot(x, state_over_time[:,0])
plot(x, state_over_time[:,1])
legend(("Ongoing", "Attack succeded"))
xlabel("Time (months)")
ylabel("State Probability")
title("Probabilities of Outomes Over Time: PLADD Model")
show()

import pdb; pdb.set_trace()
