import os

import imageio
from PIL import Image

from agents.simple_agent import SimpleAgent
from behaviours.behaviour_3 import Behaviour3
from behaviours.behaviour_meso import MesoBehaviour
from behaviours.behaviour_macro import MacroBehaviour
from behaviours.behaviour_micro import MicroBehaviour
from worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation
from worlds.hexagon_2D.hexagon_2D_world import Hexagon2DWorld


def setup_for_10_agents() -> None:
    """10 agents, 2 clusters, 50 steps, world 24*24."""
    num_steps = 70
    target = Hexagon2DLocation(12, 4)
    target_clusters = [Hexagon2DLocation(15, 4), Hexagon2DLocation(11, 4)]

    agent_cluster_indexes = [1, 1, 1, 1, 2, 2, 2, 2, 2, 2]

    agents_locations = [
        Hexagon2DLocation(18, 21),
        Hexagon2DLocation(20, 23),
        Hexagon2DLocation(18, 22),
        Hexagon2DLocation(21, 21),

        Hexagon2DLocation(4, 21),
        Hexagon2DLocation(3, 22),
        Hexagon2DLocation(4, 18),
        Hexagon2DLocation(5, 20),
        Hexagon2DLocation(6, 19),
        Hexagon2DLocation(3, 23)
    ]

    cluster_radius = 5

    walls = [
        Hexagon2DLocation(14, 15),
        Hexagon2DLocation(15, 15),
        Hexagon2DLocation(16, 16),
        Hexagon2DLocation(17, 16),
        Hexagon2DLocation(18, 17),
        Hexagon2DLocation(19, 17),
        Hexagon2DLocation(20, 17),
        Hexagon2DLocation(21, 16),

        Hexagon2DLocation(3, 16),
        Hexagon2DLocation(4, 17),
        Hexagon2DLocation(5, 16),
        Hexagon2DLocation(6, 16),
        Hexagon2DLocation(7, 15),
        Hexagon2DLocation(8, 15),
        Hexagon2DLocation(9, 14),
        Hexagon2DLocation(10, 14)
    ]

    agents = []
    for index in range(10):
        behaviour = MicroBehaviour(index, agents_locations[index], target, walls)
        agents.append(SimpleAgent(index, 0, behaviour))
        """behaviour = MacroBehaviour(index, 0, agents_locations[index], target, [])
        agents.append(SimpleAgent(index, 0, behaviour))"""
        """if index < 4:
            path = ["l", "l", "l", "l", "ld", "l", "l", "l", "l", "ld", "l", "l",
                    "l", "l", "ld", "l", "l", "l", "ld"]
        else:
            path = ["l", "lu", "l", "l", "lu", "l", "lu", "l", "l", "lu", "l", "l",
                    "lu", "l", "l", "lu", "l", "l", "lu"]
        behaviour = Behaviour3(
            index, agent_cluster_indexes[index], agents_locations[index], target,
            target_clusters[agent_cluster_indexes[index] - 1], path, []
        )
        agents.append(SimpleAgent(index, agent_cluster_indexes[index], behaviour))"""
        """behaviour = Behaviour3New(
            index, agents_locations[index], cluster_radius, target, walls
        )
        agents.append(SimpleAgent(index, 0, behaviour))"""

    world = Hexagon2DWorld(24, agents, num_steps, [])
    world.start()

    frames = [Image.open(f"./result/img/img_{step}.png") for step in range(num_steps)]
    imageio.mimsave("result/simulation_10agents.gif", frames, fps=2)
    os.system("result\\simulation_10agents.gif")


