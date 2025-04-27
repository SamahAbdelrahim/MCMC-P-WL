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