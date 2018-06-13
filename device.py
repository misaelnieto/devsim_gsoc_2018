import uuid
import logging

from ds import *

log = logging.getLogger("Device")


# TODO: Move this to the appropiate place
def CreateNodeModel(device, region, model, expression):
    """
        Creates a node model
    """
    result = node_model(
        device=device,
        region=region,
        name=model,
        equation=expression
    )
    log.debug("NODEMODEL {d} {r} {m} \"{re}\"".format(d=device, r=region, m=model, re=result))


# TODO: Move this to the appropiate place
def InNodeModelList(device, region, model):
    """
    Checks to see if this node model is available on device and region
    """
    return model in get_node_model_list(device=device, region=region)


# TODO: Move this to the appropiate place
def InEdgeModelList(device, region, model):
    """
        Checks to see if this edge model is available on device and region
    """
    return model in get_edge_model_list(device=device, region=region)


# TODO: Move this to the appropiate place
def CreateEdgeModel(device, region, model, expression):
    """
    Creates an edge model
    """
    result = edge_model(device=device, region=region, name=model, equation=expression)
    log.debug("EDGEMODEL {d} {r} {m} \"{re}\"".format(d=device, r=region, m=model, re=result))


# TODO: Move this to the appropiate place
def CreateNodeModelDerivative(device, region, model, expression, *args):
    """
    Create a node model derivative
    """
    for v in args:
        CreateNodeModel(
            device, region,
            "{m}:{v}".format(m=model, v=v),
            "simplify(diff({e},{v}))".format(e=expression, v=v)
        )


# TODO: Move this to the appropiate place
def CreateSiliconPotentialOnly(device, region):
    """
        Creates the physical models for a Silicon region
    """
    if not InNodeModelList(device, region, "Potential"):
        log("Creating Node Solution Potential")
        CreateSolution(device, region, "Potential")
    # require NetDoping
    intrinsics = (
        ("IntrinsicElectrons", "n_i*exp(Potential/V_t)"),
        ("IntrinsicHoles", "n_i^2/IntrinsicElectrons"),
        ("IntrinsicCharge", "kahan3(IntrinsicHoles, -IntrinsicElectrons, NetDoping)"),
        ("PotentialIntrinsicCharge", "-ElectronCharge * IntrinsicCharge")
    )
    for name, eq in intrinsics:
        CreateNodeModel(device, region, name, eq)
        CreateNodeModelDerivative(device, region, name, eq, "Potential")

    # TODO: Edge Average Model
    electrics = (
        ("ElectricField", "(Potential@n0-Potential@n1)*EdgeInverseLength"),
        ("PotentialEdgeFlux", "Permittivity * ElectricField")
    )
    for name, eq in electrics:
        CreateEdgeModel(device, region, name, eq)
        CreateEdgeModelDerivatives(device, region, name, eq, "Potential")

    equation(
        device=device, region=region,
        name="PotentialEquation", variable_name="Potential",
        node_model="PotentialIntrinsicCharge",
        edge_model="PotentialEdgeFlux",
        variable_update="log_damp"
    )


# TODO: Move this to the appropiate place
def CreateSiliconPotentialOnlyContact(device, region, contact, is_circuit=False):
    """
    Creates the potential equation at the contact
    if is_circuit is true, than use node given by GetContactBiasName
    """
    # Means of determining contact charge
    # Same for all contacts
    if not InNodeModelList(device, region, "contactcharge_node"):
        CreateNodeModel(device, region, "contactcharge_node", "ElectronCharge*IntrinsicCharge")
    # TODO: This is the same as D-Field
    if not InEdgeModelList(device, region, "contactcharge_edge"):
        CreateEdgeModel(device, region, "contactcharge_edge", "Permittivity*ElectricField")
        CreateEdgeModelDerivatives(device, region, "contactcharge_edge", "Permittivity*ElectricField", "Potential")


# TODO: Move this to the appropiate place
def CreateEdgeModelDerivatives(device, region, model, expression, variable):
    """
    Creates edge model derivatives
    """
    CreateEdgeModel(
        device, region,
        "{m}:{v}@n0".format(m=model, v=variable),
        "simplify(diff({e}, {v}@n0))".format(e=expression, v=variable)
    )
    CreateEdgeModel(
        device, region,
        "{m}:{v}@n1".format(m=model, v=variable),
        "simplify(diff({e}, {v}@n1))".format(e=expression, v=variable)
    )


