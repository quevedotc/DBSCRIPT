# ATUALIZAÇÕES:
# >>>> COLOCOU A PARTE DO CÓDIGO ONDE INSERE A CONDIÇÃO DE CONTORNO DO SOLO
# >>>> CORRIGIU A FORMA COMO COLOCA AS ABERTURAS DE PORTAS E JANELAS PARA VENTILACAO

#>>>>>SEMPRE LEMBRAR DE TROCAR OS PONTOS ONDE TEM USOS MISTOS CASO O IDF TENHA USO MISTO OU NÃO<<<<<<<

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
idf_file = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/REAL_U6.idf' #Name for base file that will be cleared
NBR_VN = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/adicionar_no_idf_vn.idf' #Base file for natural ventilation
NBR_HVAC = 'D:/Tiago backup/Consultorias Andrea/Bodoquena/adicionar_no_idf_ac.idf' #base file for HVAC

# cria o IDF para ser trabalhado
IDF_VILA = IDF(idf_file)
nbr_vn = IDF(NBR_VN)
nbr_ac = IDF(NBR_HVAC)

#cria os objetos de lista de zona no idf
# Precisa tirar os comentarios do MISTO caso tenha ambiente com misto
IDF_VILA.newidfobject("ZONELIST")
IDF_VILA.newidfobject("ZONELIST")
IDF_VILA.newidfobject("ZONELIST")
lista_zona = IDF_VILA.idfobjects["ZONELIST"]
lista_zona[0].Name = "salas"
lista_zona[1].Name = "dorms"
lista_zona[2].Name = "mistos"
estar = lista_zona[0]
dormitorios = lista_zona[1]
misto = lista_zona[2]
#lista de zonas para sala de estar
Zona_Estar = []
# lista de zonas para dormitórios
Zona_Dormitorio = []

# lista das zonas com uso misto
zona_misto = []

#lista com todos os objetos que vão ser deletados
#Esses objetos são padrões que vem, alguns exportados estão vindo com outros objetos a mais, por enquanto deletamos os extras na mão
lista_deletar = [IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"], IDF_VILA.idfobjects["SHADOWCALCULATION"], IDF_VILA.idfobjects["SURFACECONVECTIONALGORITHM:INSIDE"],
IDF_VILA.idfobjects["SURFACECONVECTIONALGORITHM:OUTSIDE"], IDF_VILA.idfobjects["HEATBALANCEALGORITHM"], IDF_VILA.idfobjects["ZONECAPACITANCEMULTIPLIER:RESEARCHSPECIAL"],
IDF_VILA.idfobjects["CONVERGENCELIMITS"], IDF_VILA.idfobjects["SITE:LOCATION"], IDF_VILA.idfobjects["SIZINGPERIOD:DESIGNDAY"],
IDF_VILA.idfobjects["RUNPERIODCONTROL:SPECIALDAYS"], IDF_VILA.idfobjects["RUNPERIODCONTROL:DAYLIGHTSAVINGTIME"], 
IDF_VILA.idfobjects["SITE:GROUNDTEMPERATURE:BUILDINGSURFACE"], IDF_VILA.idfobjects["SITE:GROUNDTEMPERATURE:FCFACTORMETHOD"],
IDF_VILA.idfobjects["SITE:GROUNDTEMPERATURE:SHALLOW"], IDF_VILA.idfobjects["SITE:GROUNDTEMPERATURE:DEEP"],
IDF_VILA.idfobjects["SITE:PRECIPITATION"], IDF_VILA.idfobjects["ROOFIRRIGATION"],
IDF_VILA.idfobjects["SCHEDULE:DAY:HOURLY"], IDF_VILA.idfobjects["SCHEDULE:WEEK:DAILY"],
IDF_VILA.idfobjects["SCHEDULE:YEAR"], IDF_VILA.idfobjects["SCHEDULE:FILE"],
IDF_VILA.idfobjects["SURFACEPROPERTY:CONVECTIONCOEFFICIENTS"],
IDF_VILA.idfobjects["OUTPUTCONTROL:ILLUMINANCEMAP:STYLE"], IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:REFERENCECRACKCONDITIONS"],
IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE:CRACK"], IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:EXTERNALNODE"],
IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:WINDPRESSURECOEFFICIENTARRAY"], IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:WINDPRESSURECOEFFICIENTVALUES"],
IDF_VILA.idfobjects["SIZING:PARAMETERS"], IDF_VILA.idfobjects["OUTPUT:ENVIRONMENTALIMPACTFACTORS"], IDF_VILA.idfobjects["OUTPUT:VARIABLE"],
IDF_VILA.idfobjects["PEOPLE"], IDF_VILA.idfobjects["LIGHTS"], IDF_VILA.idfobjects["ELECTRICEQUIPMENT"], IDF_VILA.idfobjects["SITE:GROUNDDOMAIN:SLAB"], IDF_VILA.idfobjects["OUTPUT:SURFACES:LIST"],
IDF_VILA.idfobjects["OUTPUT:CONSTRUCTIONS"], IDF_VILA.idfobjects["OUTPUT:TABLE:SUMMARYREPORTS"], IDF_VILA.idfobjects["OUTPUT:TABLE:TIMEBINS"], IDF_VILA.idfobjects["OUTPUT:METER"], IDF_VILA.idfobjects["SIMULATIONCONTROL"],
IDF_VILA.idfobjects["BUILDING"],IDF_VILA.idfobjects["RUNPERIOD"], IDF_VILA.idfobjects["SITE:GROUNDTEMPERATURE:UNDISTURBED:FINITEDIFFERENCE"], IDF_VILA.idfobjects["AIRFLOWNETWORK:SIMULATIONCONTROL"],
IDF_VILA.idfobjects["SURFACEPROPERTY:OTHERSIDECONDITIONSMODEL"], IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"], IDF_VILA.idfobjects["SITE:GROUNDREFLECTANCE"], IDF_VILA.idfobjects["SITE:GROUNDREFLECTANCE:SNOWMODIFIER"],
IDF_VILA.idfobjects["OTHEREQUIPMENT"]]

