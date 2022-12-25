from random import random

from behaviours.abstract_hexagon_behaviour import AbstractHexagonBehaviour


class MicroBehaviour(AbstractHexagonBehaviour):
    """Behavior implementing algorithm 1. The algorithm is as follows,
    each agent, independently of the others,
    linearly (as far as possible on a hexagonal plane) moves to the target.
    """

    def define_cluster_area(self, messages: dict) -> None:
        pass

    def define_cluster_target(self, messages) -> None:
        pass

    def define_center_cluster_location(self, messages: dict) -> None:
        pass

    def do_action(self) -> None:
        if self.num_penalty_step != 0:
            self.num_penalty_step -= 1
            self.is_random_move = True
        else:
            self.move()

    def get_message(self) -> None:
        return None

    def rec_messages(self, messages: dict) -> None:
        self.update_next_move()

    def move(self) -> None:
        self.agent_location += self.next_move
        self.is_random_move = False

    def update_next_move(self) -> None:
        if self.is_random_move:
            self.next_move = self.agent_location.get_random_move()
        else:
            self.next_move = self.agent_location.compute_proportional_move(self.target_location)

        if self.walls.count(self.agent_location + self.next_move) > 0:
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
