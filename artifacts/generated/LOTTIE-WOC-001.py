    def test_to_rgb(self):
        mode = ColorMode.RGB
        self.assert_convert((1, 0.5, 0.2), (1, 0.5, 0.2), mode)
