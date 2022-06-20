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

import os.path

from functools import partial

from qgis.PyQt import uic
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QApplication, QLineEdit

from qgis.core import QgsTaskManager

from geobarcelona.utils import var
from geobarcelona.utils import tr_strings
from geobarcelona.utils import utils
from geobarcelona.utils.task import GeoBarcelonaDownloadTask

FORM, BASE = uic.loadUiType(os.path.join(var.plugin_dir, 'ui\\geobarcelona_address_tab.ui'))

class GeoBarcelonaAddressSearch(BASE, FORM):

    def __init__(self, iface, parent=None):

        super(GeoBarcelonaAddressSearch, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.setupPlug()
        utils.setupEvents(self)

    def setupPlug(self):

        self.ui = self
        tr_strings.tr_strings_GeoBarcelonaDock(self)
        tr_strings.tr_strings_GeoBarcelonaCommon(self)

        self.stored_individual_address = None
        self.stored_individual_geometry = None
        self.dock_timer = None
        self.loading_icon_action = None
        self.task = None
        self.taskManager = QgsTaskManager()

        utils.config_rubberband(self)
        utils.config_tblResult_horizontal_headers(self)
        utils.config_ui(self)

    def closeEvent_address(self):

        if self.task:
            self.task.cancel()

        self.ui.txtSearch.clear()
        utils.clear_all_results(self)

    def on_focusChanged(self, old, now):

        if self.ui.txtSearch == now:

            self.ui.tblResult.clearSelection()
            utils.delete_rubbers(self)

    def updateSpinnerAniamation(self):

        if self.loading_icon_action is not None:
            self.ui.txtSearch.removeAction(self.loading_icon_action)

        self.loading_icon_action = self.ui.txtSearch.addAction(QIcon(var.loading_icon.currentPixmap()), QLineEdit.TrailingPosition)

    def start_timer(self):

        self.dock_timer = QTimer()
        self.dock_timer.timeout.connect(self.on_Search)
        self.dock_timer.setSingleShot(True)
        self.dock_timer.start(var.timer_delay)

    def cancel_timer(self):

        if self.dock_timer is not None:
            self.dock_timer.timeout.disconnect(self.on_Search)
            self.dock_timer.stop()
            self.dock_timer.deleteLater()
            self.dock_timer = None

    def start_typing_timer(self):

        if self.ui.txtSearch.text().strip():

            self.ui.lblResult.setText(self.searching_address_text)

            if self.loading_icon_action is None:
                self.ui.txtSearch.setClearButtonEnabled(False)
                var.loading_icon.start()

        self.cancel_timer()
        self.start_timer()

    def on_Search(self):

        self.ui.txtSearch.blockSignals(True)

        self.changedtext = self.ui.txtSearch.text()
        self.search = utils.prepare_string(self.changedtext)

        if self.search == '':

            utils.clear_error(self)

        else:

            url = utils.url_address(self.search)

            if self.task is None:

                self.task = GeoBarcelonaDownloadTask(url, type(self).__name__)
                self.task.taskCompleted.connect(self.on_Search_response)
                self.task.taskTerminated.connect(partial(utils.clear_error, self))
                self.taskManager.addTask(self.task)

    def on_Search_response(self):

        self.task.taskCompleted.disconnect(self.on_Search_response)

        error_code = self.task.response.error()

        if error_code == 0:

            self.handle_response(self.task.response.content(), self.search, self.changedtext)

        else:

            if error_code == 5:

                error_msg = self.timeout_error_text

            else:

                error_msg = self.task.response.errorString()

            utils.message_bar(self, error_msg)
            utils.info(self, error_msg)
            utils.clear_error(self)

    def handle_response(self, content, search, changedtext):

        utils.hr_init(self)
        locations = utils.hr_load_json(self, content, var.type_json_main)

        if locations is None:
            return None

        self.lid = locations[var.geobcnlabel_resultats][var.geobcnlabel_adreces]
        response_adreces = self.lid
        self.len_response_adreces = len(response_adreces)

        if self.len_response_adreces != 0:

            utils.fill_tblResult(self, response_adreces, var.pos_address_tblResult, var.pos_refcad_tblResult)
            len_addresses = len(self.stored_addresses)

            if len_addresses == 1:

                self.ui.lblResult.setText(self.lbl_1result_address_text)

            elif len_addresses == var.max_results_address:

                self.ui.lblResult.setText((self.lbl_maxresult_address_text) % var.max_results_address)

            else:

                self.ui.lblResult.setText((self.lbl_elseresult_address_text) % len_addresses)

            var.loading_icon.stop()
            self.ui.txtSearch.removeAction(self.loading_icon_action)
            self.ui.txtSearch.setClearButtonEnabled(True)
            self.loading_icon_action = None

        else:

            self.ui.lblResult.setText(self.lbl_noresult_address_text)
            utils.clear_address_results(self)
            utils.delete_rubbers(self)

        text1 = self.ui.txtSearch.text()
        self.ui.txtSearch.blockSignals(False)

        self.task = None

        if text1 != changedtext:
            self.start_typing_timer()

    def onAction_tblResult_click(self, i, j):

        self.onAction_tblResult(i, j)

    def onAction_tblResult(self, i, j):

        utils.delete_rubber_points(self)

        self.selected_point_geom = self.stored_geometry_addresses[i]
        self.point_rubberband.addGeometry(self.selected_point_geom, var.results_crs)

        if j == 2 or j == 3:

            utils.draw_rubber_polygon(self, var.request_type_districte, var.type_tblResult, i, j)

        elif j == 4 or j == 5:

            utils.draw_rubber_polygon(self, var.request_type_barri, var.type_tblResult, i, j)

        elif j == 7:

            codi_secc = self.stored_addresses[i][7]
            codi_dist = self.stored_addresses[i][2]
            utils.complementary_request(self, var.request_type_seccio_censal, codi_secc, codi_dist, i, j)

        elif j == 8:

            utils.draw_rubber_polygon(self, var.request_type_illa, var.type_tblResult, i, j)

        elif j == 9 or j == 10 or j == 11:

            codi_illa = self.stored_addresses[i][8]
            codi_parc = self.stored_addresses[i][9]
            utils.complementary_request(self, var.request_type_parcela, codi_illa, codi_parc, i, j)

        else:

            utils.delete_rubber_polygons(self)
            utils.zoom_result(self, self.point_rubberband)

        address_name = self.stored_addresses[i][0]
        self.ui.txtSearch.setText(address_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = GeoBarcelonaAddressSearch()
    app.addDockWidget(dialog)
    dialog.show()
    sys.exit(app.exec_())