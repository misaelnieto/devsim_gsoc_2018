import uuid


class Device(object):
	"""docstring for Device"""
	def __init__(self, name=None, mesh):
		self.name = name or 'device-%s'%str(uuid.uuid4())[:8]
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
        print ("{0}\t{1}\t{2}\t{3}\t{4}".format(contact, voltage, e_current, h_current, total_current))
