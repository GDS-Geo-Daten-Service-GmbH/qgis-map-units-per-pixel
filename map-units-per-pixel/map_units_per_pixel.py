# -*- coding: utf-8 -*-
"""
MapUnitsPerPixel

 Displays the current pixel size of the map in the status bar.
                              -------------------
        begin                : 2022-12-26
        copyright            : (C) 2022 by Andreas Steffens
        email                : a.steffens@gds-team.de
 /***************************************************************************
"""
import os
from enum import Enum
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QLabel,
    QFrame,
    QWidget
)

from qgis.gui import *
from qgis.core import *

class MapUnitsPerPixel:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        self.lblPixelSize = QLabel()
        self.lblPixelSize.setFrameStyle( QFrame.StyledPanel )
        self.lblPixelSize.setAlignment( Qt.AlignCenter )
        self.lblPixelSize.setMinimumWidth( 100 )
        self.iface.mainWindow().statusBar().addPermanentWidget( self.lblPixelSize )

        # Display zoom level whenever the map scale changes
        self.iface.mapCanvas().scaleChanged.connect(self.updateResolution)


    def initGui(self):
        """This plugin makes no menu or toolbar changes."""
        pass


    def unload(self):
        """This plugin makes no menu or toolbar changes."""
        pass


    def updateResolution(self):
        """Display the current pixel size in the status bar"""

        self.lblPixelSize.setText('{:.2f}'.format(self.iface.mapCanvas().mapUnitsPerPixel()) + ' ' + QgsUnitTypes.encodeUnit( self.iface.mapCanvas().mapUnits() ) + '/px')
