import argparse
import json
import sys
import imageio

from matplotlib import pyplot as plt

from src.agents.simple_agent import SimpleAgent
from src.behaviours.behaviour_macro import MacroBehaviour
from src.behaviours.behaviour_meso import MesoBehaviour
from src.behaviours.behaviour_micro import MicroBehaviour
from src.worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation
from src.worlds.hexagon_2D.hexagon_2D_world import Hexagon2DWorld

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
    argument_parser.add_argument("--configuration_file", nargs="?", default="./configurations/test_configuration.json")
    argument_parser.add_argument("--path_to_results", nargs="?", default="./result")
    argument_parser.add_argument("--create_result_graph", nargs="?", default="True")
    argument_parser.add_argument("--create_step_images", nargs="?", default="True")
    argument_parser.add_argument("--create_gif", nargs="?", default="True")
    argument_parser.add_argument("--gif_duration", nargs="?", default="4")

    return argument_parser


def parse_configuration(configuration_data) -> None:
    global num_of_tiles_side
    num_of_tiles_side = configuration_data["num_of_tiles"]

    global num_of_steps
    num_of_steps = configuration_data["num_of_steps"]

    global target
    target_location = configuration_data["target_location"]
    target = Hexagon2DLocation(target_location[0], target_location[1])

    global agent_strategy
    agent_strategy = configuration_data["type_of_strategy"]

    global walls
    for location in configuration_data["wall_locations"]:
        walls.append(Hexagon2DLocation(location[0], location[1]))

    agent_locations = []
    for location in configuration_data["agent_locations"]:
        agent_locations.append(Hexagon2DLocation(location[0], location[0]))
    create_agents(agent_locations)


def create_agents(agent_locations: []) -> None:
    global agents, target, agent_strategy
    if agent_strategy == "Micro":
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
    elif agent_strategy == "Macro":
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
    elif agent_strategy == "Meso":
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

    with open(args.configuration_file, "r", encoding="utf-8") as file:
        configuration_data = json.load(file)
    parse_configuration(configuration_data)

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
