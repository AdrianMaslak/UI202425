import random

class ZenGarden:
    def __init__(self, width, height, rocks):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        # Place rocks in the garden
        for x, y in rocks:
            self.grid[y][x] = 'K'  # Represent rocks with 'K'

    def display_garden(self):
        for row in self.grid:
            print(" ".join(f"{str(cell):>2}" for cell in row))
        print()

    def reset_garden(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != 'K':
                    self.grid[y][x] = 0

class Monk:
    def __init__(self, garden, monk_id):
        self.garden = garden
        self.id = monk_id
        self.position = None
        self.direction = None
        self.fitness = 0

    def choose_entry_point(self):
        perimeter_points = [
            (x, 0) for x in range(self.garden.width)
        ] + [
            (x, self.garden.height - 1) for x in range(self.garden.width)
        ] + [
            (0, y) for y in range(1, self.garden.height - 1)
        ] + [
            (self.garden.width - 1, y) for y in range(1, self.garden.height - 1)
        ]

        self.position = random.choice(perimeter_points)
        return True
        

    def set_initial_direction(self):
        x, y = self.position
        if y == 0:  # Top edge
            self.direction = (0, 1)  # Move down
        elif y == self.garden.height - 1:  # Bottom edge
            self.direction = (0, -1)  # Move up
        elif x == 0:  # Left edge
            self.direction = (1, 0)  # Move right
        elif x == self.garden.width - 1:  # Right edge
            self.direction = (-1, 0)  # Move left

    def rake(self):
        x, y = self.position
        dx, dy = self.direction

        while True:
            # Rake the current cell if it's not an obstacle
            if self.garden.grid[y][x] == 0:
                self.garden.grid[y][x] = self.id
                self.fitness += 1

            # Determine next position
            next_x, next_y = x + dx, y + dy

            # If next position is out of bounds, stop
            if not (0 <= next_x < self.garden.width and 0 <= next_y < self.garden.height):
                break

            # If next cell is an obstacle, decide on a turn
            if self.garden.grid[next_y][next_x] != 0:
                new_direction = self.decide_turn(x, y)
                if new_direction is None:
                    break  # No valid turn available, stop movement
                else:
                    dx, dy = new_direction
                    self.direction = new_direction
                    continue

            # Move to the next position
            x, y = next_x, next_y

    def decide_turn(self, x, y):
        # Determine the possible turns with priority: left, then right
        direction_priority = {
            (0, 1): [(-1, 0), (1, 0)],  # Down: left, right
            (0, -1): [(1, 0), (-1, 0)],  # Up: left, right
            (1, 0): [(0, -1), (0, 1)],  # Right: up, down
            (-1, 0): [(0, 1), (0, -1)]  # Left: down, up
        }

        for turn in direction_priority.get(self.direction, []):
            dx, dy = turn
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.garden.width and 0 <= new_y < self.garden.height and self.garden.grid[new_y][new_x] == 0:
                return turn

        return None

# Generate the first generation of monks
def first_generation(garden, num_monks):
    monks = []
    for i in range(1, num_monks + 1):
        monk = Monk(garden, i)
        if monk.choose_entry_point():
            monk.set_initial_direction()
            monk.rake()
            monks.append(monk)
            garden.display_garden()
    return monks

# Example usage
rocks = [(5, 3), (2, 6), (9, 1), (3, 1), (8, 6), (9, 6)]
garden = ZenGarden(12, 10, rocks)
first_generation(garden, 18)  # Generate the first generation with 10 monks
