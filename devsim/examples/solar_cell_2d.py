import sys
import logging

from devsim import materials
from devsim.device import Device, DriftDiffusionInitialSolution
from devsim.materials.light_sources import AM0
from devsim.mesh import Mesh
from devsim.models import BeerLambertModel
import ds


def enable_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


class SolarCell(Device):
    def __init__(self):
        # Define mesh. scale=1 means units are meters, the default is micrometers
        mesh = Mesh(dimension='2D')
        mesh.add_2d_line('x', 0.0,      1e-6, scale=1)
        mesh.add_2d_line('x', 0.5e-5,   1e-8, scale=1)
        mesh.add_2d_line('x', 1e-5,     1e-6, scale=1)
        mesh.add_2d_line('y', 0,        1e-6, scale=1)
        mesh.add_2d_line('y', 1e-5,     1e-6, scale=1)
        mesh.add_2d_line('x', -1e-8,     1e-8, scale=1)
        mesh.add_2d_line('x', 1.001e-5, 1e-8, scale=1)
        Si = materials.Silicon(taun=1e-8, taup=1e-8)
        mesh.add_2d_region(name='MyRegion', material=Si)
        mesh.add_2d_region(name='air1', material=Si, xl=-1e-8, xh=0)
        mesh.add_2d_region(name='air2', material=Si, xl=1.0e-5, xh=1.001e-5)
        mesh.add_2d_contact(name='top', material=materials.Metals.generic, region='MyRegion', yl=0.8e-5, yh=1e-5, xl=0, xh=0, bloat=1e-10)
        mesh.add_2d_contact(name='bot', material=materials.Metals.generic, region='MyRegion', xl=1e-5, xh=1e-5, bloat=1e-10)

        mesh.finalize()
        super(SolarCell, self).__init__('MyDevice', mesh)

        # This is specific to this device
        self.set_node_model('MyRegion', 'Acceptors', '1.0e16*step(0.5e-5-x)')
        self.set_node_model('MyRegion', 'Donors', '1.0e18*step(x-0.5e-5)')
        self.set_node_model('MyRegion', 'NetDoping', 'Donors-Acceptors')

scell = SolarCell()

# Stablish conditions (light)
# Setup the model
mdl = BeerLambertModel(scell, AM0(samples=25))
scell.setup_model(mdl)

# Solve Drift diffusion @ equilibrium
scell.initial_solution(region='MyRegion')
scell.solve(type="dc", absolute_error=1.0, relative_error=1e-12, maximum_iterations=30)

scell.export('scell_data_01.dat')
scell.export('scell_01.dat', format='devsim')

DriftDiffusionInitialSolution('MyDevice', 'MyRegion')
ds.solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
scell.print_currents()
#Look for V_oc
