import unittest


class LightsourceTestCase(unittest.TestCase):
    def test_am0(self):
        from devsim.materials.light_sources import AM0
        src = AM0()
        self.assertEqual(src.lambda_min, 280)
        self.assertEqual(src.lambda_max, 4000)
        self.assertEqual(src.irradiance(280), 8.2E-2)
        self.assertEqual(src.irradiance(4000), 8.68E-3)
        self.assertEqual(src.photon_flux(280), 2.887_797_5E+12)
        self.assertEqual(src.photon_flux(280.5), 6.985_426_2E12)
        self.assertEqual(src.photon_flux(1160), 3.087_2E+14)
        self.assertEqual(src.photon_flux(4000), 4.367E+13)
        self.assertEqual(src.acc_photon_flux(280), 2.887_797_5E+12)
        self.assertEqual(src.acc_photon_flux(4000), 6.144_539_7E+17)

    def test_am0_interpolation(self):
        from devsim.materials.light_sources import AM0
        src = AM0()
        self.assertEqual(src.irradiance(280.75), 0.124_5)
        self.assertEqual(src.irradiance(3926.25), 0.009_38)
        self.assertEqual(src.photon_flux(280.5), 6.985_426_2E+12)
        self.assertEqual(src.photon_flux(280.75), 8.794_135_75E+12)
        self.assertEqual(src.photon_flux(281.0), 1.060_284_53E+13)
        self.assertEqual(src.photon_flux(3997.50), 6.555000E+13)
        self.assertEqual(src.acc_photon_flux(280.75), 1.517464635E+13)
        self.assertEqual(src.acc_photon_flux(3997.50), 6.14432135E+17)

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
        self.assertEqual(src.photon_flux(0), 0.0)
        self.assertEqual(src.photon_flux(499), 0.0)
        self.assertEqual(src.photon_flux(500), 4.829760E+14)
        self.assertEqual(src.photon_flux(1000), 3.738000E+14)
        self.assertEqual(src.photon_flux(1001), 0.0)
        self.assertEqual(src.acc_photon_flux(0), 0.0)
        self.assertEqual(src.acc_photon_flux(499), 0.0)
        self.assertEqual(src.acc_photon_flux(500), 6.0745581E+16)
        self.assertEqual(src.acc_photon_flux(1000), 2.9414051E+17)
        self.assertEqual(src.acc_photon_flux(1001), 0.0)

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
