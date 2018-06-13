from constants import *
from enum import Enum


class Material(object):
    __material_name = 'isolator'

    def __repr__(self):
        return self.__material_name


class Metals(Enum):
    generic = 'metal'
    Aluminum = 2
    Copper = 3
    Titanium = 4
    Tungsten = 5
    Cobalt = 6


class Silicon(Material):
    """
    Silicon material
    Look at `self.parameters` for the material parameters
    """
    __material_name = 'silicon'
    __defaults = {
        "Permittivity": 11.1 * eps_0,
        "n_i": 1e10,
        "T": T,
        "kT": k * T,
        "V_t": k * T / q,
        # mu_n and mu_p are specific for Silicon
        "mu_n": 400,
        "mu_p": 200,
        # default SRH parameters
        "n1": 1e10,
        "p1": 1e10,
        "taun": 1e-5,
        "taup": 1e-5,
    }

    def __init__(self, **kwargs):
        """
        Creates a new Silicon material. Provide alternate values for the
        parameters like this:

        s = Silicon(T=327, taun=1e16, taup=1.44e-6)
        """
        self.parameters = self.__defaults.copy()
        self.parameters.update(kwargs)


class Semiconductors(Enum):
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
