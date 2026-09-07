
import connections, calculations, create_tau, neuron_packet, tp, calculations, time
import numpy as np




def run_sim(cube, sP, t,lmbda, cConst, prob, timeConstant):

    

    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                cube[i,j,k].cycles_collisions(prob) #PASSED IN FROM FRONTEND
                cube[i,j,k].production(lmbda, cConst, timeConstant*t)
    

    cube_copy = np.copy(cube)
    connections.set_connection(cube_copy)

    
    for i in range(len(cube)):
        for j in range(len(cube[0])):
            for k in range(len(cube[0][0])):
                connections.spread(cube_copy,cube,sP,i,j,k)
                
    return (connections.get_cube_concentration(cube)) #have 5 
                
        
    
    
                
