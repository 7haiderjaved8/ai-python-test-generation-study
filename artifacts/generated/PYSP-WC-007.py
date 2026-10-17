    def test_append(self):
        """Test append"""

        selection = Selection([], [], [], [], [(23, 12)])
        table = 0
        attr = AttrDict([("angle", 0.2)])

        self.cell_attr.append(CellAttribute(selection, table, attr))

        # Check if 1 item - the actual action has been added
        assert len(self.cell_attr) == 3
