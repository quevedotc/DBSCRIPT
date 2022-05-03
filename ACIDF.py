import sys
import os
import numpy as np
from eppy import modeleditor
from eppy.modeleditor import IDF, iddofobject

#escolhe a versão do E+ o qrauivo climático e os idfs que serao utilizados
epwfile = 'C:/Users/Tiago/Desktop/Work/BRA_SC_Florianopolis-Luz.AP.838990_TRY.1963.epw'
iddfile = 'C:/EnergyPlusV9-2-0/Energy+.idd'
IDF.setiddname(iddfile)
idf_file = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/REAL_U6_VN_NBR.idf' #Name for base file that will be cleared
NBR_VN = 'D:/Tiago backup/Consultorias Andrea/YRUPA 2021/adicionar_no_idf_vn.idf' #Base file for natural ventilation
NBR_HVAC = 'D:/Tiago backup/Consultorias Andrea/YRUPA 2021/adicionar_no_idf_ac.idf' #base file for HVAC

#lista de zonas para sala de estar
Zona_Estar = []
# lista de zonas para dormitórios
Zona_Dormitorio = []

# lista das zonas com uso misto
zona_misto = []

# cria o IDF para ser trabalhado
IDF_VILA = IDF(idf_file)
nbr_ac = IDF(NBR_HVAC)
nbr_vn = IDF(NBR_VN)

zonas_estar = []
zonas_dorm = []

zonas = IDF_VILA.idfobjects["ZONE"]

# Seta as janelas e portas que devem ficar abertas/fechadas para HVAC

ac_surface = nbr_ac.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
aberturas = IDF_VILA.idfobjects["FENESTRATIONSURFACE:DETAILED"]
ac_vila = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
detailed = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]

#copia as schedules de HVAC pro IDF real

sch1 = nbr_ac.idfobjects["SCHEDULE:COMPACT"][7] 
sch2 = nbr_ac.idfobjects["SCHEDULE:COMPACT"][8] 
sch3 = nbr_ac.idfobjects["SCHEDULE:COMPACT"][10]
IDF_VILA.copyidfobject(sch1)
IDF_VILA.copyidfobject(sch2)
IDF_VILA.copyidfobject(sch3)


for i in range(len(ac_vila)):
    string = aberturas[i].Name

    if "Win" in string:
        ac_vila[i].Ventilation_Control_Mode = "NoVent"
        ac_vila[i].Leakage_Component_Name= "abertura_janela"
        ac_vila[i].Ventilation_Control_Zone_Temperature_Setpoint_Schedule_Name = ' '
    if "Door" in string:
       ac_vila[i].Ventilation_Control_Mode = "NoVent"
       ac_vila[i].Leakage_Component_Name= "abertura_porta"
       ac_vila[i].Ventilation_Control_Zone_Temperature_Setpoint_Schedule_Name = ' '
    

for i in range(len(ac_vila)):
    string = ac_vila[i].Surface_Name
    if "Wc" in string:            
        if "Win" in string:
            ac_vila[i].Ventilation_Control_Mode = "Constant"

#copia os outputs de HVAC para dentro do IDF
outputs = nbr_ac.idfobjects["OUTPUT:VARIABLE"]
for objeto in outputs:
    IDF_VILA.copyidfobject(objeto)

#Copia os objetos de HVAC Template e Termostato para dentro do IDF
nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"]

termostato = nbr_ac.idfobjects["HVACTEMPLATE:THERMOSTAT"][0]


nomes_zonas = ['Dorm', 'Quarto', 'Suite']
for i in range(len(zonas)):
    string = zonas[i].Name
    if any(nome in string for nome in nomes_zonas):
        nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"][0].Zone_Name = string
        variavel = nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"][0]
        IDF_VILA.copyidfobject(variavel)
    if "Estar" in string:
        nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"][1].Zone_Name = string
        variavel = nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"][1]
        IDF_VILA.copyidfobject(variavel)       
    if "Misto" in string:
        nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"][2].Zone_Name = string
        variavel = nbr_ac.idfobjects["HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM"][2]     
        IDF_VILA.copyidfobject(variavel)

IDF_VILA.copyidfobject(termostato)

name = (idf_file[:-11] + '_AC' + '_NBR' + '.idf')
print(name)
IDF_VILA.saveas(name)