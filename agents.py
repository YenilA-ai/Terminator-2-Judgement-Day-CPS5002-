
from environment import Environment


class Agent:
    def __init__(self, name, environment, position, health=100, energy=100):
        self.name = name
        self.environment = environment
        self.position = position
        self.health = health
        self.energy = energy
        self.state = "idle"

        if not self.environment.place_agent(self.name, self.position):
            raise ValueError(f"Invalid starting position for {self.name}")

    def move(self, new_position):
        if self.energy <= 0:
            self.state = "exhausted"
            return False

        if self.environment.move_agent(self.name, new_position):
            self.position = new_position
            self.energy -= 1
            return True

        return False


class HumanAgent(Agent):
    def __init__(self, name, environment, position):
        super().__init__(name, environment, position)
        self.detection_range = 6
        self.detected_threats = []

    def perceive(self):
        self.detected_threats = []

        for name, position in self.environment.agent_positions.items():
            if name == "T-1000":
                distance = (
                    abs(self.position[0] - position[0])
                    + abs(self.position[1] - position[1])
                )

                if distance <= self.detection_range:
                    self.detected_threats.append((name, position))

        return self.detected_threats


class JohnConnor(HumanAgent):
    def __init__(self, environment, position):
        super().__init__("John Connor", environment, position)
        self.successful_evasions = 0
        self.safe_zone_reached = False

    def find_safe_zone(self, position):
        if not self.environment.safe_zones:
            return None

        return min(
            self.environment.safe_zones,
            key=lambda safe: (
                abs(position[0] - safe[0])
                + abs(position[1] - safe[1])
            )
        )

    def decide_action(self):
        neighbours = self.environment.get_neighbours(self.position)

        occupied_positions = set(
            self.environment.agent_positions.values()
        )

        available_moves = [
            position
            for position in neighbours
            if position not in occupied_positions
        ]

        if not available_moves:
            self.state = "blocked"
            return None

        threats = self.perceive()

        if threats:
            self.state = "evading"

            threat_position = threats[0][1]
            safe_zone = self.find_safe_zone(self.position)

            best_move = max(
                available_moves,
                key=lambda position: (
                    2 * (
                        abs(position[0] - threat_position[0])
                        + abs(position[1] - threat_position[1])
                    )
                    - (
                        abs(position[0] - safe_zone[0])
                        + abs(position[1] - safe_zone[1])
                        if safe_zone else 0
                    )
                )
            )

            return best_move

        self.state = "moving_to_safety"

        safe_zone = self.find_safe_zone(self.position)

        if safe_zone is None:
            self.state = "exploring"
            return available_moves[0]

        return min(
            available_moves,
            key=lambda position: (
                abs(position[0] - safe_zone[0])
                + abs(position[1] - safe_zone[1])
            )
        )

    def take_turn(self):
        next_position = self.decide_action()

        if next_position is None:
            return False

        previous_state = self.state

        if self.move(next_position):
            if previous_state == "evading":
                self.successful_evasions += 1

            self.safe_zone_reached = (
                self.position in self.environment.safe_zones
            )

            if self.safe_zone_reached:
                self.state = "safe"

            return True

        return False


if __name__ == "__main__":
    environment = Environment()

    john = JohnConnor(environment, (1, 1))

    environment.place_agent("T-1000", (4, 1))

    print("Initial Environment:")
    environment.display_environment()

    print("\nJohn Connor's Decision:")
    print("Detected Threats:", john.perceive())
    print("Current State:", john.state)

    john.take_turn()

    print("\nAfter John Connor's Movement:")
    print("Position:", john.position)
    print("State:", john.state)
    print("Health:", john.health)
    print("Energy:", john.energy)
    print("Successful Evasions:", john.successful_evasions)

    environment.display_environment()
