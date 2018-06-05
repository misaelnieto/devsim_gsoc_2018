import uuid
import logging
log = logging.getLogger("Device")


class Device(object):
    """docstring for Device"""
    def __init__(self, name=None, mesh):
        self.name = name or 'device-%s' % str(uuid.uuid4())[:8]
        self.mesh = mesh
        self.mesh.finalize()
        create_device(mesh=self.mesh, device=self.name)

    def _contact_bias_name(self, contact):
        return "{0}_bias".format(contact)

    def print_currents(self):
        for c in self.mesh._contacts:
            bias_name = self._contact_bias_name(c)
            e_current = get_contact_current(
                device=device, contact=c, equation='ElectronContinuityEquation'
            )
            h_current = get_contact_current(
                device=device, contact=c, equation='HoleContinuityEquation'
            )
            total_current = e_current + h_current
            voltage = get_parameter(
                device=device,
                name=self._contact_bias_name(contact)
            )
        log.info("{0}\t{1}\t{2}\t{3}\t{4}".format(contact, voltage, e_current, h_current, total_current))

    def create_node_model(self, region, model, expression):
        result = node_model(device=self.name, region=region, name=model, equation=expression)
        log.debug("NODEMODEL {d} {r} {m} \"{re}\"".format(d=device, r=region, m=model, re=result))

    def create_solution(self, region, name):
      '''
        Creates solution variables
        As well as their entries on each edge
      '''
      node_solution(name=name, device=self.name, region=region)
      edge_from_node_model(node_model=name, device=self.name, region=region)

    def compute_initial_solution(self, region, circuit_contacts=None):
        # Create Potential, Potential@n0, Potential@n1
        CreateSolution(device, region, "Potential")

        # Create potential only physical models
        CreateSiliconPotentialOnly(device, region)

        # Set up the contacts applying a bias
        for i in get_contact_list(device=device):
            if circuit_contacts and i in circuit_contacts:
                    CreateSiliconPotentialOnlyContact(device, region, i, True)
            else:
                ###print "FIX THIS"
                ### it is more correct for the bias to be 0, and it looks like there is side effects
                set_parameter(device=device, name=GetContactBiasName(i), value=0.0)
                CreateSiliconPotentialOnlyContact(device, region, i)

