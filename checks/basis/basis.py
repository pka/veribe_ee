 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback


try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.iface = iface
        
        self.root = QgsProject.instance().layerTreeRoot()        

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_basis", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group1 = _translate("VeriSO_EE_basis", "EO Allgemein", None)
            group1 += " (" + str(project_id) + ")" 

            group2 = _translate("VeriSO_EE_basis", "AV Allgemein", None)
            group2 += " (" + str(project_id) + ")" 

            group3 = _translate("VeriSO_EE_basis", "BB Allgemein", None)
            group3 += " (" + str(project_id) + ")" 


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","EO Flaechenelemete",None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_flaechenelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group1
            layer["sql"] = ""
            layer["style"] = "basis/eo_flaeche.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","EO Linienelemente",None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_linienelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group1
            layer["sql"] = ""
            layer["style"] = "basis/eo_linie.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","EO Punktelemente",None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_punktelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group1
            layer["sql"] = ""
            layer["style"] = "basis/eo_pkt.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Objektname",None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_objektnamepos_v"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group1
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/objektnamen.qml"
            vlayer = self.layer_loader.load(layer, False, True)



            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_basis","SDR",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_selbstrecht"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/selbstrecht.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
 

 
            layer["title"] = _translate("VeriSO_EE_basis","Liegenschaften",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft_v2"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/liegenschaft.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_basis","Hilfslinie",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grundstueckpos"
            layer["geom"] = "hilfslinie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/hilfslinie.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Hoheitsgrenzpunkt - unversichert",None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (6)"
            layer["style"] = "bodenbedeckung/hgp_unver.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Hoheitsgrenzpunkt - Kreuz",None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (5)"
            layer["style"] = "bodenbedeckung/hgp_kreuz.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Hoheitsgrenzpunkt - Bolzen,Rohr,Pfahl",None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (2,3,4)"
            layer["style"] = "bodenbedeckung/hgp_bolzen.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Hoheitsgrenzpunkt - Stein,Kunststoffzeichen",None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (0,1)"
            layer["style"] = "bodenbedeckung/hgp_stein.qml"
            vlayer = self.layer_loader.load(layer, False, True)
 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Grenzpunkt - unversichert",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (6)"
            layer["style"] = "bodenbedeckung/gp_unver.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Grenzpunkt - Kreuz",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (5)"
            layer["style"] = "bodenbedeckung/gp_kreuz.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Grenzpunkt - Bolzen,Rohr,Pfahl",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (2,3,4)"
            layer["style"] = "bodenbedeckung/gp_bolzen.qml"
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Grenzpunkt - Stein,Kunststoffzeichen",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen in (0,1)"
            layer["style"] = "bodenbedeckung/gp_stein.qml"
            vlayer = self.layer_loader.load(layer, False, True)


            layer["title"] = _translate("VeriSO_EE_basis","proj. Liegenschaften",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projliegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projliegenschaft.qml"
            vlayer = self.layer_loader.load(layer)
 

            layer["title"] = _translate("VeriSO_EE_basis","proj. SDR",None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projselbstrecht"
            layer["geom"] = "geometrie"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projselbstrecht.qml"
            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_basis","proj_Grst-Nr",None)
            layer["readonly"] = True
            layer["featuretype"] = "z_projgs_nr"
            layer["geom"] = "pos"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/proj_GS_NR.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_basis","Nr Gs(LS)",None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group2
            layer["sql"] = "(art=0) and (gesamteflaechenmass is NULL)"
            layer["style"] = "liegenschaften/nr_ls_ganz.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_basis","Nr Gs(SDR)",None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art>0) and (gesamteflaechenmass is NULL)"
            layer["style"] = "liegenschaften/nr_sdr_ganz.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_basis","Nr Gs(LS-Teil)",None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art=0) and (gesamteflaechenmass>0)"
            layer["style"] = "liegenschaften/nr_ls_teil.qml"
            vlayer = self.layer_loader.load(layer)
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","Nr Gs(SDR Teil)",None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group2
            layer["key"] = "ogc_fid"
            layer["sql"] = "art>0 and gesamteflaechenmass>0"
            layer["style"] = "liegenschaften/nr_sdr_teil.qml"
            vlayer = self.layer_loader.load(layer)






            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","proj. Gebaeude",None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_projboflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = "art = 0"
            layer["group"] = group3
            layer["style"] = "basis/projGeb.qml"
            vlayerprojGeb = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_basis","HausnummerPos",None)
            layer["featuretype"] = "v_gebaeudeadressen_hausnummerpos"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group3
            layer["style"] = "gebaeudeadressen/hausnummerpos.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres" 
            layer["title"] = _translate("VeriSO_EE_basis","Bodenbedeckung",None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group3
            layer["sql"] = ""
            layer["style"] = "basis/BB.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres" 
            layer["title"] = _translate("VeriSO_EE_basis","Objektname",None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_objektnamepos_v"
            layer["geom"] = "pos"
            layer["group"] = group3
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/objektnamen.qml"
            vlayer = self.layer_loader.load(layer, False, True)










             
        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()  

