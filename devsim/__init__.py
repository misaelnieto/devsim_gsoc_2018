from enum import Enum
from ds import set_parameter


class ParameterEnum(Enum):
    def set_parameters_for(self, device, region):
        for propname, propvalue in Environment.__members__.items():
            set_parameter(
                device=device,
                region=region,
                name=propname,
                value=propvalue
            )


class PhysicalConstants(ParameterEnum):
    # Vacuum permittivity or Dielectric constant (F/cm^2)
    eps_0 = 8.85e-14
    # The electron charge (Couloumbs)
    q = 1.6e-19
    # Planck's constant (J/K)
    k = 1.3806503e-23


class Environment(ParameterEnum):
    # Ambient temperature (k)
    T = 300
