    def test_current_invalid(self):
        """Unit test for current getter and setter with invalid parameters"""

        with pytest.raises(ValueError):
            self.grid.current = 1, 2, 3, 4
