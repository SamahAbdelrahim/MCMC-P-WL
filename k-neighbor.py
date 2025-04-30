def find_nearest_object(proposal_params, object_database):
    """Find the nearest existing object to the proposed parameters"""
    distances = []
    for obj in object_database:
        # Calculate weighted Euclidean distance between normalized parameters
        dist = (
            5.0 * (proposal_params['num_extrusions_normalized'] - obj['num_extrusions_normalized'])**2 +
            2.0 * (proposal_params['extrusion_range_normalized'] - obj['extrusion_range_normalized'])**2 +
            1.0 * (proposal_params['rotation_range_normalized'] - obj['rotation_range_normalized'])**2
        )
        distances.append((np.sqrt(dist), obj))
    
    # Return the object with minimum distance
    return min(distances, key=lambda x: x[0])[1]