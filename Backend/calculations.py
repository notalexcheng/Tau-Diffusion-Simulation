
import math
import random

def ifCollide(prob):
    options = ["y","n"]
    probabilities = [prob, 1-prob]
    return random.choices(options, probabilities)[0]

def move_tau(packet, percentage, spread_percent):
    
    total_tau = (packet.get_tau_length(1) * spread_percent) + (packet.get_tau_length(2) * (spread_percent * 1/2)) 
    + (packet.get_tau_length(3) * (spread_percent * 1/3)) + (packet.get_tau_length(4) * (spread_percent * 1/4)) 
    
    diffusable_tau = round(percentage * total_tau)
    
    return diffusable_tau
    
    

def find_least_tau_neighbors(cube, x, y, z, tau_type):
    # Define the possible directions and corresponding index changes
    directions = {
        "top": (-1, 0, 0),
        "bottom": (1, 0, 0),
        "left": (0, -1, 0),
        "right": (0, 1, 0),
        "front": (0, 0, -1),
        "back": (0, 0, 1)
    }
    
    # Get the dimensions of the cube
    x_max, y_max, z_max = cube.shape
    
    min_concentration = float('inf')
    min_neighbors = []
    
    # Iterate over all directions
    for direction, (dx, dy, dz) in directions.items():
        nx, ny, nz = x + dx, y + dy, z + dz
        
        # Check if the neighbor is within bounds
        if 0 <= nx < x_max and 0 <= ny < y_max and 0 <= nz < z_max:
            # Get the tau concentration in the neighbor
            neighbor_concentration = cube[nx, ny, nz].get_tau_length(tau_type)
            
            # Check if this is the smallest concentration found so far
            if neighbor_concentration < min_concentration:
                min_concentration = neighbor_concentration
                min_directions = [direction]
            elif neighbor_concentration == min_concentration:
                min_directions.append(direction)
    
    return min_directions


        
    
    
    





       

        
