import numpy as np
import matplotlib.pyplot as plt
from scipy. integrate import solve_ivp
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
ax.plot(sol.t, sol.y[0, :], "-k", ms=3, label='Solution 1: Runge-Kutta')


t = 0  # initial time
T = 30  # initial temperature

ax.plot([t], [T], "*r", ms=10, label='Initial value')

# Euler method: sol 2
time = [t]
temperature = [T]

delta_t = np.diff(teval)[0]  # 1.8018 for 1000 points

while t <= 1800:
    T += delta_t * heat_equations(t, T)
    t += delta_t
    time.append(t)
    temperature.append(T)

ax.plot(time, temperature, 'b:', ms=0.5, label='Solution 2: Euler Method')
ax.set_ylabel("Temperature", fontsize=18)
ax.set_xlabel("Time", fontsize=18)
plt.legend()
plt.savefig('euler_sol.png', dpi=300, bbox_inches='tight')

# # Error estimation
# E =
