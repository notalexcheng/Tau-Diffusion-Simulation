
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
    
    
        
        
    
    
        
        
        
    
    
            
            
            
            
            
    
    
        
        
        
        
    
    
