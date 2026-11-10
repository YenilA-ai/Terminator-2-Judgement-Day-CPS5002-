
class Environment:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height

        self.grid = [
            ["empty" for _ in range(width)]
            for _ in range(height)
        ]

        self.obstacles = set()
        self.safe_zones = set()
        self.agent_positions = {}

        self.create_environment()

    def create_environment(self):
        obstacles = [
            (5, 5), (5, 6), (5, 7),
            (10, 3), (10, 4), (10, 5),
            (15, 10), (15, 11), (15, 12),
            (3, 15), (4, 15), (5, 15)
        ]

        safe_zones = [
            (18, 18), (18, 17),
            (17, 18), (17, 17)
        ]

        for position in obstacles:
            self.place_obstacle(position)

        for position in safe_zones:
            self.place_safe_zone(position)

    def is_within_bounds(self, position):
        x, y = position

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def is_walkable(self, position):
        if not self.is_within_bounds(position):
            return False

        return position not in self.obstacles

    def place_obstacle(self, position):
        if not self.is_within_bounds(position):
            return False

        if position in self.safe_zones:
            return False

        self.obstacles.add(position)

        x, y = position
        self.grid[y][x] = "obstacle"

        return True

    def place_safe_zone(self, position):
        if not self.is_within_bounds(position):
            return False

        if position in self.obstacles:
            return False

        self.safe_zones.add(position)

        x, y = position
        self.grid[y][x] = "safe"

        return True

    def place_agent(self, agent_name, position):
        if not self.is_walkable(position):
            return False

        if position in self.agent_positions.values():
            return False

        self.agent_positions[agent_name] = position

        return True

    def move_agent(self, agent_name, new_position):
        if agent_name not in self.agent_positions:
            return False

        if not self.is_walkable(new_position):
            return False

        if new_position in self.agent_positions.values():
            return False

        self.agent_positions[agent_name] = new_position

        return True

    def remove_agent(self, agent_name):
        if agent_name in self.agent_positions:
            del self.agent_positions[agent_name]

    def get_cell(self, position):
        if not self.is_within_bounds(position):
            return None

        x, y = position

        return self.grid[y][x]

    def get_neighbours(self, position):
        x, y = position

        possible_positions = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        return [
            neighbour
            for neighbour in possible_positions
            if self.is_walkable(neighbour)
        ]

    def display_environment(self):
        for y in range(self.height):
            row = []

            for x in range(self.width):
                position = (x, y)

                if position in self.agent_positions.values():
                    agent_name = next(
                        name for name, agent_position
                        in self.agent_positions.items()
                        if agent_position == position
                    )

                    symbols = {
                        "John Connor": "J",
                        "T-800": "8",
                        "T-1000": "T"
                    }

                    row.append(symbols.get(agent_name, "A"))

                elif position in self.obstacles:
                    row.append("#")

                elif position in self.safe_zones:
                    row.append("S")

                else:
                    row.append(".")

            print(" ".join(row))


if __name__ == "__main__":
    environment = Environment()

    environment.place_agent("John Connor", (1, 1))
    environment.place_agent("T-800", (2, 1))
    environment.place_agent("T-1000", (18, 1))

    environment.display_environment()
