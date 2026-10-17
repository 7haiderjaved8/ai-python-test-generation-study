    def test_resolve_match_path_model(self):
        m = self.patterns_pathall.resolve('/en-us/x5/')
        response = m.func(request=None, *m.args, **m.kwargs)
        self.assertEqual(response.content, b"Model: X5 2019")
