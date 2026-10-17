    def test_px(self):
        parser = SvgParser()
        parser.dpi = 96

        self.assertEqual(parser._parse_unit("123px"), 123)
        self.assertEqual(parser._parse_unit("12.3px"), 12.3)
