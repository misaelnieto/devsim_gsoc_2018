
class BeerLambert(object):
    """
    This is the simplest model to calculate absorption
    in multi-layer/region structure. Ignores the reflection in all 
    interfaces.
    """

    node_model = ''''''
    def __init__(self, device, region, light_source):
        super(BeerLambert, self).__init__()
        self.device, self.region = device, region
        self.material = region.material
        CreateNodeModel(device, region, 'Beer-Lambert', '''

        ''')