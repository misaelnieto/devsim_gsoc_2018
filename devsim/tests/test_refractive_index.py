import unittest


class RefractiveIndexTestCase(unittest.TestCase):
    def test_rindex(self):
        from devsim.materials.refractive_index import RefractiveIndex

        ri_air = RefractiveIndex('Air.csv')
        # We know the maximum and minimum wavelength of air datafile
        self.assertEqual(ri_air.lambda_min, 200)
        self.assertEqual(ri_air.lambda_max, 4000)

        # The real part of the refractive index has two alias
        self.assertEqual(ri_air.real(200), 1.0)
        self.assertEqual(ri_air.n(200), 1.0)
        self.assertEqual(ri_air.refraction(200), 1.0)

        # The imaginary part also has two alias
        self.assertEqual(ri_air.imag(200), 0.0)
        self.assertEqual(ri_air.k(200), 0.0)
        self.assertEqual(ri_air.extinction(200), 0.0)

        # The absorption only has one alias
        self.assertEqual(ri_air.absorption(999), 0.0)
        self.assertEqual(ri_air.alpha(999), 0.0)

        # Interpolation should work too
        self.assertEqual(ri_air.n(199), 1.0)
        self.assertEqual(ri_air.k(199), 0.0)
        self.assertEqual(ri_air.alpha(199), 0.0)
        self.assertEqual(ri_air.n(999), 1.0)
        self.assertEqual(ri_air.k(999), 0.0)
        self.assertEqual(ri_air.alpha(999), 0.0)
        self.assertEqual(ri_air.n(4999), 1.0)
        self.assertEqual(ri_air.k(4999), 0.0)
        self.assertEqual(ri_air.alpha(4999), 0.0)

    def test_rindex_as_iterator(self):
        """
        If you iterate over the refractive index you will get the wave length
        """
        from devsim.materials.refractive_index import RefractiveIndex
        ri_air = RefractiveIndex('Air.csv')
        self.assertEqual(len(ri_air), 2)
        self.assertEqual(
            [float(l) for l in ri_air],
            [200, 4000]
        )
