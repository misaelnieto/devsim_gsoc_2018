import unittest
from devsim.materials.base import Material

class MaterialsTestCase(unittest.TestCase):

    def test_material_rich_comparison(self):
        m = Material(foo=123)
        self.assertTrue(m.foo < 124)
        self.assertFalse(m.foo < 123)
        self.assertTrue(m.foo <= 123)
        self.assertTrue(m.foo == 123)
        self.assertTrue(m.foo != 1337)
        self.assertTrue(m.foo > 122)
        self.assertTrue(m.foo >= 123)
        self.assertFalse(m.foo >= 124)

    def test_material_kwargs(self):
        m = Material(eg=1.7, taup=1e-6)
        self.assertTrue(hasattr(m, 'eg'))
        self.assertTrue(hasattr(m, 'taup'))
        self.assertEqual(m.eg, 1.7)
        self.assertEqual(m.taup, 1e-6)
