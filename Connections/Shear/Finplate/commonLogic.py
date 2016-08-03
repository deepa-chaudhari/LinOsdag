'''
Created on 14-Jul-2016

@author: deepa
'''
import os
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
from Connections.Shear.Finplate.drawing_2D import FinCommonData

from reportGenerator import save_html

class CommonDesignLogic(object):
    
    def __init__(self, uiObj, dictbeamdata, dictcoldata, loc, component, bolt_R, bolt_T, bolt_Ht, nut_T, display): 
                
        self.uiObj = uiObj
        self.dictbeamdata = dictbeamdata
        self.dictcoldata = dictcoldata
        self.loc = loc
        self.component = component
        self.bolt_R = bolt_R
        self.bolt_T = bolt_T
        self.bolt_Ht = bolt_Ht
        self.nut_T = nut_T
        self.display = display
        self.resultObj = self.call_finCalculation()
        self.connectivityObj = None
    
    #============================= FinCalculation ===========================================
    
    def call_finCalculation(self):#Done
        outputs = finConn(self.uiObj)
        return outputs
    
    #=========================================================================================

    def create3DBeamWebBeamWeb(self):
        '''self,uiObj,resultObj,dictbeamdata,dictcoldata):
        creating 3d cad model with beam web beam web
        
        '''
        ##### PRIMARY BEAM PARAMETERS #####
        pBeam_D = int(self.dictcoldata[QString("D")])
        pBeam_B = int(self.dictcoldata[QString("B")])
        pBeam_tw = float(self.dictcoldata[QString("tw")])
        pBeam_T = float(self.dictcoldata[QString("T")])
        pBeam_alpha = float(self.dictcoldata[QString("FlangeSlope")])
        pBeam_R1 = float(self.dictcoldata[QString("R1")])
        pBeam_R2 = float(self.dictcoldata[QString("R2")])
        pBeam_length = 800.0 # This parameter as per view of 3D cad model
        
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        column = ISection(B = pBeam_B, T = pBeam_T,D = pBeam_D,t = pBeam_tw,
                        R1 = pBeam_R1, R2 = pBeam_R2, alpha = pBeam_alpha,
                        length = pBeam_length,notchObj = None)
        
        ##### SECONDARY BEAM PARAMETERS ######
        
        sBeam_D = int(self.dictbeamdata[QString("D")])
        sBeam_B = int(self.dictbeamdata[QString("B")])
        sBeam_tw = float(self.dictbeamdata[QString("tw")])
        sBeam_T = float(self.dictbeamdata[QString("T")])
        sBeam_alpha = float(self.dictbeamdata[QString("FlangeSlope")])
        sBeam_R1 = float(self.dictbeamdata[QString("R1")])
        sBeam_R2 = float(self.dictbeamdata[QString("R2")])
        
        #--Notch dimensions
        notchObj = Notch(R1 = pBeam_R1, height = (pBeam_T + pBeam_R1), width= ((pBeam_B -(pBeam_tw + 40))/2.0 + 10),length = sBeam_B )
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B = sBeam_B, T = sBeam_T, D = sBeam_D,
                           t = sBeam_tw, R1 = sBeam_R1, R2 = sBeam_R2, 
                           alpha = sBeam_alpha, length = 500, notchObj = notchObj)
        
        
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        fillet_length = self.resultObj['Plate']['height']
        fillet_thickness =  self.resultObj['Weld']['thickness']
        plate_width = self.resultObj['Plate']['width']
        plate_thick = self.uiObj['Plate']['Thickness (mm)']
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        bolt_R = self.bolt_R
        nut_R = bolt_R
        bolt_T = self.bolt_T
        bolt_Ht = self.bolt_Ht
        nut_T = self.nut_T
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
        
        nutBoltArray = NutBoltArray(self.  resultObj,nut,bolt,gap)
        beamwebconn =  BeamWebBeamWeb(column,beam,notchObj,plate,Fweld1,nutBoltArray)
        beamwebconn.create_3dmodel()
        
        return  beamwebconn
    
    #=========================================================================================
    
    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web
        
        '''
        #uiObj = self.uiObj
        #resultObj = self.resultObj
        
        #self.dictbeamdata  = self.fetchBeamPara()
        ##### BEAM PARAMETERS #####
        beam_D = int(self.dictbeamdata[QString("D")])
        beam_B = int(self.dictbeamdata[QString("B")])
        beam_tw = float(self.dictbeamdata[QString("tw")])
        beam_T = float(self.dictbeamdata[QString("T")])
        beam_alpha = float(self.dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(self.dictbeamdata[QString("R1")])
        beam_R2 = float(self.dictbeamdata[QString("R2")])
        beam_length = 500.0 # This parameter as per view of 3D cad model
        
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B = beam_B, T = beam_T,D = beam_D,t = beam_tw,
                        R1 = beam_R1, R2 = beam_R2, alpha = beam_alpha,
                        length = beam_length,notchObj = None)
        
        ##### COLUMN PARAMETERS ######
        #self.dictcoldata = self.fetchColumnPara()
        
        column_D = int(self.dictcoldata[QString("D")])
        column_B = int(self.dictcoldata[QString("B")])
        column_tw = float(self.dictcoldata[QString("tw")])
        column_T = float(self.dictcoldata[QString("T")])
        column_alpha = float(self.dictcoldata[QString("FlangeSlope")])
        column_R1 = float(self.dictcoldata[QString("R1")])
        column_R2 = float(self.dictcoldata[QString("R2")])
        
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B = column_B, T = column_T, D = column_D,
                           t = column_tw, R1 = column_R1, R2 = column_R2, alpha = column_alpha, length = 1000,notchObj = None)
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        fillet_length = self.resultObj['Plate']['height']
        fillet_thickness =  self.resultObj['Weld']['thickness']
        plate_width = self.resultObj['Plate']['width']
        plate_thick = self.uiObj['Plate']['Thickness (mm)']
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        #bolt_R = self.boltHeadDia_Calculation(bolt_dia) /2
        bolt_R = self.bolt_R
        nut_R = bolt_R
        #bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_T = self.bolt_T
        #bolt_Ht = self.boltLength_Calculation(bolt_dia)
        bolt_Ht = self.bolt_Ht
        #bolt_Ht = 50.0 # minimum bolt length as per Indian Standard IS 3757(1989)
        #nut_T = self.nutThick_Calculation(bolt_dia)# bolt_dia = nut_dia
        nut_T = self.nut_T
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
        
        nutBoltArray = NutBoltArray(self.resultObj,nut,bolt,gap)
        
        colwebconn =  ColWebBeamWeb(column,beam,Fweld1,plate,nutBoltArray)
        colwebconn.create_3dmodel()
        
        return  colwebconn
    #=========================================================================================
    
    def create3DColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection
        
        '''
        #self.dictbeamdata  = self.fetchBeamPara()
        #print self.dictbeamdata
        #self.resultObj = self.call_finCalculation()
        fillet_length = self.resultObj['Plate']['height']
        fillet_thickness =  self.resultObj['Weld']['thickness']
        plate_width = self.resultObj['Plate']['width']
        plate_thick = self.uiObj['Plate']['Thickness (mm)']
        ##### BEAM PARAMETERS #####
        beam_D = int(self.dictbeamdata[QString("D")])
        beam_B = int(self.dictbeamdata[QString("B")])
        beam_tw = float(self.dictbeamdata[QString("tw")])
        beam_T = float(self.dictbeamdata[QString("T")])
        beam_alpha = float(self.dictbeamdata[QString("FlangeSlope")])
        beam_R1 = float(self.dictbeamdata[QString("R1")])
        beam_R2 = float(self.dictbeamdata[QString("R2")])
        beam_length = 500.0 # This parameter as per view of 3D cad model
        
        #beam = ISectionold(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        beam = ISection(B = beam_B, T = beam_T,D = beam_D,t = beam_tw,
                        R1 = beam_R1, R2 = beam_R2, alpha = beam_alpha,length = beam_length, notchObj = None)
        
        ##### COLUMN PARAMETERS ######
        
        column_D = int(self.dictcoldata[QString("D")])
        column_B = int(self.dictcoldata[QString("B")])
        column_tw = float(self.dictcoldata[QString("tw")])
        column_T = float(self.dictcoldata[QString("T")])
        column_alpha = float(self.dictcoldata[QString("FlangeSlope")])
        column_R1 = float(self.dictcoldata[QString("R1")])
        column_R2 = float(self.dictcoldata[QString("R2")])
        
        #column = ISectionold(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        column = ISection(B = column_B, T = column_T, D = column_D,
                           t = column_tw, R1 = column_R1, R2 = column_R2, alpha = column_alpha, length = 1000,notchObj = None)
        
        #### WELD,PLATE,BOLT AND NUT PARAMETERS #####
        
        fillet_length = self.resultObj['Plate']['height']
        fillet_thickness =  self.resultObj['Weld']['thickness']
        plate_width = self.resultObj['Plate']['width']
        plate_thick = self.uiObj['Plate']['Thickness (mm)']
        bolt_dia = self.uiObj["Bolt"]["Diameter (mm)"]
        bolt_r = bolt_dia/2
        #bolt_R = self.boltHeadDia_Calculation(bolt_dia) /2
        bolt_R = self.bolt_R
        #bolt_R = bolt_r + 7
        nut_R = bolt_R
        #bolt_T = self.boltHeadThick_Calculation(bolt_dia) 
        bolt_T = self.bolt_T
        #bolt_T = 10.0 # minimum bolt thickness As per Indian Standard
        #bolt_Ht = self.boltLength_Calculation(bolt_dia)
        bolt_Ht = self.bolt_Ht
        # bolt_Ht =100.0 # minimum bolt length as per Indian Standard
        #nut_T = self.nutThick_Calculation(bolt_dia)# bolt_dia = nut_dia
        nut_T = self.nut_T
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
        
        nutBoltArray = NutBoltArray(self.resultObj,nut,bolt,gap)
        
        colflangeconn =  ColFlangeBeamWeb(column,beam,Fweld1,plate,nutBoltArray)
        colflangeconn.create_3dmodel()
        return colflangeconn
    #=========================================================================================
    def display_3DModel(self):
        
        self.display.EraseAll()
        
        self.display.SetModeShaded()
        
        self.display.DisableAntiAliasing()
        
        #self.display.set_bg_gradient_color(23,1,32,150,150,170)
        self.display.set_bg_gradient_color(51,51,102,150,150,170)
        
        if self.loc == "Column flange-Beam web":
            self.display.View.SetProj(OCC.V3d.V3d_XnegYnegZpos)
        else:
            self.display.View_Iso()
            self.display.FitAll()
     
        if self.component == "Column":
            osdagDisplayShape(self.display, self.connectivityObj.columnModel, update=True)
        elif self.component == "Beam":
            osdagDisplayShape(self.display, self.connectivityObj.get_beamModel(), material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif self. component == "Finplate" :
            osdagDisplayShape(self.display, self.connectivityObj.weldModelLeft, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivityObj.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display,self.connectivityObj.plateModel,color = 'blue', update = True)
            nutboltlist = self.connectivityObj.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display,nutbolt,color = Quantity_NOC_SADDLEBROWN,update = True)
        elif self.component == "Model":
            osdagDisplayShape(self.display, self.connectivityObj.columnModel, update=True)
            osdagDisplayShape(self.display, self.connectivityObj.beamModel, material = Graphic3d_NOT_2D_ALUMINUM, update=True)
            osdagDisplayShape(self.display, self.connectivityObj.weldModelLeft, color = 'red', update = True)
            osdagDisplayShape(self.display, self.connectivityObj.weldModelRight, color = 'red', update = True)
            osdagDisplayShape(self.display,self.connectivityObj.plateModel,color = 'blue', update = True)
            nutboltlist = self.connectivityObj.nutBoltArray.getModels()
            for nutbolt in nutboltlist:
                osdagDisplayShape(self.display,nutbolt,color = Quantity_NOC_SADDLEBROWN,update = True)

    #=========================================================================================
    def call_3DModel(self,flag):#Done
        
        if flag == True:
            
            if self.loc == "Column web-Beam web":
                self.connectivityObj = self.create3DColWebBeamWeb()
                
            elif self.loc =="Column flange-Beam web":
                self.connectivityObj = self.create3DColFlangeBeamWeb()
                
            else:
                self.connectivityObj = self.create3DBeamWebBeamWeb()
                
            self.display_3DModel()
            
        else:
            self.display.EraseAll()
    #=========================================================================================
    def call_saveOutputs(self): #Done
        
        return self.call_finCalculation(self.uiObj)
    
