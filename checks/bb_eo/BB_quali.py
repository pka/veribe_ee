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
        self.settings = QSettings("CatAIS",
                                  "VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[0:2]  # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage(
                "Error",
                _translate("VeriSO_EE_quali", "project_id not set",
                           None), level=Qgis.Critical, duration=5)
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_quali", "Qualität BB/EO", None)
            group += " (" + str(project_id) + ")"
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_quali",
                                        "EO Flaechenelemete", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_flaechenelement_v"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/q_eo_fl.qml"
            vlayer = self.layer_loader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_quali",
                                        "EO Linienelemente", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_linienelement_v"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/q_eo_li.qml"
            vlayer = self.layer_loader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_quali",
                                        "EO Punktelemente", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_punktelement_v"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/q_eo_pkt.qml"
            vlayer = self.layer_loader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_quali",
                                        "Bodenbedeckung", None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/q_bb.qml"
            vlayer = self.layer_loader.load(layer, False, True)
        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage(
                "Error", str(traceback.format_exc(exc_traceback)),
                level=Qgis.Critical, duration=5)
        QApplication.restoreOverrideCursor()
