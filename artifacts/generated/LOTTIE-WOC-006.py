    def test_line_abs(self):
        self.assert_path(
            "M 10,10 L 90,90 V 10 H 50",
            [NVector(10, 10), NVector(90, 90), NVector(90, 10), NVector(50, 10)],
            [NVector( 0,  0), NVector( 0,  0), NVector( 0,  0), NVector( 0,  0)],
            [NVector( 0,  0), NVector( 0,  0), NVector( 0,  0), NVector( 0,  0)],
        )
