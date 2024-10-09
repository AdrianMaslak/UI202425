import random

class ZenGarden:
    def __init__(self, width, height, rocks):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.list_geny = []
        self.edges = self.generate_edges()

        # Place rocks in the garden
        for x, y in rocks:
            self.grid[y][x] = 'K'  # Represent rocks with 'K'

    def generate_edges(self):
        edges = {}
        # Top and Bottom edges
        for x in range(self.width):
            edges[(x, 0)] = (0, 1)  # Down
            edges[(x, self.height - 1)] = (0, -1)  # Up
        
        # Left and Right edges
        for y in range(1, self.height - 1):
            edges[(0, y)] = (1, 0)  # Right
            edges[(self.width - 1, y)] = (-1, 0)  # Left

        return edges

    def display_garden(self):
        for row in self.grid:
            print(" ".join(f"{str(cell):>3}" for cell in row))
        print()

    def pridaj_geny(self, list):
        self.list_geny = list


class Gene:
    def __init__(self, entry_point=None, direction=None):
        self.entry_point = entry_point
        self.direction = direction

    def randomize(self, garden):
        # Use the garden's edge dictionary to select an entry point and direction
        self.entry_point, self.direction = random.choice(list(garden.edges.items()))

    def generate_rotation(self):
        # Randomly rotate direction
        possible_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.direction = random.choice(possible_directions)


class Genome:
    def __init__(self, garden, genome_id, num_genes=1):
        self.genome_id = genome_id
        self.garden = garden
        self.genes = [Gene() for _ in range(num_genes)]
        for gene in self.genes:
            gene.randomize(garden)
        self.fitness = 0

    def rake(self, garden):
        for gene in self.genes:
            self.execute_gene(garden, gene)

    def execute_gene(self, garden, gene):
        x, y = gene.entry_point
        dx, dy = gene.direction

        while True:
            # Rake the current cell if it's not an obstacle
            if garden.grid[y][x] == 0:
                garden.grid[y][x] = self.genome_id  # Mark as raked with the genome ID
                self.fitness += 1

            # Determine next position
            next_x, next_y = x + dx, y + dy

            # If next position is out of bounds, stop
            if not (0 <= next_x < garden.width and 0 <= next_y < garden.height):
                break

            # If next cell is an obstacle, decide on a turn
            if garden.grid[next_y][next_x] != 0:
                new_direction = self.decide_turn(garden, x, y, (dx, dy))
                if new_direction is None:
                    break  # No valid turn available, stop movement
                else:
                    dx, dy = new_direction
                    continue

            # Move to the next position
            x, y = next_x, next_y

    def decide_turn(self, garden, x, y, current_direction):
        # Determine the possible turns with priority: left, then right
        direction_priority = {
            (0, 1): [(-1, 0), (1, 0)],  # Down: left, right
            (0, -1): [(1, 0), (-1, 0)],  # Up: left, right
            (1, 0): [(0, -1), (0, 1)],  # Right: up, down
            (-1, 0): [(0, 1), (0, -1)]  # Left: down, up
        }

        for dx, dy in direction_priority.get(current_direction, []):
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < garden.width and 0 <= new_y < garden.height and garden.grid[new_y][new_x] == 0:
                return (dx, dy)

        return None
    
    def crossover(self, other):
        # Create a new genome for the child
        new = Genome(self.garden, genome_id=random.randint(1, 1000), num_genes=len(self.genes))

        # Determine the type of crossover
        p = random.random()
        if p < 0.40:
            # Type 1: Split point crossover
            point = random.randrange(len(self.genes))
            new.genes = self.genes[:point] + other.genes[point:]
        elif p < 0.80:
            # Type 2: Randomly select genes from either parent
            new.genes = []
            for i in range(len(self.genes)):
                new.genes.append(random.choice([self.genes[i], other.genes[i]]))
        else:
            # Type 3: Copy genes from one of the parents without modification
            new.genes = random.choice([self.genes, other.genes])

        # Mutation process
        for i in range(len(new.genes)):
            # With 5% probability, generate a completely new gene
            if random.random() < 0.05:
                new.genes[i] = Gene()
                new.genes[i].randomize(self.garden)
            # With 10% probability, generate a new rotation for the gene
            elif random.random() < 0.10:
                new.genes[i].generate_rotation()

        # Calculate fitness of the new genome
        new.rake(self.garden)

        return new


def first_generation(garden, num_genomes):
    return [Genome(garden, genome_id=i + 1, num_genes=1) for i in range(num_genomes)]

def solve():
    garden = ZenGarden()
    population = []
    for x in range(54):
        population.append(Genome(garden))
    for genome in genomes:
        genome.rake(garden)
        print(f"Genome {genome.genome_id}: Fitness = {genome.fitness}")
        garden.display_garden()



# Example usage: Create and rake with the first generation of genomes without resetting the garden
rocks = [(5, 3), (2, 6), (9, 1), (3, 1), (8, 6), (9, 6)]
GARDEN = ZenGarden(12, 10, rocks)
genomes = first_generation(garden, 10)  # Generate the first generation with 54 genomes

# Iterate through each genome, rake the garden, and display the cumulative garden after each one
solve()