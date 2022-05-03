
import sys
import os
from eppy.idf_msequence import Idf_MSequence
import numpy as np
from eppy import modeleditor
from eppy.modeleditor import IDF, iddofobject

#escolhe a versão do E+ o qrauivo climático e os idfs que serao utilizados
epwfile = 'C:/Users/Tiago/Desktop/Work/BRA_SC_Florianopolis-Luz.AP.838990_TRY.1963.epw'
iddfile = 'C:/EnergyPlusV9-2-0/Energy+.idd'
IDF.setiddname(iddfile)
idf_file = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/REAL_U1_VN_NBR.idf' #Name for base file that will be cleared
NBR_VN = 'D:/Tiago backup/Consultorias Andrea/Bodoquena//adicionar_no_idf_vn.idf' #Base file for natural ventilation
NBR_HVAC = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/adicionar_no_idf_ac.idf' #base file for HVAC


nbr_vn = IDF(NBR_VN)
nbr_ac = IDF(NBR_HVAC)
# cria o IDF para ser trabalhado
IDF_VILA = IDF(idf_file)


aberturas= IDF_VILA.idfobjects["FENESTRATIONSURFACE:DETAILED"]
afn_janelas = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
afn_detailed = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]
afn_zones = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]


nomes_zonas = ['Dorm', 'Quarto', 'Suite']
janelas_com_veneziana = IDF_VILA.idfobjects['WINDOWSHADINGCONTROL']
janelas = IDF_VILA.idfobjects['AIRFLOWNETWORK:MULTIZONE:SURFACE']

for i in range(len(janelas_com_veneziana)):
    string = janelas_com_veneziana[i].Fenestration_Surface_1_Name
    string2 = janelas_com_veneziana[i].Schedule_Name

    for i in range(len(janelas)):
        string3 = janelas[i].Surface_Name
        if string == string3 and string2 == "On 24/7":
            janelas[i].Ventilation_Control_Mode = "NoVent"
            janelas[i].Ventilation_Control_Zone_Temperature_Setpoint_Schedule_Name = ''
            janelas[i].Venting_Availability_Schedule_Name = ''  







os.chdir('D:/Tiago backup/Consultorias Andrea/Bodoquena')

IDF_VILA.save()