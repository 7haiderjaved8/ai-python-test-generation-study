    def test_02_top_vars(self):
        """Whole file env variables"""
        crontab = CronTab(tab="SHELL=dash\n")
        self.assertEqual(str(crontab), "SHELL=dash\n")
        self.assertEqual(crontab.env['SHELL'], 'dash')
        crontab.env['SHELL'] = 'bash'
        self.assertEqual(str(crontab), "SHELL=bash\n")
        self.assertEqual(crontab.env['SHELL'], 'bash')
