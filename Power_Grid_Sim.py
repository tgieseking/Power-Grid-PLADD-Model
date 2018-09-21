from PLADD.PLADD import *
from PLADD.Markov import *

node_0 = MarkovNode(False)
node_1 = MarkovNode(False)
node_2 = MarkovNode(False)
node_3 = MarkovNode(True, "3:")
node_4 = MarkovNode(True, "4:")
node_0.add_transition(node_1, 0.4)
node_0.add_transition(node_2, 0.6)
node_1.add_transition(node_2, 0.2)
node_1.add_transition(node_3, 0.8)
node_2.add_transition(node_3, 0.3)
node_2.add_transition(node_4, 0.7)
model = Markov(node_0)
print(model.calculate_output_probs())

timesteps_per_unit = 100
base_attack = lambda: ExponentialAttack(0.3, timesteps_per_unit)
learned_attack = lambda: ExponentialAttack(0.6, timesteps_per_unit)
resource_0 = Resource(base_attack, learned_attack, lambda: True)
resource_1 = Resource(base_attack, learned_attack, lambda: True)
resource_2 = Resource(base_attack, learned_attack, lambda: True)
resource_3 = Resource(base_attack, learned_attack, lambda: attackable_helper([[resource_0, resource_1], [resource_2]]))
resources = [resource_0, resource_1, resource_2, resource_3]
attacker = GreedyAttacker(resources, 1, 1, timesteps_per_unit)
defender = PeriodicDefender(resources, 1, 1, timesteps_per_unit, [1, 1, 3, 10])
pladd_game = PLADD(resources, attacker, defender)
pladd_game.run_game()
