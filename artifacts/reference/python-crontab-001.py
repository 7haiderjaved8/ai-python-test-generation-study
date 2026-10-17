    def test_00_minutes(self):
        """Every Minutes"""
        for job in self.crontab:
            job.every(3).minutes()
            self.assertEqual(job.slices.clean_render(), '*/3 * * * *')
            job.minutes.every(5)
            self.assertEqual(job.slices.clean_render(), '*/5 * * * *')
