import unittest


class LightsourceTestCase(unittest.TestCase):
    def test_am0(self):
        from devsim.light_sources import AM0
        src = AM0()
        self.assertEqual(src.lambda_min, 280)
        self.assertEqual(src.lambda_max, 4000)
        self.assertEqual(src.irradiance(280), 8.2e-2)
        self.assertEqual(src.irradiance(4000), 8.68e-3)

    def test_am0_interpolation(self):
        from devsim.light_sources import AM0
        src = AM0()
        self.assertEqual(src.irradiance(280.75), 0.1245)
        self.assertEqual(src.irradiance(3926.25), 0.00938)
