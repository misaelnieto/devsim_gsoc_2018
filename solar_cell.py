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
    material=materials.Semiconductors.Silicon(taup=1e-8, taun=1e-8),
    tag1='top', tag2='bot')
pv_device = device.Device('SolarCell', mesh=mesh)
pv_device.create_node_model(substrate, 'Acceptors', '1.0e18*step(0.5e-5-x)')
pv_device.create_node_model(substrate, 'Donors', '1.0e18*step(x-0.5e-5)')
pv_device.create_node_model(substrate, 'NetDoping', 'Donors-Acceptors')

# ?? print_node_values(device=pv_device, region=region, name='NetDoping')

diode_common.InitialSolution(pv_device, region)


# Initial DC solution
solve(type='dc', absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

diode_common.DriftDiffusionInitialSolution(device, region)
###
### Drift diffusion simulation at equilibrium
###
solve(type='dc', absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)


####
#### Ramp the bias to 0.5 Volts
####
v = 0.0
while v < 0.51:
    set_parameter(device=device, name=GetContactBiasName('top'), value=v)
    solve(type='dc', absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
    pv_device.print_currents()
    v += 0.1

write_devices(file='diode_1d.dat', type='tecplot')
