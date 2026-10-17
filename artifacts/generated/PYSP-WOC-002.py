    def test_repr(self):
        """Unit test for __repr__"""

        selection = Selection([], [], [], [], [(32, 53), (34, 56)])
        assert str(selection) == \
            "Selection([], [], [], [], [(32, 53), (34, 56)])"
