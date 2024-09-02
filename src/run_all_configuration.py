import subprocess


def main():
    i = 1
    for configuration in [
        "./configurations/40_agents_vers1.json",
        "./configurations/40_agents_vers2.json",
        "./configurations/40_agents_vers3.json",
        "./configurations/40_agents_vers4.json",
        "./configurations/40_agents_vers5.json",
        "./configurations/40_agents_vers6.json"
    ]:
        subprocess.call(
            [
                "python",
                "main.py",
                f"--configuration_file={configuration}",
                f"--path_to_results=./result/{i}",
                "--create_result_graph=False",
                "--create_step_images=False"
            ]
        )


if __name__ == "__main__":
    main()
