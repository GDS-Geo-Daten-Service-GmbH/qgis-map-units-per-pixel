# -*- coding: utf-8 -*-
"""
MapUnitsPerPixel

 Displays the current pixel size of the map in the status bar.
                              -------------------
        begin                : 2022-12-26
        copyright            : (C) 2022 by Andreas Steffens (GDS Geo Daten Service GmbH)
        email                : a.steffens@gds-team.de
 /***************************************************************************
"""

__author__ = 'Andreas Steffens'
__date__ = '26/12/2022'
__copyright__ = 'Copyright 2022, Andreas Steffens (GDS Geo Daten Service GmbH)'

import os
import locale
import re
from enum import Enum
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *
from qgis.PyQt import uic
from qgis.gui import *
from qgis.core import *

from .resources import *

class MapUnitsPerPixel(QWidget):

    def __init__(self, iface):
        super().__init__()
    
        # Save reference to the QGIS interface
        self.iface = iface


    def initGui(self):
        strUiPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "PixelSize.ui")

        uic.loadUi(strUiPath, self)

        self.iface.mainWindow().statusBar().addPermanentWidget(self)

        self.lePixelSize.returnPressed.connect(self.onPixelSizeEditChanged)
        self.iface.mapCanvas().scaleChanged.connect(self.onMapCanvasScaleChanged)


    def unload(self):
        self.iface.mainWindow().statusBar().removeWidget(self)


    def onPixelSizeEditChanged(self):
        listMatches = []
        strSeparator = locale.localeconv()["decimal_point"]
        
        if strSeparator == ".":
            listMatches = re.findall("\\d+\\" + strSeparator + "\\d+", self.lePixelSize.text())
        else:
            listMatches = re.findall("\\d+" + strSeparator + "\\d+", self.lePixelSize.text())
        
        if not listMatches:
            listMatches = re.findall("\\d+", self.lePixelSize.text())
        
        if listMatches:
            dScaleFactor = float(listMatches[0]) / self.iface.mapCanvas().mapUnitsPerPixel()
            dNewScale = self.iface.mapCanvas().scale() * dScaleFactor
            self.iface.mapCanvas().zoomScale(dNewScale)


    def onMapCanvasScaleChanged(self):
        """Display the current pixel size in the status bar"""

        self.lePixelSize.setText('{:.3f}'.format(self.iface.mapCanvas().mapUnitsPerPixel()) + ' ' + QgsUnitTypes.encodeUnit( self.iface.mapCanvas().mapUnits() ) + '/px')
