    def test_main_no_processes_long(self):
        """Test running main called with --processes works as expected
        """
        called = [False]

        def foo_fun():
            """Foo function
            """
            called[0] = True
        # Monkey patch arg parser
        argparse._sys.argv = [  # pylint: disable=W0212
            "test", "--processes", "44", "foo_fun"]

        buf = io.StringIO()
        with stdout_redirector(buf):
            experiment.main(commands=[foo_fun])

        self.assertTrue(called[0])
        self.assertEqual(conf['pyexperiment.n_processes'],
                         44)
