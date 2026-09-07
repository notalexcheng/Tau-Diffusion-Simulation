
#main.py

import tp
import neuron_packet
import create_tau
import calculations
import numpy as np
import connections
import simulation, time
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS

global concentrations, cube, data, timestep, run
cube = []
data = {}
concentrations = []
timestep = 0
run = 0

@app.route("/simulator", methods=["POST"])
def simulator():
    global concentrations, timestep
    # Return the JSON response
    return jsonify([timestep, concentrations])

@app.route("/initial", methods=["POST"])
def initialize():
    global data, timestep, run
    data = request.get_json()
    print("data: " + str(data.items()))
    
    global cube
    cube = connections.create_cube(data["x"],data["y"],data["z"],data["concentrationArray"])
    
    connections.set_strength(cube,data["baseConnection"])
    connections.set_connection(cube)
    
    timestep = 0
    run = 1
    
    
    # Start the background thread for updating grid data
    update_thread = threading.Thread(target=run_sim)
    update_thread.daemon = True
    update_thread.start()
    # Return the JSON response
    
    return jsonify(1)
    
    
def run_sim():
    global concentrations
    global timestep, run
    while (True):
        if run==1:
            print("Sim is running")
            concentrations = simulation.run_sim(cube, data["spreadPercent"], timestep, data["lambda"], data["c"], data["gamma"], data["timeConstant"])
            timestep += 1
            
        elif run==2:
            break
        elif run==0:
            print("paused")
        time.sleep(0.2)

@app.route("/pause", methods=["POST"])
def pause():
    #change global pause variable to halt loop
    global run
    run = 0
    
    return jsonify(1)

@app.route("/resume", methods=["POST"])
def resume():
    #change global pause variable to resume loop
    global run
    run = 1
    
    return jsonify(1)



@app.route("/end", methods=["POST"])
def end():
    global run
    run = 2
    
    return jsonify(1)

@app.route("/reset", methods=["POST"])
def reset():
    cube = []
    data = {}
    concentrations = []
    timestep = 0
    run = 0
    
    return jsonify(1)
    

if __name__ == "__main__":
    # # Run Flask app on localhost
    app.run(host='127.0.0.1', port=5001, debug=True)

    # Run Flask app on server network
    #app.run(host='0.0.0.0', port=5001, debug=True)
    
    
