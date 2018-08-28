import random
import math

class PLAAD:
    def __init__(self, resources, attacker, defender, total_timesteps = 10000):
        self.attacker = attacker
        self.defender = defender
        self.resources = resources
        self.total_timesteps = total_timesteps

    def run_game(self):
        for i in range(self.total_timesteps):
            self.advance_timestep()
        for resource in self.resources:
            # print(resource.compromised_log)
            print(len([x for x in resource.compromised_log if x]) / self.total_timesteps)

    def advance_timestep(self):
        for resource in self.resources:
            resource.resolve_attacks()
        self.defender.take_actions()
        self.attacker.take_actions()
        for resource in self.resources:
            resource.log_status()

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
        self.compromised_log = []
        # keeps track of whether this resource was compromised at each timestep

    def resolve_attacks(self):
        # checks whether any ongoing attacks succeed
        if self.attack and self.attack.attack_succeeded():
            self.compromised = True
            self.information_gained = True
            self.attack = None

    def start_attack(self):
        # the attacker starts to attack this resource
        if self.information_gained:
            self.attack = self.learned_attack()
        else:
            self.attack = self.base_attack()

    def defender_take(self):
        # the defender makes the take move
        self.compromised = False

    def defender_morph(self):
        #the defender makes the morph move
        self.attack = None
        self.information_gained = False
        self.compromised = False

    def log_status(self):
        self.compromised_log.append(self.compromised)

class ExponentialAttack:
    # An attack whose underlying probability distribution is an exponential distribution
    def __init__(self, rate, timesteps_per_time):
        self.rate = rate
        # the rate of success per unit time
        self.timesteps_per_time = timesteps_per_time
        # the number of timesteps per unit time

    def attack_succeeded(self):
        # checks whether the attack succeeded in the previous timestep and advances one timestep
        return random.random() < self.rate / self.timesteps_per_time

class GreedyAttacker:
    def __init__(self, resources):
        self.resources = resources

    def take_actions(self):
        for resource in self.resources:
            if not resource.compromised and not resource.attack:
                resource.start_attack()

class PeriodicDefender:
    def __init__(self, resources, periods, timesteps_per_unit):
        self.resources = resources
        self.periods = periods
        # periods[i] contains the time in units between successive take moves this defender makes on resources[i]
        self.timesteps_per_unit = timesteps_per_unit
        # the number of timesteps that are run per unit time
        self.current_timestep = 0
        # the number of timesteps since the statrt of the game

    def take_actions(self):
        for i in range(len(self.resources)):
            if math.floor(self.current_timestep / self.timesteps_per_unit / self.periods[i]) < math.floor((self.current_timestep + 1) / self.timesteps_per_unit / self.periods[i]) :
                # we have reached the end of a period
                self.resources[i].defender_take()
        self.current_timestep += 1
