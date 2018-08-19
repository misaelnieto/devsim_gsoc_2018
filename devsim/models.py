import logging
from math import exp
import numpy as np

import ds
from devsim import PhysicalConstants
from devsim.materials.refractive_index import RefractiveIndex


log = logging.getLogger(__name__)


def model_exists(device, region, model):
    """
    Checks whether this node model is available on any device and region
    """
    return model in ds.get_node_model_list(device=device, region=region)


def create_solution(device, region, name):
    """
        Creates both node and edge solutions.
    """
    ds.node_solution(name=name, device=device, region=region)
    ds.edge_from_node_model(node_model=name, device=device, region=region)


def node_derivatives(device, region, model, expression, *args):
    """
    Create one or more node derivatives
    """
    for v in args:
        nd_name = "{m}:{v}".format(m=model, v=v)
        nd_eq = "simplify(diff({e},{v}))".format(e=expression, v=v)
        node_model(device, region, nd_name, nd_eq)


# TODO: Move this to the appropiate place
def edge_model_derivatives(device, region, model, expression, variable):
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


class DevSimModel(object):
    def create_solution_variable(self, name):
        """
        Creates solution variables
        As well as their entries on each edge
        """
        for region in self.device.mesh.regions:
            create_solution(device=self.device.name, region=region, name=name)


class BeerLambertModel(DevSimModel):
    """
    This is the simplest model to calculate absorption in multi-layer/region
    structure. Ignores the reflection in all interfaces.
    """

    name = 'Beer_Lambert'
    # TODO:  You have to take the data from the light source and normalize to 1 μm²)
    # phi_0 is the incident photon flux density
    # phi_0 = 'P_λ * λ / (hv)'
    node_equation = 'phi_0 * exp(alpha * x)'

    def __init__(self, device, light_source):
        self.device = device
        self.light_source = light_source
        self.create_solution_variable('G_op')

    def solve(self, *args, **kwargs):
        for region in self.device.mesh.regions:
            log.info('Computing photogeneration for region: %s' % region)
            # Assume 1D for now
            nodes = ds.get_node_model_values(
                device=self.device.name,
                region=region,
                name='x'
            )

            pg = np.zeros((len(nodes), len(self.light_source)), dtype=float)
            rfidx = RefractiveIndex(region.material)
            for idλ, λ in enumerate(self.light_source):
                # I know, using unicode names here is asking for trouble
                # ... but looks nice when using greek letters
                # TODO: compute the real reflection
                R = 0
                # λ is nm, but irradiance's units are W⋅m–2⋅nm–1
                P = self.light_source.irradiance(λ)
                Φ_0 = (P * λ * 1e-9 / PhysicalConstants.hc) * (1 - R)
                # α(λ)'s units are cm-1. But we use m
                α = rfidx.alpha(λ) * 1e+2
                # TODO: do not assume conversion efficiency is 100% (1 photon = 1EHP by now)
                η_g = 1.0

                # Debug
                print('\n' + '-'*70)
                print('Photogeneration dump. Parameters:')
                print('λ={:.2f} nm; P(λ)={:.2f}; Φ_0(λ)={:8.2e} m-2 s-1; α(λ)={:8.2e} m-1'.format(λ, P, Φ_0, α))
                print('-'*24)
                print('   x(μm)  |  G_op(x, λ)')
                print('-'*24)
                for idx, x in enumerate(nodes):
                    pg[idx, idλ] = η_g  * Φ_0 * exp(-α * x)
                    print('{:8.2f}  | {:8.2e}'.format(
                        x * 1e6, pg[idx, idλ]
                    ))

            # Total photogeneration for each node
            # Conditions:
            #   100% quantum efficiency
            #   Ignoring reflection
            pgen_by_node = np.add.reduce(pg, 1)
            for i, v in enumerate(pgen_by_node):
                ds.set_node_value(
                    device=self.device.name,
                    region=region,
                    name='G_op',
                    index=i,
                    value=float(v)
                )
        if 'type' in kwargs:
            ds.solve(**kwargs)
        else:
            ds.solve(type='dc', **kwargs)
