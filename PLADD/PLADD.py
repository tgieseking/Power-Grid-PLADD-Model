import random
import math

class PLADD:
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
        print("attacker cost:", self.attacker.calculate_total_cost())
        print("defender cost:", self.defender.calculate_total_cost())

    def advance_timestep(self):
        for resource in self.resources:
            resource.resolve_attacks()
        self.defender.take_actions()
        for resource in self.resources:
            resource.cancel_if_unattackable()
        self.attacker.take_actions()
        for resource in self.resources:
            resource.log_status()

class Resource:
    def __init__(self, base_attack, learned_attack, attackable):
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
        self.attackable = attackable
        # a function that says whether the attacker can attack this resource

    def resolve_attacks(self):
        # checks whether any ongoing attacks succeed
        if self.attack and self.attack.attack_succeeded():
            self.compromised = True
            self.information_gained = True
            self.attack = None

    def cancel_if_unattackable(self):
        # Cancels ongoing attacks on this resource if it is not cancel_if_unattackable
        if not self.attackable():
            self.attack = None

    def start_attack(self):
        # the attacker starts to attack this resource
        if not self.attackable():
            raise ImpossibleAttackError()

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

def attackable_helper(resource_list_list):
    # used to express arbitrary boolean expressions on whether resources are compromised
    # given a list of list of resources [[r11, ..., r1m], ..., [rN1, ..., rNn]] returns (r11 and ... and r1m) or ... or (rN1 and .. and rNn)
    return any([all([resource.compromised for resource in resource_list]) for resource_list in resource_list_list])

class ExponentialAttack:
    # An attack whose underlying probability distribution is an exponential distribution
    def __init__(self, rate, timesteps_per_unit):
        self.rate = rate
        # the rate of success per unit time
        self.timesteps_per_unit = timesteps_per_unit
        # the number of timesteps per unit time

    def attack_succeeded(self):
        # checks whether the attack succeeded in the previous timestep and advances one timestep
        return random.random() < self.rate / self.timesteps_per_unit

class Attacker:
    def __init__(self, resources, fixed_attack_cost, ongoing_attack_cost, timesteps_per_unit):
        self.resources = resources
        self.fixed_attack_cost = fixed_attack_cost
        # the cost to start an attack
        self.ongoing_attack_cost = ongoing_attack_cost
        # the cost per unit time to keep an attack going
        self.timesteps_per_unit = timesteps_per_unit
        # the number of timesteps per unit time
        self.attacks_count = 0
        # how many attacks this attacker has made
        self.attack_timesteps_count = 0
        # counts the total time of ongoing attacks

    def start_attack(self, resource):
        # attacks should always be started by calling this function
        resource.start_attack()
        self.attacks_count += 1

    def calculate_ongoing_costs(self):
        for resource in resources:
            if resource.attack:
                self.attack_timesteps_count += 1

    def calculate_total_cost(self):
        return (self.attacks_count * self.fixed_attack_cost) + (self.attack_timesteps_count * self.ongoing_attack_cost / self.timesteps_per_unit)

class GreedyAttacker(Attacker):
    def take_actions(self):
        for resource in self.resources:
            if not resource.compromised and resource.attackable() and not resource.attack:
                self.start_attack(resource)

class Defender:
    def __init__(self, resources, take_cost, morph_cost):
        self.resources = resources
        self.take_cost = take_cost
        self.morph_cost = morph_cost
        self.take_count = 0
        # how many takes the defender has made
        self.morph_count = 0
        # how many morphs the defender has made

    def take(self, resource):
        resource.defender_take()
        self.take_count += 1

    def morph(self, resource):
        resource.defender_morph()
        self.morph_count += 1

    def calculate_total_cost(self):
        return self.take_count * self.take_cost + self.morph_count + self.morph_cost


class PeriodicDefender(Defender):
    def __init__(self, resources, take_cost, morph_cost, timesteps_per_unit, periods):
        if len(resources) != len(periods):
            raise ArrayLengthMismatchError()

        super().__init__(resources, take_cost, morph_cost)
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
                self.take(self.resources[i])
        self.current_timestep += 1

class ImpossibleAttackError(Exception):
    pass

class ArrayLengthMismatchError(Exception):
    pass
