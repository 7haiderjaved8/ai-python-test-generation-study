    def test_missing(self):
        """Test if missing value returns None"""

        key = (1, 2, 3)
        assert self.dict_grid[key] is None

        self.dict_grid[key] = 7

        assert self.dict_grid[key] == 7
