    def test_center(self):
        bb = objects.BoundingBox(10, 20, 30, 40)
        c = bb.center()
        self.assertEqual(c, objects.NVector(20, 30))
