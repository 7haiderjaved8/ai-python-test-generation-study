    def test_default(self):
        an = objects.Animation()
        self.assertDictEqual(
            an.to_dict(),
            {
                "ip": 0,
                "op": 60,
                "fr": 60,
                "w": 512,
                "h": 512,
                "ddd": 0,
                "v": objects.Animation._version,
                "layers": [],
                "assets": [],
            }
        )