<<<<<<< HEAD
    #=========================================================================================
=======
    
>>>>>>> LinuxOsdag/master
    def call2D_Drawing(self,view, filename): #DONE
        
        fname = str(filename)
        
        if view == "All":
            self.display.set_bg_gradient_color(255,255,255,255,255,255)
            self.display.ExportToImage('output/finplate/Report/3D_Model.png')
            
        else:
            f = open(fname,'w')
            f.close()
            
        self.callDesired_View(fname, view)
<<<<<<< HEAD
    #=========================================================================================
        
    def callDesired_View(self,filename,view):# Done
        
=======
    
        
    def callDesired_View(self,filename,view):
        
>>>>>>> LinuxOsdag/master
        finCommonObj = FinCommonData(self.uiObj,self.resultObj,self.dictbeamdata,self.dictcoldata)
        finCommonObj.saveToSvg(str(filename),view)
    #========================================================================================= 
    def call_saveMessages(self): # Done
        
        fileName ="Connections/Shear/Finplate/fin.log"
        
        return fileName
    
    #=========================================================================================
    def call_designReport(self,htmlfilename,profileSummary):
        
        fileName = str(htmlfilename)
        if os.path.isfile(fileName):
            print self.uiObj
            save_html( self.resultObj,self.uiObj, self.dictbeamdata, self.dictcoldata,profileSummary,htmlfilename)
        
    #=========================================================================================   
        
    def laod_userProfile(self):
        pass
    
               
    