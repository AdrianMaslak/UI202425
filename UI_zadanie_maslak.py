import random

class ZenGarden:
    def __init__(self, width, height, rocks):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.rocks = rocks

        # Place rocks in the garden
        for rock in rocks:
            x, y = rock
            self.grid[y][x] = 'K'  # 'K' represents a rock in the garden

    def display_garden(self):
        for row in self.grid:
            print(" ".join(f"{str(cell):>2}" for cell in row))
        print()

class Monk:
    def __init__(self, garden, monk_id):
        self.garden = garden
        self.position = None
        self.direction = None  # Current direction of movement
        self.id = monk_id  # Unique ID for each monk

    def get_all_perimeter_points(self):
        perimeter_points = []
        # Entry points on the perimeter of the garden (top, bottom, left, right edges)
        for x in range(self.garden.width):
            perimeter_points.append((x, 0))  # Top edge
            perimeter_points.append((x, self.garden.height - 1))  # Bottom edge
        for y in range(1, self.garden.height - 1):
            perimeter_points.append((0, y))  # Left edge
            perimeter_points.append((self.garden.width - 1, y))  # Right edge
        return perimeter_points

    def start_raking(self):
        # Select any random perimeter point, regardless of whether it's blocked or not
        perimeter_points = self.get_all_perimeter_points()
        self.position = random.choice(perimeter_points)

        # If the chosen entry point is blocked, the monk cannot start
        x, y = self.position
        if self.garden.grid[y][x] != 0:
            print(f"Monk {self.id} attempted to start at a blocked position ({x}, {y}) and stopped.")
            return False
 # 
        # Set initial direction based on the entry point
        if y == 0:  # Top edge
            self.direction = (0, 1)  # Moving down
        elif y == self.garden.height - 1:  # Bottom edge
            self.direction = (0, -1)  # Moving up
        elif x == 0:  # Left edge
            self.direction = (1, 0)  # Moving right
        elif x == self.garden.width - 1:  # Right edge
            self.direction = (-1, 0)  # Moving left

        # Start raking
        self.rake()
        return True

    def rake(self):
        x, y = self.position
        dx, dy = self.direction

        while True:
            # Rake the current cell if it's not an obstacle
            if self.garden.grid[y][x] == 0:
                self.garden.grid[y][x] = self.id

            # Look ahead to the next position
            next_x = x + dx
            next_y = y + dy

            # If the next position is out of bounds, stop at the edge
            if not (0 <= next_x < self.garden.width and 0 <= next_y < self.garden.height):
                print(f"Monk {self.id} reached the edge at ({x}, {y}) and stopped.")
                break

            # If the next cell is an obstacle (rock or raked cell), decide to turn
            if self.garden.grid[next_y][next_x] != 0:
                new_direction = self.decide_turn(x, y)
                if new_direction is None:
                    # No valid turn available, stop movement
                    print(f"Monk {self.id} stopped at position ({x}, {y}) - no valid turn available.")
                    break
                else:
                    # Turn before moving
                    dx, dy = new_direction
                    self.direction = new_direction
                    print(f"Monk {self.id} turned to new direction {self.direction} at position ({x}, {y})")
                    continue  # Re-evaluate with the new direction

            # Move to the next position
            x += dx
            y += dy

    def decide_turn(self, x, y):
        # Determine the possible turns (priority left, then right)
        direction_priority = {
            (0, 1): [(-1, 0), (1, 0)],  # Moving down, priority: left (right), right (left)
            (0, -1): [(1, 0), (-1, 0)],  # Moving up, priority: left (left), right (right)
            (1, 0): [(0, -1), (0, 1)],  # Moving right, priority: up, down
            (-1, 0): [(0, 1), (0, -1)]   # Moving left, priority: down, up
        }

        possible_turns = direction_priority.get(self.direction, [])
        for turn in possible_turns:
            dx, dy = turn
            new_x, new_y = x + dx, y + dy
            # Check if the turn leads to an unraked and unobstructed cell
            if 0 <= new_x < self.garden.width and 0 <= new_y < self.garden.height and self.garden.grid[new_y][new_x] == 0:
                return turn

        # No valid turn available
        return None

# Main logic for creating the first generation of monks
def first_generation(garden, num_monks):
    successful_monks = 0

    for i in range(num_monks):
        monk_id = i + 1
        monk = Monk(garden, monk_id)
        if monk.start_raking():
            successful_monks += 1
            garden.display_garden()

    print(f"Total successful monks: {successful_monks}")

# Example usage
rocks = [(5, 3), (2, 6), (9, 1), (3, 1), (8, 6), (9, 6)]
garden = ZenGarden(12, 10, rocks)
first_generation(garden, 18)  # Run with 18 monks
