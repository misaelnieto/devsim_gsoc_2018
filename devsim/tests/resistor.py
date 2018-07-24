import mesh
import device
import materials

mesh = mesh.Mesh('Cell Mesh')
# default units are micrometers
mesh.add_line(0.0, 0.01, 'left')
mesh.add_line(10.0, 1.0, 'right')
mesh.add_contact(name='left', tag='left', material=materials.Metals.generic)
mesh.add_contact(name='right', tag='right', material=materials.Metals.generic)

region_name = 'Substrate'
mesh.add_region(
    name=region_name,
    material=materials.Silicon(),
    tag1='left', tag2='right'
)
mesh.finalize()

resistor = device.Device('Resistor', mesh=mesh)
resistor.create_node_model(region_name, 'Acceptors', '1.0e16')
resistor.create_node_model(region_name, 'Donors', '1.0e4')
resistor.create_node_model(region_name, 'NetDoping', 'Donors-Acceptors')
resistor.solve()
resistor.solve(type='dc', absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

# TODO: move this to another place, maybe solution module?
resistor.drift_diffusion_initial_solution()

# Drift diffusion simulation at equilibrium
resistor.solve(type='dc', absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
resistor.export('resistor.dat')
