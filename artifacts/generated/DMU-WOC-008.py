    def test_reverse(self):
        self.assertEqual('joe/', self.patterns_catchall.reverse('person', 'joe'))
        self.assertEqual('joe/', self.patterns_catchall.reverse('place', 'joe'))
        self.assertEqual('joe/', self.patterns_catchall.reverse('thing', 'joe'))
        with self.assertRaises(urlresolvers.NoReverseMatch):
            self.patterns_catchall.reverse('person')
        with self.assertRaises(urlresolvers.NoReverseMatch):
            self.patterns_catchall.reverse('argh', 'xyz')
