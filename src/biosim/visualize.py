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

        self.axes[0][1].plot(self.year, self.herbs)
        self.axes[0][1].plot(self.year, self.carnis)
        self.axes[0][1].plot(self.year, self.total)

        cell_map.get_population_maps()
        sb.heatmap(data=cell_map.map_herbivores, ax=self.axes[1][0], cmap="YlGnBu")
        sb.heatmap(data=cell_map.map_carnivores, ax=self.axes[1][1])

        # sb.lineplot(data=, ax=self.axes[0][1])
        #self.line1 = self.axes[0][1].plot(np.arange(n_steps),
        #               np.full(n_steps, np.nan), 'b-')[0]


        plt.show()


        # self.ax0 = self.fig.add_subplot(221)

        # self.ax0.title = ('Map of Rossumøya')
        #self.ax0.sb.heatmap(map_matrix)

        #self.ax1 = self.fig.add_subplot(222)
        #self.ax2= self.fig.add_subplot(223)
        #self.ax3 = self.fig.add_subplot(224)
        # self.map = plt.subplot(2, 2, 1)
        #plt.title('Map of Rossumøya')
        #sb.heatmap(map_matrix)
        ## self.population_statistics = plt.subplot(2, 2, 2)
        ##plt.subplot(2, 2, 2)
        #plt.title('Total amount of creatures')
        #plt.xlabel('Year')
        #plt.ylabel('Number of creatures')
        #plt.subplot(2, 2, 3)
        #plt.title('Spread of Herbivores')
        #plt.subplot(2, 2, 4)
        #plt.title('Spread of Carnivores')
        #plt.show()




    def update(self, herbs, carnis, year, cell_map):
        #plt.ion()

        self.update_population_statistics(herbs, carnis, year)
        self.axes[0][1].plot(self.year, self.herbs)
        self.axes[0][1].plot(self.year, self.carnis)
        self.axes[0][1].plot(self.year, self.total)

        #sb.heatmap(data=cell_map.map_herbivores, ax=self.axes[1][0], cmap="YlGnBu")
        #sb.heatmap(data=cell_map.map_herbivores, ax=self.axes[1][1])


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
