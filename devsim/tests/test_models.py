import unittest

from ds import get_node_model_values
from devsim .mesh import Mesh
from devsim.device import Device
from devsim import materials


class BeerLambertModelTestCase(unittest.TestCase):
    def test_node_model(self):
        # Define mesh (default units are micrometers)
        mesh = Mesh('Test Mesh')
        mesh.add_line(0.0, 0.01, 'left')
        mesh.add_line(10.0, 1.0, 'right')
        mesh.add_contact(
            name='left',
            tag='left',
            material=materials.Metals.generic
        )
        mesh.add_contact(
            name='right',
            tag='right',
            material=materials.Metals.generic
        )
        mesh.add_region(
            name='Bulk',
            material=materials.Silicon(),
            tag1='left', tag2='right'
        )

        mesh.finalize()

        sample_device = Device('Sample device', mesh=mesh)

        # Stablish conditions (light)
        # Setup the model
        from devsim.materials.light_sources import AM0
        from devsim.models import BeerLambertModel
        mdl = BeerLambertModel(sample_device, AM0())
        sample_device.setup_model(mdl)
        # Solve
        sample_device.solve()

        # Check results
        results = [n for n in get_node_model_values(
            device=sample_device.name,
            region=sample_device.mesh.regions[0],
            name='Beer_Lambert')
        ]
        self.assertEqual(len(results), 47)

