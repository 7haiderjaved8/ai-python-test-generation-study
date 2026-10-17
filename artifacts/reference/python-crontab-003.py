    def test_02_simple_enum(self):
        """Simple Enumerations"""
        e = list(self.crontab.find_command('enums'))[0]
        self.assertEqual(e.month, 'JAN')
        self.assertEqual(e.month.render(True), '1')
        self.assertEqual(e.dow, 'SAT')
        self.assertEqual(e.dow.render(True), '6')
