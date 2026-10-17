    def test_captures_stdout_stderr(self):
        """Test capturing stdout and stderr from print
        """
        message1 = "This should be captured on stdout..."
        message2 = "And this should be captured on stderr..."

        buf_out = io.StringIO()
        buf_err = io.StringIO()

        with stdout_err_redirector(buf_out, buf_err):
            print(message1)
            print(message2, file=sys.stderr)

        self.assertEqual(buf_out.getvalue(), message1 + '\n')
        self.assertEqual(buf_err.getvalue(), message2 + '\n')
