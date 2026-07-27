from scipy.optimize import minimize
import numpy as np
from Trans_Ag_film import sim_eot

def fom(params):
    """
    Calculates the figure of merit (FOM) to be minimized.

    Args:
        params (list or numpy.ndarray): A list or array containing l1 and l2.

    Returns:
        float: The negative FOM value to be minimized.
    """
    l1, l2 = params
    trans = sim_eot(l1, l2)
    fmax = trans * (1 - l1*l2)**4
    fmin = -fmax
    return fmin

# List to store history
history = []

def callback(params):
    """
    Callback function to store and print optimization history.

    Args:
        params (numpy.ndarray): The current parameter values (l1, l2).
    """
    l1, l2 = params
    fval = fom(params)
    history.append([l1, l2, fval])
    print(f"Iteration: l1={l1:.6f}, l2={l2:.6f}, fom={fval:.6e}")

# Define bounds for the 2 parameters
bounds = [(0, 1), (0, 1)]  # l1, l2

# Initial guess: random values within bounds
initial_guess = [0.19, 0.2]

#initial_simplex = np.array([[0.21, 0.19], [0.2, 0.2], [0.19, 0.21]])
initial_simplex = np.random.rand(3,2)/10 + 0.2
# Set Optimization Options
options = {
    'disp': True,           # Print convergence messages
    'xatol': 1e-6,          # Absolute error in xopt between iterations
    'fatol': 1e-6,          # Absolute error in func(xopt) between iterations
    'adaptive': True,       # Use adaptive parameters
    'maxfev': 100,
    'initial_simplex': initial_simplex
}

result = minimize(
    fom,                    # Function to minimize
    initial_guess,          # Starting point
    method='Nelder-Mead',   # Use Nelder-Mead method
    bounds=bounds,          # Parameter constraints
    options=options,
    callback=lambda x: callback(x) #modified callback to accept x as argument
)

# Extract results
best_params = result.x
best_value = result.fun

# Print results
print("\nOptimization Results:")
print("Best parameters (l_i):")
for i, d in enumerate(best_params):
    print(f"l_{i+1} = {d:.2e}")
print(f"Minimum value of f: {best_value:.2e}")

# Save history to a text file
with open('optimization_history.txt', 'w') as f:
    f.write("Iteration\tl1\tl2\tfom\n")
    for i, (l1, l2, fval) in enumerate(history):
        f.write(f"{i}\t{l1:.6e}\t{l2:.6e}\t{fval:.6e}\n")

print("\nHistory saved to 'optimization_history.txt'")