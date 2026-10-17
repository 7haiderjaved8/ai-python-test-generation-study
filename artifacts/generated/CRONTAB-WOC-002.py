    def test_02_top_vars(self):
        """Whole file env variables"""
        crontab = CronTab(tab="MAILTO=test@example.com\n")
        self.assertEqual(str(crontab), "MAILTO=test@example.com\n")
        self.assertEqual(crontab.env['MAILTO'], 'test@example.com')
