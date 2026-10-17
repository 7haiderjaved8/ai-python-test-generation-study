    def test_invalid_app1_segment(self):
        """Verify that an image with an invalid APP1 segment marker raises an IOError.

        In this case, an invalid APP1 segment marker occurs when the parser finds an 0xFFE1 in the
        image data itself (and hence finds no metadata/tags).

        """
        image_path = os.path.join(os.path.dirname(__file__), "invalid_exif_app1.png")
        with open(image_path, "rb") as image_file:
            my_image = Image(image_file)

        self.assertFalse(my_image.has_exif)
