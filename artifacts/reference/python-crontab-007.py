    def test_00_slice_frequency(self):
        """Each Slice Frequency"""
        # Make sure some of these overlap
        self.job.setall("13-16,14-15 6,*/3 2,3,4 * *")
        self.assertEqual(len(self.job[0]), 4)
        self.assertEqual(len(self.job[1]), 8)
        self.assertEqual(len(self.job[2]), 3)
        self.assertEqual(len(self.job[3]), 12)
        self.assertEqual(len(self.job[4]), 7)