#deleta os objetos que nao sao utilizados
for objeto in lista_deletar:
    objeto.clear()

#deleta schedules que nao sao uteis
schedule_idf = IDF_VILA.idfobjects["SCHEDULE:COMPACT"]

for schedule in schedule_idf:
    string = schedule.Name
    if "Clot" in string:
        schedule_idf.remove(schedule)
    if "Activity" in string:
        schedule_idf.remove(schedule)

#adiciona os novos objetos
lista_adicionarIDF = [nbr_vn.idfobjects["SIMULATIONCONTROL"], nbr_vn.idfobjects["BUILDING"], nbr_vn.idfobjects["RUNPERIOD"], nbr_vn.idfobjects["SITE:GROUNDTEMPERATURE:UNDISTURBED:FINITEDIFFERENCE"],
nbr_vn.idfobjects["SITE:GROUNDDOMAIN:SLAB"], nbr_vn.idfobjects["SCHEDULETYPELIMITS"], nbr_vn.idfobjects["SCHEDULE:COMPACT"], nbr_vn.idfobjects["MATERIAL:AIRGAP"],
nbr_vn.idfobjects["SURFACEPROPERTY:OTHERSIDECONDITIONSMODEL"], nbr_vn.idfobjects["PEOPLE"], nbr_vn.idfobjects["LIGHTS"], nbr_vn.idfobjects["ELECTRICEQUIPMENT"], nbr_vn.idfobjects["AIRFLOWNETWORK:SIMULATIONCONTROL"],
nbr_vn.idfobjects["OUTPUT:TABLE:SUMMARYREPORTS"], nbr_vn.idfobjects["OUTPUT:VARIABLE"]]

for objeto in lista_adicionarIDF:
    for i in range(len(objeto)):
        variavel = objeto[i]
        IDF_VILA.copyidfobject(variavel)

#Coloca as superfícies em contato com o solo com o ConditionModel
building_surfaces = IDF_VILA.idfobjects["BUILDINGSURFACE:DETAILED"]
for surface in building_surfaces:
    string = surface.Outside_Boundary_Condition
    if "Ground" in string:
        surface.Outside_Boundary_Condition = "OtherSideConditionsModel"
        surface.Outside_Boundary_Condition_Object = "Solo Dux - Slab Boundary Condition Model - 1 "


#adiciona as zonas de dormitorio e sala em suas respectivas listas
zonas = IDF_VILA.idfobjects["ZONE"]
nomes_zonas = ['Dorm', 'Quarto', 'Suite']
for zona in zonas:
    string = zona.Name
    if any(nome in string for nome in nomes_zonas):
        Zona_Dormitorio.append(zona)
    if "Estar" in string:
        Zona_Estar.append(zona)
    if "Misto" in string:
        zona_misto.append(zona)

