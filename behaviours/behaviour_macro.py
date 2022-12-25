from random import random

from behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour
from worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation


class MacroBehaviour(AbstractHexagonBehaviour):
    """Behavior implementing algorithm 2.
    Agents determine the center of their cluster by moving it to the target,
    move themselves parallel to the movement of the cluster center.
    """

    def __init__(
        self,
        agent_id: int,
        cluster_id: int,
        agent_location: Hexagon2DLocation,
        target_location: Hexagon2DLocation,
        walls: list,
    ):
        """Creating an instance of a class with agent id, location and target and cluster id.

        :param agent_id: agent id
        :type agent_id: int
        :param agent_location: agent start location
        :type agent_location: Hexagon2DLocation
        :param target_location: agent target location
        :type target_location: Hexagon2DLocation
        :param walls: walls on hexagon plane
        :type walls: list
        """
        super().__init__(agent_id, agent_location, target_location, walls)
        self.cluster_id = cluster_id
        self.center_cluster_location = agent_location
        self.is_synchronization = False

    def define_center_cluster_location(self, messages: dict) -> None:
        center_cluster_locations = [message[1] for _, message in messages.items() if message[0] == self.cluster_id]

        cluster_location = Hexagon2DLocation(0, 0)
        for location in center_cluster_locations:
            cluster_location += location
        cluster_location //= len(center_cluster_locations)

        self.center_cluster_location = cluster_location
        self.is_synchronization = True

    def define_cluster_area(self, messages: dict) -> None:
        pass

    def define_cluster_target(self, messages) -> None:
        pass

    def do_action(self) -> None:
        if self.is_synchronization:
            self.move()

    def get_message(self) -> list:
        return [self.cluster_id, self.center_cluster_location]

    def rec_messages(self, messages: dict) -> None:
        if not self.is_synchronization:
            self.define_center_cluster_location(messages)
        self.update_next_move()

    def move(self) -> None:
        self.agent_location += self.next_move
        self.center_cluster_location += self.center_cluster_location.compute_move(self.target_location)

    def update_next_move(self):
        self.next_move = self.agent_location.compute_move(
            self.target_location - self.center_cluster_location + self.agent_location
        )
        if self.walls.count(self.next_move + self.agent_location) > 0:
            self.correct_next_move()

    def correct_next_move(self) -> None:
        possible_moves = [
            move
            for move in self.agent_location.get_possible_moves()
            if self.walls.count(self.agent_location + move) == 0
            and self.agent_location + move != self.previous_location
        ]

        self.next_move *= -1
        for move in possible_moves:
            if self.target_location.get_distance(
                self.agent_location + self.next_move
            ) > self.target_location.get_distance(self.agent_location + move):
                self.next_move = move
            elif self.target_location.get_distance(
                self.agent_location + self.next_move
            ) == self.target_location.get_distance(self.agent_location + move):
                random_number = random()
                if random_number > 0.5:
                    self.next_move = move
