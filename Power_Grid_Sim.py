from PLAAD.PLAAD import *

timesteps_per_time = 100
base_attack = lambda: ExponentialAttack(0.3, timesteps_per_time)
learned_attack = lambda: ExponentialAttack(0.6, timesteps_per_time)
plaad_game = PLAAD([Resource(base_attack, learned_attack)])
plaad_game.run_game()
