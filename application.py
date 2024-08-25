import os
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
)

from agents.simple_agent import SimpleAgent
from behaviours.behaviour_macro import MacroBehaviour
from behaviours.behaviour_meso import MesoBehaviour
from behaviours.behaviour_micro import MicroBehaviour
from worlds.hexagon_2D.hexagon_2D_location import Hexagon2DLocation
from worlds.hexagon_2D.hexagon_2D_world import Hexagon2DWorld

simulation_world_file: str
simulation_world: Hexagon2DWorld
num_of_tiles_side: int
num_of_steps: int
agents = []
target: Hexagon2DLocation
agent_strategy: str
walls = []

start_window: QMainWindow
create_simulation_window: QMainWindow
load_simulation_window: QMainWindow
main_window: QMainWindow
show_window: QMainWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-agent simulation application")
        self.setFixedSize(QSize(400, 300))

        create_button = QPushButton("Create new simulation")
        create_button.setFixedSize(250, 40)
        create_button.clicked.connect(self.create_simulation)

        load_button = QPushButton("Load existing simulation")
        load_button.setFixedSize(250, 40)
        load_button.clicked.connect(self.load_simulation)

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(create_button)
        layout.addWidget(load_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    @staticmethod
    def create_simulation():
        create_simulation_window.show()
        start_window.hide()

    @staticmethod
    def load_simulation():
        load_simulation_window.show()
        start_window.hide()


class CreateSimulationWindow(QMainWindow):
    folder_path_line_edit: QLineEdit
    file_name_line_edit: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create simulation")
        self.setFixedSize(QSize(400, 300))

        self.folder_path_line_edit = QLineEdit()
        self.folder_path_line_edit.setFixedSize(250, 40)
        self.folder_path_line_edit.setPlaceholderText(
            "Enter the full path to the creation folder"
        )

        self.file_name_line_edit = QLineEdit()
        self.file_name_line_edit.setFixedSize(250, 40)
        self.file_name_line_edit.setPlaceholderText("Enter the file name")

        create_button = QPushButton("Create simulation")
        create_button.setFixedSize(250, 40)
        create_button.clicked.connect(self.create_simulation)

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(self.folder_path_line_edit)
        layout.addWidget(self.file_name_line_edit)
        layout.addWidget(create_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def create_simulation(self):
        if os.path.exists(self.folder_path_line_edit.text()):
            global simulation_world_file
            simulation_world_file = os.path.join(
                self.folder_path_line_edit.text(), self.file_name_line_edit.text()
            )

            main_window.show()
            create_simulation_window.hide()
        else:
            print(self.folder_path_line_edit.text() + " does not exist")


class LoadSimulationWindow(QMainWindow):
    line_edit: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load simulation")
        self.setFixedSize(QSize(400, 300))

        self.line_edit = QLineEdit()
        self.line_edit.setFixedSize(250, 40)
        self.line_edit.setPlaceholderText(
            "Enter the full path to the simulation world file"
        )

        create_button = QPushButton("Load simulation")
        create_button.setFixedSize(250, 40)
        create_button.clicked.connect(self.load_simulation)

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(self.line_edit)
        layout.addWidget(create_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def load_simulation(self):
        if os.path.exists(self.line_edit.text()):
            global simulation_world_file
            simulation_world_file = self.line_edit.text()

            main_window.show()
            main_window.reload_options()
            load_simulation_window.hide()
        else:
            print(self.line_edit.text() + " does not exist")


class MainWindow(QMainWindow):
    size_world_line_edit: QLineEdit
    number_of_steps_line_edit: QLineEdit
    agent_locations_line_edit: QLineEdit
    target_location_line_edit: QLineEdit
    types_of_strategies_line_edit: QLineEdit
    wall_locations_line_edit: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation options")
        self.setFixedSize(QSize(800, 600))

        self.size_world_line_edit = QLineEdit()
        self.size_world_line_edit.setFixedSize(250, 40)
        self.size_world_line_edit.setPlaceholderText(
            "Enter the number of tiles of the side of the simulation world"
        )

        self.number_of_steps_line_edit = QLineEdit()
        self.number_of_steps_line_edit.setFixedSize(250, 40)
        self.number_of_steps_line_edit.setPlaceholderText(
            "Enter the number of steps of the simulation world"
        )

        self.agent_locations_line_edit = QLineEdit()
        self.agent_locations_line_edit.setFixedSize(250, 40)
        self.agent_locations_line_edit.setPlaceholderText(
            "Enter the agent locations (like: '(1, 3);(2, 6)')"
        )

        self.target_location_line_edit = QLineEdit()
        self.target_location_line_edit.setFixedSize(250, 40)
        self.target_location_line_edit.setPlaceholderText(
            "Enter the target location (like: '(1, 3)')"
        )

        self.types_of_strategies_line_edit = QLineEdit()
        self.types_of_strategies_line_edit.setFixedSize(250, 40)
        self.types_of_strategies_line_edit.setPlaceholderText(
            "Enter a strategy for agents (like: 'Micro', 'Macro', " "'Meso')"
        )

        self.wall_locations_line_edit = QLineEdit()
        self.wall_locations_line_edit.setFixedSize(250, 40)
        self.wall_locations_line_edit.setPlaceholderText(
            "Enter the walls locations (like: '(1, 3);(2, 6)')"
        )

        reload_options_button = QPushButton("Reload options")
        reload_options_button.setFixedSize(250, 40)
        reload_options_button.clicked.connect(self.reload_options)

        save_options_button = QPushButton("Save options")
        save_options_button.setFixedSize(250, 40)
        save_options_button.clicked.connect(self.save_options)

        start_simulation_button = QPushButton("Start simulation")
        start_simulation_button.setFixedSize(250, 40)
        start_simulation_button.clicked.connect(self.start_simulation)

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(self.size_world_line_edit)
        layout.addWidget(self.number_of_steps_line_edit)
        layout.addWidget(self.agent_locations_line_edit)
        layout.addWidget(self.target_location_line_edit)
        layout.addWidget(self.types_of_strategies_line_edit)
        layout.addWidget(self.wall_locations_line_edit)
        layout.addWidget(reload_options_button)
        layout.addWidget(save_options_button)
        layout.addWidget(start_simulation_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def reload_options(self):
        try:
            with open(simulation_world_file, "r") as file:
                for line in file.readlines():
                    if line.__contains__("num_of_tiles:"):
                        self.size_world_line_edit.setText(
                            line.split(":")[1].replace("\n", "")
                        )
                    elif line.__contains__("num_of_steps:"):
                        self.number_of_steps_line_edit.setText(
                            line.split(":")[1].replace("\n", "")
                        )
                    elif line.__contains__("agent_locations:"):
                        self.agent_locations_line_edit.setText(
                            line.split(":")[1].replace("\n", "")
                        )
                    elif line.__contains__("target_location:"):
                        self.target_location_line_edit.setText(
                            line.split(":")[1].replace("\n", "")
                        )
                    elif line.__contains__("type_of_strategy:"):
                        self.types_of_strategies_line_edit.setText(
                            line.split(":")[1].replace("\n", "")
                        )
                    elif line.__contains__("wall_locations:"):
                        self.wall_locations_line_edit.setText(
                            line.split(":")[1].replace("\n", "")
                        )
        except Exception:
            print(Exception)

    def save_options(self):
        try:
            with open(simulation_world_file, "w") as file:
                file.write("num_of_tiles:" + self.size_world_line_edit.text() + "\n")
                file.write(
                    "num_of_steps:" + self.number_of_steps_line_edit.text() + "\n"
                )
                file.write(
                    "agent_locations:" + self.agent_locations_line_edit.text() + "\n"
                )
                file.write(
                    "target_location:" + self.target_location_line_edit.text() + "\n"
                )
                file.write(
                    "type_of_strategy:"
                    + self.types_of_strategies_line_edit.text()
                    + "\n"
                )
                file.write(
                    "wall_locations:" + self.wall_locations_line_edit.text() + "\n"
                )
        except Exception:
            print(Exception)

    def start_simulation(self):
        try:
            agent_locations = []

            with open(simulation_world_file, "r") as file:
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

            self.create_agents(agent_locations)

            global simulation_world
            simulation_world = Hexagon2DWorld(
                num_of_tiles_side=num_of_tiles_side,
                agents=agents,
                num_steps=num_of_steps,
                walls=walls,
                path_to_results="result",
                create_step_images=True
            )
            simulation_world.start()

            show_window.show()
            main_window.hide()
        except Exception:
            print(Exception)

    @staticmethod
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
        else:
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


class ShowWindow(QMainWindow):
    image_label: QLabel
    index = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show simulation")
        self.setMinimumSize(QSize(800, 600))

        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(600, 600)
        self.image_label.setPixmap(QPixmap(f"./result/img/img_{self.index}.png"))

        next_button = QPushButton("Next step")
        next_button.setFixedSize(250, 40)
        next_button.clicked.connect(self.next_step)

        previous_button = QPushButton("Previous step")
        previous_button.setFixedSize(250, 40)
        previous_button.clicked.connect(self.previous_step)

        button_layout = QVBoxLayout()
        button_layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        button_layout.addWidget(next_button)
        button_layout.addWidget(previous_button)

        layout = QHBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def next_step(self):
        if os.path.exists(f"./result/img/img_{self.index + 1}.png"):
            self.index += 1
        else:
            print("This is last img")

        try:
            self.image_label.setPixmap(QPixmap(f"./result/img/img_{self.index}.png"))
        except Exception:
            print(Exception)

    def previous_step(self):
        if os.path.exists(f"./result/img/img_{self.index - 1}.png"):
            self.index -= 1
        else:
            print("This is first img")

        try:
            self.image_label.setPixmap(QPixmap(f"./result/img/img_{self.index}.png"))
        except Exception:
            print(Exception)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(
        "QMainWindow{background-color: white; border: 1px solid lightgray;}"
    )

    start_window = StartWindow()
    create_simulation_window = CreateSimulationWindow()
    load_simulation_window = LoadSimulationWindow()
    main_window = MainWindow()
    show_window = ShowWindow()

    start_window.show()

    sys.exit(app.exec())
