    def test_01_atevery(self):
        """At Every"""
        tab = CronTab(tab="""
*  *  *  *  * command
61 *  *  *  * command
*  25 *  *  * command
*  *  32 *  * command
*  *  *  13 * command
*  *  *  *  8 command
        """)
        self.assertEqual(len(tab), 1)
        self.assertLog("error", "'61', not in 0-59 for Minutes")
        self.assertLog("error", "'25', not in 0-23 for Hours")
        self.assertLog("error", "'32', not in 1-31 for Day of Month")
        self.assertLog("error", "'13', not in 1-12 for Month")
        self.assertLog("error", "'8', not in 0-6 for Day of Week")
