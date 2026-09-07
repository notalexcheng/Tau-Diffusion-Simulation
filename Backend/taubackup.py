#calculations.py

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


        
    
    
    





       

        
    
#connections.py

import numpy as np
import neuron_packet
import calculations

def create_cube(x,y,z,a):
    cube = np.empty((x,y,z), dtype=object)


    # Initialize the 3D array with packet objects
    for i in range(x):
        for j in range(y):
            for k in range(z):
                cube[i, j, k] = neuron_packet.packet(i, j, k, a[i][j][k][0], a[i][j][k][1], a[i][j][k][2], a[i][j][k][3], a[i][j][k][4])
    
    
    
    return cube
    


def set_strength(cube,c):
    # Set strength values
    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                if i > 0:  # top neighbor
                    cube[i, j, k].set_side_strength("top", c)
                    cube[i - 1, j, k].set_side_strength("bottom", c)

                if i < cube[i,j,k].getX() - 1:  # bottom neighbor
                    cube[i, j, k].set_side_strength("bottom", c)
                    cube[i + 1, j, k].set_side_strength("top", c)

                if j > 0:  # left neighbor
                    cube[i, j, k].set_side_strength("left", c)
                    cube[i, j - 1, k].set_side_strength("right", c)

                if j < cube[i,j,k].getY()- 1:  # right neighbor
                    cube[i, j, k].set_side_strength("right", c)
                    cube[i, j + 1, k].set_side_strength("left", c)

                if k > 0:  # front neighbor
                    cube[i, j, k].set_side_strength("front", c)
                    cube[i, j, k - 1].set_side_strength("back", c)

                if k < cube[i,j,k].getZ() - 1:  # back neighbor
                    cube[i, j, k].set_side_strength("back", c)
                    cube[i, j, k + 1].set_side_strength("front", c)


def set_connection(cube):
    connect = 0
    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                if i > 0:  # top neighbor
                    connect = abs(cube[i,j,k].getConcentration() - cube[i-1,j,k].getConcentration()) * cube[i,j,k].sideStrength.get("top")
                    ##print(cube[i,j,k].sideStrength.get("top"))
                    #cube[i,j,k].getConcentration() - cube[i-1,j,k].getConcentration()
                    cube[i, j, k].set_side("top", connect)
                    cube[i - 1, j, k].set_side("bottom", connect)
                    
    
                if i < cube[i,j,k].getX() - 1:  # bottom neighbor
                    connect = abs(cube[i,j,k].getConcentration() - cube[i+1,j,k].getConcentration()) * cube[i,j,k].sideStrength.get("bottom")
                    ##print(cube[i,j,k].sideStrength.get("bottom"))
                    #cube[i,j,k].getConcentration() - cube[i+1,j,k].getConcentration()
                    cube[i, j, k].set_side("bottom", connect)
                    cube[i + 1, j, k].set_side("top", connect)

                if j > 0:  # left neighbor
                    connect = abs(cube[i,j,k].getConcentration() - cube[i,j-1,k].getConcentration()) * cube[i,j,k].sideStrength.get("left")
                    ##print(cube[i,j,k].sideStrength.get("left"))
                    cube[i, j, k].set_side("left", connect)
                    cube[i, j - 1, k].set_side("right", connect)

                if j < cube[i,j,k].getY() - 1:  # right neighbor
                    connect = abs(cube[i,j,k].getConcentration() - cube[i,j+1,k].getConcentration()) * cube[i,j,k].sideStrength.get("right")
                    ##print(cube[i,j,k].sideStrength.get("right"))
                    cube[i, j, k].set_side("right", connect)
                    cube[i, j + 1, k].set_side("left", connect)

                if k > 0:  # front neighbor
                    connect = abs(cube[i,j,k].getConcentration() - cube[i,j,k-1].getConcentration()) * cube[i,j,k].sideStrength.get("front")
                    ##print(cube[i,j,k].sideStrength.get("front"))
                    cube[i, j, k].set_side("front", connect)
                    cube[i, j, k - 1].set_side("back", connect)

                if k < cube[i,j,k].getZ() - 1:  # back neighbor
                    connect = abs(cube[i,j,k].getConcentration() - cube[i,j,k+1].getConcentration()) * cube[i,j,k].sideStrength.get("back")
                    ##print(cube[i,j,k].sideStrength.get("back"))
                    cube[i, j, k].set_side("back", connect)
                    cube[i, j, k + 1].set_side("front", connect)
    
    




def getStrength(c, x1, y1, z1, x2, y2, z2):
    # Validate coordinates
    size = len(c)
    if not (0 <= x1 < size and 0 <= y1 < len(c[0]) and 0 <= z1 < len(c[0][0])):
        return "Invalid coordinates for packet 1"
    if not (0 <= x2 < size and 0 <= y2 < len(c[0]) and 0 <= z2 < len(c[0][0])):
        return "Invalid coordinates for packet 2"

    # Determine the side from packet1 to packet2
    if x1 == x2 and y1 == y2 and abs(z1 - z2) == 1:  # Front-back neighbors
        if z1 < z2:
            return c[x1, y1, z1].sideStrength.get("back")
        else:
            return c[x1, y1, z1].sideStrength.get("front")
    elif x1 == x2 and abs(y1 - y2) == 1 and z1 == z2:  # Left-right neighbors
        if y1 < y2:
            return c[x1, y1, z1].sideStrength.get("right")
        else:
            return c[x1, y1, z1].sideStrength.get("left")
    elif abs(x1 - x2) == 1 and y1 == y2 and z1 == z2:  # Top-bottom neighbors
        if x1 < x2:
            return c[x1, y1, z1].sideStrength.get("bottom")
        else:
            return c[x1, y1, z1].sideStrength.get("top")
    else:
        return "Packets are not neighbors"
    
