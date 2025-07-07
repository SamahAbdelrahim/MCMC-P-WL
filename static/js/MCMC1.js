const experimentSetup = {
    totalTrials: 80,
    burnInTrials: 15,
    currentTrial: 0,
    currentState: null,  // Current object
    objectDatabase: [],  // Will be populated with your stimulus data
    chainHistory: [],    // Track the chain's path
    condition: "complex"  // or "simple" 
};

// Initialize experiment
function initExperiment() {
    // Load object database from your CSV/JSON
    loadObjectDatabase().then(() => {
        // Select random starting object
        experimentSetup.currentState = getRandomObject();
        experimentSetup.chainHistory.push(experimentSetup.currentState.object_id);
        
        // Start first trial
        runTrial();
    });
}

// Run a single trial
function runTrial() {
    // Generate proposal
    const proposalParams = generateProposal(experimentSetup.currentState);
    const proposalObject = findNearestObject(proposalParams);
    
    // Display current state and proposal
    if (Math.random() < 0.5) {
        // Randomly assign left/right positions
        displayObject("left", experimentSetup.currentState);
        displayObject("right", proposalObject);
        experimentSetup.leftIsCurrentState = true;
    } else {
        displayObject("left", proposalObject);
        displayObject("right", experimentSetup.currentState);
        experimentSetup.leftIsCurrentState = false;
    }
    
    // Wait for response (handled by button click event listeners)
    document.getElementById('left-button').addEventListener('click', () => handleResponse(true));
    document.getElementById('right-button').addEventListener('click', () => handleResponse(false));
}

// Handle response
function handleResponse(selectedLeft) {
    const selectedCurrentState = (selectedLeft && experimentSetup.leftIsCurrentState) || 
                                 (!selectedLeft && !experimentSetup.leftIsCurrentState);
    
    // If proposal was selected, update current state
    if (!selectedCurrentState) {
        experimentSetup.currentState = selectedLeft ? 
            getObjectById(document.getElementById("left-img").dataset.objectId) : 
            getObjectById(document.getElementById("right-img").dataset.objectId);
    }
    
    // Record this step in chain history
    experimentSetup.chainHistory.push(experimentSetup.currentState.object_id);
    
    // Move to next trial or end experiment
    experimentSetup.currentTrial++;
    if (experimentSetup.currentTrial < experimentSetup.totalTrials) {
        runTrial();
    } else {
        endExperiment();
    }
}

// Load the stimulus database
async function loadObjectDatabase() {
    const response = await fetch('stimulus_database.csv');
    const data = await response.text();
    experimentSetup.objectDatabase = parseCSV(data);
}

// Get a random object from the database
function getRandomObject() {
    const randomIndex = Math.floor(Math.random() * experimentSetup.objectDatabase.length);
    return experimentSetup.objectDatabase[randomIndex];
}

// Generate proposal parameters based on current state
function generateProposal(currentObject) {
    // Use current object's parameters as base
    const params = { ...currentObject };
    
    // Add small random perturbations to parameters
    params.num_extrusions += (Math.random() - 0.5) * 2;
    params.extrusion_range += (Math.random() - 0.5) * 0.1;
    params.rotation_range += (Math.random() - 0.5) * 30;
    
    return params;
}

// Find nearest object in database to proposed parameters
function findNearestObject(proposedParams) {
    return experimentSetup.objectDatabase.reduce((nearest, current) => {
        const currentDistance = calculateDistance(proposedParams, current);
        const nearestDistance = calculateDistance(proposedParams, nearest);
        return currentDistance < nearestDistance ? current : nearest;
    });
}

// Display an object in the interface
function displayObject(position, object) {
    const imgElement = document.getElementById(`${position}-img`);
    imgElement.src = object.stl_file;
    imgElement.dataset.objectId = object.object_id;
}

// Calculate distance between two parameter sets
function calculateDistance(params1, params2) {
    return Math.sqrt(
        Math.pow(params1.num_extrusions_normalized - params2.num_extrusions_normalized, 2) +
        Math.pow(params1.extrusion_range_normalized - params2.extrusion_range_normalized, 2) +
        Math.pow(params1.rotation_range_normalized - params2.rotation_range_normalized, 2)
    );
}

// Start the experiment when the page loads
window.addEventListener('load', initExperiment);