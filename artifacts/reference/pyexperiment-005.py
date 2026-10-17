    def test_get_section_lazy(self):
        """Test getting a section of the state lazily
        """
        state['a.a'] = 12
        state['a.b'] = 13
        state['c'] = 24

        self.assertIn('a', state)
        section_a = state['a']
        self.assertIn('a', section_a)
        self.assertIn('b', section_a)
        self.assertNotIn('c', section_a)
        self.assertEqual(section_a['a'], 12)
        self.assertEqual(section_a['b'], 13)

        with tempfile.NamedTemporaryFile() as temp:
            state.save(temp.name)
            state.reset_instance()
            self.assertNotIn('a', state)

            state.load(temp.name)

            self.assertIn('a', state)

            section_a = state['a']

            self.assertIn('a', section_a)
            self.assertIn('b', section_a)
            self.assertNotIn('c', section_a)
            self.assertEqual(section_a['a'], 12)
            self.assertEqual(section_a['b'], 13)
