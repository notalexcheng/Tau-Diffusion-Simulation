
#neuron_packet.py

#Creates the neuron
import tp
import calculations

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
                    while len(selected_list) == 0 and selected_list is not self.ta5:
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
    
