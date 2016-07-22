'''
Created on 14-Jul-2016

@author: deepa
'''
from PyQt4.QtCore import QString
from colWebBeamWebConnectivity import ColWebBeamWeb
from beamWebBeamWebConnectivity import BeamWebBeamWeb
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from finPlateCalc import finConn
from filletweld import FilletWeld
from plate import Plate
from bolt import Bolt
from nut import Nut 
from notch import Notch
from ISection import ISection
from nutBoltPlacement import NutBoltArray

from utilities import osdagDisplayShape

import OCC.V3d
from OCC.Quantity import Quantity_NOC_SADDLEBROWN
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM

class CommonDesignLogic(object):
    
    ###### Fincalculation file
    def call_finCalculation(self,Inputs):
        outputs = finConn(Inputs)
        return outputs
        
    def create3DBeamWebBeamWeb(self,uiObj,resultObj,dictbeamdata,dictcoldata):
        '''
        creating 3d cad model with beam web beam web
        
        '''
        uiObj = self.uiObj
        resultObj = self.resultObj
        
        ##### PRIMARY BEAM PARAMETERS #####
        
        dictbeamdata  = self.fetchColumnPara()
        pBeam_D = int(dictbeamdata[QString("D")])
        pBeam_B = int(dictbeamdata[QString("B")])
        pBeam_tw = float(dictbeamdata[QString("tw")])
        pBeam_T = float(dictbeamdata[QString("T")])
        pBeam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        pBeam_R1 = float(dictbeamdata[QString("R1")])
        pBeam_R2 = float(dictbeamdata[QString("R2")])
        pBeam_length = 800.0 # This parameter as per view of 3D cad model
        
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B = pBeam_B, T = pBeam_T,D = pBeam_D,t = pBeam_tw,
                        R1 = pBeam_R1, R2 = pBeam_R2, alpha = pBeam_alpha,
                        length = pBeam_length,notchObj = None)
        
        ##### SECONDARY BEAM PARAMETERS ######
        dictbeamdata2 = self.fetchBeamPara()
        
        sBeam_D = int(dictbeamdata2[QString("D")])
        sBeam_B = int(dictbeamdata2[QString("B")])
        sBeam_tw = float(dictbeamdata2[QString("tw")])
        sBeam_T = float(dictbeamdata2[QString("T")])
        sBeam_alpha = float(dictbeamdata2[QString("FlangeSlope")])
        sBeam_R1 = float(dictbeamdata2[QString("R1")])
        sBeam_R2 = float(dictbeamdata2[QString("R2")])
        
        #--Notch dimensions
        notchObj = Notch(R1 = pBeam_R1, height = (pBeam_T + pBeam_R1), width= ((pBeam_B -(pBeam_tw + 40))/2.0 + 10),length = sBeam_B )
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B = sBeam_B, T = sBeam_T, D = sBeam_D,
                           t = sBeam_tw, R1 = sBeam_R1, R2 = sBeam_R2, 
                           alpha = sBeam_alpha, length = 500, notchObj = notchObj)
        
        
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        fillet_length = resultObj['Plate']['height']
        fillet_thickness =  resultObj['Weld']['thickness']
        plate_width = resultObj['Plate']['width']
        plate_thick = uiObj['Plate']['Thickness (mm)']
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) /2
        nut_R = bolt_R
        bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        #bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nutThick_Calculation(bolt_dia)# bolt_dia = nut_dia
        nut_Ht = 12.2 #150
        
        #plate = Plate(L= 300,W =100, T = 10)
        plate = Plate(L= fillet_length,W =plate_width, T = plate_thick)
        
        #Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        Fweld1 = FilletWeld(L= fillet_length,b = fillet_thickness, h = fillet_thickness)

        #bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R = bolt_R,T = bolt_T, H = bolt_Ht, r = bolt_r )
         
        #nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R = bolt_R, T = nut_T,  H = nut_Ht, innerR1 = bolt_r)
        
        gap = sBeam_tw + plate_thick + nut_T
        
        nutBoltArray = NutBoltArray(resultObj,nut,bolt,gap)
        beamwebconn =  BeamWebBeamWeb(column,beam,notchObj,plate,Fweld1,nutBoltArray)
        beamwebconn.create_3dmodel()
        
        return  beamwebconn
       
    def create3DColWebBeamWeb(self,uiObj,resultObj,dictbeamdata,dictcoldata):
        '''
        creating 3d cad model with column web beam web
        
        '''
        uiObj = self.uiObj
        resultObj = self.resultObj
        
        dictbeamdata  = self.fetchBeamPara()
        ##### BEAM PARAMETERS #####
        beam_D = int(dictbeamdata[QString("D")])
        beam_B = int(dictbeamdata[QString("B")])
        beam_tw = float(dictbeamdata[QString("tw")])
        beam_T = float(dictbeamdata[QString("T")])
        beam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(dictbeamdata[QString("R1")])
        beam_R2 = float(dictbeamdata[QString("R2")])
        beam_length = 500.0 # This parameter as per view of 3D cad model
        
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B = beam_B, T = beam_T,D = beam_D,t = beam_tw,
                        R1 = beam_R1, R2 = beam_R2, alpha = beam_alpha,
                        length = beam_length,notchObj = None)
        
        ##### COLUMN PARAMETERS ######
        dictcoldata = self.fetchColumnPara()
        
        column_D = int(dictcoldata[QString("D")])
        column_B = int(dictcoldata[QString("B")])
        column_tw = float(dictcoldata[QString("tw")])
        column_T = float(dictcoldata[QString("T")])
        column_alpha = float(dictcoldata[QString("FlangeSlope")])
        column_R1 = float(dictcoldata[QString("R1")])
        column_R2 = float(dictcoldata[QString("R2")])
        
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B = column_B, T = column_T, D = column_D,
                           t = column_tw, R1 = column_R1, R2 = column_R2, alpha = column_alpha, length = 1000,notchObj = None)
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        fillet_length = resultObj['Plate']['height']
        fillet_thickness =  resultObj['Weld']['thickness']
        plate_width = resultObj['Plate']['width']
        plate_thick = uiObj['Plate']['Thickness (mm)']
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) /2
        nut_R = bolt_R
        bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        #bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        nut_T = self.nutThick_Calculation(bolt_dia)# bolt_dia = nut_dia
        nut_Ht = 12.2 #150
        
        #plate = Plate(L= 300,W =100, T = 10)
        plate = Plate(L= fillet_length,W =plate_width, T = plate_thick)
        
        #Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        Fweld1 = FilletWeld(L= fillet_length,b = fillet_thickness, h = fillet_thickness)

        #bolt = Bolt(R = 17,T = 12.5, H = 50.0, r = 10.0 )
        bolt = Bolt(R = bolt_R,T = bolt_T, H = bolt_Ht, r = bolt_r )
        #nut =Nut(R = 17, T = 17.95,  H = 12.2, innerR1 = 10.0)
        nut = Nut(R = bolt_R, T = nut_T,  H = nut_Ht, innerR1 = bolt_r)
        
        gap = beam_tw + plate_thick+ nut_T
        
        nutBoltArray = NutBoltArray(resultObj,nut,bolt,gap)
        
        colwebconn =  ColWebBeamWeb(column,beam,Fweld1,plate,nutBoltArray)
        colwebconn.create_3dmodel()
        
        return  colwebconn
        
    def create3DColFlangeBeamWeb(self,uiObj,resultObj,dictbeamdata,dictcoldata):
        '''
        Creating 3d cad model with column flange beam web connection
        
        '''
        uiObj = self.uiObj#self.getuser_inputs()
        resultObj = self.resultObj#finConn(uiObj)
        
        dictbeamdata  = self.fetchBeamPara()
        print dictbeamdata
        fillet_length = resultObj['Plate']['height']
        fillet_thickness =  resultObj['Weld']['thickness']
        plate_width = resultObj['Plate']['width']
        plate_thick = uiObj['Plate']['Thickness (mm)']
        ##### BEAM PARAMETERS #####
        beam_D = int(dictbeamdata[QString("D")])
        beam_B = int(dictbeamdata[QString("B")])
        beam_tw = float(dictbeamdata[QString("tw")])
        beam_T = float(dictbeamdata[QString("T")])
        beam_alpha = float(dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(dictbeamdata[QString("R1")])
        beam_R2 = float(dictbeamdata[QString("R2")])
        beam_length = 500.0 # This parameter as per view of 3D cad model
        
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B = beam_B, T = beam_T,D = beam_D,t = beam_tw,
                        R1 = beam_R1, R2 = beam_R2, alpha = beam_alpha,length = beam_length, notchObj = None)
        
        ##### COLUMN PARAMETERS ######
        dictcoldata = self.fetchColumnPara()
        print dictcoldata
        
        column_D = int(dictcoldata[QString("D")])
        column_B = int(dictcoldata[QString("B")])
        column_tw = float(dictcoldata[QString("tw")])
        column_T = float(dictcoldata[QString("T")])
        column_alpha = float(dictcoldata[QString("FlangeSlope")])
        column_R1 = float(dictcoldata[QString("R1")])
        column_R2 = float(dictcoldata[QString("R2")])
        
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B = column_B, T = column_T, D = column_D,
                           t = column_tw, R1 = column_R1, R2 = column_R2, alpha = column_alpha, length = 1000,notchObj = None)
        
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        fillet_length = resultObj['Plate']['height']
        fillet_thickness =  resultObj['Weld']['thickness']
        plate_width = resultObj['Plate']['width']
        plate_thick = uiObj['Plate']['Thickness (mm)']
        bolt_dia = uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = self.boltHeadDia_Calculation(bolt_dia) /2
        #bolt_R = bolt_r + 7
        nut_R = bolt_R
        bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        #bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        bolt_Ht = self.boltLength_Calculation(bolt_dia)
        # bolt_Ht =100.0 # minimum bolt length as per Indian Standard
        nut_T = self.nutThick_Calculation(bolt_dia)# bolt_dia = nut_dia
        #nut_T = 12.0 # minimum nut thickness As per Indian Standard
        nut_Ht = 12.2 #
        
        #plate = Plate(L= 300,W =100, T = 10)
        plate = Plate(L= fillet_length,W =plate_width, T = plate_thick)
        
        #Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        Fweld1 = FilletWeld(L= fillet_length,b = fillet_thickness, h = fillet_thickness)

        #bolt = Bolt(R = bolt_R,T = bolt_T, H = 38.0, r = 4.0 )
        bolt = Bolt(R = bolt_R,T = bolt_T, H = bolt_Ht, r = bolt_r )
        
         
        #nut =Nut(R = bolt_R, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut = Nut(R = bolt_R, T = nut_T,  H = nut_Ht, innerR1 = bolt_r)
        
        gap = beam_tw + plate_thick+ nut_T
        
        nutBoltArray = NutBoltArray(resultObj,nut,bolt,gap)
        
        colflangeconn =  ColFlangeBeamWeb(column,beam,Fweld1,plate,nutBoltArray)
        colflangeconn.create_3dmodel()
        return colflangeconn
    
    def display_3DModel(self,loc,display,component):
        
        display.EraseAll()
        
        display.SetModeShaded()
        
        display.DisableAntiAliasing()
        
        #self.display.set_bg_gradient_color(23,1,32,150,150,170)
        self.display.set_bg_gradient_color(51,51,102,150,150,170)
        
        if loc == "Column flange-Beam web":
            self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
        else:
            self.display.View_Iso()
            self.display.FitAll()
     
        if component == "Column":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
        elif component == "Beam":
            osdagDisplayShape(self.display, self.connectivity.get_beamModel(), material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif component == "Finplate" :
            osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display,self.connectivity.plateModel,color = 'blue', update = True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display,nutbolt,color = Quantity_NOC_SADDLEBROWN,update = True)
        elif component == "Model":
            osdagDisplayShape(self.display, self.connectivity.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivity.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
            osdagDisplayShape(self.display, self.connectivity.weldModelLeft, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivity.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display,self.connectivity.plateModel,color = 'blue', update = True)
            nutboltlist = self.connectivity.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display,nutbolt,color = Quantity_NOC_SADDLEBROWN,update = True)

    
    def call_3DModel(self,display,component,loc,uiInputs,resultInputs,dictbeamdata,dictcoldata):
        
        if loc == "Column web-Beam web":
            self.connectivityObj = self.create3DColWebBeamWeb(loc,uiInputs,resultInputs,dictbeamdata,dictcoldata)
        elif loc =="Column flange-Beam web":
            self.connectivityObj = self.create3DColFlangeBeamWeb(loc,uiInputs,resultInputs,dictbeamdata,dictcoldata)
        else:
            self.connectivityObj = self.create3DBeamWebBeamWeb(loc,uiInputs,resultInputs,dictbeamdata,dictcoldata)
            
        self.display3Dmodel(loc,display,component)
        
    def call_saveOutputs(self,inputs):
        return self.call_finCalculation(inputs)
    
    def call_designReport(self):
        #save_design()
        pass
    
#     def call_2Ddrawing(self,view):
#         #call2D_Drawing()
#         finCommonObj = FinCommonData(uiObj,resultObj,dictbeamdata,dictcoldata)
#         finCommonObj.saveToSvg(str(fileName),view)
#         pass
    
    def call_saveMessages(self):
        
        fileObj = open("Connections/Shear/Finplate/fin.log", "rb")
        data = fileObj.read()
        fileObj.close()
        
        return data
    
               
    