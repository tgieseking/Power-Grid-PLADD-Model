import random

class Resource:
    def __init__(self, base_attack, learned_attack):
        self.compromised = False
        # whether the attacker has control of the resource
        self.information_gained = False
        # whether the attacker has previously had control of the resource and uses the learned attack distribution
        self.base_attack = base_attack
        # the initializer for a base attack object
        self.learned_attack = learned_attack
        # the initializer for a learned attack object
        self.attack = None
        # the ongoing attack object, if any

    def resolve_attacks(self):
        # checks whether any ongoing attacks succeed
        if self.attack and self.attack.attack_succeeded():
            self.compromised = True
            self.information_gained = True

    def start_attack(self):
        # the attacker starts to attack this resource
        if self.information_gained:
            self.learned_attack()
        else:
            self.base_attack()

    def defender_take(self):
        # the defender makes the take move
        self.compromised = False

    def defender_morph(self):
        #the defender makes the morph move
        self.attack = None
        self.information_gained = False
        self.compromised = False

class ExponentialAttack:
    # An attack whose underlying probability distribution is an exponential distribution
    def __init__(self, rate, timesteps_per_time):
        self.rate = rate
        # the rate of success per unit time
        self.timesteps_per_time
        # the number of timesteps per unit time

    def attack_succeeded(self):
        # checks whether the attack succeeded in the previous timestep and advances one timestep
        return random.rand() < self.rate / self.timesteps_per_time

class Attacker:
    def take_actions(self):
        pass

class Defender:
    def take_actions(self):
        pass

class PLAAD:
    def __init__(self, resources, attacker = Attacker(), defender = Defender(), total_timesteps = 10000):
        self.attacker = attacker
        self.defender = defender
        self.resources = resources
        self.total_timesteps = total_timesteps

    def run_game(self):
        for i in range(self.total_timesteps):
            self.advance_timestep()

    def advance_timestep(self):
        for resource in self.resources:
            resource.resolve_attacks()
        self.defender.take_actions()
        self.attacker.take_actions()
