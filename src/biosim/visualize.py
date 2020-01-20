import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb


class Visualize:
    """
    This class will create the visual aids, then help us updating them.
    """

    def __init__(self, cell_map, year=0):
        """
        Creates subplots, and visualizes the map.
        :param map_matrix: list
        """
        self.year = [year]

        herbs, carnis, total = cell_map.get_populations()
        self.herbs = [herbs]
        self.carnis = [carnis]
        self.total = [total]

        self.map_matrix = cell_map.map_matrix

        # Might get population for the next year heh
        self.fig, self.axes = plt.subplots(figsize=(10, 5), ncols=2, nrows=2)

        #Setting titles
        y_title_margin = 1
        self.axes[0][0].set_title("Map of Rossumøya", y=y_title_margin)
        self.axes[0][1].set_title("Population", y=y_title_margin)
        self.axes[1][0].set_title("Herbivore spread", y=y_title_margin)
        self.axes[1][1].set_title("Carnivore spread", y=y_title_margin)

        sb.heatmap(data=cell_map.map_matrix, ax=self.axes[0][0])

        # self.axes[0][1].plot(self.year, self.herbs)
        # self.axes[0][1].plot(self.year, self.carnis)
        # self.axes[0][1].plot(self.year, self.total)

        self.line1, = plt.plot(self.year, self.herbs)
        self.line2, = plt.plot(self.year, self.carnis)
        self.line3, = plt.plot(self.year, self.total)

        self.axes[0][1].imshow()



        cell_map.get_population_maps()
        sb.heatmap(data=cell_map.map_herbivores, ax=self.axes[1][0], cmap="YlGnBu")
        sb.heatmap(data=cell_map.map_carnivores, ax=self.axes[1][1])



        plt.show()




    def update(self, herbs, carnis, year, cell_map):
        #plt.ion()

        self.update_population_statistics(herbs, carnis, year)
        # self.axes[0][1].plot(self.year, self.herbs)
        # self.axes[0][1].plot(self.year, self.carnis)
        # self.axes[0][1].plot(self.year, self.total)

        #sb.heatmap(data=cell_map.map_herbivores, ax=self.axes[1][0], cmap="YlGnBu")
        #sb.heatmap(data=cell_map.map_herbivores, ax=self.axes[1][1])

        # self.axes[1][0].set_data(cell_map.map_herbivores)


        # self.axes[0][1].set_data(herbs)


        # plot values against indices, use autoscale_view and relim to readjust the axes
        self.line1.set_data(self.year, self.herbs)
        self.line2.set_data(self.year, self.carnis)
        self.line3.set_data(self.year, self.total)

        plt.draw()
        plt.pause(1e-6)

        print('should plot...', self.herbs)


    def update_population_statistics(self, herbs, carnis, year):
        """
        Will take information about new creatures, and update the plot
        accordingly.
        :param herbs: int
        :param carnis: int
        :param year: int
        :return:
        """
        self.year.append(year)
        self.herbs.append(herbs)
        self.carnis.append(carnis)
        self.total.append(herbs+carnis)





if __name__ == '__main__':
    test = Visulualize()
