    def test_list_attributes_simple(self):
        """Verify that calling dir() on a simple image lists the expected EXIF attributes."""
        with open(
            os.path.join(os.path.dirname(__file__), "noise.jpg"), "rb"
        ) as image_file:
            image = Image(image_file)
        dunder_dir_text = "\n".join(textwrap.wrap(repr(sorted(dir(image))), 90))
        self.assertEqual(
            dunder_dir_text,
            Baseline(
                """
            ['_exif_ifd_pointer', '_segments', 'color_space', 'compression', 'datetime', 'delete',
            'delete_all', 'get', 'get_all', 'get_file', 'get_thumbnail', 'has_exif',
            'jpeg_interchange_format', 'jpeg_interchange_format_length', 'list_all', 'orientation',
            'pixel_x_dimension', 'pixel_y_dimension', 'resolution_unit', 'software', 'x_resolution',
            'y_resolution']
            """
            ),
        )
