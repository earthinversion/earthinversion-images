import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.style.use('seaborn')

# the governing equation


def heat_equations(t, T):
    k = 0.075
    C = 10
    T_f = 20
    return -k * (T - T_f) / C


# Time steps
teval = np.linspace(0, 1800, 1000)

# ivp solver: Runge-Kutta
sol = solve_ivp(heat_equations, (teval[0], teval[-1]), (30,), t_eval=teval)

fig, ax = plt.subplots()
ax.plot(sol.t, sol.y[0, :], "-k", ms=3, label='Scipy Runge-Kutta')

ax.set_ylabel("Temperature", fontsize=18)
ax.set_xlabel("Time", fontsize=18)
plt.legend()
plt.savefig('runge_kutta_heat_transfer_sol.png', dpi=300, bbox_inches='tight')
