class Component:
    def advance_timestep(self):
        pass


class Agent:
    def __init__(self, components, globals):
        self.components = components
        self.globals = globals
        self.init_strategies()

    def init_strategies(self):
        pass

class Log:
    def __init__(self, timeless_init, timed_init):
        self.timeless_vars = timeless_init
        self.timed_init = timed_init
        self.timed_vars = []
        self.advance_timestep()

    def advance_timestep(self):
        self.timed_vars.append(self.timed_init.copy())
        self.current_time_vars = self.timed_vars[-1]

class Game:
    def __init__(self, maximum_timesteps, timesteps_per_unit):
        self.maximum_timesteps = maximum_timesteps
        self.timesteps_per_unit = timesteps_per_unit
        self.log = self.init_log()

        self.components = self.init_components()
        self.attacker = self.init_attacker()
        self.defender = self.init_defender()
        self.init_globals()

    def run_game(self):
        while(not self.is_game_finished()):
            for component in self.component:
                component.advance_timestep()
            self.log.advance_timestep()

    def init_log(self):
        pass

    def init_components(self):
        pass

    def init_attacker(self):
        pass

    def init_defender(self):
        pass

    def init_globals(self):
        pass

    def is_game_finished(self):
        pass
