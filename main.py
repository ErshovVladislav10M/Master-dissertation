import argparse
import sys
import imageio

from matplotlib import pyplot as plt

from agents.simple_agent import SimpleAgent
from behaviours.behaviour_macro import MacroBehaviour
from behaviours.behaviour_meso import MesoBehaviour
from behaviours.behaviour_micro import MicroBehaviour
from worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation
from worlds.hexagon_2D.hexagon_2D_world import Hexagon2DWorld

import matplotlib
matplotlib.use("Agg")

num_of_tiles_side: int
num_of_steps: int
agents = []
agent_strategy = ""
target: Hexagon2DLocation
walls = []


def create_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--configuration_file", nargs="?", default="./configurations/test_configuration")
    argument_parser.add_argument("--path_to_results", nargs="?", default="./result")
    argument_parser.add_argument("--create_result_graph", nargs="?", default="True")
    argument_parser.add_argument("--create_step_images", nargs="?", default="True")
    argument_parser.add_argument("--create_gif", nargs="?", default="True")
    argument_parser.add_argument("--gif_duration", nargs="?", default="4")

    return argument_parser


def parse_configuration(configuration_file) -> None:
    try:
        agent_locations = []

        with open(configuration_file, "r") as file:
            for line in file.readlines():
                if line.__contains__("num_of_tiles:"):
                    global num_of_tiles_side
                    num_of_tiles_side = int(line.split(":")[1])
                elif line.__contains__("num_of_steps:"):
                    global num_of_steps
                    num_of_steps = int(line.split(":")[1])
                elif line.__contains__("agent_locations:"):
                    for agent in line.split(":")[1].split(";"):
                        agent = agent.replace("(", "")
                        agent = agent.replace(")", "")
                        row, column = agent.split(",")
                        agent_locations.append(
                            Hexagon2DLocation(int(row), int(column))
                        )
                elif line.__contains__("target_location:"):
                    target_location = line.split(":")[1]
                    target_location = target_location.replace("(", "")
                    target_location = target_location.replace(")", "")
                    row, column = target_location.split(",")
                    global target
                    target = Hexagon2DLocation(int(row), int(column))
                elif line.__contains__("type_of_strategy:"):
                    global agent_strategy
                    agent_strategy = line.split(":")[1]
                elif line.__contains__("wall_locations:"):
                    global walls
                    for wall in line.split(":")[1].split(";"):
                        wall = wall.replace("(", "")
                        wall = wall.replace(")", "")
                        row, column = wall.split(",")
                        walls.append(Hexagon2DLocation(int(row), int(column)))

        create_agents(agent_locations)
    except Exception:
        print(Exception)


def create_agents(agent_locations: []) -> None:
    global agents, target, agent_strategy
    if agent_strategy == "Micro\n":
        for index, agent_location in zip(
                range(len(agent_locations)), agent_locations
        ):
            behaviour = MicroBehaviour(
                agent_id=index,
                agent_location=agent_location,
                target_location=target,
                walls=walls,
            )
            agents.append(
                SimpleAgent(agent_id=index, cluster_id=0, behaviour=behaviour)
            )
    elif agent_strategy == "Macro\n":
        for index, agent_location in zip(
                range(len(agent_locations)), agent_locations
        ):
            behaviour = MacroBehaviour(
                agent_id=index,
                cluster_id=0,
                agent_location=agent_location,
                target_location=target,
                walls=[],
            )
            agents.append(
                SimpleAgent(agent_id=index, cluster_id=0, behaviour=behaviour)
            )
    elif agent_strategy == "Meso\n":
        for index, agent_location in zip(
                range(len(agent_locations)), agent_locations
        ):
            behaviour = MesoBehaviour(
                agent_id=index,
                agent_location=agent_location,
                cluster_radius=5,
                target_location=target,
                walls=walls,
            )
            agents.append(
                SimpleAgent(agent_id=index, cluster_id=0, behaviour=behaviour)
            )
    else:
        raise ValueError("Incorrect agent strategy")


def create_gif(path_to_results: str, gif_duration: str) -> None:
    images = []
    for index in range(num_of_steps):
        images.append(imageio.v2.imread(path_to_results + f"/img/img_{index}.png"))
    imageio.mimsave(path_to_results + "/result.gif", images, duration=int(gif_duration))


def create_result_graph(path_to_results: str):
    figure = plt.figure(figsize=(12, 5))

    sub_plot_accuracy = figure.add_subplot(1, 2, 1)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Accuracy", fontsize="xx-large")

    x_value = []
    with open(path_to_results + "/accuracy.txt", "r") as file:
        for value in file.read().replace("[", "").replace("]", "").replace(" ", "").split(","):
            x_value.append(int(value))

    plt.plot(range(len(x_value)), x_value, label=agent_strategy)
    plt.legend(loc="upper right")

    sub_plot_diameter = figure.add_subplot(1, 2, 2)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Diameter", fontsize="xx-large")

    x_value = []
    with open(path_to_results + "/diameter.txt", "r") as file:
        for value in file.read().replace("[", "").replace("]", "").replace(" ", "").split(","):
            x_value.append(int(value))

    plt.plot(range(len(x_value)), x_value, label=agent_strategy)
    plt.legend(loc="upper right")

    plt.savefig(path_to_results + f"/result_graph.png", transparent=False, facecolor="white", dpi=300)


if __name__ == "__main__":
    parser = create_parser()
    args: argparse.Namespace = parser.parse_args(sys.argv[1:])

    print(args)

    parse_configuration(args.configuration_file)

    simulation_world = Hexagon2DWorld(
        num_of_tiles_side=num_of_tiles_side,
        agents=agents,
        num_steps=num_of_steps,
        walls=walls,
        path_to_results=args.path_to_results,
        create_step_images=args.create_step_images
    )
    simulation_world.start()

    simulation_world.join()

    if bool(args.create_gif):
        if bool(args.create_step_images):
            create_gif(path_to_results=args.path_to_results, gif_duration=args.gif_duration)
        else:
            print("Can't create gif: not created step images")

    if bool(args.create_result_graph):
        create_result_graph(path_to_results=args.path_to_results)
