    def test_resolve_match_last(self):
        m = self.patterns_catchall.resolve('/bacon/')
        response = m.func(request=None, *m.args, **m.kwargs)
        self.assertEqual(response.content, b"Thing: Bacon")
