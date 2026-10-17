    def test_01_read(self):
        """Read existing command"""
        job = self.crontab[0]
        self.assertEqual(job.user, 'palin')
        self.assertEqual(job.command, 'one_cross_each')
        job = self.crontab[1]
        self.assertEqual(job.user, 'matias')
        self.assertEqual(job.command, 'tab_user_error')
        self.assertEqual(len(self.crontab), 2)
