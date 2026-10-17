    def test_00_minutes(self):
        """Every Minutes"""
        for job in self.crontab:
            job.every(5).minutes()
            self.assertEqual(job.slices.clean_render(), '*/5 * * * *')
