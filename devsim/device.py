import uuid
import logging

from ds import *
from devsim import PhysicalConstants, AmbientConditions

log = logging.getLogger("Device")

#TODO: move this to the appropiate place
contactcharge_node="contactcharge_node"
contactcharge_edge="contactcharge_edge"
ece_name="ElectronContinuityEquation"
hce_name="HoleContinuityEquation"
celec_model = "(1e-10 + 0.5*abs(NetDoping+(NetDoping^2 + 4 * n_i^2)^(0.5)))"
chole_model = "(1e-10 + 0.5*abs(-NetDoping+(NetDoping^2 + 4 * n_i^2)^(0.5)))"



# Make sure that the model exists, as well as it's node model
def EnsureEdgeFromNodeModelExists(device, region, nodemodel):
    """
    Checks if the edge models exists
    """
    if not InNodeModelList(device, region, nodemodel):
        raise("{} must exist" % (nodemodel))

    # emlist = get_edge_model_list(device=device, region=region)
    emtest = ("{0}@n0".format(nodemodel) and "{0}@n1".format(nodemodel))
    if not emtest:
        log.debug("INFO: Creating ${0}@n0 and ${0}@n1".format(nodemodel))
        edge_from_node_model(device=device, region=region, node_model=nodemodel)


def CreateElectronCurrent(device, region, mu_n):
    """
    Electron current
    """
    EnsureEdgeFromNodeModelExists(device, region, "Potential")
    EnsureEdgeFromNodeModelExists(device, region, "Electrons")
    EnsureEdgeFromNodeModelExists(device, region, "Holes")
    # Make sure the bernoulli functions exist
    if not InEdgeModelList(device, region, "Bern01"):
        CreateBernoulli(device, region)
    # test for requisite models here
    #  Jn = "ElectronCharge*{0}*EdgeInverseLength*V_t*(Electrons@n1*Bern10 - Electrons@n0*Bern01)".format(mu_n)
    Jn = "ElectronCharge*{0}*EdgeInverseLength*V_t*kahan3(Electrons@n1*Bern01,  Electrons@n1*vdiff,  -Electrons@n0*Bern01)".format(mu_n)
    #  Jn = "ElectronCharge*{0}*EdgeInverseLength*V_t*((Electrons@n1-Electrons@n0)*Bern01 +  Electrons@n1*vdiff)".format(mu_n)
    CreateEdgeModel(device, region, "ElectronCurrent", Jn)
    for i in ("Electrons", "Potential", "Holes"):
        CreateEdgeModelDerivatives(device, region, "ElectronCurrent", Jn, i)

def CreateHoleCurrent(device, region, mu_p):
    """
    Hole current
    """
    EnsureEdgeFromNodeModelExists(device, region, "Potential")
    EnsureEdgeFromNodeModelExists(device, region, "Holes")
    # Make sure the bernoulli functions exist
    if not InEdgeModelList(device, region, "Bern01"):
        CreateBernoulli(device, region)
    # test for requisite models here
    #  Jp ="-ElectronCharge*{0}*EdgeInverseLength*V_t*(Holes@n1*Bern01 - Holes@n0*Bern10)".format(mu_p)
    Jp ="-ElectronCharge*{0}*EdgeInverseLength*V_t*kahan3(Holes@n1*Bern01, -Holes@n0*Bern01, -Holes@n0*vdiff)".format(mu_p)
    #  Jp ="-ElectronCharge*{0}*EdgeInverseLength*V_t*((Holes@n1 - Holes@n0)*Bern01 - Holes@n0*vdiff)".format(mu_p)
    CreateEdgeModel(device, region, "HoleCurrent", Jp)
    for i in ("Holes", "Potential", "Electrons"):
        CreateEdgeModelDerivatives(device, region, "HoleCurrent", Jp, i)


def CreatePE(device, region):
    pne = "-ElectronCharge*kahan3(Holes, -Electrons, NetDoping)"
    CreateNodeModel(device, region, "PotentialNodeCharge", pne)
    CreateNodeModelDerivative(device, region, "PotentialNodeCharge", pne, "Electrons")
    CreateNodeModelDerivative(device, region, "PotentialNodeCharge", pne, "Holes")

    equation(device=device,
        region=region,
        name="PotentialEquation", variable_name="Potential",
        node_model="PotentialNodeCharge", edge_model="PotentialEdgeFlux",
        time_node_model="", variable_update="log_damp")


