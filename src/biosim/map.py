
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'


class Map:
    """
    Creates the coordinates of the map based on multi_line_map_string, and add
    the corresponding landscape type
    """

    def __init__(self, multi_line_map_string):
        self.multi_line_map_string = multi_line_map_string
        self.multi_line_map_string.splitlines()
        dictionary = {}
        # length = len(self.multi_line_map_string)
        # for i in range(length):
        #     for j in range(length):
        #         dictionary[(i, j)] = island_map[i][j]
        #
        for index, _ in enumerate(self.multi_line_map_string):
            for sub_index, item in enumerate(_):
                dictionary[index, sub_index] = item

        print(dictionary)
        print(dictionary)
