    def test_delete_method(self):
        """Test behavior when setting tags using the ``delete()`` method."""
        self.image.delete("model")

        with self.assertRaisesRegex(
            AttributeError, "image does not have attribute model"
        ):
            self.image.model
