from worlds.abstract_world import AbstractWorld
from worlds.hexagon_2D.hexagon_2D_drawer import Hexagon2DDrawer


class Hexagon2DWorld(AbstractWorld):
    """Class world for storing the location of agents on a plane, consisting of regular hexagons."""

    def __init__(self, num_of_titles_side: int, agents: list, num_steps: int, walls: list):
        """Create world by number of tiles per side.

        :param num_of_titles_side: number of tiles per side of a square
        :type num_of_titles_side: int
        :param agents: agents that in this world
        :type agents: list
        :param num_steps: number of steps to simulate
        :type num_steps: int
        :param walls: walls on world
        :type walls: list
        """
        super().__init__(agents, num_steps, walls)
        self.num_of_titles_side = num_of_titles_side
        self.drawer = Hexagon2DDrawer(num_of_titles_side, agents, walls)

    def is_have_connection(self, agent1_id: int, agent2_id: int) -> bool:
        return True

    def rec_messages(self) -> None:
        self.all_messages.update([(agent.id, agent.get_message()) for agent in self.agents])

    def sent_messages(self) -> None:
        for agent in self.agents:
            messages_for_agent = {}
            for agent_id, message in self.all_messages.items():
                if self.is_have_connection(agent.id, agent_id):
                    messages_for_agent.update({agent_id: message})
            agent.rec_messages(messages_for_agent)

    def start(self) -> None:
        for step in range(self.num_steps):
            print(step)
            #self.agent_reset()
            self.rec_messages()
            self.sent_messages()
            self.drawer.draw_plane(step)
            self.start_agent_action()

    def agent_reset(self) -> None:
        for agent in self.agents:
            agent.behaviour.cluster_id = 0
            agent.behaviour.is_cluster_definition = False
            agent.behaviour.center_cluster_location = agent.behaviour.agent_location

    def start_agent_action(self) -> None:
        required_agent_locations = self.get_required_locations()
        agents_locations = [agent.behaviour.agent_location for agent in self.agents]
        # print([(location.row, location.column) for location in required_agent_locations])
        # print([(location.row, location.column) for location in agents_locations])
        # print([agent.behaviour.num_penalty_step for agent in self.agents])
        # print([agent.behaviour.is_synchronization for agent in self.agents])
        # print([agent.behaviour.is_random_move for agent in self.agents])
        for agent, required_location in zip(self.agents, required_agent_locations):
            if required_location == agent.behaviour.agent_location:
                agent.do_action()
                continue
            elif required_agent_locations.count(required_location) > 1:
                agent.behaviour.num_penalty_step = 1
            elif agents_locations.count(required_location) > 0 or self.walls.count(required_location) > 0:
                agent.behaviour.num_penalty_step = 1

            agent.do_action()

    def get_required_locations(self) -> list:
        required_locations = []
        for agent in self.agents:
            agent_behaviour = agent.behaviour
            if agent_behaviour.num_penalty_step > 0:
                required_locations.append(agent_behaviour.agent_location)
            else:
                required_locations.append(agent_behaviour.agent_location + agent_behaviour.next_move)

        return required_locations