# TODO: Move this to the appropiate place
def DriftDiffusionInitialSolution(device, region, circuit_contacts=None):
    # drift diffusion solution variables
    CreateSolution(device, region, "Electrons")
    CreateSolution(device, region, "Holes")

    # create initial guess from dc only solution
    set_node_values(device=device, region=region, name="Electrons", init_from="IntrinsicElectrons")
    set_node_values(device=device, region=region, name="Holes", init_from="IntrinsicHoles")

    # Set up equations
    CreateSiliconDriftDiffusion(device, region)
    for i in get_contact_list(device=device):
        if circuit_contacts and i in circuit_contacts:
            CreateSiliconDriftDiffusionAtContact(device, region, i, True)
        else:
            CreateSiliconDriftDiffusionAtContact(device, region, i)


# TODO: Move this to the appropiate place
def CreateSolution(device, region, name):
    """
        Creates solution variables
        As well as their entries on each edge
    """
    node_solution(name=name, device=device, region=region)
    edge_from_node_model(node_model=name, device=device, region=region)


class Device(object):
    """docstring for Device"""

    def __init__(self, name=None, mesh=None):
        self.name = name or 'device-%s' % str(uuid.uuid4())[:8]
        self.mesh = mesh
        create_device(mesh=self.mesh.name, device=self.name)

    def _contact_bias_name(self, contact):
        return "{0}_bias".format(contact)

    def print_currents(self):
        for c in self.mesh.contacts:
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
        log.debug("NODEMODEL {d} {r} {m} \"{re}\"".format(d=self.name, r=region, m=model, re=result))

    def create_solution(self, region, name):
        '''
        Creates solution variables
        As well as their entries on each edge
        '''
        node_solution(name=name, device=self.name, region=region)
        edge_from_node_model(node_model=name, device=self.name, region=region)

    def solve(self, *args, **kwargs):
        if not args and not kwargs:
            self.initial_solution()
        elif kwargs.get('type', '') == 'ramp':
            kwargs['type'] = 'dc'
            start = kwargs.pop('start')
            stop = kwargs.pop('stop')
            step = kwargs.pop('step')
            contact = kwargs.pop('contact')
            for v in range(start, stop, step):
                set_parameter(
                    device=self.name,
                    name=self._contact_bias_name(contact),
                    value=v
                )
                solve(**kwargs)
                self.print_currents()
        else:
            solve(*args, **kwargs)

    def initial_solution(self):
        region = self.mesh.regions[0]
        # Create Potential, Potential@n0, Potential@n1
        CreateSolution(self.name, region, "Potential")

        # Create potential only physical models
        # TODO: move to materials, relate region with material
        CreateSiliconPotentialOnly(self.name, region)

        # Set up the contacts applying a bias
        # TODO: Try to use self.contacts instead
        # it is more correct for the bias to be 0, and it looks like there is side effects

        for c in self.mesh.contacts:
            set_parameter(device=self.name, name=self._contact_bias_name(c), value=0.0)
            # TODO: move to models module
            CreateSiliconPotentialOnlyContact(self.name, region, c)

    def create_solution_variable(self, name):
        """
        Creates solution variables
        As well as their entries on each edge
        """
        node_solution(name=name, device=self.name, region=self.mesh.regions[0])
        edge_from_node_model(node_model=name, device=self.name, region=self.mesh.regions[0])

    def drift_diffusion_initial_solution(self):
        # TODO: move it to somewhere else
        # drift diffusion solution variables
        create_solution_variable("Electrons")
        create_solution_variable("Holes")

        # Create initial guess from DC only solution
        set_node_values(
            device=self.name,
            region=self.mesh.regions[0],
            name="Electrons",
            init_from="IntrinsicElectrons"
        )
        set_node_values(
            device=self.name,
            region=self.mesh.regions[0],
            name="Holes",
            init_from="IntrinsicHoles"
        )

        # Set up equations
        CreateSiliconDriftDiffusion(self.name, self.mesh.regions[0])
        for c in self.mesh.contacts:
            CreateSiliconDriftDiffusionAtContact(device, region, c)

    def export(self, filename, format):
        write_devices(file=filename, type=format)
