    def test_02_remove_all(self):
        """Remove All"""
        self.crontab.remove_all()
        self.assertEqual(len(self.crontab), 0)
        self.assertEqual(str(self.crontab), '')
