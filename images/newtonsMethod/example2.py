import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

x = np.zeros((1000, 1))

x[0] = 10.0  # initial guess

fig, ax = plt.subplots(1, 1)
func = (np.exp(x[0]) - np.tan(x[0]))
size = 10
ax.plot(x[0], func, 'o', color='r', ms=size)
for j in range(1000):
    # x_{n+1} = x_n - \frac{exp(x_n) - tan(x_n)}{exp(x_n) - sec^2(x_n)}
    x[j+1] = x[j] - (np.exp(x[j]) - np.tan(x[j])) / \
        (np.exp(x[j]) - (1/np.cos(x[j]))**2)

    # f(x) = exp(x) - tan(x)
    func = (np.exp(x[j+1]) - np.tan(x[j+1]))
    size -= 1
    ax.plot(x[j+1], func, 'o', color='b', ms=size)

    # termination criteria
    if np.abs(func) < 10**-6:
        break

# plt.gca().invert_xaxis()
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
plt.savefig('example2.png', dpi=300, bbox_inches='tight')
# plt.savefig('example2_badguess.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"The root of the function is: {x[j+1]}")
print(f"Function value at the root: {func}")
