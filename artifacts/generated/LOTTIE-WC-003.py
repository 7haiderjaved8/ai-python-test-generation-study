    def test_center(self):
        bb = objects.BoundingBox(0, 0, 30, 40)
        c = bb.center()
        self.assertEqual(c[0], 15)
        self.assertEqual(c[1], 20)
