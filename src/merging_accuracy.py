import argparse
import json
import sys

import matplotlib
from matplotlib import pyplot as plt

matplotlib.use("Agg")


def create_parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--path_to_results", nargs="?", default="./result")

    return argument_parser


def create_accuracy_graph(path_to_results: str):
    figure = plt.figure(figsize=(12, 5))

    sub_plot_accuracy = figure.add_subplot(1, 2, 1)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Accuracy", fontsize="xx-large")

    for strategy in ["Micro", "Macro", "Meso"]:
        with open(path_to_results + "/" + strategy + "/result.json", "r") as file:
            result = json.load(file)
            x_value = [value for value in result["accuracy"]]

        plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    sub_plot_diameter = figure.add_subplot(1, 2, 2)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Diameter", fontsize="xx-large")

    for strategy in ["Micro", "Macro", "Meso"]:
        with open(path_to_results + "/" + strategy + "/result.json", "r") as file:
            result = json.load(file)
            x_value = [value for value in result["diameter"]]

        plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    plt.savefig(path_to_results + f"/merged_accuracy.svg", transparent=False, facecolor="white", dpi=300)


def create_num_of_clusters_graph(path_to_results: str, strategy: str):
    figure = plt.figure(figsize=(12, 5))

    sub_plot_accuracy = figure.add_subplot(1, 2, 1)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Number of clusters", fontsize="xx-large")

    with open(path_to_results + "/result.json", "r") as file:
        result = json.load(file)
        x_value = [value for value in result["num_of_clusters"]]

    plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    sub_plot_diameter = figure.add_subplot(1, 2, 2)
    plt.xlabel("Step number", fontsize="xx-large")
    plt.ylabel("Average number of agents in cluster", fontsize="xx-large")

    with open(path_to_results + "/result.json", "r") as file:
        result = json.load(file)
        x_value = [value for value in result["avg_agents_in_cluster"]]

    plt.plot(range(len(x_value)), x_value, label=strategy)
    plt.legend(loc="upper right")

    plt.savefig(path_to_results + f"/num_of_clusters.svg", transparent=False, facecolor="white", dpi=300)


def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    print(args)

    create_accuracy_graph(path_to_results=args.path_to_results)
    # create_num_of_clusters_graph(path_to_results=args.path_to_results)


if __name__ == "__main__":
    main()