def getConnection(c, x1, y1, z1, x2, y2, z2):
    # Validate coordinates
    size = len(c)
    if not (0 <= x1 < size and 0 <= y1 < len(c[0]) and 0 <= z1 < len(c[0][0])):
        return "Invalid coordinates for packet 1"
    if not (0 <= x2 < size and 0 <= y2 < len(c[0]) and 0 <= z2 < len(c[0][0])):
        return "Invalid coordinates for packet 2"

    # Determine the side from packet1 to packet2
    if x1 == x2 and y1 == y2 and abs(z1 - z2) == 1:  # Front-back neighbors
        if z1 < z2:
            return c[x1, y1, z1].get_side("back")
        else:
            return c[x1, y1, z1].get_side("front")
    elif x1 == x2 and abs(y1 - y2) == 1 and z1 == z2:  # Left-right neighbors
        if y1 < y2:
            return c[x1, y1, z1].get_side("right")
        else:
            return c[x1, y1, z1].get_side("left")
    elif abs(x1 - x2) == 1 and y1 == y2 and z1 == z2:  # Top-bottom neighbors
        if x1 < x2:
            return c[x1, y1, z1].get_side("bottom")
        else:
            return c[x1, y1, z1].get_side("top")
    else:
        return "Packets are not neighbors"
    

    
