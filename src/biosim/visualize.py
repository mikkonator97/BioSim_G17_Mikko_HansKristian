import matplotlib.pyplot as plt
import seaborn as sb

class Visualize:
    """
    This class will create the visual aids, then help us updating them.
    """

    def __init__(self, map_matrix):
        plt.subplot(2, 2, 1)
        plt.title('Map of Rossumøya')
        island = sb.heatmap(map_matrix)
        plt.subplot(2, 2, 2)
        plt.title('Total amount of creatures')
        plt.subplot(2, 2, 3)
        plt.title('Spread of Herbivores')
        plt.subplot(2, 2, 4)
        plt.title('Spread of Carnivores')
        plt.show()



    def update(self):

        self.update_population_statistics()
        self.update_herbivores()
        self.update_carnivores()

    def update_population_statistics(self):
        pass

    def update_herbivores(self):
        pass

    def update_carnivores(self):
        pass


if __name__ == '__main__':
    test = Visulualize()
