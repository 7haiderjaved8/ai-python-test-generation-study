    def test_from_xml(self):
        canvas = api.Canvas.from_xml_file(self.file)
        self._check_file(canvas)
