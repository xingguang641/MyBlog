import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- Step 1: Simulate Input Data ---
# Simulate a batch of activation values, intentionally making the mean non-zero
# Example: Mean = 5.0, Standard Deviation = 2.0
np.random.seed(42)
input_data = np.random.normal(loc=5.0, scale=2.0, size=1000)

# Simulate BN's Learnable Parameters
# gamma and beta are optimized during training
gamma = 1.5  # Scaling Factor
beta = -1.0  # Shifting Factor
epsilon = 1e-5 # Small value to prevent division by zero

print(f"Original Data Mean: {np.mean(input_data):.2f}")
print(f"Original Data Variance: {np.var(input_data):.2f}\n")


# --- Step 2: Batch Normalization Calculation Process ---

# 2.1 Compute Batch Statistics
mu = np.mean(input_data)         # Batch Mean
variance = np.var(input_data)   # Batch Variance

# 2.2 Normalization
# x_hat = (x - mu) / sqrt(var + epsilon)
normalized_data = (input_data - mu) / np.sqrt(variance + epsilon)

# 2.3 Scale and Shift
# y = gamma * x_hat + beta
output_data = gamma * normalized_data + beta


# --- Step 3: Visualization Results ---

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
bins = 40 # Number of histogram bins

# 1. Original Data (Input)
axes[0].hist(input_data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
axes[0].axvline(mu, color='red', linestyle='dashed', linewidth=2, label=f'Mean={mu:.2f}')
axes[0].set_title(f'Input Data', fontsize=12)
axes[0].legend(loc='upper right')
axes[0].set_xlabel('Value')
axes[0].set_ylabel('Frequency')

# 2. Normalized Data (Normalized)
mean_norm = np.mean(normalized_data)
var_norm = np.var(normalized_data)
axes[1].hist(normalized_data, bins=bins, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1].axvline(mean_norm, color='red', linestyle='dashed', linewidth=2, label=f'Mean={mean_norm:.2f}')
axes[1].set_title(f'Normalized Data', fontsize=12)
axes[1].legend(loc='upper right')
axes[1].set_xlabel('Value')

# 3. BN Final Output (Output)
mean_out = np.mean(output_data)
var_out = np.var(output_data)
axes[2].hist(output_data, bins=bins, color='salmon', edgecolor='black', alpha=0.7)
axes[2].axvline(mean_out, color='red', linestyle='dashed', linewidth=2, label=f'Mean={mean_out:.2f}')
axes[2].set_title(f'BN Final Output', fontsize=12)
axes[2].legend(loc='upper right')
axes[2].set_xlabel('Value')


# Overall Styling (Main Title is in English)
plt.suptitle('Batch Normalization Core Workflow Visualization', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout for suptitle
plt.show()

print(f"\nNormalized Data Mean: {mean_norm:.2f}")
print(f"Normalized Data Variance: {var_norm:.2f}")
print(f"Final Output Data Mean: {mean_out:.2f}")
print(f"Final Output Data Variance: {var_out:.2f}")