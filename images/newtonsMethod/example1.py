import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

x = np.zeros((1000, 1))

x[0] = 5.0  # initial guess

fig, ax = plt.subplots(1, 1)
func = x[0]**3 - 3*x[0] + 1
size = 10
ax.plot(x[0], func, 'o', color='r', ms=size)
for j in range(1000):
    # x_{n+1} = x_n - \frac{x^3 - 3x + 1}{3x^2 - 3}
    x[j+1] = x[j] - (x[j]**3 - 3*x[j] + 1)/(3*x[j]**2 - 3)

    # f(x) = x^3 - 3x + 1
    func = x[j+1]**3 - 3*x[j+1] + 1
    size -= 1
    ax.plot(x[j+1], func, 'o', color='b', ms=size)

    # termination criteria
    if np.abs(func) < 10**-6:
        break

plt.gca().invert_xaxis()
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
plt.savefig('example1.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"The root of the function is: {x[j+1]}")
print(f"Function value at the root: {func}")
