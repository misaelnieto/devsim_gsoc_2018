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
    # Vacuum permittivity or Dielectric constant (F/cm)
    eps_0 = 8.854_187_817e-14
    # The electron charge (Couloumbs)
    q = 1.602_176_46e-19
    ElectronCharge = q
    # Boltzmann constant (J/K)
    k = 1.380_648_52e-23
    # Speed of light in vacuum (m/s)
    c = 299_792_458
    # The Planck Constant (J*s)
    h = 6.626_0697e-34
    # Planck's constant times speed of light (J*m)
    hc = 1.986_445_683e-25


PhysicalConstants = _PhysicalConstants()


class _AmbientConditions(ParameterEnum):
    # Ambient temperature (k)
    T = 300

    @property
    def kT(self):
        return PhysicalConstants.k * self.T

    @property
    def V_t(self):
        return self.kT/PhysicalConstants.q


AmbientConditions = _AmbientConditions()
