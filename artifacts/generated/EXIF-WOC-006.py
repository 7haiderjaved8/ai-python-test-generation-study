    def test_read(self):
        """Test reading a user comment."""
        self.assertEqual(
            self.image.user_comment,
            "This image shall be used in a package regression/unit test to verify reading this "
            "user comment attribute.",
        )
