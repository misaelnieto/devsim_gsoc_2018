from devsim import PhysicalConstants
from devsim.materials import Material, MaterialProperty


class Silicon(Material):
    """
    Cristaline Silicon material
    Provide alternate values for the
    parameters like this:

    s = Silicon(T=327, taun=1e16, taup=1.44e-6)
    """
    name = 'silicon'
    Permittivity = MaterialProperty(11.1 * PhysicalConstants.eps_0)
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