def spread(cube, percent, x, y, z):
    # Define the possible directions and corresponding index changes
    directions = {
        "top": (-1, 0, 0),
        "bottom": (1, 0, 0),
        "left": (0, -1, 0),
        "right": (0, 1, 0),
        "front": (0, 0, -1),
        "back": (0, 0, 1)
    }
    
    connections = {
        "top": None,
        "bottom": None,
        "left": None,
        "right": None,
        "front": None,
        "back": None
    }
    
    
    # Get the size of the cube
    x_max = len(cube)
    y_max = len(cube[0])
    z_max = len(cube[0][0])
    
    # Iterate over all directions
    for direction, (dx, dy, dz) in directions.items():
        nx, ny, nz = x + dx, y + dy, z + dz
        
        # Check if the neighbor is within bounds
        if 0 <= nx < x_max and 0 <= ny < y_max and 0 <= nz < z_max:
            # Example operation: modify neighbor's concentration
            # This is just a placeholder, replace it with your desired operation
            current_connection = getConnection(cube,x,y,z,nx,ny,nz)
            
            if x == nx and y == ny and abs(z - nz) == 1:  # Front-back neighbors
                if z < nz:
                    connections["back"] = current_connection
                    #print(f"back: {connections["back"]}")
                else:
                    connections["front"] = current_connection
                    #print(f"front: {connections["front"]}")
            elif x == nx and abs(y - ny) == 1 and z == nz:  # Left-right neighbors
                if y < ny:
                    connections["right"] = current_connection
                    #print(f"right: {connections["right"]}")
                else:
                    connections["left"] = current_connection
                    #print(f"left: {connections["left"]}")
            elif abs(x - nx) == 1 and y == ny and z == nz:  # Top-bottom neighbors
                if x < nx:
                    connections["bottom"] = current_connection
                    #print(f"bottom: {connections["bottom"]}")
                else:
                    connections["top"] = current_connection
                    #print(f"top: {connections["top"]}")
            else:
                return "Packets are not neighbors"
            
                
            
            
            
            
            # For demonstration, we will just print the difference
            #print(f"Connection between ({x}, {y}, {z}) and ({nx}, {ny}, {nz}): {current_connection}")
            
            # Additional operations can be added here
            # For instance, update some properties of the neighbor
            # cube[nx, ny, nz].setConcentration(new_value)
    total_connection = 0
    for key, value in connections.items():
        if value is not None:
            total_connection += value
    
    least_tau1 = []
    least_tau2 = []
    least_tau3 = []
    least_tau4 = []
    
    
    
    if cube[x,y,z].get_tau_length(1) > 0:
        least_tau1 = calculations.find_least_tau_neighbors(cube,x,y,z,1)
        diff_tau1 = cube[x,y,z].get_tau_length(1) * percent
        moved_tau1 = diff_tau1 / len(least_tau1)
        #print("mt1: " + str(moved_tau1 * move_back))
    
    if cube[x,y,z].get_tau_length(2) > 0:
        least_tau2 = calculations.find_least_tau_neighbors(cube,x,y,z,2)
        diff_tau2 = cube[x,y,z].get_tau_length(2) * percent * 1/2
        moved_tau2 = diff_tau2 / len(least_tau2)
    
    if cube[x,y,z].get_tau_length(3) > 0:
        least_tau3 = calculations.find_least_tau_neighbors(cube,x,y,z,3)
        diff_tau3 = cube[x,y,z].get_tau_length(3) * percent * 1/3
        moved_tau3 = diff_tau3 / len(least_tau3)

    if cube[x,y,z].get_tau_length(4) > 0:
        least_tau4 = calculations.find_least_tau_neighbors(cube,x,y,z,4)
        diff_tau4 = cube[x,y,z].get_tau_length(4) * percent * 1/4
        moved_tau4 = diff_tau4 / len(least_tau4)
    #for i in range(6):
       
       
       
       
    #tau 1 spread   
    if total_connection > 0:
        if (connections["back"] is not None and 'back' in least_tau1):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau1 * move_back > move_back):
                cube[x,y,z+1].add_tau1(move_back)
                cube[x,y,z].remove_tau1(move_back)
            else:
                cube[x,y,z+1].add_tau1(round(moved_tau1 * move_back))
                cube[x,y,z].remove_tau1(round(moved_tau1 * move_back))
            #print(f"{moved_tau1 * move_back} tau1 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau1):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau1 * move_bottom > move_bottom):
                cube[x+1,y,z].add_tau1(move_bottom)
                cube[x,y,z].remove_tau1(move_bottom)
            else:
                cube[x+1,y,z].add_tau1(round(moved_tau1 * move_bottom))
                cube[x,y,z].remove_tau1(round(moved_tau1 * move_bottom))
            #print(f"{moved_tau1 * move_back} tau1 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau1):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau1 * move_front > move_front):
                cube[x,y,z-1].add_tau1(move_front)
                cube[x,y,z].remove_tau1(move_front)
            else:
                cube[x,y,z-1].add_tau1(round(moved_tau1 * move_front))
                cube[x,y,z].remove_tau1(round(moved_tau1 * move_front))
            #print(f"{moved_tau1 * move_back} tau1 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau1) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau1 * move_left > move_left):
                cube[x,y-1,z].add_tau1(move_left)
                cube[x,y,z].remove_tau1(move_left)
                
            else:
                cube[x,y-1,z].add_tau1(round(moved_tau1 * move_left))
                cube[x,y,z].remove_tau1(round(moved_tau1 * move_left))
            #print(f"{moved_tau1 * move_back} tau1 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau1):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau1 * move_right > move_right):
                cube[x,y+1,z].add_tau1(move_right)
                cube[x,y,z].remove_tau1(move_right)
            else:
                cube[x,y+1,z].add_tau1(round(moved_tau1 * move_right))
                cube[x,y,z].remove_tau1(round(moved_tau1 * move_right))
            #print(f"{moved_tau1 * move_back} tau1 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau1):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau1 * move_top > move_top):
                cube[x-1,y,z].add_tau1(move_top)
                cube[x,y,z].remove_tau1(move_top)
            else:
                cube[x-1,y,z].add_tau1(round(moved_tau1 * move_top))
                cube[x,y,z].remove_tau1(round(moved_tau1 * move_top))
            #print(f"{moved_tau1 * move_back} tau1 was added to top neighbor")
                #add tau cube[x-1,y,z]
    
        #tau 2 spread
        if (connections["back"] is not None and 'back' in least_tau2):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau2 * move_back > move_back):
                cube[x,y,z+1].add_tau2(move_back)
                cube[x,y,z].remove_tau2(move_back)
            else:
                cube[x,y,z+1].add_tau2(round(moved_tau2 * move_back))
                cube[x,y,z].remove_tau2(round(moved_tau2 * move_back))
            #print(f"{moved_tau2 * move_back} tau2 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau2):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau2 * move_bottom > move_bottom):
                cube[x+1,y,z].add_tau2(move_bottom)
                cube[x,y,z].remove_tau2(move_bottom)
            else:
                cube[x+1,y,z].add_tau2(round(moved_tau2 * move_bottom))
                cube[x,y,z].remove_tau2(round(moved_tau2 * move_bottom))
            #print(f"{moved_tau2 * move_back} tau2 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau2):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau2 * move_front > move_front):
                cube[x,y,z-1].add_tau2(move_front)
                cube[x,y,z].remove_tau2(move_front)
            else:
                cube[x,y,z-1].add_tau2(round(moved_tau2 * move_front))
                cube[x,y,z].remove_tau2(round(moved_tau2 * move_front))
            #print(f"{moved_tau2 * move_back} tau2 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau2) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau2 * move_left > move_left):
                cube[x,y-1,z].add_tau2(move_left)
                cube[x,y,z].remove_tau2(move_left)
                
            else:
                cube[x,y-1,z].add_tau2(round(moved_tau2 * move_left))
                cube[x,y,z].remove_tau2(round(moved_tau2 * move_left))
            #print(f"{moved_tau2 * move_back} tau2 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau2):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau2 * move_right > move_right):
                cube[x,y+1,z].add_tau2(move_right)
                cube[x,y,z].remove_tau2(move_right)
            else:
                cube[x,y+1,z].add_tau2(round(moved_tau2 * move_right))
                cube[x,y,z].remove_tau2(round(moved_tau2 * move_right))
            #print(f"{moved_tau2 * move_back} tau2 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau2):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau2 * move_top > move_top):
                cube[x-1,y,z].add_tau2(move_top)
                cube[x,y,z].remove_tau2(move_top)
            else:
                cube[x-1,y,z].add_tau2(round(moved_tau2 * move_top))
                cube[x,y,z].remove_tau2(round(moved_tau2 * move_top))
            #print(f"{moved_tau2 * move_back} tau2 was added to top neighbor")
        
    
    
    
    #tau 3 spread   
        if (connections["back"] is not None and 'back' in least_tau3):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau3 * move_back > move_back):
                cube[x,y,z+1].add_tau3(move_back)
                cube[x,y,z].remove_tau3(move_back)
            else:
                cube[x,y,z+1].add_tau3(round(moved_tau3 * move_back))
                cube[x,y,z].remove_tau3(round(moved_tau3 * move_back))
            #print(f"{moved_tau3 * move_back} tau3 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau3):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau3 * move_bottom > move_bottom):
                cube[x+1,y,z].add_tau3(move_bottom)
                cube[x,y,z].remove_tau3(move_bottom)
            else:
                cube[x+1,y,z].add_tau3(round(moved_tau3 * move_bottom))
                cube[x,y,z].remove_tau3(round(moved_tau3 * move_bottom))
            #print(f"{moved_tau3 * move_back} tau3 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau3):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau3 * move_front > move_front):
                cube[x,y,z-1].add_tau3(move_front)
                cube[x,y,z].remove_tau3(move_front)
            else:
                cube[x,y,z-1].add_tau3(round(moved_tau3 * move_front))
                cube[x,y,z].remove_tau3(round(moved_tau3 * move_front))
            #print(f"{moved_tau3 * move_back} tau3 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau3) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau3 * move_left > move_left):
                cube[x,y-1,z].add_tau3(move_left)
                cube[x,y,z].remove_tau3(move_left)
                
            else:
                cube[x,y-1,z].add_tau3(round(moved_tau3 * move_left))
                cube[x,y,z].remove_tau3(round(moved_tau3 * move_left))
            #print(f"{moved_tau3 * move_back} tau3 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau3):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau3 * move_right > move_right):
                cube[x,y+1,z].add_tau3(move_right)
                cube[x,y,z].remove_tau3(move_right)
            else:
                cube[x,y+1,z].add_tau3(round(moved_tau3 * move_right))
                cube[x,y,z].remove_tau3(round(moved_tau3 * move_right))
            #print(f"{moved_tau3 * move_back} tau3 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau3):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau3 * move_top > move_top):
                cube[x-1,y,z].add_tau3(move_top)
                cube[x,y,z].remove_tau3(move_top)
            else:
                cube[x-1,y,z].add_tau3(round(moved_tau3 * move_top))
                cube[x,y,z].remove_tau3(round(moved_tau3 * move_top))
            #print(f"{moved_tau3 * move_back} tau3 was added to top neighbor")
        
    
    
    #tau 4 spread   
        if (connections["back"] is not None and 'back' in least_tau4):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau4 * move_back > move_back):
                cube[x,y,z+1].add_tau4(move_back)
                cube[x,y,z].remove_tau4(move_back)
            else:
                cube[x,y,z+1].add_tau4(round(moved_tau4 * move_back))
                cube[x,y,z].remove_tau4(round(moved_tau4 * move_back))
            #print(f"{moved_tau4 * move_back} tau4 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau4):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau4 * move_bottom > move_bottom):
                cube[x+1,y,z].add_tau4(move_bottom)
                cube[x,y,z].remove_tau4(move_bottom)
            else:
                cube[x+1,y,z].add_tau4(round(moved_tau4 * move_bottom))
                cube[x,y,z].remove_tau4(round(moved_tau4 * move_bottom))
            #print(f"{moved_tau4 * move_back} tau4 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau4):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau4 * move_front > move_front):
                cube[x,y,z-1].add_tau4(move_front)
                cube[x,y,z].remove_tau4(move_front)
            else:
                cube[x,y,z-1].add_tau4(round(moved_tau4 * move_front))
                cube[x,y,z].remove_tau4(round(moved_tau4 * move_front))
            #print(f"{moved_tau4 * move_back} tau4 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau4) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau4 * move_left > move_left):
                cube[x,y-1,z].add_tau4(move_left)
                cube[x,y,z].remove_tau4(move_left)
                
            else:
                cube[x,y-1,z].add_tau4(round(moved_tau4 * move_left))
                cube[x,y,z].remove_tau4(round(moved_tau4 * move_left))
            #print(f"{moved_tau4 * move_back} tau4 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau4):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau4 * move_right > move_right):
                cube[x,y+1,z].add_tau4(move_right)
                cube[x,y,z].remove_tau4(move_right)
            else:
                cube[x,y+1,z].add_tau4(round(moved_tau4 * move_right))
                cube[x,y,z].remove_tau4(round(moved_tau4 * move_right))
            #print(f"{moved_tau4 * move_back} tau4 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau4):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau4 * move_top > move_top):
                cube[x-1,y,z].add_tau4(move_top)
                cube[x,y,z].remove_tau4(move_top)
            else:
                cube[x-1,y,z].add_tau4(round(moved_tau4 * move_top))
                cube[x,y,z].remove_tau4(round(moved_tau4 * move_top))
            #print(f"{moved_tau4 * move_back} tau4 was added to top neighbor")
            
        
    