# edita o objeto zone list para adicionar as zonas em suas respectivas listas
for i in range(len(Zona_Estar)):
    j = i + 2
    estar[estar.fieldnames[j]] = Zona_Estar[i].Name
for x in range(len(Zona_Dormitorio)):
    z = x + 2
    dormitorios[dormitorios.fieldnames[z]] = Zona_Dormitorio[x].Name
for a in range(len(zona_misto)):
    b = a + 2
    misto[misto.fieldnames[b]] = zona_misto[a].Name

# Deleta os elementos em AFN ZONE que não possuem ventilacao

afn_zones = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:ZONE"]

        
# copia os elementos comuns aos IDFs de VN e HVAC para dentro do IDF da NBR
#Seta as janelas e portas que devem ficar abertas/fechadas

afn_surface = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
aberturas= IDF_VILA.idfobjects["FENESTRATIONSURFACE:DETAILED"]
afn_janelas = IDF_VILA.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"]
afn_detailed = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"]

for i in range(len(afn_detailed)):
    variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][i]
    IDF_VILA.copyidfobject(variavel)

for i in range(len(aberturas)):
    string = aberturas[i].Name
    string1 = aberturas[i].Outside_Boundary_Condition_Object

    if "Estar" in string:
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][0].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][0].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][0].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][0]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][1].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
             

    if any(nome in string for nome in nomes_zonas):    
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][3].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][3].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][10].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][3]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            if "WC" in string1:
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][3].Name
                variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
                IDF_VILA.copyidfobject(variavel)
            else:
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][2].Surface_Name = string
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][2].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][3].Name
                variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][2]
                IDF_VILA.copyidfobject(variavel)

    if "Wc" in string:     
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][9].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][9].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][6].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][9]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][7].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if "Lavanderia" in string:     
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][8].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][9].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if "Circ" in string:     
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][8].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][8]
            IDF_VILA.copyidfobject(variavel)
        if "Door" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][9].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
            IDF_VILA.copyidfobject(variavel)
    if "Misto" in string:
        if "Win" in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][4].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][4].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][4].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][4]
            IDF_VILA.copyidfobject(variavel)
        
        if "Wall" in string and "Door" in string:
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Surface_Name = string
                nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][5].Name
                variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][1]
                IDF_VILA.copyidfobject(variavel)

        if "Door" in string and 'Partition' in string:
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][7].Surface_Name = string
            nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][7].Leakage_Component_Name = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING"][5].Name
            variavel = nbr_vn.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"][7]
            IDF_VILA.copyidfobject(variavel)



# Deleta as partes do AFN Surface que não precisam - VEntilation control mode, conttrol mode temp - schedule
for zona in afn_zones:
    zona.Ventilation_Control_Mode = ' '
    zona.Ventilation_Control_Zone_Temperature_Setpoint_Schedule_Name = ' '
    zona.Venting_Availability_Schedule_Name = ' '

#Coloca os controles de veneziana conforme define a norma
'''IDF_VILA.idfobjects["WINDOWMATERIAL:BLIND"][0].Name = "veneziana_yrupa"
venezianas = IDF_VILA.idfobjects["WINDOWSHADINGCONTROL"]

venezianas.clear()

for abertura in aberturas:
    string = abertura.Name
    if "Dorm" in string:
        if "Win" in string:
            nbr_vn.idfobjects["WINDOWSHADINGCONTROL"][0].Name = string
            nbr_vn.idfobjects["WINDOWSHADINGCONTROL"][0].Zone_Name = string[:-21]
            nbr_vn.idfobjects["WINDOWSHADINGCONTROL"][0].Fenestration_Surface_1_Name = string
            nbr_vn.idfobjects["WINDOWSHADINGCONTROL"][0].Shading_Device_Material_Name = "veneziana"
            adicionar = nbr_vn.idfobjects["WINDOWSHADINGCONTROL"][0]
            IDF_VILA.copyidfobject(adicionar)'''

#coloca nas janelas o frame da referencia

adicionar = nbr_vn.idfobjects["WINDOWPROPERTY:FRAMEANDDIVIDER"][0]
IDF_VILA.copyidfobject(adicionar)
for i in range(len(aberturas)):
    string = aberturas[i].Name
    if "Win" in string:
        aberturas[i].Frame_and_Divider_Name = "framedivider"

name = (idf_file[:-4] + '_VN'+'_NBR' + '.idf')
IDF_VILA.saveas(name)