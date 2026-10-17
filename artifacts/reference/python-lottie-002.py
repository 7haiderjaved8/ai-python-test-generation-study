    def test_scale(self):
        m = TransformMatrix()
        self.assertIs(m.scale(2), m)
        self.assertEqual(m._mat, [
            2, 0, 0, 0,
            0, 2, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])
        self.assertIs(m.scale(3, 4), m)
        self.assertEqual(m._mat, [
            6, 0, 0, 0,
            0, 8, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1,
        ])
