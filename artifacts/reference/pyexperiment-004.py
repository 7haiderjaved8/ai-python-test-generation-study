    def test_delegate_singleton_dir(self):
        """Test calling the dir method on a delegated singleton
        """
        class FooSingleton(Singleton):
            """Singleton test class
            """
            @staticmethod
            def bla():
                """Returns foo
                """
                return "foo"

        singleton = delegate_singleton(FooSingleton)
        self.assertIn('bla', dir(singleton))
