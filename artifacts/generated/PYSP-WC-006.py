    def test_pop(self):
        """Unit test for pop"""

        self.data_array[(1, 2, 3)] = "12"
        self.data_array[(1, 2, 4)] = "13"

        assert self.data_array.pop((1, 2, 3)) == "12"

        assert sorted(self.data_array.keys()) == [(1, 2, 4)]
