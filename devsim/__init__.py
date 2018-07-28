from os.path import join as joinpath
from os.path import dirname, abspath
from ds import set_parameter


DS_DATADIR = abspath(joinpath(dirname(__file__), 'data'))


class ParameterEnum(object):
    def set_parameters_for(self, device, region):
        """
        Use this function to register the parameters of this class into the
        simulation context. Internally uses ds.set_parameters()
        """
        props = [
            pname for pname in dir(self)
            if not pname.startswith('_') and not callable(getattr(self, pname))
        ]

        for propname in props:
            set_parameter(
                device=device,
                region=region,
                name=propname,
                value=getattr(self, propname)
            )


class _PhysicalConstants(ParameterEnum):
    # Vacuum permittivity or Dielectric constant (F/cm^2)
    eps_0 = 8.85e-14
    # The electron charge (Couloumbs)
    q = 1.6e-19
    # Planck's constant (J/K)
    k = 1.3806503e-23

PhysicalConstants = _PhysicalConstants()


class _AmbientConditions(ParameterEnum):
    # Ambient temperature (k)
    T = 300

AmbientConditions = _AmbientConditions()
