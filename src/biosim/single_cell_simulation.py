
"""
This file should not be included in the finnished project.
Will simulate the population of herbivores in a single cell.
The purpose of this is to get a greater understanding of how to deal with the
next problem, which is implementing carnivores and then using the entire map.


"""
from fauna import Fauna, Herbivore
from Cell import Cell

cell = Cell((3 ,4), landscape='J', fodder=800)




def run_simulation(number_years, start_population):

    # Creating the start population in the cell.
    for element in start_population:
        print(element['loc'])
        # print(element['pop'])
        for item in element['pop']:
            # print(item.get('species'))
            species = item.get('species')
            weight = item.get('weight')
            age = item.get('age')
            # print(item['species'])
            cell.population.append(Herbivore(species, weight, age))
            cell.number_of_herbivores += 1

    for year in range(number_years):
        cell.add_fodder()
        print('Year: ', year +1)
        print('Population: ', cell.number_of_herbivores)
        for creature in cell.population:
            creature.reduce_weight()
            print('Weight: ' ,creature.weight)
            creature.fitness = creature.calculate_fitness()
            print('Fitness: ', creature.get_fitness(), '\n')

        cell.remove_pop()



test = [{'loc': (3,4),
         'pop': [{'species': 'herbivore', 'age': 10, 'weight': 15},
                {'species': 'herbivore', 'age': 5, 'weight': 40},
                {'species': 'herbivore', 'age': 15, 'weight': 25}]}]

run_simulation(20,test)