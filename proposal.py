def generate_proposal(current_params, step_size=0.1):
    proposal = {}
    # Apply random changes to each parameter
    proposal['num_extrusions'] = max(1, current_params['num_extrusions'] + 
                                    np.random.normal(0, step_size * 3))  # Larger step for discrete param
    proposal['min_extrude'] = max(0.05, current_params['min_extrude'] + 
                                 np.random.normal(0, step_size * 0.05))
    proposal['max_extrude'] = max(proposal['min_extrude'] + 0.01, 
                                 current_params['max_extrude'] + 
                                 np.random.normal(0, step_size * 0.05))
    proposal['min_rotation'] = max(0, current_params['min_rotation'] + 
                                  np.random.normal(0, step_size * 15))
    proposal['max_rotation'] = max(proposal['min_rotation'] + 5, 
                                  current_params['max_rotation'] + 
                                  np.random.normal(0, step_size * 15))
    
    # Calculate derived parameters
    proposal['extrusion_range'] = proposal['max_extrude'] - proposal['min_extrude']
    proposal['rotation_range'] = proposal['max_rotation'] - proposal['min_rotation']
    
    return proposal