def CreateBernoulli(device, region):
    """
    Creates the Bernoulli function for Scharfetter Gummel
    """
    # test for requisite models here
    EnsureEdgeFromNodeModelExists(device, region, "Potential")
    vdiffstr = "(Potential@n0 - Potential@n1)/V_t"
    CreateEdgeModel(device, region, "vdiff", vdiffstr)
    CreateEdgeModel(device, region, "vdiff:Potential@n0", "V_t^(-1)")
    CreateEdgeModel(device, region, "vdiff:Potential@n1", "-vdiff:Potential@n0")
    CreateEdgeModel(device, region, "Bern01", "B(vdiff)")
    CreateEdgeModel(device, region, "Bern01:Potential@n0", "dBdx(vdiff) * vdiff:Potential@n0")
    CreateEdgeModel(device, region, "Bern01:Potential@n1", "-Bern01:Potential@n0")


def CreateSRH(device, region):
    USRH = "(Electrons*Holes - n_i^2)/(taup*(Electrons + n1) + taun*(Holes + p1))"
    Gn = "-ElectronCharge * USRH + G_op"
    Gp = "+ElectronCharge * USRH + G_op"
    CreateNodeModel(device, region, "USRH", USRH)
    CreateNodeModel(device, region, "ElectronGeneration", Gn)
    CreateNodeModel(device, region, "HoleGeneration", Gp)
    for i in ("Electrons", "Holes"):
        CreateNodeModelDerivative(device, region, "USRH", USRH, i)
        CreateNodeModelDerivative(device, region, "ElectronGeneration", Gn, i)
        CreateNodeModelDerivative(device, region, "HoleGeneration", Gp, i)


def CreateECE(device, region, mu_n):
    CreateElectronCurrent(device, region, mu_n)

    NCharge = "ElectronCharge * Electrons"
    CreateNodeModel(device, region, "NCharge", NCharge)
    CreateNodeModelDerivative(device, region, "NCharge", NCharge, "Electrons")

    equation(
        device=device, region=region,
        name="ElectronContinuityEquation", variable_name="Electrons",
        time_node_model="NCharge",
        edge_model="ElectronCurrent", variable_update="positive", node_model="ElectronGeneration"
    )


def CreateHCE(device, region, mu_p):
    CreateHoleCurrent(device, region, mu_p)
    PCharge = "-ElectronCharge * Holes"
    CreateNodeModel(device, region, "PCharge", PCharge)
    CreateNodeModelDerivative(device, region, "PCharge", PCharge, "Holes")

    equation(
        device=device, region=region, name="HoleContinuityEquation",
        variable_name="Holes",
        time_node_model="PCharge",
        edge_model="HoleCurrent", variable_update="positive",
        node_model="HoleGeneration"
    )


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


def CreateContactNodeModel(device, contact, model, expression):
    """
    Creates a contact node model
    """
    result = contact_node_model(device=device, contact=contact, name=model, equation=expression)
    log.debug("CONTACTNODEMODEL {d} {c} {m} \"{re}\"".format(d=device, c=contact, m=model, re=result))


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
def CreateSiliconDriftDiffusion(device, region, mu_n="mu_n", mu_p="mu_p"):
    CreatePE(device, region)
    CreateBernoulli(device, region)
    CreateSRH(device, region)
    CreateECE(device, region, mu_n)
    CreateHCE(device, region, mu_p)


