    def test_02_simple_enum(self):
        """Simple Enumerations"""
        job = list(self.crontab.find_command('enums'))[0]
        self.assertEqual(job.month, 'JAN')
        self.assertEqual(job.dow, 'SAT')
        self.assertEqual(job.month.render(True), '1')
        self.assertEqual(job.dow.render(True), '6')
