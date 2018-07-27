import logging
from ds import *

log = logging.getLogger("Device")


class BeerLambertModel(object):
    """
    This is the simplest model to calculate absorption in multi-layer/region
    structure. Ignores the reflection in all interfaces.
    """

    name = 'Beer-Lambert'
    node_equation = '''
        phi = phi_0 * exp(-alpha * x)
    '''

    def __init__(self, device, light_source):
        self.device = device
        self.light_source = light_source

        for region in device.mesh.regions:
            result = node_model(
                device=device.name,
                region=region,
                name='Beer-Lambert',
                equation=self.node_equation
            )
            set_parameter(
                device=device.name,
                region=region,
                name="phi_0",
                value=1e-8
            )

            log.debug(
                'Beer-Lambert model for device "{d}" (region: "{r}"); result: {re}'.format(
                    d=device, r=region, re=result
                )
            )

    def solve(self, *args, **kwargs):
        for region in device.mesh.regions:
            node_solution(name)
            node_solution(name=self.name, device=self.device.name, region=region)
            edge_from_node_model(node_model=self.name, device=self.device.name, region=region)
