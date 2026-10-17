    def test_modify_bytes(self):
        """Verify that modifying a BYTE tag updates the tag value as expected."""
        assert self.image.gps_altitude_ref == 0
        self.image.gps_altitude_ref = 1
        assert self.image.gps_altitude_ref == 1
