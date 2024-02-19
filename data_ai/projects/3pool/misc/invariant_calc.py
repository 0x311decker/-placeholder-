from scipy.optimize import newton
import numpy as np

# Given data for the Curve 3pool
balances = np.array([74805452.85, 82108323.44, 35172872.71])  # DAI, USDC, USDT balances
A = 2000  # Amplification coefficient
n = 3  # Number of tokens in the pool

# Calculating sum and product of balances for the invariant equation
sum_xi = np.sum(balances)
prod_xi = np.prod(balances)

# Defining the StableSwap invariant function f(D) to solve for D
def f(D):
    return A * n ** n * sum_xi + D - A * n ** n * D - D ** (n + 1) / (n ** n * prod_xi)

# Initial guess for D, a reasonable starting point might be the sum of the balances
initial_guess = sum_xi

# Using SciPy's newton method to find the root of f(D)=0
# The scipy.optimize.newton function can automatically handle the derivative if not explicitly provided
D_solution = newton(f, initial_guess)

print("Solution for D:", D_solution)
