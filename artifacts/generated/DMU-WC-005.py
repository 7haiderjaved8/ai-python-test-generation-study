    def test_resolve_match_path_brand(self):
        m = self.patterns_pathall.resolve('/en-us/bmw/')
        response = m.func(request=None, *m.args, **m.kwargs)
        self.assertEqual(response.content, b"Brand: BMW Series")
