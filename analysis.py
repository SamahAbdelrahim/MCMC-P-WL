import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

# Load all chain data
def load_all_chains(data_dir, condition):
    chains = []
    for file in os.listdir(data_dir):
        if file.endswith(f'_{condition}.json'):
            with open(os.path.join(data_dir, file), 'r') as f:
                chain_data = json.load(f)
                # Remove burn-in period
                chains.append(chain_data['chain_history'][15:])
    return chains

# Compare distributions between conditions
def compare_distributions(complex_chains, simple_chains, object_database):
    # Convert chains to parameter values
    complex_params = get_params_from_chains(complex_chains, object_database)
    simple_params = get_params_from_chains(simple_chains, object_database)
    
    # Create density estimates
    for param in ['num_extrusions', 'extrusion_range', 'rotation_range']:
        plt.figure(figsize=(10, 6))
        
        # Plot complex condition
        sns.kdeplot(complex_params[param], label='Complex')
        
        # Plot inverted simple condition
        sns.kdeplot(simple_params[param], label='Simple (inverted)')
        
        plt.title(f'Distribution of {param}')
        plt.legend()
        plt.savefig(f'results/{param}_distribution.png')