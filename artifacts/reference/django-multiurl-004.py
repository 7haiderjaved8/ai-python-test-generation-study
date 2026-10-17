    def test_resolve_match_middle(self):
        m = self.patterns_catchall.resolve('/sf/')
        response = m.func(request=None, *m.args, **m.kwargs)
        self.assertEqual(response.content, b"Place: San Francisco")
