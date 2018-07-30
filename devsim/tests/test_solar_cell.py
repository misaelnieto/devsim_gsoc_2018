import unittest

from devsim.mesh import Mesh
from devsim.device import Device
from devsim import materials


class SolarCellTestCase(unittest.TestCase):
    def setUp(self):
        mesh = Mesh('Solar Cell Mesh')
        # default units are micrometers
        # (position, spacing, tag)
        mesh.add_line(position=0.00, spacing=0.01, tag='anode')
        mesh.add_line(position=10.00, spacing=1.0, tag='cathode')
        mesh.add_contact(name='anode', tag='anode', material=materials.Metals.generic)
        mesh.add_contact(name='cathode', tag='cathode', material=materials.Metals.generic)

        substrate = 'Cell Substrate'
        mesh.add_region(
            name=substrate,
            material=materials.Silicon(taup=1e-8, taun=1e-8),
            tag1='anode', tag2='cathode'
        )
        mesh.finalize()

        pv_cell = device.Device('SolarCell', mesh=mesh)
        pv_cell.create_node_model(substrate, 'Acceptors', '1.0e16*step(0.5e-5-x)')
        pv_cell.create_node_model(substrate, 'Donors', '1.0e18*step(x-0.5e-5)')
        pv_cell.create_node_model(substrate, 'NetDoping', 'Donors-Acceptors')
        pv_cell.solve()
        pv_cell.solve(type='dc', absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

        # TODO: move this to another place, maybe solution module?
        pv_cell.drift_diffusion_initial_solution()

        # Drift diffusion simulation at equilibrium
        pv_cell.solve(type='dc', absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)

        # Ramp the bias to 0.5 Volts
        pv_cell.solve(type='ramp', start=0.0, stop=0.5, step=0.1,
                      absolute_error=1e10,
                      relative_error=1e-10,
                      maximum_iterations=30)

        pv_cell.export(file='pv_cell.dat', type='tecplot')
