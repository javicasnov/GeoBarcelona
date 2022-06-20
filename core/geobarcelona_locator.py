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

from qgis.PyQt.QtCore import QByteArray, QTimer

from qgis.gui import QgisInterface
from qgis.core import QgsLocatorFilter, QgsLocatorResult, QgsLocatorContext, QgsFeedback, QgsWkbTypes

from geobarcelona.utils import var
from geobarcelona.utils import tr_strings
from geobarcelona.utils import utils

class GeoBarcelonaLocatorFilter(QgsLocatorFilter):

    def __init__(self, iface: QgisInterface = None):

        super().__init__()

        self.point_rubberband = None
        self.iface = None
        self.canvas = None
        self.current_timer = None
        tr_strings.tr_strings_GeoBarcelonaLocatorFilter(self)
        tr_strings.tr_strings_GeoBarcelonaCommon(self)

        if iface is not None:

            self.iface = iface
            self.canvas = iface.mapCanvas()
            utils.config_rubberband(self)

    def name(self):
        return type(self).__name__

    def clone(self):
        return GeoBarcelonaLocatorFilter(self.iface)

    def displayName(self):
        return 'GeoBarcelona'

    def prefix(self):
        return 'bcn'

    def priority(self):
        return QgsLocatorFilter.Highest

    #def flags(self):
        #return QgsLocatorFilter.FlagFast

    def clearPreviousResults(self):

        if self.point_rubberband:
            self.point_rubberband.reset(QgsWkbTypes.PointGeometry)

        if self.current_timer is not None:
            self.current_timer.timeout.disconnect(self.clearPreviousResults)
            self.current_timer.stop()
            self.current_timer.deleteLater()
            self.current_timer = None

    def fetchResults(self, search, context: QgsLocatorContext, feedback: QgsFeedback):

        search_text = utils.prepare_string(search)

        if len(search_text) < 2:
            utils.clear_locator(self, self.lbl_noresult_locator_text)
            return

        url = utils.url_locator(search_text)

        response = utils.networkRequest(url, feedback, type(self).__name__)
        error_code = response.error()

        if error_code == 0:

            self.handle_response(response.content(), feedback)

        else:

            if error_code == 5:

                error_msg = self.timeout_error_text

            else:

                error_msg = response.errorString()

            utils.info(self, error_msg)
            utils.clear_locator(self, error_msg)

    def handle_response(self, content: QByteArray, feedback: QgsFeedback):

        locations = utils.hr_load_json(self, content, var.type_json_main)

        if locations is None:
            return None

        lid = locations[var.geobcnlabel_resultats][var.geobcnlabel_adreces]

        if len(lid) != 0:

            for count in range(len(lid)):

                locator_items, point = utils.prepare_tblResult(self, count, lid)
                result = QgsLocatorResult()
                result.filter = self
                result.displayString = '{}, {}, {}, {}'.format(*locator_items)
                result.userData = point
                result.score = 1 - ((count+1)/len(lid))
                self.resultFetched.emit(result)

        else:

            utils.clear_locator(self, self.lbl_noresult_locator_text)

    def triggerResult(self, result: QgsLocatorResult):

        self.clearPreviousResults()

        if hasattr(result, 'getUserData'):

            doc = result.getUserData()

        else:

            doc = result.userData

        if type(doc).__name__ == 'QgsGeometry':

            self.point_rubberband.addGeometry(doc, var.results_crs)
            utils.zoom_result(self, self.point_rubberband)

            self.current_timer = QTimer()
            self.current_timer.timeout.connect(self.clearPreviousResults)
            self.current_timer.setSingleShot(True)
            self.current_timer.start(var.locator_timer*1000)