    def test_listdifference(self):
        """Test diference between lists"""
        self.assertEqual(set(self.crontab2) - set(self.crontab1), {self.crontab2[3]})
