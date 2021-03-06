import logging
from ds import set_parameter

log = logging.getLogger(__name__)

class MaterialProperty(object):
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other


class Material(object):
    name = 'isolator'

    def __init__(self, **kwargs):
        self.__parameters = []
        for name, value in kwargs.items():
            setattr(self, name, MaterialProperty(value))

    def __repr__(self):
        return self.name

    def set_parameters_for(self, device_name, region_name):
        props = [
            p for p in dir(self)
            if not p.startswith('_') and isinstance(getattr(self, p), MaterialProperty)
        ]
        for pname in props:
            set_parameter(
                device=device_name,
                region=region_name,
                name=pname, value=getattr(self, pname).value
            )
            log.debug('set_parameter(device={}, region={}, name={}, value={})'.format(
                device_name, region_name, pname, getattr(self, pname).value))

