class Component:
    """
    Represents a mostly self-contained portion of a game.
    """

    def advance_timestep(self):
        """
        Moves this component forward one timestep
        """
        pass

class Strategy:
    """
    Specifies how an agent makes choices for some component.

    Each component should subclass Strategy, adding a method for each type of choice the agent may need to make about the component. Specific strategies should be subclasses of the component strategy.
    """

    def __init__(self, agent, component):
        """
        args:
            agent: The agent which executes the strategy
            component: The component which the strategy involves
        """
        self.agent  = agent
        self.component = component


class Agent:
    """
    A person who makes game decisions.
    """

    def __init__(self, components, globals):
        """
        args:
            components: the complete list of game components
            globals: the dict of global game variables
        """
        self.components = components
        self.globals = globals
        self.init_strategies()

    def init_strategies(self):
        """
        Sets the strategies this agent uses for all components.

        This should be overridden by game-specific subclasses.
        """
        pass

class Log:
    """
    Logs important information over the course of the game for analysis.

    The log is split into timeless_vars, which contains variables that are updated over the course of the game and timed_vars, which contains variables that correspond to a specific timestep.

    args:
        timeless_init: the initialization of timeless_vars
        timed_init: the initialization of each timestep of timed_vars
    """
    def __init__(self, timeless_init, timed_init):
        self.timeless_vars = timeless_init
        self.timed_init = timed_init
        self.timed_vars = []
        self.advance_timestep()

    """
    Moves the log forward one timestep.
    """
    def advance_timestep(self):
        self.timed_vars.append(self.timed_init.copy())
        self.current_time_vars = self.timed_vars[-1]

class Game:
    """
    A game that takes plave over time.
    """

    def __init__(self, maximum_time, timesteps_per_unit):
        """
        args:
            maximum_time: the time limit on the game
            timesteps_per_unit: how many timesteps to run per unit time
        """
        self.maximum_timesteps = maximum_time
        self.timesteps_per_unit = timesteps_per_unit

        self.log = self.init_log()
        self.components = self.init_components()
        self.attacker = self.init_attacker()
        self.defender = self.init_defender()
        self.init_globals()

    def run_game(self):
        """
        Run a complete game.
        """
        while(not self.is_game_finished()):
            for component in self.component:
                component.advance_timestep()
            self.log.advance_timestep()

    def init_log(self):
        """
        initialize the game log.
        """
        return Log({}, {})

    def init_components(self):
        """
        initialize the game components.
        """
        pass

    def init_attacker(self):
        """
        initialize the attacker
        """
        pass

    def init_defender(self):
        """
        initialize the defender.
        """
        pass

    def init_globals(self):
        """
        initialize the global game variables.
        """
        pass

    def is_game_finished(self):
        """
        Checks whether the game is in a final state.
        """
        pass
