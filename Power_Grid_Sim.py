from PLADD.PLADD import *

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
