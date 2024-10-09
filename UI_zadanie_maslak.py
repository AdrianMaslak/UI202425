import random
import copy

class ZenGarden:
    def __init__(self, width, height, rocks):
        self.width = width
        self.height = height
        self.base_grid = [[0] * width for _ in range(height)]  # Initialize a base grid

        # Place rocks in the base grid as -1
        for x, y in rocks:
            self.base_grid[y][x] = -1

        self.grid = self.copy_garden()
        self.max_fitness = width * height - len(rocks)

        # Place rocks in the garden as -1
        for x, y in rocks:
            self.grid[y][x] = -1  # -1 represents a rock

    def copy_garden(self):
        """Create a copy of the garden grid for each genome."""
        return [row[:] for row in self.base_grid]

    def display_garden(self, grid=None):
        """Display the garden grid."""
        if grid is None:
            grid = self.grid
        for row in grid:
            print(" ".join(f"{' K ' if cell == -1 else f'{cell:3}'}" for cell in row))
        print()

class Gene:
    def __init__(self, garden):
        # Choose a random edge to start from
        width = garden.width
        height = garden.height
        edge = random.randrange(garden.width + garden.width + garden.height +garden.height)

        # Starting from the top edge
        if edge < width:
            self.start = (0, edge)
            self.direction = 'down'

        # Starting from the bottom edge
        elif width <= edge < height + width :
            self.start = (edge - width, width - 1)
            self.direction = 'left'

        # Starting from the left edge
        elif width + height <= edge < width + width + height:
            self.start = (height - 1, 2 * width + height - edge - 1)
            self.direction = 'up'

        # Starting from the right edge
        else:
            self.start = (2 * (height + width) - edge - 1, 0)
            self.direction = 'right'

        self.generate_rotation()

    def generate_rotation(self):
        # Define possible rotations or directional changes
        directions = ['up', 'right', 'down', 'left']
        
        # Find the current index of the direction
        current_index = directions.index(self.direction)
        
        # Randomly choose whether to rotate left (-1) or right (+1)
        rotation = random.choice([-1, 1])
        
        # Calculate the new direction index (wrap around with modulo)
        new_index = (current_index + rotation) % len(directions)
        
        # Assign the new direction
        self.direction = directions[new_index]

