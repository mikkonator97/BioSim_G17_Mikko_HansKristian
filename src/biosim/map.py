__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'


class Map:
    """
    Creates a dictionary with the coordinates of the map based on
    multi_line_map_string, and add the corresponding landscape type
    """

    def __init__(self, map_string):
        self.map_string = map_string
        self.map_string_split = map_string.split()
        self.n_rows = len(self.map_string_split)
        self.n_cols = len(str(self.map_string_split[0]))
        self.coords = []
        self.landscape_list = []
        self.landscape = []
        # self.landscape_matrix = np.zeros([self.n_rows,self.n_cols])
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                test = (i, j)
                self.coords.append(test)
                self.landscape_list.append(self.map_string_split[i][j])

    self.landscape = list(zip(self.coords, self.landscape_list))
    for i in range(len(self.landscape)):
        self.landscape.append({"Fodder:": 0})


    def convert_landscape(self, landscape_type):
        if landscape_type == 'O':
            return 0
        elif landscape_type == 'M':
            return 1
        elif landscape_type == 'D':
            return 2
        elif landscape_type == 'S':
            return 3
        else:
            return 4

    # def create_map(self):
    #     for i in range(self.n_rows):
    #         for j in range(self.n_cols):
    #             test = (i, j)
    #             map_value = convert_landscape(self.map_string_split[i][j])
    #             self.landscape_matrix[i][j] = map_value

    def create_map(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                self.current_map.append(
                    Cell(self.map_string_split[i], self.coords[j]))

    def get_map(self):
        return self.current_map


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
if __name__ == "__main__":
    map_string = """\
                  OOOOOOOOOOOOOOOOOOOOO
                  OOOOOOOOSMMMMJJJJJJJO
                  OSSSSSJJJJMMJJJJJJJOO
                  OSSSSSSSSSMMJJJJJJOOO
                  OSSSSSJJJJJJJJJJJJOOO
                  OSSSSSJJJDDJJJSJJJOOO
                  OSSJJJJJDDDJJJSSSSOOO
                  OOSSSSJJJDDJJJSOOOOOO
                  OSSSJJJJJDDJJJJJJJOOO
                  OSSSSJJJJDDJJJJOOOOOO
                  OOSSSSJJJJJJJJOOOOOOO
                  OOOSSSSJJJJJJJOOOOOOO
                  OOOOOOOOOOOOOOOOOOOOO"""

    test_map = Map(map_string)
    print((test_map.landscape))