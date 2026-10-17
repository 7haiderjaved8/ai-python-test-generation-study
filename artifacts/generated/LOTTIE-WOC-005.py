    def test_keyframes(self):
        md = objects.MultiDimensional(NVector(0, 0))
        md.add_keyframe(0, NVector(1, 2))
        md.add_keyframe(3, NVector(4, 5))
        self.assertDictEqual(
            md.to_dict(),
            {
                "a": 1,
                "k": [
                    {
                        "t": 0,
                        "s": [1, 2],
                        "e": [4, 5],
                        "i": {"x": [1], "y": [1]},
                        "o": {"x": [0], "y": [0]},
                    },
                    {
                        "t": 3,
                        "s": [4, 5],
                    }
                ]
            }
        )
