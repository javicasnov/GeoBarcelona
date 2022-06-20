# -*- coding: utf-8 -*-
"""
/***************************************************************************
                               GeoBarcelona

 A QGIS plugin to search and zoom addresses in Barcelona city

        copyright            : (C) 2022 by Javier Casado
        email                : javicasnov@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.PyQt.QtWidgets import QApplication

from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsPointXY, QgsApplication, QgsGeometry, QgsCoordinateTransform, QgsProject

from geobarcelona.utils import var

class GeoBarcelonaCoordinateCapture(QgsMapToolEmitPoint):

    canvasClicked = pyqtSignal(QgsPointXY)
    canvasRightClicked = pyqtSignal(int)

    def __init__(self, canvas):

        super(GeoBarcelonaCoordinateCapture, self).__init__(canvas)
        self.mapCanvas = canvas
        self.type = 0

    def activate(self):

        self.cursor = QgsApplication.getThemeCursor(QgsApplication.Cursor.CrossHair)
        QApplication.setOverrideCursor(self.cursor)

    def canvasPressEvent(self, e):

        if e.button() == Qt.LeftButton:

            original_pt = QgsPointXY(self.mapCanvas.getCoordinateTransform().toMapCoordinates(e.x(), e.y()))
            geom_pt = QgsGeometry.fromPointXY(original_pt)

            source_crs = QgsProject.instance().crs()
            tr = QgsCoordinateTransform(source_crs, var.results_crs, QgsProject.instance())
            geom_pt.transform(tr)
            reprojected_pt = geom_pt.asPoint()

            self.canvasClicked.emit(reprojected_pt)
            self.type = 1
            self.deactivate()

        elif e.button() == Qt.RightButton:

            self.type = 0
            self.deactivate()

    def deactivate(self):

        QApplication.restoreOverrideCursor()
        self.canvasRightClicked.emit(self.type)
        super(GeoBarcelonaCoordinateCapture, self).deactivate()