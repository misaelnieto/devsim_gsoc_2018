import unittest


class MaterialsTestCase(unittest.TestCase):
    def test_material_kwargs(self):
        from devsim.materials import Material
        m = Material(eg=1.7, taup=1e-6)
        self.assertTrue(hasattr(m, 'eg'))
        self.assertTrue(hasattr(m, 'taup'))
        self.assertEqual(m.eg, 1.7)
        self.assertEqual(m.taup, 1e-6)
