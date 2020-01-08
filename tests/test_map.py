
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'


class TestMap:

    def test_fodder_jungle(self):
        """
        test that the correct amount of fodder is added to the jungle cell.
        :return:
        """
        added_fodder = Map.add_fodder_jungle(800)
        assert added_fodder == 800
        assert added_fodder >= 0

    def test_fodder_savannah(self):
        """
        test that the correct amount of fodder is added to the savannah cell.
        :return:
        """
        alpha = 0.3
        f_max = 300
        fodderij =
        added_fodder = Map.add_fodder_savannah(100)
        assert added_fodder == 100
        assert added_fodder >= 0

    def test_get_cell_info(self):



