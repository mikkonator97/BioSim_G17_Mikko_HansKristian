
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'


class Map:
    """
    Creates a dictionary with the coordinates of the map based on
    multi_line_map_string, and add the corresponding landscape type
    """

    def __init__(self, map_string):
        self.map_string = map_string
        self.map_string.splitlines()
        self.dictionary = {}
        antall_rader = len(self.map_string)

        self.map_string_split = [k.replace(' ', '') for k in self.map_string]

        # for i in range(antall_rader):
        #     old_value = str(map_string_split[i])
        #     new_value = old_value.replace(' ', '')
        #     map_string_split[i] = new_value

        antall_kolonner = len(str(self.map_string_split[0]))
        for i in range(antall_rader):
            for j in range(antall_kolonner):
                # dictionary[index, sub_index] = item
                self.dictionary[i, j] = {'landscape':self.map_string_split[i][j]}, \
                                        {'population': 0}, {'fodder': 0}

        print(self.dictionary)

    def add_fodder(self):

        for element in self.dictionary:
            if dictionary.values.landscape == 'J':




"""
dictionary = {}
antall_rader = len(map_string_split)
for i in range(antall_rader):
    old_value = str(map_string_split[i])
    new_value = old_value.replace(' ','')
    map_string_split[i] = new_value
    # print(map_string_split[i])
    antall_kolonnner = len(str(map_string_split[0]))
    for j in range(antall_kolonner):
        dictionary[i, j] = map_string_split[i][j]

print(dictionary)"""
