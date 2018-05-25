contactcharge_node="contactcharge_node"
contactcharge_edge="contactcharge_edge"
ece_name="ElectronContinuityEquation"
hce_name="HoleContinuityEquation"
celec_model = "(1e-10 + 0.5*abs(NetDoping+(NetDoping^2 + 4 * n_i^2)^(0.5)))"
chole_model = "(1e-10 + 0.5*abs(-NetDoping+(NetDoping^2 + 4 * n_i^2)^(0.5)))"

# THe electron charge
q      = 1.6e-19 # Couloumbs
# Planck's constant
k      = 1.3806503e-23 # J/K
eps_0  = 8.85e-14 # F/cm^2
# Ambient temperature
T      = 300 # K
eps_si = 11.1
eps_ox = 3.9
