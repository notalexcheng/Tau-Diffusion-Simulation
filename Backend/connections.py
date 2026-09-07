    
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
    

    
def spread(real,cube, percent, x, y, z):
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
                real[x,y,z+1].add_tau1(move_back)
                real[x,y,z].remove_tau1(move_back)
            else:
                real[x,y,z+1].add_tau1(round(moved_tau1 * move_back))
                real[x,y,z].remove_tau1(round(moved_tau1 * move_back))
            #print(f"{moved_tau1 * move_back} tau1 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau1):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau1 * move_bottom > move_bottom):
                real[x+1,y,z].add_tau1(move_bottom)
                real[x,y,z].remove_tau1(move_bottom)
            else:
                real[x+1,y,z].add_tau1(round(moved_tau1 * move_bottom))
                real[x,y,z].remove_tau1(round(moved_tau1 * move_bottom))
            #print(f"{moved_tau1 * move_back} tau1 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau1):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau1 * move_front > move_front):
                real[x,y,z-1].add_tau1(move_front)
                real[x,y,z].remove_tau1(move_front)
            else:
                real[x,y,z-1].add_tau1(round(moved_tau1 * move_front))
                real[x,y,z].remove_tau1(round(moved_tau1 * move_front))
            #print(f"{moved_tau1 * move_back} tau1 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau1) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau1 * move_left > move_left):
                real[x,y-1,z].add_tau1(move_left)
                real[x,y,z].remove_tau1(move_left)
                
            else:
                real[x,y-1,z].add_tau1(round(moved_tau1 * move_left))
                real[x,y,z].remove_tau1(round(moved_tau1 * move_left))
            #print(f"{moved_tau1 * move_back} tau1 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau1):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau1 * move_right > move_right):
                real[x,y+1,z].add_tau1(move_right)
                real[x,y,z].remove_tau1(move_right)
            else:
                real[x,y+1,z].add_tau1(round(moved_tau1 * move_right))
                real[x,y,z].remove_tau1(round(moved_tau1 * move_right))
            #print(f"{moved_tau1 * move_back} tau1 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau1):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau1 * move_top > move_top):
                real[x-1,y,z].add_tau1(move_top)
                real[x,y,z].remove_tau1(move_top)
            else:
                real[x-1,y,z].add_tau1(round(moved_tau1 * move_top))
                real[x,y,z].remove_tau1(round(moved_tau1 * move_top))
            #print(f"{moved_tau1 * move_back} tau1 was added to top neighbor")
                #add tau cube[x-1,y,z]
    
        #tau 2 spread
        if (connections["back"] is not None and 'back' in least_tau2):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau2 * move_back > move_back):
                real[x,y,z+1].add_tau2(move_back)
                real[x,y,z].remove_tau2(move_back)
            else:
                real[x,y,z+1].add_tau2(round(moved_tau2 * move_back))
                real[x,y,z].remove_tau2(round(moved_tau2 * move_back))
            #print(f"{moved_tau2 * move_back} tau2 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau2):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau2 * move_bottom > move_bottom):
                real[x+1,y,z].add_tau2(move_bottom)
                real[x,y,z].remove_tau2(move_bottom)
            else:
                real[x+1,y,z].add_tau2(round(moved_tau2 * move_bottom))
                real[x,y,z].remove_tau2(round(moved_tau2 * move_bottom))
            #print(f"{moved_tau2 * move_back} tau2 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau2):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau2 * move_front > move_front):
                real[x,y,z-1].add_tau2(move_front)
                real[x,y,z].remove_tau2(move_front)
            else:
                real[x,y,z-1].add_tau2(round(moved_tau2 * move_front))
                real[x,y,z].remove_tau2(round(moved_tau2 * move_front))
            #print(f"{moved_tau2 * move_back} tau2 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau2) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau2 * move_left > move_left):
                real[x,y-1,z].add_tau2(move_left)
                real[x,y,z].remove_tau2(move_left)
                
            else:
                real[x,y-1,z].add_tau2(round(moved_tau2 * move_left))
                real[x,y,z].remove_tau2(round(moved_tau2 * move_left))
            #print(f"{moved_tau2 * move_back} tau2 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau2):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau2 * move_right > move_right):
                real[x,y+1,z].add_tau2(move_right)
                real[x,y,z].remove_tau2(move_right)
            else:
                real[x,y+1,z].add_tau2(round(moved_tau2 * move_right))
                real[x,y,z].remove_tau2(round(moved_tau2 * move_right))
            #print(f"{moved_tau2 * move_back} tau2 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau2):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau2 * move_top > move_top):
                real[x-1,y,z].add_tau2(move_top)
                real[x,y,z].remove_tau2(move_top)
            else:
                real[x-1,y,z].add_tau2(round(moved_tau2 * move_top))
                real[x,y,z].remove_tau2(round(moved_tau2 * move_top))
            #print(f"{moved_tau2 * move_back} tau2 was added to top neighbor")
        
    
    
    
    #tau 3 spread   
        if (connections["back"] is not None and 'back' in least_tau3):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau3 * move_back > move_back):
                real[x,y,z+1].add_tau3(move_back)
                real[x,y,z].remove_tau3(move_back)
            else:
                real[x,y,z+1].add_tau3(round(moved_tau3 * move_back))
                real[x,y,z].remove_tau3(round(moved_tau3 * move_back))
            #print(f"{moved_tau3 * move_back} tau3 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau3):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau3 * move_bottom > move_bottom):
                real[x+1,y,z].add_tau3(move_bottom)
                real[x,y,z].remove_tau3(move_bottom)
            else:
                real[x+1,y,z].add_tau3(round(moved_tau3 * move_bottom))
                real[x,y,z].remove_tau3(round(moved_tau3 * move_bottom))
            #print(f"{moved_tau3 * move_back} tau3 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau3):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau3 * move_front > move_front):
                real[x,y,z-1].add_tau3(move_front)
                real[x,y,z].remove_tau3(move_front)
            else:
                real[x,y,z-1].add_tau3(round(moved_tau3 * move_front))
                real[x,y,z].remove_tau3(round(moved_tau3 * move_front))
            #print(f"{moved_tau3 * move_back} tau3 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau3) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau3 * move_left > move_left):
                real[x,y-1,z].add_tau3(move_left)
                real[x,y,z].remove_tau3(move_left)
                
            else:
                real[x,y-1,z].add_tau3(round(moved_tau3 * move_left))
                real[x,y,z].remove_tau3(round(moved_tau3 * move_left))
            #print(f"{moved_tau3 * move_back} tau3 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau3):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau3 * move_right > move_right):
                real[x,y+1,z].add_tau3(move_right)
                real[x,y,z].remove_tau3(move_right)
            else:
                real[x,y+1,z].add_tau3(round(moved_tau3 * move_right))
                real[x,y,z].remove_tau3(round(moved_tau3 * move_right))
            #print(f"{moved_tau3 * move_back} tau3 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau3):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau3 * move_top > move_top):
                real[x-1,y,z].add_tau3(move_top)
                real[x,y,z].remove_tau3(move_top)
            else:
                real[x-1,y,z].add_tau3(round(moved_tau3 * move_top))
                real[x,y,z].remove_tau3(round(moved_tau3 * move_top))
            #print(f"{moved_tau3 * move_back} tau3 was added to top neighbor")
        
    
    
    #tau 4 spread   
        if (connections["back"] is not None and 'back' in least_tau4):
            tau_back = connections["back"] / total_connection
            move_back = calculations.move_tau(cube[x,y,z],tau_back,percent)
            #print(f"{move_back} tau will be moved back")
            if (moved_tau4 * move_back > move_back):
                real[x,y,z+1].add_tau4(move_back)
                real[x,y,z].remove_tau4(move_back)
            else:
                real[x,y,z+1].add_tau4(round(moved_tau4 * move_back))
                real[x,y,z].remove_tau4(round(moved_tau4 * move_back))
            #print(f"{moved_tau4 * move_back} tau4 was added to back neighbor")
            
            
            #add tau cube[x,y,z+1]
        if (connections["bottom"] is not None and 'bottom' in least_tau4):
            tau_bottom = connections["bottom"] / total_connection
            move_bottom = calculations.move_tau(cube[x,y,z],tau_bottom,percent)
            #print(f"{move_bottom} tau will be moved to the bottom")
            if (moved_tau4 * move_bottom > move_bottom):
                real[x+1,y,z].add_tau4(move_bottom)
                real[x,y,z].remove_tau4(move_bottom)
            else:
                real[x+1,y,z].add_tau4(round(moved_tau4 * move_bottom))
                real[x,y,z].remove_tau4(round(moved_tau4 * move_bottom))
            #print(f"{moved_tau4 * move_back} tau4 was added to bottom neighbor")
            #add tau cube[x+1,y,z]
            
        if (connections["front"] is not None and 'front' in least_tau4):
            tau_front = connections["front"] / total_connection
            move_front = calculations.move_tau(cube[x,y,z],tau_front,percent)
            #print(f"{move_front} tau will be moved to the front")
            if (moved_tau4 * move_front > move_front):
                real[x,y,z-1].add_tau4(move_front)
                real[x,y,z].remove_tau4(move_front)
            else:
                real[x,y,z-1].add_tau4(round(moved_tau4 * move_front))
                real[x,y,z].remove_tau4(round(moved_tau4 * move_front))
            #print(f"{moved_tau4 * move_back} tau4 was added to front neighbor")
            #add tau cube[x,y,z-1]
            
        if (connections["left"] is not None and 'left' in least_tau4) :
            tau_left = connections["left"] / total_connection
            move_left = calculations.move_tau(cube[x,y,z],tau_left,percent)
            #print(f"{move_left} tau will be moved left")
            if (moved_tau4 * move_left > move_left):
                real[x,y-1,z].add_tau4(move_left)
                real[x,y,z].remove_tau4(move_left)
                
            else:
                real[x,y-1,z].add_tau4(round(moved_tau4 * move_left))
                real[x,y,z].remove_tau4(round(moved_tau4 * move_left))
            #print(f"{moved_tau4 * move_back} tau4 was added to left neighbor")
            #add tau cube[x,y-1,z]
            
        if (connections["right"] is not None and 'right' in least_tau4):
            tau_right = connections["right"] / total_connection
            move_right = calculations.move_tau(cube[x,y,z],tau_right,percent)
            #print(f"{move_right} tau will be moved right")
            if (moved_tau4 * move_right > move_right):
                real[x,y+1,z].add_tau4(move_right)
                real[x,y,z].remove_tau4(move_right)
            else:
                real[x,y+1,z].add_tau4(round(moved_tau4 * move_right))
                real[x,y,z].remove_tau4(round(moved_tau4 * move_right))
            #print(f"{moved_tau4 * move_back} tau4 was added to right neighbor")
            #add tau cube[x,y+1,z]
            
        if (connections["top"] is not None and 'top' in least_tau4):
            tau_top = connections["top"] / total_connection
            move_top = calculations.move_tau(cube[x,y,z],tau_top,percent)
            #print(f"{move_top} tau will be moved to the top")
            if (moved_tau4 * move_top > move_top):
                real[x-1,y,z].add_tau4(move_top)
                real[x,y,z].remove_tau4(move_top)
            else:
                real[x-1,y,z].add_tau4(round(moved_tau4 * move_top))
                real[x,y,z].remove_tau4(round(moved_tau4 * move_top))
            #print(f"{moved_tau4 * move_back} tau4 was added to top neighbor")
            
        
    
def get_cube_concentration(cube):
    #np.empty((len(cube),len(cube[0]),len(cube[0][0])), dtype = object)
    a = [[[[0, 0, 0, 0, 0] for i in range(len(cube[0][0]))] for j in range(len(cube[0]))] for k in range(len(cube))]
    
    
    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                    a[i][j][k] = [cube[i,j,k].get_tau_length(1), cube[i,j,k].get_tau_length(2), cube[i,j,k].get_tau_length(3), cube[i,j,k].get_tau_length(4), cube[i,j,k].get_tau_length(5)]
    
    return a
    
    
    
    
    


    
