import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

class Visualize:
    """
    This class will create the visual aids, then help us updating them.
    """

    def __init__(self, map_matrix, herbi, carni, total):
        """
        Creates subplots, and visualizes the map.
        :param map_matrix: list
        """
        # self.year = []
        # self.herbs = []
        # self.carnis = []
        # self.total = []

        #self.df = pd.DataFrame({'Herbivores': {0: 100},
        #                        'Carnivores': {0: carni}, 'Total': {0: total}})

        self.df = pd.DataFrame({
        'Herbivore': [herbi], 'Carnivore': [carni]}, index = [0])

        # self.fig = plt.figure()

        self.fig, self.axes = plt.subplots(figsize=(10, 5), ncols=2, nrows=2)

        #Setting titles
        y_title_margin = 1
        self.axes[0][0].set_title("Map of Rossumøya", y=y_title_margin)
        self.axes[0][1].set_title("Population", y=y_title_margin)
        self.axes[1][0].set_title("Herbivore spread", y=y_title_margin)
        self.axes[1][1].set_title("Carnivore spread", y=y_title_margin)

        sb.heatmap(data=map_matrix, ax=self.axes[0][0])
        sb.lineplot(data=self.df, ax=self.axes[0][1])
        # sb.lineplot(x="year", y="population", data=self.df)
        #self.axes[0][1] = df.plot.line()
        plt.show()
        # sb.boxplot(y="b", x="a", data=df, orient='v', ax=axes[1])
        # sb.boxplot(y="b", x="a", data=df, orient='v', ax=axes[2])
        # sb.boxplot(y="b", x="a", data=df, orient='v', ax=axes[3])


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




    def update(self, herbs, carnis, year):
        self.update_population_statistics(herbs, carnis, year)
        #s elf.axes[0][1].sns(data=self.data)
        sb.lineplot(data=self.df, ax=self.axes[0][1])
        print('hei')
        #sb.lineplot(x="year", y="population", data=self.df)
        #plt.show()
        #self.axes[01][1]
        #self.axes[0][1]


    def update_population_statistics(self, herbs, carnis, year):
        """
        Will take information about new creatures, and update the plot
        accordingly.
        :param herbs: int
        :param carnis: int
        :param year: int
        :return:
        """
        self.df.append({'Herbivore': [herbs], 'Carnivore': [carnis]}, index: year)
        # self.year.append(year)
        # self.herbs.append(herbs)
        # self.carnis.append(carnis)
        # total = herbs + carnis
        # self.total.append(total)
        # self.data['year']



if __name__ == '__main__':
    test = Visulualize()
