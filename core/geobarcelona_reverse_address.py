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

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import QgsPointXY, QgsGeometry, QgsProject, QgsTaskManager

from geobarcelona.utils import var
from geobarcelona.utils import tr_strings
from geobarcelona.utils import utils
from geobarcelona.utils.task import GeoBarcelonaDownloadTask
from geobarcelona.utils.coordinate_capture import GeoBarcelonaCoordinateCapture

FORM, BASE = uic.loadUiType(os.path.join(var.plugin_dir, 'ui\\geobarcelona_reverse_address_tab.ui'))

class GeoBarcelonaReverseAddressSearch(BASE, FORM):

    def __init__(self, iface, parent=None):

        super(GeoBarcelonaReverseAddressSearch, self).__init__(parent)
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
        self.annot_manager = QgsProject.instance().annotationManager()
        self.coordinate_capture = None
        self.labels = []
        self.task = []
        self.taskManager = QgsTaskManager()

        utils.config_rubberband(self)
        utils.config_tblResult_horizontal_headers(self)
        utils.config_tblclickedpoint_vertical_headers(self)
        utils.config_ui(self)

    def closeEvent_reverse_address(self):

        for count in range(len(self.task)):

            if self.task[count]:
                self.task[count].cancel()

        utils.clear_all_results(self)

    def startCapturing(self):

        if len(QgsProject.instance().mapLayers()) == 0 and not QgsProject.instance().title():

             self.iface.newProject()

        if self.coordinate_capture is None:

            self.coordinate_capture = GeoBarcelonaCoordinateCapture(self.canvas)
            self.canvas.setMapTool(self.coordinate_capture)
            self.coordinate_capture.canvasClicked.connect(self.on_Search)
            self.coordinate_capture.canvasRightClicked.connect(self.stopCapturing)
            self.ui.start_capture.setText(var.start_capture_text_space + self.capt_button_text_2)

    def stopCapturing(self, type):

        self.coordinate_capture = None

        if type == 0:

            self.ui.start_capture.setText(var.start_capture_text_space + self.capt_button_text)
            utils.identify_selected_table(self)

    def on_Search(self, point: QgsPointXY):

        utils.delete_rubbers(self)
        utils.delete_labels(self)

        self.ui.start_capture.setText(var.start_capture_text_space + self.capt_button_text_3)
        self.coordinate_x = str(round(point.x(), var.round_x))
        self.coordinate_y = str(round(point.y(), var.round_y))
        self.clicked_point_geom = QgsGeometry.fromPointXY(point)

        url = utils.url_reverse(self.coordinate_x, self.coordinate_y)

        if self.task == []:

            self.taskManager.allTasksFinished.connect(self.on_Search_response)

            for count in range(len(url)):

                self.task.append(GeoBarcelonaDownloadTask(url[count], type(self).__name__))
                self.taskManager.addTask(self.task[-1])

    def on_Search_response(self):

        self.taskManager.allTasksFinished.disconnect(self.on_Search_response)

        contents = []
        stop_flag = False
        error_num_task = None

        for count in range(len(self.task)):

            error_code = self.task[count].response.error()

            if error_code == 0:

                contents.append(self.task[count].response.content())

            else:

                stop_flag = True
                error_num_task = count

            if stop_flag:
                break

        if not stop_flag:

            self.handle_response(contents)
            self.clicked_point_rubberband.addGeometry(self.clicked_point_geom, var.results_crs)

        else:

            if error_code == 5:

                error_msg = self.timeout_error_text

            else:

                error_msg = self.task[error_num_task].response.errorString()

            utils.message_bar(self, error_msg)
            utils.info(self, error_msg)
            contents = []
            self.ui.start_capture.setText(var.start_capture_text_space + self.capt_button_text)
            utils.clear_error(self)

    def handle_response(self, contents):

        utils.hr_init(self)
        locations = utils.hr_load_json(self, contents, var.type_json_main)

        if locations is None:
            return None

        for count in range(len(locations)):
            self.lid.append(locations[count][var.geobcnlabel_resultats])

        utils.fill_tblclickedpoint(self)

        response_adreces = self.lid[var.pos_lid_adreces]
        self.len_response_adreces = len(response_adreces)

        if self.len_response_adreces != 0:

            utils.fill_tblResult(self, response_adreces, var.pos_address_tblResult_reverse, var.pos_refcad_tblResult_reverse)
            utils.rubbers_labels_reverse(self)

            self.ui.save_all_results.setEnabled(True)

            len_addresses = len(self.stored_addresses)

            if len_addresses == 1:

                self.ui.lblResult.setText((self.lbl_1result_reverse_text) % var.search_radius)

            elif len_addresses == var.max_results_reverse:

                self.ui.lblResult.setText((self.lbl_maxresult_reverse_text) % (var.max_results_reverse, var.search_radius))

            else:

                self.ui.lblResult.setText((self.lbl_elseresult_reverse_text) % (len_addresses, var.search_radius))

        else:

            self.ui.lblResult.setText((self.lbl_noresult_reverse_text) % var.search_radius)
            utils.clear_address_results(self)
            self.ui.save_all_results.setEnabled(False)

        self.ui.clear_capture_results.setEnabled(True)
        self.ui.start_capture.setText(var.start_capture_text_space + self.capt_button_text)
        self.task = []

    def onAction_tblResult_click(self, i, j):

        self.onAction_tblResult(i, j)

    def onAction_tblclickedpoint_click(self, i, j):

        self.onAction_tblclickedpoint(i, j)

    def onAction_tblResult(self, i, j):

        self.selected_point_geom = self.stored_geometry_addresses[i]
        self.ui.tblclickedpoint.clearSelection()
        utils.delete_rubber_selected_point(self)
        self.selected_point_rubberband.addGeometry(self.selected_point_geom, var.results_crs)

        if j == 3 or j == 4:

            utils.draw_rubber_polygon(self, var.request_type_districte, var.type_tblResult, i, j)

        elif j == 5 or j == 6:

            utils.draw_rubber_polygon(self, var.request_type_barri, var.type_tblResult, i, j)

        elif j == 8:

            codi_secc = self.stored_addresses[i][8]
            codi_dist = self.stored_addresses[i][3]
            utils.complementary_request(self, var.request_type_seccio_censal, codi_secc, codi_dist, i, j)

        elif j == 9:

            utils.draw_rubber_polygon(self, var.request_type_illa, var.type_tblResult, i, j)

        elif j == 10 or j == 11 or j == 12:

            codi_illa = self.stored_addresses[i][9]
            codi_parc = self.stored_addresses[i][10]
            utils.complementary_request(self, var.request_type_parcela, codi_illa, codi_parc, i, j)

        else:

            utils.delete_rubber_polygons(self)
            utils.zoom_result(self, self.selected_point_rubberband)

    def onAction_tblclickedpoint(self, i, j):

        self.ui.tblResult.clearSelection()
        utils.delete_rubber_selected_point(self)

        if i == 0 or i == 1:

            utils.draw_rubber_polygon(self, var.request_type_districte, var.type_tblclickedpoint, i, j)

        elif i == 2 or i == 3:

            utils.draw_rubber_polygon(self, var.request_type_barri, var.type_tblclickedpoint, i, j)

        elif i == 4 or i == 5:

            utils.draw_rubber_polygon(self, var.request_type_illa, var.type_tblclickedpoint, i, j)

        elif i == 6 or i == 7 or i == 8:

            utils.draw_rubber_polygon(self, var.request_type_parcela, var.type_tblclickedpoint, i, j)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = GeoBarcelonaReverseAddressSearch()
    app.addDockWidget(dialog)
    dialog.show()
    sys.exit(app.exec_())