    def test_resolve_match_first(self):
        m = self.patterns_catchall.resolve('/jane/')
        response = m.func(request=None, *m.args, **m.kwargs)
        self.assertEqual(response.content, b"Person: Jane Doe")
