from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import json

app = Flask(__name__)

# Load object database
object_database = pd.read_csv('stimulus_database.csv')

@app.route('/')
def index():
    return render_template('MCMC.html')

@app.route('/api/get-objects', methods=['GET'])
def get_objects():
    # Return a subset of objects for client-side use
    return jsonify(object_database.to_dict(orient='records'))

@app.route('/api/save-chain', methods=['POST'])
def save_chain():
    data = request.json
    participant_id = data.get('participant_id')
    condition = data.get('condition')
    chain_history = data.get('chain_history')
    
    # Save to file
    with open(f'data/participant_{participant_id}_{condition}.json', 'w') as f:
        json.dump(data, f)
    
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)