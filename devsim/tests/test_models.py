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

        class SolarCell(Device):
            def __init__(self, name=None, mesh=None):
                super(SolarCell, self).__init__(name, mesh)
                # This is specific to this device
                self.set_node_model('Bulk', 'Acceptors', '1.0e16*step(0.5e-5-x)')
                self.set_node_model('Bulk', 'Donors', '1.0e18*step(x-0.5e-5)')
                self.set_node_model('Bulk', 'NetDoping', 'Donors-Acceptors')

        scell = SolarCell('MySolarCell', mesh=mesh)

        import pdb; pdb.set_trace()
        # Stablish conditions (light)
        # Setup the model
        from devsim.materials.light_sources import AM0
        from devsim.models import BeerLambertModel
        mdl = BeerLambertModel(scell, AM0())
        scell.setup_model(mdl)
        # Solve
        scell.initial_solution()
        scell.solve()
        scell.export('scell.dat')

        # Check results
        results = [n for n in get_node_model_values(
            device=scell.name,
            region=scell.mesh.regions[0],
            name='Beer_Lambert')
        ]
        self.assertEqual(len(results), 47)

