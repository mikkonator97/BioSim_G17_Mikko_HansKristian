import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import subprocess
import os

class Visualize(object):
    """Provides user interface for simulation, including visualization."""

    def __init__(self,ymax=10000, years=50, img_dir=None, img_name='biosim',
                 img_fmt='png'):
        """
        :param sys_size:  system size, e.g. (5, 10)
        :type sys_size: (int, int)
        :param noise: noise level
        :type noise: float
        :param seed: random generator seed
        :type seed: int
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix, default 'png'
        :type img_fmt: str
        """
        self.i = 0
        self.ymax = ymax

        self.map_size = np.random.random((10,10))

        # self.carnivore

        # self._system = DiffSys(sys_size, noise)
        # self._herbivore_data = [0, 0, 0, 0]

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None
        self._img_fmt = img_fmt

        self._step = 0
        self._final_step = years
        self._img_ctr = 0

        # the following will be initialized by _setup_graphics
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._stats_ax = None
        self._herbivore_ax = None
        self._carnivore_ax = None

        self._herbivore_line = None
        self._carnivore_line = None
        self._total_line = None


        self._setup_graphics()


    def _setup_graphics(self):
        """Creates subplots."""


        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()
            self._fig.subplots_adjust(left=None, bottom=None, right=None,
                                      top=None, wspace=0.5, hspace=0.5)

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self._map_ax.set_title('Map of Rossumøya')
            self._img_axis = None

        # Add right subplot for line graph of mean.
        if self._stats_ax is None:
            self._stats_ax = self._fig.add_subplot(2, 2, 2)
            self._stats_ax.set_title('Population')
            self._stats_ax.set_ylim(0, self.ymax)

        # needs updating on subsequent calls to simulate()
        self._stats_ax.set_xlim(0, self._final_step + 1)

        if self._herbivore_line is None:
            stats_plot = self._stats_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._herbivore_line = stats_plot[0]

        if self._carnivore_line is None:
            stats_plot = self._stats_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._carnivore_line = stats_plot[0]

        if self._total_line is None:
            stats_plot = self._stats_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._total_line = stats_plot[0]

        if self._herbivore_ax is None:
            self._herbivore_ax = self._fig.add_subplot(2, 2, 3)
            self._herbivore_ax.set_title('Spread of herbivores')
            self._herbivore_ax.imshow(self.map_size)


        if self._carnivore_ax is None:
            self._carnivore_ax = self._fig.add_subplot(2, 2, 4)
            self._carnivore_ax.set_title('Spread of carnivores')
            #self._carnivore_ax.hspace(0.5)
        #self._carnivore_line = stats_plot[0]

        # plt.show()

    def _update_graphics(self, cell_map):
        herbivore, carnivore, total = cell_map.get_creatures()
        _update_stats_graph(herbivore, carnivore)
        _update_herbivore_spread(cell_map.map_herbivores)
        plt.pause(1e-6)
        plt.pause(3)

    def _update_stats_graph(self, herbivore, carnivore):

        # print(type(self._herbivore_line))

        herbivore_data = self._herbivore_line.get_ydata()
        carnivore_data = self._carnivore_line.get_ydata()
        total_data = self._total_line.get_ydata()

        herbivore_data[self.i] = herbivore
        carnivore_data[self.i] = carnivore
        total_data[self.i] = herbivore + carnivore

        self._herbivore_line.set_ydata(herbivore_data)
        self._carnivore_line.set_ydata(carnivore_data)
        self._total_line.set_ydata(total_data)
        self.i += 1


    def _update_herbivore_spread(self, herbivore_spread):
        im.set_data(data)






if __name__ == '__main__':
    test = Visualize()
    test._setup_graphics()
    test._update_stats_graph(100, 10)
    test._update_stats_graph(1000, 31)
    test._update_stats_graph(5000, 142)
    test._update_stats_graph(10000, 4000)

    # test.update(300, 60)

