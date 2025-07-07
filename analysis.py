import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import os
import json

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

# Convert chains to parameter values
def get_params_from_chains(chains, object_database):
    params = {
        'num_extrusions': [],
        'extrusion_range': [],
        'rotation_range': []
    }
    
    for chain in chains:
        for step in chain:
            # Extract parameters from each chain step
            # Assuming step contains parameter values
            if 'num_extrusions' in step:
                params['num_extrusions'].append(step['num_extrusions'])
            if 'extrusion_range' in step:
                params['extrusion_range'].append(step['extrusion_range'])
            if 'rotation_range' in step:
                params['rotation_range'].append(step['rotation_range'])
    
    return params

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
        plt.close()

# Main execution
if __name__ == "__main__":
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Load data and run analysis
    data_dir = 'data'  # Adjust path as needed
    complex_chains = load_all_chains(data_dir, 'complex')
    simple_chains = load_all_chains(data_dir, 'simple')
    
    # Load object database
    object_database = pd.read_csv('stimulus_database.csv')
    
    # Run comparison
    compare_distributions(complex_chains, simple_chains, object_database)