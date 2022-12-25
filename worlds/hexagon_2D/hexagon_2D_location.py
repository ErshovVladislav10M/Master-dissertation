from random import random

from worlds.abstract_location import AbstractLocation


class Hexagon2DLocation(AbstractLocation):
    """Location on a plane of hexagons."""

    def __init__(self, row: int, column: int):
        """Creating an instance of a class by row and column.

        :param row: row in plane of hexagons
        :type row: int
        :param column: column in plane of hexagons
        :type column: int
        """
        self.row = row
        self.column = column

    def compute_move(self, target_location):
        if self.row == target_location.row and self.column == target_location.column:
            return Hexagon2DLocation(0, 0)
        elif (
            abs(self.row - target_location.row) < abs(self.column - target_location.column)
            and self.column > target_location.column
        ):
            return Hexagon2DLocation(0, -1)
        elif (
            abs(self.row - target_location.row) < abs(self.column - target_location.column)
            and self.column < target_location.column
        ):
            return Hexagon2DLocation(0, 1)
        elif self.row > target_location.row and self.column == target_location.column:
            return Hexagon2DLocation(-1, 0)
        elif self.row < target_location.row and self.column == target_location.column:
            return Hexagon2DLocation(1, 0)
        elif self.row % 2 == 0:
            if self.row < target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(1, 0)
            elif self.row > target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(-1, 0)
            elif self.row > target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(-1, -1)
            elif self.row < target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(1, -1)
        elif self.row % 2 == 1:
            if self.row < target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(1, 1)
            elif self.row > target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(-1, 1)
            elif self.row > target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(-1, 0)
            elif self.row < target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(1, 0)

        return Hexagon2DLocation(0, 0)

    def compute_proportional_move(self, target_location):
        """Compute proportional of movement relative to own and target location.

        :param target_location: target location
        :return: new location for moving towards the target
        """
        steps = self.get_steps(target_location)
        steps_horizontal = [step for step in steps if step.row == 0]

        random_number = random()
        if len(steps) == 0 or float(len(steps_horizontal)) / len(steps) < random_number:
            return self.compute_vertical_move(target_location)
        else:
            return self.compute_horizontal_move(target_location)

    def compute_horizontal_move(self, target_location):
        """Compute horizontal (change only column) of movement relative to own and target location.

        :param target_location: target location
        :return: new location for moving towards the target
        """
        if self.column > target_location.column:
            return Hexagon2DLocation(0, -1)
        elif self.column < target_location.column:
            return Hexagon2DLocation(0, 1)

        return Hexagon2DLocation(0, 0)

    def compute_vertical_move(self, target_location):
        """Compute vertical of movement relative to own and target location.

        :param target_location: target location
        :return: new location for moving towards the target
        """
        if self.row > target_location.row and self.column == target_location.column:
            return Hexagon2DLocation(-1, 0)
        elif self.row < target_location.row and self.column == target_location.column:
            return Hexagon2DLocation(1, 0)
        elif self.row % 2 == 0:
            if self.row < target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(1, 0)
            elif self.row > target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(-1, 0)
            elif self.row > target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(-1, -1)
            elif self.row < target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(1, -1)
        elif self.row % 2 == 1:
            if self.row < target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(1, 1)
            elif self.row > target_location.row and self.column < target_location.column:
                return Hexagon2DLocation(-1, 1)
            elif self.row > target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(-1, 0)
            elif self.row < target_location.row and self.column > target_location.column:
                return Hexagon2DLocation(1, 0)

        return Hexagon2DLocation(0, 0)

    def get_distance(self, other) -> int:
        distance = 0
        location = Hexagon2DLocation(self.row, self.column)
        while location != other:
            location += location.compute_move(other)
            distance += 1

        return distance

    def get_random_move(self):
        random_number = random()
        if random_number < 1.0 / 6:
            return Hexagon2DLocation(0, -1)
        if random_number < 2.0 / 6:
            return Hexagon2DLocation(1, -((1 + self.row) % 2))
        if random_number < 3.0 / 6:
            return Hexagon2DLocation(1, self.row % 2)
        if random_number < 4.0 / 6:
            return Hexagon2DLocation(0, 1)
        if random_number < 5.0 / 6:
            return Hexagon2DLocation(-1, self.row % 2)
        if random_number <= 1:
            return Hexagon2DLocation(-1, -((1 + self.row) % 2))

    def get_move(self, direction: str):
        """Get move in direction relative to self for neighboring location.

        :param direction: direction relative to self
        :type direction: str
        :return: move in direction relative to self for neighboring location
        """
        if direction == "l":
            return Hexagon2DLocation(0, -1)
        if direction == "lu":
            return Hexagon2DLocation(1, -((1 + self.row) % 2))
        if direction == "ru":
            return Hexagon2DLocation(1, self.row % 2)
        if direction == "r":
            return Hexagon2DLocation(0, 1)
        if direction == "rd":
            return Hexagon2DLocation(-1, -self.row % 2)
        if direction == "ld":
            return Hexagon2DLocation(-1, -((1 + self.row) % 2))
        return Hexagon2DLocation(0, 0)

    def get_steps(self, target_location) -> list:
        """Get steps (list of moves) to achieve the target.

        :param target_location: target location
        :return: steps (list of moves) to achieve the target
        """
        steps = []
        location = Hexagon2DLocation(self.row, self.column)
        while location != target_location:
            move = location.compute_move(target_location)
            location += move
            steps.append(move)

        return steps

    def get_possible_moves(self) -> list:
        return [
            Hexagon2DLocation(0, -1),
            Hexagon2DLocation(1, -((1 + self.row) % 2)),
            Hexagon2DLocation(1, self.row % 2),
            Hexagon2DLocation(0, 1),
            Hexagon2DLocation(-1, self.row % 2),
            Hexagon2DLocation(-1, -((1 + self.row) % 2)),
        ]

    def __eq__(self, other) -> bool:
        return self.row == other.row and self.column == other.column

    def __add__(self, other):
        return Hexagon2DLocation(self.row + other.row, self.column + other.column)

    def __sub__(self, other):
        return Hexagon2DLocation(self.row - other.row, self.column - other.column)

    def __floordiv__(self, num: int):
        return Hexagon2DLocation(self.row // num, self.column // num)

    def __mul__(self, num: int):
        return Hexagon2DLocation(self.row * num, self.column * num)
