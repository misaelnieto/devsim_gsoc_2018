import logging

import ds
from devsim import models as ds_models
from devsim import PhysicalConstants
from .base import Material, MaterialProperty

log = logging.getLogger('Material (Silicon)')


class Silicon(Material):
    '''
    Cristaline Silicon material
    Provide alternate values for the
    parameters like this:

    s = Silicon(T=327, taun=1e16, taup=1.44e-6)
    '''
    name = 'silicon'
    Permittivity = MaterialProperty(11.1 * PhysicalConstants.eps_0)
    n_i = MaterialProperty(1e10)

    # mu_n and mu_p are specific for Silicon
    mu_n = MaterialProperty(400)
    mu_p = MaterialProperty(200)

    # default SRH parameters
    n1 = MaterialProperty(1e10)
    p1 = MaterialProperty(1e10)
    taun = MaterialProperty(1e-5)
    taup = MaterialProperty(1e-5)

    def set_parameters_for(self, device_name, region_name):
        super(Silicon, self).set_parameters_for(device_name, region_name)

    def setup_models(self, device, region):
        '''
            Creates the models for a Silicon region. It is here because Silicon
            should know to be simulated.

            This was called CreateSiliconDriftDiffusion.
        '''
        #######################################################################
        ## Potential on the Silicon material
        ## (CreateSiliconDriftDiffusion)
        if not ds_models.model_exists(device, region, 'Potential'):
            ds_models.create_solution(device, region, 'Potential')

        # TODO: require NetDoping
        intrinsics = (
            ('IntrinsicElectrons', 'n_i*exp(Potential/V_t)'),
            ('IntrinsicHoles', 'n_i^2/IntrinsicElectrons'),
            ('IntrinsicCharge', 'kahan3(IntrinsicHoles, -IntrinsicElectrons, NetDoping)'),
            ('PotentialIntrinsicCharge', '-ElectronCharge * IntrinsicCharge')
        )
        for name, eq in intrinsics:
            ds.node_model(device=device, region=region, name=model, equation=eq)
            ds_models.node_derivatives(device, region, name, eq, 'Potential')

        # TODO: Edge Average Model
        electrics = (
            ('ElectricField', '(Potential@n0-Potential@n1)*EdgeInverseLength'),
            ('PotentialEdgeFlux', 'Permittivity * ElectricField')
        )
        for name, eq in electrics:
            ds.edge_model(device, region, name, eq)
            ds.edge_model(device, region,
                '{}:Potential@n0'.format(name),
                'simplify(diff({}, Potential@n0))'.format(eq)
            )
            ds.edge_model(device, region,
                '{}:Potential@n1'.format(name),
                'simplify(diff({}, Potential@n1))'.format(eq)
            )

        equation(
            device=device, region=region,
            name='PotentialEquation', variable_name='Potential',
            node_model='PotentialIntrinsicCharge',
            edge_model='PotentialEdgeFlux',
            variable_update='log_damp'
        )

        #######################################################################
        ## Potential at the contact with Silicon (was CreateSiliconPotentialOnlyContact)
        if not ds_models.model_exists(device, region, 'contactcharge_node'):
            ds.node_model(device, region, 'contactcharge_node', 'ElectronCharge*IntrinsicCharge')
        # TODO: This is the same as D-Field
        if not ds_models.model_exists(device, region, 'contactcharge_edge'):
            ds.edge_model(device, region,
                'contactcharge_edge', 'Permittivity*ElectricField')
            ds.edge_model(device, region,
                'Potential:contactcharge_edge@n0',
                'simplify(diff(Potential, contactcharge_edge@n0))'.format()
            )
            ds.edge_model(device, region,
                'Potential:contactcharge_edge@n1',
                'simplify(diff({e}, contactcharge_edge@n01))'.format()
            )

    def setup_contacts(self, device, region, contacts):
        # I'm being lazy and just imported the function instead of porting it.
        from device import CreateSiliconDriftDiffusionAtContact
        for c in contacts:
            CreateSiliconDriftDiffusionAtContact(self.name, region.name, c)