def get_cube_concentration(cube):
    #np.empty((len(cube),len(cube[0]),len(cube[0][0])), dtype = object)
    a = [[[[0, 0, 0, 0, 0] for i in range(len(cube[0][0]))] for j in range(len(cube[0]))] for k in range(len(cube))]
    
    
    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                    a[i][j][k] = [cube[i,j,k].get_tau_length(1), cube[i,j,k].get_tau_length(2), cube[i,j,k].get_tau_length(3), cube[i,j,k].get_tau_length(4), cube[i,j,k].get_tau_length(5)]
    
    return a
    
    
    
    
    


    
    
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
            concentrations = simulation.run_sim(cube, data["spreadPercent"])
            print(concentrations)
            timestep += 1
            
        elif run==2:
            break
        time.sleep(1)

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

@app.route("/reset", methods=["POST"])
def reset():
    global run
    run = 2
    
    return jsonify(1)
    

if __name__ == "__main__":
    # # Run Flask app on localhost
    # app.run(host='127.0.0.1', port=5000, debug=True)

    # Run Flask app on server network
    app.run(host='0.0.0.0', port=5001, debug=True)
    
    













#neuron_packet.py

#Creates the neuron
import tp
import calculations
import side
import random
import create_tau
import math


class packet:
    
    def __init__(self,x,y,z,t1,t2,t3,t4,t5):
        
        #initializes packet edges
        self.sides = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "front": None,
            "back": None
        }
        
        self.sideStrength = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "front": None,
            "back": None
        }
        
        self.x = x
        self.y = y
        self.z = z
        
        self.ta1 = []
        self.ta2 = []
        self.ta3 = []
        self.ta4 = []
        self.ta5 = []
        create_tau.createTau1(self.ta1, t1)
        create_tau.createTau2(self.ta2, t2)
        create_tau.createTau3(self.ta3, t3)
        create_tau.createTau4(self.ta4, t4)
        create_tau.createTau5(self.ta5, t5)
    
    
    def get_tau_length(self, num):
        if num == 1:
            return len(self.ta1)
        if num == 2:
            return len(self.ta2)
        if num == 3:
            return len(self.ta3)
        if num == 4:
            return len(self.ta4)
        if num == 5:
            return len(self.ta5)
    
    def add_tau1(self,num):
        create_tau.createTau1(self.ta1,num)
    def add_tau2(self,num):
        create_tau.createTau2(self.ta2,num)
    def add_tau3(self,num):
        create_tau.createTau3(self.ta3,num)
    def add_tau4(self,num):
        create_tau.createTau4(self.ta4,num)
    def add_tau5(self,num):
        create_tau.createTau1(self.ta5,num)
        
    def remove_tau1(self,num):
        if num <= len(self.ta1):
            for i in range(num):
                self.ta1.pop()
    def remove_tau2(self,num):
        if num <= len(self.ta2):
            for i in range(num):
                self.ta2.pop()
    def remove_tau3(self,num):
        if num <= len(self.ta3):
            for i in range(num):
                self.ta3.pop()
    def remove_tau4(self,num):
        if num <= len(self.ta4):
            for i in range(num):
                self.ta4.pop()
    def remove_tau5(self,num):
        if num <= len(self.ta5):
            for i in range(num):
                self.ta5.pop()
    
    
    
    
    def set_side_strength(self, side, value):
        self.sideStrength[side] = value
        
    def get_side_strength(self,side):
        return self.sideStrength[side]
    
    def set_side(self,side, value):
        self.sides[side] = value
    
    def get_side(self,side):
        return self.sides[side]
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
    
    def cycles_collisions(self, prob): #, self.ta1, self.ta2, self.ta3, self.ta4, self.ta5):
        
        all_tau = [self.ta1, self.ta2, self.ta3, self.ta4, self.ta5]
        
        new_tau = [[], [], [], [], []]
        
        
        #Tau 1 loop
        for i in range(len(self.ta1)):
            if (len(self.ta1) > 0):
                if(calculations.ifCollide(prob) == "y"):
                    
                    selected_list = []
                    while len(selected_list) == 0:
                        selected_list = random.choice(all_tau)
                    selected_element = random.choice(selected_list)
                    num = selected_element.getForm() + 1
                    if num > 5:
                        num = 5
                    
                    #print("Tau 1 collides with Tau " + str(selected_element.getForm()))
                    
                    self.ta1.pop()
                    #print("Tau 1 was removed from self.ta1. 1length: " + str(len(self.ta1))) #NEED TO REMOVE CURRENT TAU
                    
                    if selected_element.getForm() == 1 and len(self.ta1) > 0:
                        self.ta1.pop()
                        #print("Tau 1 was removed from self.ta1. 1length: " + str(len(self.ta1)))
                    
                    if selected_element.getForm() == 2 and len(self.ta2) > 0:
                        self.ta2.pop()
                        #print("Tau 2 was removed from self.ta2. 2length: " + str(len(self.ta2)))
                    
                    if selected_element.getForm() == 3 and len(self.ta3) > 0:
                        self.ta3.pop()
                        #print("Tau 3 was removed from self.ta3. 3length: " + str(len(self.ta3)))
                        
                    if selected_element.getForm() == 4 and len(self.ta4) > 0:
                        self.ta4.pop()
                        #print("Tau 4 was removed from self.ta4. 4length: " + str(len(self.ta4)))
                        
                    if selected_element.getForm() == 5 and len(self.ta5) > 0:
                        self.ta5.pop()
                        #print("Tau 5 was removed from self.ta5. 5length: " + str(len(self.ta5)))
                        
                        
                    # # try:
                    # all_tau.remove(selected_element)
                    # #print("Tau " + str(selected_element.getForm()) + " was removed from all_tau")
                    # all_tau.remove(random.choice(all_tau[0]))
                    # #print("Tau 1 was removed from all_tau")
                    # # except ValueError:
                    # #     #print("Element not found in the list")
                    
                    if num == 2:
                        new_tau[1].append(tp.tau_protein(2))
                        #print("Tau 2 has been created and added to new_tau. 2length: " + str(len(self.ta2)) + "\tnew2length: " + str(len(new_tau[1])))
                    
                    if num == 3:
                        new_tau[2].append(tp.tau_protein(3))
                        #print("Tau 3 has been created and added to new_tau. 3length: " + str(len(self.ta3)) + "\tnew3length: " + str(len(new_tau[2])))
                        
                    if num == 4:
                        new_tau[3].append(tp.tau_protein(4))
                        #print("Tau 4 has been created and added to new_tau. 4length: " + str(len(self.ta4)) + "\tnew4length: " + str(len(new_tau[3])))
                        
                    if num == 5:
                        new_tau[4].append(tp.tau_protein(5))
                        #print("Tau 5 has been created and added to new_tau. 5length: " + str(len(self.ta5)) + "\tnew5length: " + str(len(new_tau[4])))                
                        
                #else:
                    #print("Tau 1 does not collide. 1Len: " + str(len(self.ta1)))
            else:
                break
        
        #Tau 2 loop
        for i in range(len(self.ta2)):
            if (len(self.ta2) > 0):
                if(calculations.ifCollide(prob) == "y"):
                    
                    selected_list = []
                    while len(selected_list) == 0:
                        selected_list = random.choice(all_tau)
                    selected_element = random.choice(selected_list)
                    
                    num = selected_element.getForm() + 2
                    if num > 5:
                        num = 5
                    #print("Tau 2 collides with Tau " + str(selected_element.getForm()))
                    
                    self.ta2.pop()
                    #print("Tau 2 was removed from self.ta2. 2length: " + str(len(self.ta2))) #NEED TO REMOVE CURRENT TAU
                    
                    if selected_element.getForm() == 1 and len(self.ta1) > 0:
                        self.ta1.pop()
                        #print("Tau 1 was removed from self.ta1. 1length: " + str(len(self.ta1)))
                    
                    if selected_element.getForm() == 2 and len(self.ta2) > 0:
                        self.ta2.pop()
                        #print("Tau 2 was removed from self.ta2. 2length: " + str(len(self.ta2)))
                    
                    if selected_element.getForm() == 3 and len(self.ta3) > 0:
                        self.ta3.pop()
                        #print("Tau 3 was removed from self.ta3. 3length: " + str(len(self.ta3)))
                        
                    if selected_element.getForm() == 4 and len(self.ta4) > 0:
                        self.ta4.pop()
                        #print("Tau 4 was removed from self.ta4. 4length: " + str(len(self.ta4)))
                        
                    if selected_element.getForm() == 5 and len(self.ta5) > 0:
                        self.ta5.pop()
                        #print("Tau 5 was removed from self.ta5. 5length: " + str(len(self.ta5)))
                        
                    # # try:
                    # all_tau.remove(selected_element)
                    # #print("Tau " + str(selected_element.getForm()) + " was removed from all_tau")
                    # all_tau.remove(random.choice(all_tau[1]))
                    # #print("Tau 2 was removed from all_tau")
                        
                    # # except ValueError:
                    # #     #print("Element not found in the list")
                    
                    
                    if num == 2:
                        new_tau[1].append(tp.tau_protein(2))
                        #print("Tau 2 has been created and added to new_tau. 2length: " + str(len(self.ta2)) + "\tnew2length: " + str(len(new_tau[1])))
                    
                    if num == 3:
                        new_tau[2].append(tp.tau_protein(3))
                        #print("Tau 3 has been created and added to new_tau. 3length: " + str(len(self.ta3)) + "\tnew3length: " + str(len(new_tau[2])))
                        
                    if num == 4:
                        new_tau[3].append(tp.tau_protein(4))
                        #print("Tau 4 has been created and added to new_tau. 4length: " + str(len(self.ta4)) + "\tnew4length: " + str(len(new_tau[3])))
                        
                    if num == 5:
                        new_tau[4].append(tp.tau_protein(5))
                        #print("Tau 5 has been created and added to new_tau. 5length: " + str(len(self.ta5)) + "\tnew5length: " + str(len(new_tau[4])))                 
                        
                #else:
                    #print("Tau 2 does not collide. 2Len: " + str(len(self.ta2)))
            else:
                break
            
            #Tau 3 loop
        for i in range(len(self.ta3)):
            if (len(self.ta3) > 0):
                if(calculations.ifCollide(prob) == "y"):
                    
                    selected_list = []
                    while len(selected_list) == 0:
                        selected_list = random.choice(all_tau)
                    selected_element = random.choice(selected_list)
                    
                    num = selected_element.getForm() + 3
                    if num > 5:
                        num = 5
                    #print("Tau 3 collides with Tau " + str(selected_element.getForm()))
                    
                    
                    self.ta3.pop()
                    #print("Tau 3 was removed from self.ta3. 3length: " + str(len(self.ta3))) #NEED TO REMOVE CURRENT TAU
                    
                    if selected_element.getForm() == 1 and len(self.ta1) > 0:
                        self.ta1.pop()
                        #print("Tau 1 was removed from self.ta1. 1length: " + str(len(self.ta1)))
                    
                    if selected_element.getForm() == 2 and len(self.ta2) > 0:
                        self.ta2.pop()
                        #print("Tau 2 was removed from self.ta2. 2length: " + str(len(self.ta2)))
                    
                    if selected_element.getForm() == 3 and len(self.ta3) > 0:
                        self.ta3.pop()
                        #print("Tau 3 was removed from self.ta3. 3length: " + str(len(self.ta3)))
                        
                    if selected_element.getForm() == 4 and len(self.ta4) > 0:
                        self.ta4.pop()
                        #print("Tau 4 was removed from self.ta4. 4length: " + str(len(self.ta4)))
                        
                    if selected_element.getForm() == 5 and len(self.ta5) > 0:
                        self.ta5.pop()
                        #print("Tau 5 was removed from self.ta5. 5length: " + str(len(self.ta5)))
                        
                    # # try:
                    # all_tau.remove(selected_element)
                    # #print("Tau " + str(selected_element.getForm()) + " was removed from all_tau")
                    # all_tau.remove(random.choice(all_tau[2]))
                    # #print("Tau 3 was removed from all_tau")
                    # # except ValueError:
                    # #     #print("Element not found in the list")
                    
                    if num == 2:
                        new_tau[1].append(tp.tau_protein(2))
                        #print("Tau 2 has been created and added to new_tau. 2length: " + str(len(self.ta2)) + "\tnew2length: " + str(len(new_tau[1])))
                    
                    if num == 3:
                        new_tau[2].append(tp.tau_protein(3))
                        #print("Tau 3 has been created and added to new_tau. 3length: " + str(len(self.ta3)) + "\tnew3length: " + str(len(new_tau[2])))
                        
                    if num == 4:
                        new_tau[3].append(tp.tau_protein(4))
                        #print("Tau 4 has been created and added to new_tau. 4length: " + str(len(self.ta4)) + "\tnew4length: " + str(len(new_tau[3])))
                        
                    if num == 5:
                        new_tau[4].append(tp.tau_protein(5))
                        #print("Tau 5 has been created and added to new_tau. 5length: " + str(len(self.ta5)) + "\tnew5length: " + str(len(new_tau[4])))                  
                        
                #else:
                    #print("Tau 3 does not collide. 3Len: " + str(len(self.ta3)))
            else:
                break
            
        
        for i in range(len(self.ta4)):
            if (len(self.ta4) > 0):
                if(calculations.ifCollide(prob) == "y"):
                    
                    selected_list = []
                    while len(selected_list) == 0:
                        selected_list = random.choice(all_tau)
                    selected_element = random.choice(selected_list)
                    
                    num = selected_element.getForm() + 4
                    if num > 5:
                        num = 5
                    #print("Tau 4 collides with Tau " + str(selected_element.getForm()))
                    
                    self.ta4.pop()
                    #print("Tau 4 was removed from self.ta4. 4length: " + str(len(self.ta4))) #NEED TO REMOVE CURRENT TAU
                    
                    if selected_element.getForm() == 1 and len(self.ta1) > 0:
                        self.ta1.pop()
                        #print("Tau 1 was removed from self.ta1. 1length: " + str(len(self.ta1)))
                    
                    if selected_element.getForm() == 2 and len(self.ta2) > 0:
                        self.ta2.pop()
                        #print("Tau 2 was removed from self.ta2. 2length: " + str(len(self.ta2)))
                    
                    if selected_element.getForm() == 3 and len(self.ta3) > 0:
                        self.ta3.pop()
                        #print("Tau 3 was removed from self.ta3. 3length: " + str(len(self.ta3)))
                        
                    if selected_element.getForm() == 4 and len(self.ta4) > 0:
                        self.ta4.pop()
                        #print("Tau 4 was removed from self.ta4. 4length: " + str(len(self.ta4)))
                        
                    if selected_element.getForm() == 5 and len(self.ta5) > 0:
                        self.ta5.pop()
                        #print("Tau 5 was removed from self.ta5. 5length: " + str(len(self.ta5)))
                    
                    # # try:
                    # all_tau.remove(selected_element)
                    # #print("Tau " + str(selected_element.getForm()) + " was removed from all_tau")
                    # all_tau.remove(random.choice(all_tau[3]))
                    # #print("Tau 4 was removed from all_tau")
                    # # except ValueError:
                    # #     #print("Element not found in the list")
                    
                    if num == 2:
                        new_tau[1].append(tp.tau_protein(2))
                        #print("Tau 2 has been created and added to new_tau. 2length: " + str(len(self.ta2)) + "\tnew2length: " + str(len(new_tau[1])))
                    
                    if num == 3:
                        new_tau[2].append(tp.tau_protein(3))
                        #print("Tau 3 has been created and added to new_tau. 3length: " + str(len(self.ta3)) + "\tnew3length: " + str(len(new_tau[2])))
                        
                    if num == 4:
                        new_tau[3].append(tp.tau_protein(4))
                        #print("Tau 4 has been created and added to new_tau. 4length: " + str(len(self.ta4)) + "\tnew4length: " + str(len(new_tau[3])))
                        
                    if num == 5:
                        new_tau[4].append(tp.tau_protein(5))
                        #print("Tau 5 has been created and added to new_tau. 5length: " + str(len(self.ta5)) + "\tnew5length: " + str(len(new_tau[4])))               
                        
                #else:
                    #print("Tau 4 does not collide. 4Len: " + str(len(self.ta4)))
            else:
                break
                    
                
        for i in range(len(self.ta5)):
            if (len(self.ta5) > 0):
                if(calculations.ifCollide(prob) == "y"):
                    
                    selected_list = []
                    while len(selected_list) == 0:
                        selected_list = random.choice(all_tau)
                    selected_element = random.choice(selected_list)
                    
                    num = selected_element.getForm() + 5
                    if num > 5:
                        num = 5
                    #print("Tau 5 collides with Tau " + str(selected_element.getForm()))
                    
                    self.ta5.pop()
                    #print("Tau 5 was removed from self.ta5. 5length: " + str(len(self.ta5)))
                    
                    if selected_element.getForm() == 1 and len(self.ta1) > 0:
                        self.ta1.pop()
                        #print("Tau 1 was removed from self.ta1. 1length: " + str(len(self.ta1)))
                    
                    if selected_element.getForm() == 2 and len(self.ta2) > 0:
                        self.ta2.pop()
                        #print("Tau 2 was removed from self.ta2. 2length: " + str(len(self.ta2)))
                    
                    if selected_element.getForm() == 3 and len(self.ta3) > 0:
                        self.ta3.pop()
                        #print("Tau 3 was removed from self.ta3. 3length: " + str(len(self.ta3)))
                        
                    if selected_element.getForm() == 4 and len(self.ta4) > 0:
                        self.ta4.pop()
                        #print("Tau 4 was removed from self.ta4. 4length: " + str(len(self.ta4)))
                        
                    if selected_element.getForm() == 5 and len(self.ta5) > 0:
                        self.ta5.pop()
                        #print("Tau 5 was removed from self.ta5. 5length: " + str(len(self.ta5)))
                        
                    # # try:
                    # all_tau.remove(selected_element)
                    # #print("Tau " + str(selected_element.getForm()) + " was removed from all_tau")
                    # all_tau.remove(random.choice(all_tau[4]))
                    # #print("Tau 5 was removed from all_tau")
                    # # except ValueError:
                    # #     #print("Element not found in the list")
                    
                    if num == 2:
                        new_tau[1].append(tp.tau_protein(2))
                        #print("Tau 2 has been created and added to new_tau. 2length: " + str(len(self.ta2)) + "\tnew2length: " + str(len(new_tau[1])))
                    
                    if num == 3:
                        new_tau[2].append(tp.tau_protein(3))
                        #print("Tau 3 has been created and added to new_tau. 3length: " + str(len(self.ta3)) + "\tnew3length: " + str(len(new_tau[2])))
                        
                    if num == 4:
                        new_tau[3].append(tp.tau_protein(4))
                        #print("Tau 4 has been created and added to new_tau. 4length: " + str(len(self.ta4)) + "\tnew4length: " + str(len(new_tau[3])))
                        
                    if num == 5:
                        new_tau[4].append(tp.tau_protein(5))
                        #print("Tau 5 has been created and added to new_tau. 5length: " + str(len(self.ta5)) + "\tnew5length: " + str(len(new_tau[4])))                
                        
                #else:
                    #print("Tau 5 does not collide. 5Len: " + str(len(self.ta5)))
            else:
                break
        
        self.ta1 = self.ta1 + new_tau[0]
        #print("new_tau[0] has been added to self.ta1. 1length: " + str(len(self.ta1)))
        self.ta2 = self.ta2 + new_tau[1]
        #print("new_tau[1] has been added to self.ta2. 2length: " + str(len(self.ta2)))
        self.ta3 = self.ta3 + new_tau[2]
        #print("new_tau[2] has been added to self.ta3. 3length: " + str(len(self.ta3)))
        self.ta4 = self.ta4 + new_tau[3]
        #print("new_tau[3] has been added to self.ta4. 4length: " + str(len(self.ta4)))
        self.ta5 = self.ta5 + new_tau[4]
        #print("new_tau[4] has been added to self.ta5. 5length: " + str(len(self.ta5)))
            
            
    #If there's only tau x in the packet, can it only make tau x?
    def production(self, lmbda, cConst,time):
        all_tau = [self.ta1 + self.ta2 + self.ta3 + self.ta4 + self.ta5]
        # for i in range(int((cConst * ((time/lmbda)**(-1 * (time/lmbda)))))):
        #     num = random.randint(0,4)
        #     while(len(all_tau[num]) == 0):
        #         num = random.randint(0,4)
        #     all_tau[num].append(tp.tau_protein(num+1))
        
        if (len(all_tau)) > 0:
            for i in range(round((cConst * ((time/lmbda) * math.exp((-1 * (time/lmbda))))))):
                self.ta1.append(tp.tau_protein(1))
            
    
    
    
    def getConcentration(self):
        return len(self.ta1) + len(self.ta2) + len(self.ta3) + len(self.ta4) + len(self.ta5)
    
    
    def get_ta1_length(self):
        return len(self.ta1)
    
    
