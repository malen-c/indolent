import unittest

from indolent.rhythm import (
    Rhythm
)


class TestRhythmMethods(unittest.TestCase):
    def test_multiplication(self):
        r = Rhythm(length=4, pattern=[1, 1, 0, 0])

        scalars = [
            1,
            2,
            1.5,
            0.5
        ]
        desired_outputs = [
            Rhythm(length=4, pattern=[1, 1, 0, 0]),
            Rhythm(length=8, pattern=[1, 1, 0, 0, 1, 1, 0, 0]),
            Rhythm(length=6, pattern=[1, 1, 0, 0, 1, 1]),
            Rhythm(length=2, pattern=[1, 1])
        ]

        for i in range(len(scalars)):
            with self.subTest(f"{r} * {scalars[i]} = {desired_outputs[i]}"):
                self.assertEqual(r * scalars[i], desired_outputs[i])

    def test_multiplication_errors(self):
        r = Rhythm(length=4, pattern=[1, 1, 0, 0])
        with self.assertRaises(ValueError, msg="Float which results in non-integer pattern length throws error"):
            r * 1.1
        with self.assertRaises(TypeError, msg="Float which results in negative pattern length throws error"):
            r * -1


if __name__ == '__main__':
    unittest.main()
