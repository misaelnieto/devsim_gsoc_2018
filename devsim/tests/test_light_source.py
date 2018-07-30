import unittest


class LightsourceTestCase(unittest.TestCase):
    def test_am0(self):
        from devsim.materials.light_sources import AM0
        src = AM0()
        self.assertEqual(src.lambda_min, 280)
        self.assertEqual(src.lambda_max, 4000)
        self.assertEqual(src.irradiance(280), 8.2e-2)
        self.assertEqual(src.irradiance(4000), 8.68e-3)

    def test_am0_interpolation(self):
        from devsim.materials.light_sources import AM0
        src = AM0()
        self.assertEqual(src.irradiance(280.75), 0.1245)
        self.assertEqual(src.irradiance(3926.25), 0.00938)

    def test_am0_windowing(self):
        from devsim.materials.light_sources import AM0
        src = AM0(lambda_min=500, lambda_max=1000)
        self.assertEqual(src.lambda_min, 500)
        self.assertEqual(src.lambda_max, 1000)
        self.assertEqual(src.irradiance(0), 0.0)
        self.assertEqual(src.irradiance(499), 0.0)
        self.assertEqual(src.irradiance(500), 1.92)
        self.assertEqual(src.irradiance(1000), 0.743)
        self.assertEqual(src.irradiance(1001), 0.0)

    def test_am0_subsambpling(self):
        from devsim.materials.light_sources import AM0
        src = AM0(samples=25)
        self.assertEqual(len(src), 25)
        src = AM0(samples=87)
        self.assertEqual(len(src), 87)
        # Except for 1001, because the AM0 csv file has 2002 rows
        src = AM0(samples=1001)
        self.assertEqual(len(src), 1001)

    def test_am0_as_iterator(self):
        from devsim.materials.light_sources import AM0
        src = AM0(samples=10)
        self.assertEqual(
            [l for l in src],
            [280.0, 380.0, 560.0, 760.0, 960.0, 1160.0, 1360.0, 1560.0, 1995.0, 2995.0]
        )
