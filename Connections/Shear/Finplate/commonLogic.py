'''
Created on 14-Jul-2016

@author: deepa
'''
from Connections.Shear.Finplate.finPlateCalc import finConn
class CommonDesignLogic(object):
    
    ###### Fincalculation file
    def call_finCalculation(self,Inputs):
        outputs = finConn(Inputs)
        return outputs
        
        
    def call_3DModel(self):
        #create3DColWebBeamWeb()
        #create3DColFlangeBeamWeb
        #create3DBeamWebBeamWeb
        #display3Dmodel(loc,display,component)
        
        pass
    def call_designReport(self):
        #save_design()
        pass
    def call_2Ddrawing(self,view):
        #call2D_Drawing()
        pass
    def call_saveMessages(self):
        pass
    