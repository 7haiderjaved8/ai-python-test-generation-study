    def test_contains(self):
        """Test the HierarchicalOrderedDict with `in`
        """
        self.assertEqual(len(self.hod), 0)

        self.assertFalse('a' in self.hod)
        self.hod['a'] = 1
        self.assertTrue('a' in self.hod)

        self.assertFalse('b.c.d' in self.hod)
        self.hod['b.c.d'] = 1
        self.assertTrue('b.c.d' in self.hod)