def setup_for_40_agents() -> None:
    """40 agents, 3 clusters, 100 steps, world 100*100."""
    num_steps = 160
    target = Hexagon2DLocation(54, 10)
    target_clusters = [Hexagon2DLocation(54, 13), Hexagon2DLocation(50, 6), Hexagon2DLocation(46, 13)]

    agent_cluster_indexes = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                             3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

    cluster_radius = 5

    """agents_locations = [
        Hexagon2DLocation(70, 83),
        Hexagon2DLocation(71, 85),
        Hexagon2DLocation(70, 82),
        Hexagon2DLocation(69, 81),
        Hexagon2DLocation(70, 79),
        Hexagon2DLocation(73, 83),
        Hexagon2DLocation(75, 85),
        Hexagon2DLocation(72, 82),
        Hexagon2DLocation(73, 81),
        Hexagon2DLocation(74, 79),
        Hexagon2DLocation(69, 83),
        Hexagon2DLocation(67, 85),
        Hexagon2DLocation(67, 82),
        Hexagon2DLocation(69, 82),
        Hexagon2DLocation(69, 79),

        Hexagon2DLocation(50, 83),
        Hexagon2DLocation(49, 85),
        Hexagon2DLocation(50, 82),
        Hexagon2DLocation(51, 81),
        Hexagon2DLocation(50, 79),
        Hexagon2DLocation(53, 83),
        Hexagon2DLocation(52, 85),
        Hexagon2DLocation(53, 82),
        Hexagon2DLocation(52, 80),
        Hexagon2DLocation(53, 79),
        Hexagon2DLocation(45, 83),
        Hexagon2DLocation(47, 85),
        Hexagon2DLocation(45, 82),
        Hexagon2DLocation(46, 80),
        Hexagon2DLocation(45, 79),

        Hexagon2DLocation(25, 83),
        Hexagon2DLocation(25, 85),
        Hexagon2DLocation(25, 82),
        Hexagon2DLocation(23, 81),
        Hexagon2DLocation(24, 79),
        Hexagon2DLocation(23, 83),
        Hexagon2DLocation(24, 85),
        Hexagon2DLocation(26, 82),
        Hexagon2DLocation(27, 80),
        Hexagon2DLocation(26, 79),
    ]"""

    agents_locations = [
        Hexagon2DLocation(68, 77),
        Hexagon2DLocation(65, 85),
        Hexagon2DLocation(71, 83),
        Hexagon2DLocation(71, 80),
        Hexagon2DLocation(66, 79),
        Hexagon2DLocation(65, 79),
        Hexagon2DLocation(70, 83),
        Hexagon2DLocation(70, 79),
        Hexagon2DLocation(70, 82),
        Hexagon2DLocation(71, 82),
        Hexagon2DLocation(64, 77),
        Hexagon2DLocation(63, 79),
        Hexagon2DLocation(62, 80),
        Hexagon2DLocation(66, 83),
        Hexagon2DLocation(64, 76),
        Hexagon2DLocation(68, 76),
        Hexagon2DLocation(66, 82),
        Hexagon2DLocation(69, 82),
        Hexagon2DLocation(67, 79),
        Hexagon2DLocation(67, 77),

        Hexagon2DLocation(48, 82),
        Hexagon2DLocation(38, 81),
        Hexagon2DLocation(44, 82),
        Hexagon2DLocation(47, 83),
        Hexagon2DLocation(38, 84),
        Hexagon2DLocation(41, 80),
        Hexagon2DLocation(44, 84),
        Hexagon2DLocation(39, 85),
        Hexagon2DLocation(45, 79),
        Hexagon2DLocation(46, 81),
        Hexagon2DLocation(38, 80),
        Hexagon2DLocation(41, 78),
        Hexagon2DLocation(47, 79),
        Hexagon2DLocation(46, 78),
        Hexagon2DLocation(40, 85),
        Hexagon2DLocation(38, 82),
        Hexagon2DLocation(44, 79),
        Hexagon2DLocation(42, 85),
        Hexagon2DLocation(44, 78),
        Hexagon2DLocation(39, 82),
    ]

    walls = [
        Hexagon2DLocation(58, 62),
        Hexagon2DLocation(58, 63),
        Hexagon2DLocation(59, 63),
        Hexagon2DLocation(59, 64),
        Hexagon2DLocation(60, 65),
        Hexagon2DLocation(60, 66),
        Hexagon2DLocation(61, 66),
        Hexagon2DLocation(61, 67),
        Hexagon2DLocation(62, 68),
        Hexagon2DLocation(62, 69),
        Hexagon2DLocation(63, 69),
        Hexagon2DLocation(63, 70),
        Hexagon2DLocation(64, 71),
        Hexagon2DLocation(64, 72),
        Hexagon2DLocation(65, 72),
        Hexagon2DLocation(65, 73),
        Hexagon2DLocation(66, 72),
        Hexagon2DLocation(66, 71),
        Hexagon2DLocation(67, 70),
        Hexagon2DLocation(67, 69),
        Hexagon2DLocation(68, 69),
        Hexagon2DLocation(68, 68),
        Hexagon2DLocation(69, 67),
        Hexagon2DLocation(69, 66),
        # Hexagon2DLocation(70, 66),
        # Hexagon2DLocation(70, 65),
        # Hexagon2DLocation(71, 64),
        # Hexagon2DLocation(71, 63),
        # Hexagon2DLocation(72, 63),
        # Hexagon2DLocation(72, 62),

        # Hexagon2DLocation(38, 62),
        # Hexagon2DLocation(38, 63),
        # Hexagon2DLocation(39, 63),
        # Hexagon2DLocation(39, 64),
        # Hexagon2DLocation(40, 65),
        # Hexagon2DLocation(40, 66),
        Hexagon2DLocation(41, 66),
        Hexagon2DLocation(41, 67),
        Hexagon2DLocation(42, 68),
        Hexagon2DLocation(42, 69),
        Hexagon2DLocation(43, 69),
        Hexagon2DLocation(43, 70),
        Hexagon2DLocation(44, 71),
        Hexagon2DLocation(44, 72),
        Hexagon2DLocation(45, 72),
        Hexagon2DLocation(45, 73),
        Hexagon2DLocation(46, 72),
        Hexagon2DLocation(46, 71),
        Hexagon2DLocation(47, 70),
        Hexagon2DLocation(47, 69),
        Hexagon2DLocation(48, 69),
        Hexagon2DLocation(48, 68),
        Hexagon2DLocation(49, 67),
        Hexagon2DLocation(49, 66),
        Hexagon2DLocation(50, 66),
        Hexagon2DLocation(50, 65),
        Hexagon2DLocation(51, 64),
        Hexagon2DLocation(51, 63),
        Hexagon2DLocation(52, 63),
        Hexagon2DLocation(52, 62),
    ]

    agents = []
    for index in range(40):
        """behaviour = MicroBehaviour(index, agents_locations[index], target, walls)
        agents.append(SimpleAgent(index, 0, behaviour))"""
        """behaviour = Behaviour2(index, 0, agents_locations[index], target)
        agents.append(SimpleAgent(index, 0, behaviour))"""
        """if index < 15:
            path = ["l", "l", "l", "l", "ld", "l", "l", "l", "l", "ld", "l", "l",
                    "l", "l", "ld", "l", "l", "l", "l", "ld", "l", "l", "l", "l",
                    "ld", "l", "l", "l", "l", "ld", "l", "l", "l", "ld", "l", "l",
                    "l", "l", "ld", "l", "l", "l", "l", "ld", "l", "l", "l", "l",
                    "l", "l", "ld", "l", "l", "l", "l", "ld", "l", "l", "l", "l",
                    "ld", "l", "l", "l", "l", "ld", "l", "l", "l", "l", "ld", "l",
                    "l", "ld", "l", "ld", "l"]
        elif index < 30:
            path = ["l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l",
                    "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l",
                    "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l",
                    "l", "l", "l", "l", "l", "lu", "l", "l", "l", "l", "l", "l",
                    "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l",
                    "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l", "l",
                    "l", "l", "l", "l"]
        else:
            path = ["l", "l", "l", "lu", "l", "l", "l", "lu", "l", "l", "l", "lu",
                    "l", "l", "l", "lu", "l", "l", "l", "lu", "l", "l", "l", "lu",
                    "l", "l", "l", "lu", "l", "l", "l", "lu", "l", "l", "l", "lu",
                    "l", "l", "l", "lu", "l", "l", "l", "lu", "l", "l", "l", "lu",
                    "l", "l", "l", "lu", "l", "l", "l", "lu", "l", "l", "l", "lu",
                    "l", "l", "l", "lu", "l", "l", "l", "lu", "l", "l", "l", "lu",
                    "lu", "l", "lu", "l", "lu", "l", "lu"]
        behaviour = Behaviour3(
            index, agent_cluster_indexes[index], agents_locations[index], target,
            target_clusters[agent_cluster_indexes[index] - 1], path
        )
        agents.append(SimpleAgent(index, agent_cluster_indexes[index], behaviour))"""
        behaviour = MesoBehaviour(
            index, agents_locations[index], cluster_radius, target, walls
        )
        agents.append(SimpleAgent(index, 0, behaviour))

    world = Hexagon2DWorld(100, agents, num_steps, walls)
    world.start()

    frames = [Image.open(f"./result/img/img_{step}.png") for step in range(num_steps)]
    imageio.mimsave("result/simulation_40agents.gif", frames, fps=2)
    os.system("result\\simulation_40agents.gif")


if __name__ == "__main__":
    setup_for_10_agents()
    # setup_for_40_agents()
