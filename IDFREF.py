import sys
import os
import numpy as np
from eppy import modeleditor
from eppy.modeleditor import IDF, iddofobject



epwfile = 'C:/Users/Tiago/Desktop/Work/BRA_SC_Florianopolis-Luz.AP.838990_TRY.1963.epw'
iddfile = 'C:/EnergyPlusV9-2-0/Energy+.idd'
IDF.setiddname(iddfile)
idf_file = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/REF_U6_VN_NBR.idf'
NBR_VN = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/adicionar_no_idf_vn.idf' #Base file for natural ventilation
NBR_HVAC = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/adicionar_no_idf_ac.idf' #base file for HVAC
NBR_OPENING = 'D:/Tiago backup/Consultorias Andrea/YRUPA 2021/opening_detailed.idf' #base file for HVAC
nbr_vn = IDF(NBR_VN)
nbr_ac = IDF(NBR_HVAC)
opening = IDF(NBR_OPENING)
# lista de zonas para sala de estar
Zona_Estar = []
# lista de zonas para dormitórios
Zona_Dormitorio = []

# lista das zonas com uso misto
zona_misto = []

# cria o IDF para ser trabalhado
IDF_VILA = IDF(idf_file)

#Alguns objetos do E+ do IDF template e do IDF da vila
aberturas= IDF_VILA.idfobjects["FENESTRATIONSURFACE:DETAILED"]
building_surfaces = IDF_VILA.idfobjects["BUILDINGSURFACE:DETAILED"]
referencia_materials = nbr_vn.idfobjects["MATERIAL"]
referencia_constructions = nbr_vn.idfobjects["CONSTRUCTION"]
constructions_idf = IDF_VILA.idfobjects["CONSTRUCTION"]
materiais_idf = IDF_VILA.idfobjects["MATERIAL"]
framedivider = nbr_vn.idfobjects["WINDOWPROPERTY:FRAMEANDDIVIDER"]

# lista de constructions da referencia
lista_ref = []
lista_construction = []

#listas auxiliares para absortancia e nome das constructions internas paredes
abs_par = []
nome_paredes = []

#listas auxiliares para absortancia e nome das constructions do piso
abs_piso = []
nome_piso = []

#listas auxiliares para absortancia e nome das constructions da cobertura
abs_forro = []
nome_forro = []

# Adiciona o objeto frame divider da REF
#adicionar = nbr_vn.idfobjects["WINDOWPROPERTY:FRAMEANDDIVIDER"][0]
#IDF_VILA.copyidfobject(adicionar)

#coloca nas janelas o frame da referencia
#for i in range(len(aberturas)):
#    string = aberturas[i].Name
#    if "Win" in string:
#        aberturas[i].Frame_and_Divider_Name = "framedivider"

#limpa do IDF as venezianas
lista_veneziana = [IDF_VILA.idfobjects["WINDOWMATERIAL:BLIND"],  IDF_VILA.idfobjects["WINDOWSHADINGCONTROL"]]

for veneziana in lista_veneziana:
    veneziana.clear()
# LIMPA AS CONSTRUCTIONS QUE VEM DO DB COM SHADING
for construction in constructions_idf:
    string = construction.Outside_Layer
    if '20001' in string:
        constructions_idf.remove(construction)
    if '30000' in string:
        constructions_idf.remove(construction)

#limpa do IDF os shadings e as schedules de transmitancia
'''lista_shadings = IDF_VILA.idfobjects["SHADING:BUILDING:DETAILED"]
lista_shadings.clear()'''

#adiciona os detailed openings da nBR
detailed_opening = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]
detailed_opening.clear()

afn_detailed = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]
for i in range(len(afn_detailed)):
    variavel = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][i]
    IDF_VILA.copyidfobject(variavel)

afn_surface_vila = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
afn_surface_vila.clear()

afn_surface = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
aberturas= IDF_VILA.idfobjects["FENESTRATIONSURFACE:DETAILED"]

nomes_zonas = ['Dorm', 'Quarto', 'Suite']


for i in range(len(aberturas)):
    string = aberturas[i].Name
    string1 = aberturas[i].Outside_Boundary_Condition_Object
    if "Estar" in string:
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][0].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][0].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][0]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if any(nome in string for nome in nomes_zonas): 
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][3].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][3].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][3]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            if "Wc" in string1:
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
                variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
                IDF_VILA.copyidfobject(variavel)
            else:
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][2].Surface_Name = string
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][2].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
                variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][2]
                IDF_VILA.copyidfobject(variavel)

    if "Wc" in string:     
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][9].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][9].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][9]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if "Lavanderia" in string:     
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if "Circ" in string:     
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if "Misto" in string:
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][4].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][4].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][4]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][7].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][7].Leakage_Component_Name = opening.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][7]
            IDF_VILA.copyidfobject(variavel)


par_ext =  nbr_vn.idfobjects['CONSTRUCTION'][2]
mat_par_ext = nbr_vn.idfobjects["MATERIAL"][4]
IDF_VILA.copyidfobject(par_ext)
IDF_VILA.copyidfobject(mat_par_ext)

porta = nbr_vn.idfobjects['CONSTRUCTION'][4]
mat_porta = nbr_vn.idfobjects["MATERIAL"][1]
IDF_VILA.copyidfobject(porta)
IDF_VILA.copyidfobject(mat_porta)

janela = nbr_vn.idfobjects['CONSTRUCTION'][5]
mat_janela = nbr_vn.idfobjects["WINDOWMATERIAL:GLAZING"][0]
IDF_VILA.copyidfobject(janela)
IDF_VILA.copyidfobject(mat_janela)

telha = nbr_vn.idfobjects['CONSTRUCTION'][1]
mat_cob = nbr_vn.idfobjects["MATERIAL"][5]
IDF_VILA.copyidfobject(telha)
IDF_VILA.copyidfobject(mat_cob)

forro = nbr_vn.idfobjects['CONSTRUCTION'][6]
mat_forro = nbr_vn.idfobjects["MATERIAL"][3]

IDF_VILA.copyidfobject(forro)
IDF_VILA.copyidfobject(mat_forro)




# coloca o nome das constructions das aberturas nos locais corretos
for i in range(len(aberturas)):
    string = aberturas[i].Name
    if "Win" in string:
        aberturas[i].Construction_Name = 'vidro'
    if "Door" in string:
        aberturas[i].Construction_Name = "porta"

# coloca o nome das constructions de paredes internas da referencia no building surface detailed   
for i in range(len(building_surfaces)):
    for ref in lista_construction:
        string = ref
        string2 = building_surfaces[i].Construction_Name
        if string2 in string:
            building_surfaces[i].Construction_Name = ref
            
# coloca o nome das constructions das paredes externas da referencia no building surface detailed           
for i in range(len(building_surfaces)):
    string = building_surfaces[i].Name
    if "Wall" in string:
        building_surfaces[i].Construction_Name = " par_ext"

for i in range(len(building_surfaces)):
    string = building_surfaces[i].Construction_Name
    if "Combined semi-exposed roof - Energy code standard - Medium weight" in string:
        building_surfaces[i].Construction_Name = "laje_ref"
    if "Telha Metálica" in string:
        building_surfaces[i].Construction_Name = "Cob_ref"


IDF_VILA.save()
