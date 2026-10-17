    def test_main_shows_default_state(self):
        """Test running main shows the default state
        """
        with tempfile.NamedTemporaryFile() as temp:
            state['bla'] = 12
            state.save(temp.name)

            spec = ('[pyexperiment]\n'
                    'state_filename = string(default=%s)' % temp.name)
            # Monkey patch arg parser
            argparse._sys.argv = [  # pylint: disable=W0212
                "test", "show_state"]

            buf = io.StringIO()
            with stdout_redirector(buf):
                experiment.main(config_spec=spec)
            self.assertRegexpMatches(buf.getvalue(), r"bla")
            self.assertRegexpMatches(buf.getvalue(), r"12")
