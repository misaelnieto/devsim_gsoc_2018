import sys
import logging

from devsim import materials
from devsim.device import Device, DriftDiffusionInitialSolution
from devsim.materials.light_sources import AM0
from devsim.mesh import Mesh
from devsim.models import BeerLambertModel
import ds


# Enable logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

class SolarCell(Device):
    def __init__(self):
        # Define mesh (default units are micrometers)
        mesh = Mesh()
        mesh.add_line(0.0, 0.1, 'top')
        mesh.add_line(5, 1, 'mid')
        mesh.add_line(100, 1, 'bottom')
        mesh.add_contact(name='top', tag='top', material=materials.Metals.generic)
        mesh.add_contact(name='bottom', tag='bottom', material=materials.Metals.generic)
        Si = materials.Silicon(taun=1e-8, taup=1e-8)
        mesh.add_region(name='MyRegion', material=Si, tag1='top', tag2='bottom')
        mesh.finalize()
        super(SolarCell, self).__init__('MySolarCell', mesh)

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
scell.initial_solution('MyRegion')
scell.solve(type="dc", absolute_error=1.0, relative_error=1e-12, maximum_iterations=30)

scell.export('scell_data_01.dat')
scell.export('scell_01.dat', format='devsim')

DriftDiffusionInitialSolution('MySolarCell', 'MyRegion')
ds.solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
#Look for V_oc
# scell.print_currents()