# TODO: Move this to the appropiate place
def CreateSiliconDriftDiffusionAtContact(device, region, contact, is_circuit=False):
    """
        Restrict electrons and holes to their equilibrium values
        Integrates current into circuit
    """
    contact_electrons_model = "Electrons - ifelse(NetDoping > 0, {0}, n_i^2/{1})".format(celec_model, chole_model)
    contact_holes_model = "Holes - ifelse(NetDoping < 0, +{1}, +n_i^2/{0})".format(celec_model, chole_model)
    contact_electrons_name = "{0}nodeelectrons".format(contact)
    contact_holes_name = "{0}nodeholes".format(contact)

    CreateContactNodeModel(device, contact, contact_electrons_name, contact_electrons_model)
    # TODO: The simplification of the ifelse statement is time consuming
    #  CreateContactNodeModelDerivative(device, contact, contact_electrons_name, contact_electrons_model, "Electrons")
    CreateContactNodeModel(device, contact, "{0}:{1}".format(contact_electrons_name, "Electrons"), "1")

    CreateContactNodeModel(device, contact, contact_holes_name, contact_holes_model)
    CreateContactNodeModel(device, contact, "{0}:{1}".format(contact_holes_name, "Holes"), "1")

    # TODO: keyword args
    if is_circuit:
        contact_equation(
            device=device,
            contact=contact,
            name="ElectronContinuityEquation",
            variable_name="Electrons",
            node_model=contact_electrons_name,
            edge_current_model="ElectronCurrent",
            circuit_node=GetContactBiasName(contact)
        )

        contact_equation(
            device=device,
            contact=contact,
            name="HoleContinuityEquation",
            variable_name="Holes",
            node_model=contact_holes_name,
            edge_current_model="HoleCurrent",
            circuit_node=GetContactBiasName(contact)
        )
    else:
        contact_equation(
            device=device,
            contact=contact,
            name="ElectronContinuityEquation",
            variable_name="Electrons",
            node_model=contact_electrons_name,
            edge_current_model="ElectronCurrent")

        contact_equation(
            device=device,
            contact=contact,
            name="HoleContinuityEquation",
            variable_name="Holes",
            node_model=contact_holes_name,
            edge_current_model="HoleCurrent")


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
        self._models = []

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

    def set_node_model(self, region, model, expression):
        node_model(device=self.name, region=region, name=model, equation=expression)

    def initial_solution(self):
        self.setup_parameters()
        for region in self.mesh.regions:
            # Create Potential, Potential@n0, Potential@n1
            self.create_solution(region, "Potential")

            # Create potential only physical models
            # TODO: move to materials, relate region with material
            CreateSiliconPotentialOnly(self.name, region)

            # Set up the contacts applying a bias
            # TODO: Try to use self.contacts instead it is more correct for
            # the bias to be 0, and it looks like there are side effects

            for c in self.mesh.contacts:
                set_parameter(device=self.name, name=self._contact_bias_name(c), value=0.0)
                # TODO: move to models module
                CreateSiliconPotentialOnlyContact(self.name, region, c)

    def create_solution(self, region, solution_name):
        '''
        Creates solution variables
        As well as their entries on each edge
        '''
        node_solution(name=solution_name, device=self.name, region=region)
        edge_from_node_model(
            node_model=solution_name, device=self.name, region=region
        )

    def create_solution_variable(self, name):
        """
        Creates solution variables
        As well as their entries on each edge
        TODO: this was replicated
        """
        for region in self.mesh.regions:
            node_solution(device=self.name, region=region, name=name)
            edge_from_node_model(device=self.name, region=region, node_model=name)

    def drift_diffusion_initial_solution(self):
        # TODO: move it to somewhere else
        # drift diffusion solution variables
        self.create_solution_variable("Electrons")
        self.create_solution_variable("Holes")

        for region in self.mesh.regions:
            # Create initial guess from DC only solution
            set_node_values(
                device=self.name,
                region=region.name,
                name="Electrons",
                init_from="IntrinsicElectrons"
            )
            set_node_values(
                device=self.name,
                region=region.name,
                name="Holes",
                init_from="IntrinsicHoles"
            )

            # Set up equations
            region.material.setup_models(self.name, region.name)
            region.material.setup_contacts(self.name, region.name, mesh.contacts)

    def setup_model(self, model):
        self._models.append(model)

    def setup_parameters(self):
        """
            Initialize the context for the simulation.
            Region is an instance of the mesh.Region class
        """
        for region in self.mesh.regions:
            PhysicalConstants.set_parameters_for(self.name, region.name)
            AmbientConditions.set_parameters_for(self.name, region.name)
            region.material.set_parameters_for(self.name, region.name)

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

        for mdl in self._models:
            mdl.solve(*args, **kwargs)

    def export(self, filename, format='devsim_data'):
        write_devices(file=filename, type=format)
