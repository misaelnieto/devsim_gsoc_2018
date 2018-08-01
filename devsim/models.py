import logging
from ds import *

from devsim import PhysicalConstants
from devsim.materials.refractive_index import RefractiveIndex

log = logging.getLogger("Device")


class BeerLambertModel(object):
    """
    This is the simplest model to calculate absorption in multi-layer/region
    structure. Ignores the reflection in all interfaces.
    """

    name = 'Beer_Lambert'
    # phi_0 is the incident photon flux density
    ##  START HERE!!! You have to take the data from the light source and normalize to 1 μm²)
    phi_0 = 'P_λ * λ / (hv)'
    node_equation = '''
        phi_0 * exp(-alpha * x)
    '''

    def __init__(self, device, light_source):
        self.device = device
        self.light_source = light_source

    def solve(self, *args, **kwargs):
        for region in self.device.mesh.regions:
            rfidx = RefractiveIndex(region.material)
            λ = self.light_source.lambda_min
            # set_parameter(
            #     device=self.device.name,
            #     region=region,
            #     name="λ",
            #     value=λ
            # )
            # set_parameter(
            #     device=self.device.name,
            #     region=region,
            #     name="P_λ",
            #     value=self.light_source.photon_flux(λ)
            # )
            set_parameter(
                device=self.device.name,
                region=region,
                name="phi_0",
                value=self.light_source.photon_flux(λ) * λ / PhysicalConstants.hv
            )
            set_parameter(
                device=self.device.name,
                region=region,
                name="alpha",
                value=rfidx.alpha(λ)
            )
            result = node_model(
                device=self.device.name,
                region=region,
                name=self.name,
                equation=self.node_equation
            )

            log.debug(
                'Beer-Lambert model for device "{d}" (region: "{r}"); result: {re}'.format(
                    d=self.device, r=region, re=result
                )
            )
            node_solution(name=self.name, device=self.device.name, region=region)
            edge_from_node_model(node_model=self.name, device=self.device.name, region=region)
