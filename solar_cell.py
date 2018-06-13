import mesh
import device
import materials

mesh = mesh.Mesh('Cell Mesh')
mesh.add_line(pos=0, ps=1e-7, tag='top')
mesh.add_line(pos=0.5e-5, ps=1e-9, tag='middle')
mesh.add_line(pos=1e-5, ps=1e-7, tag='bottom')
mesh.add_contact(name='top', tag='top', material=materials.Metals.generic)
mesh.add_contact(name='bottom', tag='bottom', material=materials.Metals.generic)

substrate = 'Cell Substrate'
mesh.add_region(
    name=substrate,
    material=materials.Silicon(taup=1e-8, taun=1e-8),
    tag1='top', tag2='bottom'
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
