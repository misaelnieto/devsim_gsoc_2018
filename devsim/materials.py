from enum import Enum

from devsim import PhysicalConstants


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
        props= [p for p in dir(self) if not p.startswith('_') and isinstance(getattr(self, p), MaterialProperty)]
        for pname in props:
            set_parameter(
                device=device_name,
                region=region_name,
                name=pname, value=getattr(self, pname)
            )


class Air(Material):
    name = 'air'

    refractive_index = {}


class Silicon(Material):
    """
    Cristaline Silicon material
    Provide alternate values for the
    parameters like this:

    s = Silicon(T=327, taun=1e16, taup=1.44e-6)
    """
    name = 'silicon'
    Permittivity = MaterialProperty(11.1 * PhysicalConstants.eps_0.value)
    n_i = MaterialProperty(1e10)

    # mu_n and mu_p are specific for Silicon
    mu_n = MaterialProperty(400)
    mu_p = MaterialProperty(200)

    # default SRH parameters
    n1 = MaterialProperty(1e10)
    p1 = MaterialProperty(1e10)
    taun = MaterialProperty(1e-5)
    taup = MaterialProperty(1e-5)

    def __init__(self, *args, **kwargs):
        super(Silicon, self).__init__(*args, **kwargs)


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
