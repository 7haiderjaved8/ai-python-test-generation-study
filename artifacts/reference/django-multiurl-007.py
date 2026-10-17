    def test_resolve_match_faillthrough(self):
        m = self.patterns_no_fallthrough.resolve('/bacon/')
        with self.assertRaises(urlresolvers.Resolver404):
            m.func(request=None, *m.args, **m.kwargs)
