# from ds import *
# import diode_common
import mesh, device, materials


mesh = mesh.Mesh('Cell Mesh')
mesh.add_line(pos=0, ps=1e-7, tag='top')
mesh.add_line(pos=0.5e-5, ps=1e-9, tag='middle')
mesh.add_line(pos=1e-5, ps=1e-7, tag='bottom')
mesh.add_contact(name='top', tag='top', material=Metals.generic)
mesh.add_contact(name='bottom', tag='bottom', material=Metals.generic)
mesh.add_region(
    name='Cell Substrate',
    material=materials.Semiconductors.Silicon,
    tag1='top', tag2='bot')
device = device.Device("SolarCell", mesh=mesh)

region="MyRegion"

diode_common.CreateMesh(device=device, region=region)
  create_1d_mesh(mesh="dio")
  add_1d_mesh_line(mesh="dio", pos=0, ps=1e-7, tag="top")
  add_1d_mesh_line(mesh="dio", pos=0.5e-5, ps=1e-9, tag="mid")
  add_1d_mesh_line(mesh="dio", pos=1e-5, ps=1e-7, tag="bot")
  add_1d_contact  (mesh="dio", name="top", tag="top", material="metal")
  add_1d_contact  (mesh="dio", name="bot", tag="bot", material="metal")
  add_1d_region   (mesh="dio", material="Si", region=region, tag1="top", tag2="bot")
  finalize_mesh(mesh="dio")
  create_device(mesh="dio", device=device)

diode_common.SetParameters(device=device, region=region)
set_parameter(device=device, region=region, name="taun", value=1e-8)
set_parameter(device=device, region=region, name="taup", value=1e-8)

diode_common.SetNetDoping(device=device, region=region)

print_node_values(device=device, region=region, name="NetDoping")

diode_common.InitialSolution(device, region)

# Initial DC solution
solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)

diode_common.DriftDiffusionInitialSolution(device, region)
###
### Drift diffusion simulation at equilibrium
###
solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)


####
#### Ramp the bias to 0.5 Volts
####
v = 0.0
while v < 0.51:
    set_parameter(device=device, name=GetContactBiasName("top"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
    PrintCurrents(device, "top")
    PrintCurrents(device, "bot")
    v += 0.1

write_devices(file="diode_1d.dat", type="tecplot")
