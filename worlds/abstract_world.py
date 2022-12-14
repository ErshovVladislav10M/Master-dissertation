from abc import ABC, abstractmethod


class AbstractWorld(ABC):
    """Abstract world-class."""

    def __init__(self, agents: list, num_steps: int, walls: list):
        """Creating an instance of a class with agents and number of steps.

        :param agents: agents that in this world
        :type agents: list
        :param num_steps: number of steps to simulate
        :type num_steps: int
        :param walls: walls on world
        :type walls: list
        """
        self.agents = agents
        self.num_steps = num_steps
        self.walls = walls
        self.all_messages = {}

    @abstractmethod
    def is_have_connection(self, agent1_id: int, agent2_id: int) -> bool:
        """Check connection between two agents.

        :param agent1_id: first agent id
        :type agent1_id: int
        :param agent2_id: second agent id
        :type agent2_id: int
        :return: is connection
        :rtype: bool
        """
        pass

    @abstractmethod
    def rec_messages(self) -> None:
        """Receiving messages from agents."""
        pass

    @abstractmethod
    def sent_messages(self) -> None:
        """Sent messages to agents."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Runs a simulation in this world."""
        pass