class Genome:
    def __init__(self, garden, num_genes, initialize = True):
        self.original_garden = garden  # Keep a reference to the original garden
        self.garden = ZenGarden(garden.width, garden.height, [(x, y) for y in range(garden.height) for x in range(garden.width) if garden.base_grid[y][x] == -1])
        self.fitness = 0
        self.genes = []

        if initialize:
            for _ in range(num_genes):
                gene = Gene(self.original_garden)  # Pass the reference to original garden
                self.genes.append(gene)
            self.rake()
            
    def rake(self):
        """Use each gene to rake the garden and calculate fitness."""
        g = self.garden
        monk_id = 0  # Start monk ID from 1

        # Go through each gene (monk)
        for gene in self.genes:
            pos = list(gene.start)  # Current position of the monk
            direction = gene.direction  # The direction the monk is moving in
            ri = 0  # Rotation index

            if g.grid[pos[0]][pos[1]] !=0:
                continue
            monk_id +=1

            # Start raking cells
            while True:
                # If the cell is a rock (-1), stop raking
                g.grid[pos[0]][pos[1]] = monk_id

                if direction == 'up':
                    pos[0] -= 1
                elif direction == 'down':
                    pos[0] += 1
                elif direction == 'left':
                    pos[1] -= 1
                else:
                    pos[1] += 1
                
                if pos[0] not in range(g.height) or pos[1] not in range(g.width):
                    break

                if g.grid[pos[0]][pos[1]] == 0:
                    continue

                # Ak je tam prekazka tak sa vratime...
                if direction == 'up':
                    pos[0] += 1
                elif direction == 'down':
                    pos[0] -= 1
                elif direction == 'left':
                    pos[1] += 1
                else:
                    pos[1] -= 1

                # ...a vyberieme ine policko
                if direction == 'up' or direction == 'down':
                    n = (
                        [pos[0], pos[1] - 1],
                        [pos[0], pos[1] + 1],
                    )
                else:
                    n = (
                        [pos[0] - 1, pos[1]],
                        [pos[0] + 1, pos[1]],
                    )
                nv = []
                for p in n:
                    try:
                        nv.append(g.grid[p[0]][p[1]])
                    except IndexError:
                        nv.append('e')

                # Ak je len jedno nepohrabane tak ho vyberieme
                if nv.count(0) == 1:
                    pos = n[nv.index(0)]

                # A ak su dve tak jedno vyberieme
                elif nv.count(0) == 2:
                    pos = n[gene.rotation[ri]]
                    ri += 1
                    if ri == len(gene.rotation):
                        ri = 0

                # Ak ani jedno nie je nepohrabane tak koncime
                else:
                    # Ak sme skoncili v strede mapy tak uz sa neda pokracovat
                    # na dalsi gen
                    if 'e' not in nv:
                        self.set_fitness()
                        return
                    break

                # Nastavime novy smer pohybu
                if direction in ('up', 'down'):
                    direction = 'left' if n.index(pos) == 0 else 'right'
                else:
                    direction = 'up' if n.index(pos) == 0 else 'down'

            self.set_fitness()

    def handle_turn(self, gene, direction, ri):
        """Handle turn based on the gene's rotation list."""
        rotation = gene.rotation[ri]
        if direction == (1, 0):  # Moving down
            return (0, 1) if rotation == 'right' else (0, -1)  # Turn right or left
        elif direction == (-1, 0):  # Moving up
            return (0, -1) if rotation == 'left' else (0, 1)  # Turn left or right
        elif direction == (0, 1):  # Moving right
            return (-1, 0) if rotation == 'left' else (1, 0)  # Turn up or down
        elif direction == (0, -1):  # Moving left
            return (1, 0) if rotation == 'left' else (-1, 0)  # Turn down or up

    def set_fitness(self):
        """Calculate the fitness as the number of raked cells."""
        self.fitness = sum(1 for row in self.garden for cell in row if cell > 0)  # Count only raked cells

    def crossover(self, other):
        """Create a new genome by crossing over genes from two parents."""
        new = Genome(self.original_garden, num_genes=len(self.genes))

        # Randomly choose the crossover type
        p = random.random()
        if p < 0.40:
            # One-point crossover: take part from the first parent, part from the second
            point = random.randrange(len(self.genes))
            new.genes = self.genes[:point] + other.genes[point:]
        elif p < 0.80:
            # Uniform crossover: randomly choose genes from either parent
            new.genes = [random.choice([self.genes[i], other.genes[i]]) for i in range(len(self.genes))]
        else:
            # Full copy: take all genes from one parent
            new.genes = random.choice([self.genes, other.genes])

        # Mutations: new gene generation or rotation regeneration
        for i in range(len(new.genes)):
            p = random.random()
            if p < 0.1:  # 5% chance to generate a new gene
                new.genes[i] = Gene(self.original_garden)
            elif p < 0.10:  # 10% chance to regenerate rotations
                new.genes[i].generate_rotation()

        # After crossover, rake the garden with the new genome
        new.rake()

        return new

def solve(rocks, width=12, height=10):
    """Solve the ZenGarden problem with the given rock positions."""
    garden = ZenGarden(width, height, rocks)
    population_size = 100
    generations = 10  # Run for 10 generations
    num_genes = 28
    population = [Genome(garden, num_genes) for _ in range(population_size)]

    for gc in range(generations):
        best = max(population, key=lambda x: x.fitness)
        next_generation = [best]
        for _ in range(population_size - 1):
            # Tournament selection and crossover
            parent1, parent2 = random.sample(population, 2)
            child = parent1.crossover(parent2)
            next_generation.append(child)
        population = next_generation

        # Print generation stats
        print(f'Generation: {gc + 1}, Best Fitness: {best.fitness}/{garden.max_fitness}')
        garden.display_garden(best.garden)

        # Check if the best genome solved the garden
        if best.fitness == garden.max_fitness:
            print("Solution found!")
            garden.display_garden(best.garden)
            break

# Example usage
rocks = [(5, 3), (2, 6), (9, 1), (3, 1), (8, 6), (9, 6)]
solve(rocks)
