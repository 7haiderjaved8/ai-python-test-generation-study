    def test_no_match(self):
        with self.assertRaises(urlresolvers.Resolver404):
            self.patterns_catchall.resolve('/eggs/and/bacon/')
