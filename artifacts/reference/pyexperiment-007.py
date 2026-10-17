    def test_get_default(self):
        """Test getting config values with a default argument
        """
        self.assertRaises(KeyError, lambda: conf['a'])
        self.assertRaises(KeyError, conf.get, 'a')
        self.assertEqual(conf.get('a', default=12), 12)
        self.assertRaises(KeyError, conf.get, 'a')
