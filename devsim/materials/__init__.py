from enum import Enum

from .silicon import Silicon


class MaterialProperty(object):
    def __init__(self, value):
        self.value = value


class Material(object):
    name = 'isolator'
    __parameters = None

    def __init__(self, **kwargs):
        self.__parameters = []
        for name, value in kwargs.items():
            setattr(self, name, value)
            self.__parameters.append(name)

    def __repr__(self):
        return self.name

    def set_parameters_for(self, device_name, region_name):
        from ds import set_parameter
        props = [
            p for p in dir(self)
            if not p.startswith('_') and isinstance(getattr(self, p), MaterialProperty)
        ]
        for pname in props:
            set_parameter(
                device=device_name,
                region=region_name,
                name=pname, value=getattr(self, pname)
            )


class Air(Material):
    name = 'air'
    refractive_index = {}


##############################################################################
# Enums below
class Metals(Enum):
    generic = 'metal'
    Aluminum = 2
    Copper = 3
    Titanium = 4
    Tungsten = 5
    Cobalt = 6


class Semiconductors(object):
    Silicon = Silicon
    Si = Silicon
    # PolySilicon = 2
    # Poly = 2
    # PolySi = 2
    # GaAs = 3
    # AlGaAs = 4
    # InGaAs = 5
    # SiGe = 6
    # InP = 7
    # Germanium = 8
    # Ge = 8
    # SiC_4H = 9
    # SiC_6H = 10
    # SiC_3C = 11


class Insulators(Enum):
    Photoresist = 1
    Oxide = 2
    SiO2 = 2
    Nitride = 3


class Impurities(Enum):
    Aluminum = 1
    Al = 1

    Antimony = 2
    Sb = 2

    Arsenic = 3
    As = 3

    Beryllium = 4
    Be = 4

    Boron = 5
    B = 5

    Carbon = 6
    C = 6

    Phosphorous = 7
    Phos = 7
    P = 7
