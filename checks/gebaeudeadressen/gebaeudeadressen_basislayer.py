# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback

from veriso.modules.complexcheck_base import ComplexCheckBase


def _translate(context, text, disambig):
    return QApplication.translate(context, text, disambig)


class ComplexCheck(ComplexCheckBase):

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.iface = iface

        self.root = QgsProject.instance().layerTreeRoot()

    def run(self):
        self.settings = QSettings("CatAIS", "VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[0:2]

        if not project_id:
            self.iface.messageBar().pushMessage(
                "Error",
                _translate("VeriSO_EE_gebaeudeadressen_basislayer",
                           "project_id not set", None),
                level=Qgis.Critical, duration=5)
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_gebaeudeadressen_basislayer",
                               "Gebaeudeadressen - Basislayer", None)
            group += " (" + str(project_id) + ")"

            layer = {}
            layer["type"] = "wms"
            layer["group"] = group
            layer["title"] = _translate("VeriSO_EE_Geb_Basis", "PLZ Ortschaft",
                                        None)
            layer["url"] = "http://wms.geo.admin.ch/?"
            layer["layers"] = "ch.swisstopo-vd.ortschaftenverzeichnis_plz"
#            layer["layers"] ="PLZ und Ortschaften"

            layer["format"] = "image/jpeg"
            # layer["crs"] ="EPSG:21781"
            layer["sql"] = ""
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "Bodenbedeckung", None)
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            # Mit 'LIKE' anstelle von 'IN' oder '==' können kantonale Erweiterungen der Arten abgefangen werden.
            # Klassiker: Kt. Solothurn hat uebrig_befestigte circa 10-fach unterteilt. Mit 'LIKE' werden die trotzdem
            # geladen, auch wenn sie nicht alle einzeln aufgelistet werden.
            layer["sql"] = "art_txt LIKE 'Gebaeude%' OR art_txt LIKE 'befestigt.Strasse_Weg%' OR art_txt LIKE 'befestigt.Trottoir%' OR art_txt LIKE 'befestigt.uebrige_befestigte%'"
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "bodenbedeckung/gebaeude_strassen_trottoir_erschliessung.qml"

            # Die Sichtbarkeit des Layer und ob die Legende
            # und die Gruppe zusammengeklappt sein sollen:
            # self.layer_loader.load(layer, True, True, True)
            # Legende = vorletztes True (default is False)
            # Gruppe = letztes True (default is False)
            # Sichtbarkeit des Layers = erstes True (default is True)
            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "EO.Flaechenelemente", None)
            layer["featuretype"] = "v_einzelobjekte_flaechenelement"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = "art_txt LIKE 'unterirdisches_Gebaeude%' OR art_txt LIKE 'uebriger_Gebaeudeteil%' OR art_txt LIKE 'Reservoir%' OR art_txt LIKE 'Unterstand%'"
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "einzelobjekte/eo_flaeche_gebdetail_unterstand_reservoir_unterirdisch.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "EO.Linienelemente", None)
            layer["featuretype"] = "v_einzelobjekte_linienelement"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = "art_txt LIKE 'uebriger_Gebaeudeteil%'"
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "einzelobjekte/eo_linie_gebdetail.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "GEB.Nachführung", None)
            layer["featuretype"] = "gebaeudeadressen_gebnachfuehrung"
            # layer["geom"] = "perimeter" # Wird als geometryless Table geladen.
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "Benanntes Gebiet", None)
            layer["featuretype"] = "gebaeudeadressen_benanntesgebiet"
            layer["geom"] = "flaeche"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "gebaeudeadressen/benanntesgebiet_gruen.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "Strassenstueck (geometrie)", None)
            layer["featuretype"] = "gebaeudeadressen_strassenstueck"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "gebaeudeadressen/strassenachsen_gruen.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "Strassenstueck (anfangspunkt)", None)
            layer["featuretype"] = "gebaeudeadressen_strassenstueck"
            layer["geom"] = "anfangspunkt"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "gebaeudeadressen/anfangspunkt_gruen.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "Gebaeudeeingang", None)
            layer["featuretype"] = "gebaeudeadressen_gebaeudeeingang"
            layer["geom"] = "lage"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "gebaeudeadressen/gebaeudeeingang_blaues_viereck_mit_label.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis", "HausnummerPos",
                                        None)
            layer["featuretype"] = "v_gebaeudeadressen_hausnummerpos"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "gebaeudeadressen/hausnummerpos.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "LokalisationsName", None)
            layer["featuretype"] = "gebaeudeadressen_lokalisationsname"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "LokalisationsNamePos", None)
            layer["featuretype"] = "v_gebaeudeadressen_lokalisationsnamepos"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "gebaeudeadressen/lokalisationsnamepos.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Geb_Basis",
                                        "Gemeindegrenze", None)
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "gemeindegrenze/gemgre_strichliert.qml"

            gemgrelayer = self.layer_loader.load(layer)

            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()

        except Exception as e:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage(
                "Error", str(traceback.format_exc(exc_traceback)),
                level=Qgis.Critical, duration=5)
        QApplication.restoreOverrideCursor()
