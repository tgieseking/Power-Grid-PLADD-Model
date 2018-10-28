import random
import math

class PLADD:
    def __init__(self, resources, attacker, defender, total_timesteps = 10000):
        self.attacker = attacker
        self.defender = defender
        self.resources = resources
        self.total_timesteps = total_timesteps
        self.first_compromised = None

    def run_game(self):
        for i in range(self.total_timesteps):
            self.advance_timestep()
            if (not self.first_compromised and all([resource.compromised for resource in self.resources])):
                self.first_compromised = i
        # for resource in self.resources:
        #     # print(resource.compromised_log)
        #     print(len([x for x in resource.compromised_log if x]) / self.total_timesteps)
        # print("attacker cost:", self.attacker.calculate_total_cost())
        # print("defender cost:", self.defender.calculate_total_cost())
        return [resource.compromised_log for resource in self.resources], self.first_compromised

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
    def __init__(self, base_attack, learned_attack, attackable, attacker_fixed_cost, attacker_ongoing_cost, defender_take_cost, defender_morph_cost, timesteps_per_unit):
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
        self.attacker_fixed_cost = attacker_fixed_cost
        # the fixed cost for an attacker take move
        self.attacker_ongoing_cost = attacker_ongoing_cost
        # the ongoing cost for an attacker take move
        self.defender_take_cost = defender_take_cost
        # the cost for a defender take move
        self.defender_morph_cost = defender_morph_cost
        # the cost for a defender take move
        self.attacker_take_counter = 0
        # the number of attacker takes on this resource
        self.attacker_ongoing_counter = 0
        # the number of timesteps of ongoing attacks on this resource
        self.defender_take_counter = 0
        # the number of defender takes on this resource
        self.defender_morph_counter = 0
        # the number of defender morphs on this resource
        self.timesteps_per_unit = timesteps_per_unit
        # the number of timesteps per unit time

    def resolve_attacks(self):
        # checks whether any ongoing attacks succeed
        if self.attack:
            self.attacker_ongoing_counter += 1
            if self.attack.attack_succeeded():
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
        self.attacker_take_counter += 1

    def defender_take(self):
        # the defender makes the take move
        self.compromised = False
        self.defender_take_counter += 1

    def defender_morph(self):
        #the defender makes the morph move
        self.attack = None
        self.information_gained = False
        self.compromised = False
        self.defender_morph_counter += 1

    def log_status(self):
        self.compromised_log.append(self.compromised)

    def attacker_total_cost(self):
        return (self.attacker_take_counter * self.attacker_fixed_cost) + (self.attacker_ongoing_counter * self.attacker_ongoing_cost / self.timesteps_per_unit)

    def defender_total_cost(self):
        return (self.defender_take_counter * self.defender_take_cost) + (self.defender_morph_counter * self.defender_morph_cost)

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
    def __init__(self, resources):
        self.resources = resources

    def start_attack(self, resource):
        # attacks should always be started by calling this function
        resource.start_attack()

    def calculate_total_cost(self):
        total_cost = 0
        for resource in self.resources:
            total_cost += resource.attacker_total_cost()
        return total_cost
        # return (self.attacks_count * self.fixed_attack_cost) + (self.attack_timesteps_count * self.ongoing_attack_cost / self.timesteps_per_unit)

class GreedyAttacker(Attacker):
    def take_actions(self):
        for resource in self.resources:
            if not resource.compromised and resource.attackable() and not resource.attack:
                self.start_attack(resource)

class Defender:
    def __init__(self, resources):
        self.resources = resources

    def take(self, resource):
        resource.defender_take()

    def morph(self, resource):
        resource.defender_morph()

    def calculate_total_cost(self):
        total_cost = 0
        for resource in self.resources:
            total_cost += resource.defender_total_cost()
        return total_cost


class PeriodicDefender(Defender):
    def __init__(self, resources, timesteps_per_unit, periods):
        if len(resources) != len(periods):
            raise ArrayLengthMismatchError()

        super().__init__(resources)
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
