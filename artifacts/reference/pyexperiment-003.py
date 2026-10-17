    def test_singleton_resets(self):
        """Test that singletons properly reset themselves.
        """
        class SingletonTest(Singleton):
            """Singleton test class
            """
            def __init__(self):
                """Initializer
                """
                self.memory = []

            def add(self, number):
                """Append a number to the memory
                """
                self.memory.append(number)

        singleton_a = SingletonTest.get_instance()
        singleton_a.add(12)
        self.assertEqual(singleton_a.memory, [12])

        SingletonTest.reset_instance()

        singleton_b = SingletonTest.get_instance()
        self.assertNotEqual(singleton_a, singleton_b)

        self.assertEqual(singleton_b.memory, [])
