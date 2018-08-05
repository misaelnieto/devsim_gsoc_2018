import logging
from math import exp
import numpy as np

import ds
from devsim import PhysicalConstants
from devsim.materials.refractive_index import RefractiveIndex


class DevSimModel(object):
    def create_solution_variable(self, name):
        """
        Creates solution variables
        As well as their entries on each edge
        """
        for region in self.device.mesh.regions:
            ds.node_solution(name=name, device=self.device.name, region=region)
            ds.edge_from_node_model(node_model=name, device=self.device.name, region=region)


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
            print('Computing photogeneration for region: %s' % region)
            # Assume 1D for now
            nodes = ds.get_node_model_values(
                device=self.device.name,
                region=region,
                name='x'
            )
            pg = np.zeros((len(nodes), len(self.light_source)), dtype=float)
            rfidx = RefractiveIndex(region.material)
            for idx, x in enumerate(nodes):
                # I know, using unicode names here is asking for trouble
                # ..., but looks nice ;)
                for idλ, λ in enumerate(self.light_source):
                    P = self.light_source.irradiance
                    α = rfidx.alpha
                    Φ_0 = P(λ) * λ / PhysicalConstants.hc
                    η_g = 0.01
                    x_norm = x * 10e-2
                    pg[idx, idλ] = η_g * Φ_0 * exp(-α(λ) * x_norm)

            # Total photogeneration for each node
            # Conditions:
            #   100% quantum efficiency
            #   Ignoring reflection
            pgen_by_node = np.add.reduce(pg, 1)
            ds.node_solution(device=self.device.name, region=region, name='G_op')
            for i, v in enumerate(pgen_by_node):
                ds.set_node_value(
                    device=self.device.name,
                    region=region,
                    name='G_op',
                    index=i,
                    value=float(v)
                )
        ds.solve(type='dc', **kwargs)