#simulation.py

import connections, calculations, create_tau, neuron_packet, tp, calculations, time




def run_sim(cube, sP):

    
    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                
        
                cube[i,j,k].cycles_collisions(0.1)
                connections.set_connection(cube) #CHANGE SO THAT IT UHYPTDUATI7TMI8TUKUJYTRSDTHYJHTRGDTHYUJ AT SAME TIME
                connections.spread(cube,sP,i,j,k)
                
    return (connections.get_cube_concentration(cube)) #have 5 
                
        
    
    
                
#tp.py

# Creates the Tau protein and it's attributes
import math

class tau_protein:
    
    def __init__(self, form):
        self.x = form
        self.distance = 0
        self.g = 0
        self.tInitial = 0
        self.probability = 0
        self.cConst = 0
        self.sT = 0
        self.totalTime = 0
        self.timeStep = 0
        self.lmbda = 0
        
    
    #Form getter
    def getForm(self):
        return self.x

    #Probability setter/getter
    
        
    

    def __str__(self):
         return "Tau protein " + str(self.x)
    
    #EQUATION VARIABLE GETTER/SETTERS (MAYBE NOT USED)
    
    # #Distance getter/setter
    # def getDist(self):
    #     return self.distance
    # def setDist(self,dist):
    #     self.distance = dist
        
    # #Calculate G/
    # def calculateG(self):
    #     #no idea
    #     pass
    
    # #Time setter/getter
    # def setTime(self,ts):
    #     self.timeStep = ts
    # def getTime(self):
    #     return self.totalTime
    
    
    # #C Constant setter/getter
    # def setC(self,c):
    #     self.cConst = c
    # def getC(self):
    #     return self.cConst
    
    # #Lambda setter
    # def setLambda(self, lam):
    #     self.lmbda = lam
    
    # #sT setter/getter
    # def calculateST(self):
    #     return (self.totalTime / self.lmbda)**(-1 * self.totalTime / self.lmbda)
    # def getST(self):
    #     return self.sT
    
    
        
        
    
    
        
        
        
    
    
            
            
            
            
            
    
    
        
        
        
        
    
    
                

  
        
        
        
    
    
            
            
            
            
            
    
    
        
        
        
        
    
    
    
    


    





       
