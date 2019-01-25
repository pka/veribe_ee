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

        locale = QSettings().value('locale/userLocale')[0:2]  # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage(
                "Error",
                _translate("VeriSO_EE_FP3", "project_id not set", None),
                level=Qgis.Critical, duration=5)
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_FP3", "FixpunkteKategorie3", None)
            group += " (" + str(project_id) + ")"

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "Toleranzstufen",
                                        None)  # Mit Linguist übersetzen. Deutsche Übersetzugn nicht unbedingt nötig, da dieser Text hier verwendet wird, falls die Übersetzung für eine bestimmte Sprache fehlt.
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "tseinteilung/toleranzstufe_de.qml"

            # Die Sichtbarkeit des Layer und ob die Legende
            # und die Gruppe zusammengeklappt sein sollen:
            # self.layer_loader.load(layer, True, True, True)
            # Legende = vorletztes True (default is False)
            # Gruppe = letztes True (default is False)
            # Sichtbarkeit des Layers = erstes True (default is True)
            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
#            layer["title"] = self.tr("LFP3 Nachführung") # Mit Linguist übersetzen. -> Achtung: Testen ob Übersetzungen mit Umlauten funktionieren...
            layer["title"] = _translate("VeriSO_EE_FP3", "LFP3 Nachführung",
                                        None)
            layer["featuretype"] = "fixpunktekatgrie3_lfp3nachfuehrung"
            layer["geom"] = "perimeter"  # Falls layer["geom"] bei Tabellen/Layern mit einer Geomtriespalte weggelassen wird, wird die Tabelle als "geometryless" geladen.
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group

            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "LFP3", None)
            layer["featuretype"] = "fixpunktekatgrie3_lfp3"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "fixpunkte/lfp3.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3_PZ", "Punktzeichen",
                                        None)
            layer["featuretype"] = "fixpunktekatgrie3_lfp3"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "fixpunkte/punktversicherung.qml"

            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3",
                                        "LFP3 ausserhalb Gemeinde", None)
            layer["featuretype"] = "v_lfp3_ausserhalb_gemeinde"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "fixpunkte/lfp3ausserhalb.qml"

            vlayer = self.layer_loader.load(layer)

            # So funktionieren WMS:
            layer = {}
            layer["type"] = "wms"
            layer["title"] = _translate("VeriSO_EE_FP3",
                                        "LFP1 + LFP2 Schweiz", None)
            layer["url"] = "http://wms.geo.admin.ch/"
            layer["layers"] = "ch.swisstopo.fixpunkte-lfp1,ch.swisstopo.fixpunkte-lfp2"
            layer["format"] = "image/png"
            layer["crs"] = "EPSG:" + str(epsg)
            layer["group"] = group

            vlayer = self.layer_loader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate(
                "VeriSO_EE_FP3", "LFP3 pro Toleranzstufe", None)
            layer["featuretype"] = "fixpunktekatgrie3_lfp3_pro_toleranzstufe_v"
            # layer["geom"] = ""
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            vlayer = self.layer_loader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "Gemeindegrenze",
                                        None)
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "gemeindegrenze/gemgre_strichliert.qml"
            gemgrelayer = self.layer_loader.load(layer)

            # Kartenausschnit verändern.
            # Bug (?) in QGIS: http://hub.qgis.org/issues/10980
            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()
            # Bei gewissen Fragestellungen sicher sinnvoller
            # auf den ganzen Kartenausschnitt zu zoomen:
            # self.iface.mapCanvas().zoomToFullExtent()

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage(
                "Error", str(traceback.format_exc(exc_traceback)),
                level=Qgis.Critical, duration=5)
        QApplication.restoreOverrideCursor()

        # Geometryless Bug scheint behoben.
        # Falscher EPSG-Code und falsche
        # Scale-Unit waren eingestellt, falls
        # der erste geladene Layer OHNE
        # Geometrie war.
        # Habe es mit LFP3Nachfuehrung
        # OHNE "geom" getestet.
        # Workaround war notwendig.
