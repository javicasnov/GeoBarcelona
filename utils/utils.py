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

import webbrowser
import json

from functools import partial

from qgis.PyQt.QtGui import QColor, QTextDocument
from qgis.PyQt.QtCore import QUrl, QSize, Qt, QSizeF
from qgis.PyQt.QtWidgets import QPushButton, QTableWidgetItem, QHeaderView, QShortcut, QHBoxLayout, QLabel, QWidget, QLineEdit, QApplication
from qgis.PyQt.QtNetwork import QNetworkRequest

from qgis.gui import QgsRubberBand
from qgis.core import QgsMessageLog, Qgis, QgsWkbTypes, QgsPointXY, QgsCoordinateTransform, QgsGeometry, QgsProject, QgsField, QgsVectorLayer, QgsFeature, QgsFeatureRequest, QgsNetworkAccessManager, QgsTextAnnotation, QgsMarkerSymbol, QgsLocatorResult
from qgis.utils import iface

from geobarcelona.utils import var

def info(self, msg=""):

    QgsMessageLog.logMessage('{}'.format(msg), type(self).__name__, Qgis.Info)

def message_bar(self, msg=""):

    iface.messageBar().pushMessage(type(self).__name__, msg, level=Qgis.Warning, duration=8)

def config_rubberband(self):

    class_type = type(self).__name__

    self.point_rubberband = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
    self.point_rubberband.setColor(QColor(50,50,255,255))
    self.point_rubberband.setIcon(self.point_rubberband.ICON_CIRCLE)
    self.point_rubberband.setIconSize(8)
    self.point_rubberband.setWidth(8)
    self.point_rubberband.setBrushStyle(Qt.NoBrush)

    if class_type == var.type_reverse or class_type == var.type_address:

        self.polygon_rubberband = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.polygon_rubberband.setColor(QColor(255, 50, 50, 255))
        self.polygon_rubberband.setFillColor(QColor(0, 0, 0, 0))
        self.polygon_rubberband.setBrushStyle(Qt.SolidPattern)
        self.polygon_rubberband.setLineStyle(Qt.SolidLine)
        self.polygon_rubberband.setWidth(4)

        if class_type == var.type_reverse:

            self.clicked_point_rubberband = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)
            self.selected_point_rubberband = QgsRubberBand(self.canvas, QgsWkbTypes.PointGeometry)

            self.clicked_point_rubberband.setColor(QColor(255,0,0,255))
            self.clicked_point_rubberband.setIcon(self.clicked_point_rubberband.ICON_CIRCLE)
            self.clicked_point_rubberband.setIconSize(4)
            self.clicked_point_rubberband.setWidth(4)
            self.clicked_point_rubberband.setBrushStyle(Qt.NoBrush)

            self.selected_point_rubberband.setColor(QColor(255,50,255,255))
            self.selected_point_rubberband.setIcon(self.selected_point_rubberband.ICON_CIRCLE)
            self.selected_point_rubberband.setIconSize(12)
            self.selected_point_rubberband.setWidth(12)
            self.selected_point_rubberband.setBrushStyle(Qt.NoBrush)

def config_tblResult_horizontal_headers(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        HorizontalHeaderLabels = self.HorizontalHeaderLabels_reverse_address

    elif class_type == var.type_address:

        HorizontalHeaderLabels = self.HorizontalHeaderLabels_search_address

    self.column_count = len(HorizontalHeaderLabels)
    self.ui.tblResult.setColumnCount(self.column_count)

    for count in range(self.column_count):

        horizontalheaderitem = QTableWidgetItem()
        horizontalheaderitem.setText(HorizontalHeaderLabels[count][var.pos_label_text])
        horizontalheaderitem.setToolTip(HorizontalHeaderLabels[count][var.pos_tooltip])

        if HorizontalHeaderLabels[count][var.pos_tooltip]:
            horizontalheaderitem.setIcon(var.info_icon)

        self.ui.tblResult.setHorizontalHeaderItem(count, horizontalheaderitem)

    self.ui.tblResult.resizeColumnsToContents()
    self.ui.tblResult.resizeRowsToContents()
    self.ui.tblResult.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.ui.tblResult.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

def config_tblclickedpoint_vertical_headers(self):

    self.row_count = len(self.VerticalHeaderLabels_reverse_address)
    self.ui.tblclickedpoint.setRowCount(self.row_count)

    for count in range(self.row_count):

        verticalheaderitem = QTableWidgetItem()
        verticalheaderitem.setText(self.VerticalHeaderLabels_reverse_address[count][var.pos_label_text])
        verticalheaderitem.setToolTip(self.VerticalHeaderLabels_reverse_address[count][var.pos_tooltip])

        if self.VerticalHeaderLabels_reverse_address[count][var.pos_tooltip]:
            verticalheaderitem.setIcon(var.info_icon)

        self.ui.tblclickedpoint.setVerticalHeaderItem(count, verticalheaderitem)

    self.ui.tblclickedpoint.resizeColumnsToContents()
    self.ui.tblclickedpoint.resizeRowsToContents()
    self.ui.tblclickedpoint.verticalHeader().setStretchLastSection(True)
    self.ui.tblclickedpoint.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.ui.tblclickedpoint.horizontalHeader().hide()
    self.ui.tblclickedpoint.horizontalHeader().setStretchLastSection(True)
    self.ui.tblclickedpoint.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

def config_ui(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        self.ui.label.setText(self.lbl_instructions_reverse_text)
        self.ui.label_3.setText(self.lbl_tblresult_reverse_text)
        self.ui.label_4.setText(self.lbl_tblclickedpoint_text)
        self.ui.lblResult.setText(var.void_results_text)

        self.ui.start_capture.setIcon(var.capture_icon)
        self.ui.start_capture.setIconSize(QSize(30,30))
        self.ui.start_capture.setStyleSheet("padding: 5px;")
        self.ui.start_capture.setText(var.start_capture_text_space + self.capt_button_text)

        self.ui.clear_capture_results.setIcon(var.clear_icon)
        self.ui.clear_capture_results.setIconSize(QSize(30,30))
        self.ui.clear_capture_results.setText(var.clear_capt_text_space + self.clear_capt_button_text)
        self.ui.clear_capture_results.setEnabled(False)

        self.ui.save_all_results.setIcon(var.download_icon)
        self.ui.save_all_results.setIconSize(QSize(20,20))
        self.ui.save_all_results.setText(var.save_all_results_text_space + self.save_all_button_text)
        self.ui.save_all_results.setEnabled(False)

    elif class_type == var.type_address:

        self.ui.txtSearch.setPlaceholderText(self.search_address_text)
        self.ui.lblResult.setText(var.void_results_text)
        self.search_icon_action = self.ui.txtSearch.addAction(var.search_icon, QLineEdit.LeadingPosition)

def setupEvents(self):

    self.ui.tblResult.cellActivated.connect(self.onAction_tblResult)
    self.ui.tblResult.cellClicked.connect(self.onAction_tblResult_click)
    QgsProject.instance().crsChanged.connect(partial(crs_changed, self))
    QgsProject.instance().cleared.connect(partial(cleared_project, self))
    QShortcut(Qt.Key_Down, self.ui.tblResult, activated=partial(key_shortcut_down, self))
    QShortcut(Qt.Key_Up, self.ui.tblResult, activated=partial(key_shortcut_up, self))
    QShortcut(Qt.Key_Left, self.ui.tblResult, activated=partial(key_shortcut_left, self))
    QShortcut(Qt.Key_Right, self.ui.tblResult, activated=partial(key_shortcut_right, self))

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        self.ui.tblclickedpoint.cellClicked.connect(self.onAction_tblclickedpoint_click)
        self.ui.tblclickedpoint.cellActivated.connect(self.onAction_tblclickedpoint)
        self.ui.start_capture.clicked.connect(self.startCapturing)
        self.ui.clear_capture_results.clicked.connect(partial(clear_all_results, self))
        self.ui.save_all_results.clicked.connect(partial(save_results, self))

    elif class_type == var.type_address:

        self.ui.txtSearch.textEdited.connect(self.start_typing_timer)
        var.loading_icon.frameChanged.connect(self.updateSpinnerAniamation)
        QShortcut(Qt.Key_Enter, self.ui.tblResult, activated=partial(key_shortcut_enter, self))
        QShortcut(Qt.Key_Return, self.ui.tblResult, activated=partial(key_shortcut_enter, self))
        QApplication.instance().focusChanged.connect(self.on_focusChanged)

def crs_changed(self):

    delete_rubbers(self)

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        if self.stored_geometry_addresses:

            for count in range(len(self.stored_geometry_addresses)):
                self.point_rubberband.addGeometry(self.stored_geometry_addresses[count], var.results_crs)

        if self.selected_point_geom:
            self.selected_point_rubberband.addGeometry(self.selected_point_geom, var.results_crs)

        if self.clicked_point_geom:
            self.clicked_point_rubberband.addGeometry(self.clicked_point_geom, var.results_crs)

    elif class_type == var.type_address:

        if self.selected_point_geom:
            self.point_rubberband.addGeometry(self.selected_point_geom, var.results_crs)

    if self.polygon_geom:
        self.polygon_rubberband.addGeometry(self.polygon_geom, var.results_crs)

def key_shortcut_down(self):

    class_type = type(self).__name__

    if self.ui.tblResult.hasFocus():

        row = self.ui.tblResult.currentRow() + 1

        if row < self.ui.tblResult.rowCount():

            if class_type == var.type_reverse:

                self.ui.tblclickedpoint.clearSelection()

            col = self.ui.tblResult.currentColumn()
            self.ui.tblResult.setCurrentCell(row, col)
            self.onAction_tblResult(row, col)

        return

    if class_type == var.type_address:

        if self.ui.txtSearch.hasFocus():

            self.ui.tblResult.setCurrentCell(0, 0)
            self.ui.tblResult.setFocus()
            self.onAction_tblResult(0, 0)

    elif class_type == var.type_reverse:

        if self.ui.tblclickedpoint.hasFocus():

            row = self.ui.tblclickedpoint.currentRow() + 1

            if row < self.ui.tblclickedpoint.rowCount():

                self.ui.tblResult.clearSelection()
                delete_rubber_selected_point(self)
                col = self.ui.tblclickedpoint.currentColumn()
                self.ui.tblclickedpoint.setCurrentCell(row, col)
                self.onAction_tblclickedpoint(row, col)

def key_shortcut_up(self):

    class_type = type(self).__name__

    if self.ui.tblResult.hasFocus():

        row = self.ui.tblResult.currentRow() - 1

        if row >= 0:

            if class_type == var.type_reverse:

                self.ui.tblclickedpoint.clearSelection()

            col = self.ui.tblResult.currentColumn()
            self.ui.tblResult.setCurrentCell(row, col)
            self.onAction_tblResult(row, col)

        elif class_type == var.type_address:

            self.ui.tblResult.clearSelection()
            self.ui.txtSearch.setFocus()
            delete_rubbers(self)

        return

    if class_type == var.type_reverse:

        if self.ui.tblclickedpoint.hasFocus():

            row = self.ui.tblclickedpoint.currentRow() - 1

            if row >= 0:

                self.ui.tblResult.clearSelection()
                delete_rubber_selected_point(self)
                col = self.ui.tblclickedpoint.currentColumn()
                self.ui.tblclickedpoint.setCurrentCell(row, col)
                self.onAction_tblclickedpoint(row, col)

def key_shortcut_left(self):

    if self.ui.tblResult.hasFocus():

        col = self.ui.tblResult.currentColumn() - 1

        if col >= 0:

            row = self.ui.tblResult.currentRow()
            self.ui.tblResult.setCurrentCell(row, col)
            self.onAction_tblResult(row, col)

def key_shortcut_right(self):

    if self.ui.tblResult.hasFocus():

        col = self.ui.tblResult.currentColumn() + 1

        if col < self.ui.tblResult.columnCount():

            row = self.ui.tblResult.currentRow()
            self.ui.tblResult.setCurrentCell(row, col)
            self.onAction_tblResult(row, col)

def key_shortcut_enter(self):

    if self.ui.txtSearch.hasFocus():

        self.ui.tblResult.setCurrentCell(0, 0)
        self.ui.tblResult.setFocus()
        self.onAction_tblResult(0, 0)

def cleared_project(self):

    try:
        clear_all_results(self)
    except:
        pass

def clear_error(self):

    class_type = type(self).__name__

    if class_type == var.type_address:

        self.task = None
        self.ui.txtSearch.blockSignals(False)

    elif class_type == var.type_reverse:

        self.task = []

    clear_all_results(self)

def clear_all_results(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        delete_labels(self)

    clear_results(self)
    delete_rubbers(self)
    clear_geometries(self)

def clear_results(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        clear_point_results(self)
        self.ui.save_all_results.setEnabled(False)
        self.ui.clear_capture_results.setEnabled(False)

    self.lid = []
    clear_address_results(self)
    self.ui.lblResult.setText(var.void_results_text)

def clear_address_results(self):

    self.ui.tblResult.clearContents()
    self.ui.tblResult.scrollTo(self.ui.tblResult.model().index(0,0))
    self.ui.tblResult.setRowCount(0)
    self.ui.tblResult.resizeColumnsToContents()
    self.ui.tblResult.resizeRowsToContents()

    self.stored_addresses = []
    self.stored_individual_address = None

    class_type = type(self).__name__

    if class_type == var.type_address:

        if self.loading_icon_action is not None:

            var.loading_icon.stop()
            self.ui.txtSearch.removeAction(self.loading_icon_action)
            self.ui.txtSearch.setClearButtonEnabled(True)
            self.loading_icon_action = None

def clear_point_results(self):

    self.ui.tblclickedpoint.clearContents()
    self.ui.tblclickedpoint.setColumnCount(0)
    self.ui.tblclickedpoint.resizeColumnsToContents()

def delete_rubbers(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        delete_rubber_clicked_point(self)
        delete_rubber_selected_point(self)

    delete_rubber_points(self)
    delete_rubber_polygons(self)

def delete_rubber_points(self):

    self.point_rubberband.reset(QgsWkbTypes.PointGeometry)

def delete_rubber_polygons(self):

    self.polygon_rubberband.reset(QgsWkbTypes.PolygonGeometry)

def delete_rubber_clicked_point(self):

    self.clicked_point_rubberband.reset(QgsWkbTypes.PointGeometry)

def delete_rubber_selected_point(self):

    self.selected_point_rubberband.reset(QgsWkbTypes.PointGeometry)

def delete_labels(self):

    for ct in range(len(self.labels)):

        if self.labels[ct] in self.annot_manager.annotations():

            self.annot_manager.removeAnnotation(self.labels[ct])

    self.labels = []

def clear_geometries(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        self.clicked_point_geom = None

    self.stored_geometry_addresses = []
    self.stored_individual_geometry = None
    self.selected_point_geom = None
    self.polygon_geom = None

def clear_error_complementary_request(self, error_msg):

    message_bar(self, error_msg)
    info(self, error_msg)
    self.secc = []
    self.complementary_task = None
    delete_rubber_polygons(self)

def clear_locator(self, error_msg):

    result = QgsLocatorResult()
    result.filter = self
    result.displayString = error_msg
    result.userData = []
    self.resultFetched.emit(result)

def networkRequest(url, feedback, ua_type):

    if ua_type == var.type_reverse:
        user_agent = var.user_agent_reverse
    elif ua_type == var.type_address:
        user_agent = var.user_agent_address
    elif ua_type == var.type_locator:
        user_agent = var.user_agent_locator

    network_manager = QgsNetworkAccessManager()
    request = QNetworkRequest(QUrl(url))
    request.setRawHeader(b'User-Agent', user_agent)
    response = network_manager.blockingGet(request, forceRefresh = True, feedback = feedback)

    return response

def url_reverse(coordinate_x, coordinate_y):

    url = ['https://w33.bcn.cat/geoBCN/serveis/territori/adreces?x=' + coordinate_x + '&y=' + coordinate_y + '&out_proj=' + var.results_crs_code + '&proj=' + var.results_crs_code + '&radi=' + str(var.search_radius) + '&max=' + str(var.max_results_reverse) + '&geometria=true',
           'https://w33.bcn.cat/geoBCN/serveis/territori/districtes?x=' + coordinate_x + '&y=' + coordinate_y + '&out_proj=' + var.results_crs_code + '&proj=' + var.results_crs_code + '&geometria=true',
           'https://w33.bcn.cat/geoBCN/serveis/territori/barris?x=' + coordinate_x + '&y=' + coordinate_y + '&out_proj=' + var.results_crs_code + '&proj=' + var.results_crs_code + '&geometria=true',
           'https://w33.bcn.cat/geoBCN/serveis/territori/illes?x=' + coordinate_x + '&y=' + coordinate_y + '&out_proj=' + var.results_crs_code + '&proj=' + var.results_crs_code + '&geometria=true',
           'https://w33.bcn.cat/geoBCN/serveis/territori/parcelles?x=' + coordinate_x + '&y=' + coordinate_y + '&out_proj=' + var.results_crs_code + '&proj=' + var.results_crs_code + '&geometria=true']

    return url

def url_address(search):

    url = 'https://w33.bcn.cat/geoBCN/serveis/territori?q=' + search + '&geometria=true&out_proj=' + var.results_crs_code

    return url

def url_locator(search):

    url = 'https://w33.bcn.cat/geoBCN/serveis/territori?q=' + search + '&out_proj=' + var.results_crs_code

    return url

def url_complementary_request(request_type, codi1, codi2):

    if request_type == var.request_type_seccio_censal:

        url = 'https://w33.bcn.cat/geoBCN/serveis/territori/seccionscensals?codi='+codi1+'&districte='+codi2+'&geometria=true&out_proj=' + var.results_crs_code

    elif request_type == var.request_type_parcela:

        url = 'https://w33.bcn.cat/geoBCN/serveis/territori/parcelles/'+ codi1 + codi2 + '?geometria=true&out_proj=' + var.results_crs_code

    return url

def hr_init(self):

    class_type = type(self).__name__

    self.lid = []
    self.stored_addresses = []
    self.stored_geometry_addresses = []
    self.selected_point_geom = None
    self.polygon_geom = None
    self.complementary_task = None

    if class_type == var.type_address:

        self.task = None

    elif class_type == var.type_reverse:

        self.task = []

def load_json(self, content_string, json_type):

    class_type = type(self).__name__

    try:

        locations = json.loads(content_string)
        return locations

    except:

        error_msg = self.json_error_text

        if class_type == var.type_locator:

            clear_locator(self, error_msg)

        else:

            info(self, error_msg)
            message_bar(self, error_msg)

            if json_type == var.type_json_complementary:

                delete_rubber_polygons(self)
                self.complementary_task = None

            elif json_type == var.type_json_main:

                clear_error(self)

        return None

def hr_load_json(self, content, json_type):

    class_type = type(self).__name__

    if json_type == var.type_json_complementary or class_type == var.type_address or class_type == var.type_locator:

        content_string = content.data().decode(var.encoding)
        locations = load_json(self, content_string, json_type)
        return locations

    elif class_type == var.type_reverse:

        locations = []

        for count in range(len(content)):

            content_string = content[count].data().decode(var.encoding)
            json_result = load_json(self, content_string, json_type)

            if json_result is None:

                return None

            else:

                locations.append(json_result)

        return locations

def prepare_string(search):

    search = search.strip()

    #remove digits before characters to avoid api freeze in some cases

    dig = 0

    for count in range(len(search)):

        if search[count].isdigit():

            dig += 1

        else:

            break

    search = search[dig:]

    #remove non alphanumeric characters in the first 3 characters of the string

    if len(search) >= 3:

        if not search[2].isalnum():

            if len(search) == 3:
                search = ''
            else:
                search = search[3:].strip()

        elif not search[1].isalnum():

            search = search[2:].strip()

        elif not search[0].isalnum():

            search = search[1:].strip()

    return search

def prepare_tblclickedpoint(lid):

    if not lid[var.pos_lid_districtes]:
        codi_districte = var.void_results_text_2
        districte = var.void_results_text_2
    else:
        codi_districte = lid[var.pos_lid_districtes][0][var.geobcnlabel_codi]
        districte = lid[var.pos_lid_districtes][0][var.geobcnlabel_descripcio]

    if not lid[var.pos_lid_barris]:
        codi_barri = var.void_results_text_2
        barri = var.void_results_text_2
    else:
        codi_barri = lid[var.pos_lid_barris][0][var.geobcnlabel_codi]
        barri = lid[var.pos_lid_barris][0][var.geobcnlabel_nom]

    if not lid[var.pos_lid_illa]:
        illa = var.void_results_text_2
        illa_area = var.void_results_text_2
    else:
        illa = lid[var.pos_lid_illa][0][var.geobcnlabel_codi]
        illa_area = str(round(lid[var.pos_lid_illa][0][var.geobcnlabel_area],2)) + ' m\u00b2'

    if not lid[var.pos_lid_parcela]:
        parcela = var.void_results_text_2
        parcela_area = var.void_results_text_2
        ref_cad = var.void_results_text_2
    else:
        parcela = lid[var.pos_lid_parcela][0][var.geobcnlabel_codi]
        parcela_area = str(round(lid[var.pos_lid_parcela][0][var.geobcnlabel_area],2)) + ' m\u00b2'
        ref_cad = lid[var.pos_lid_parcela][0][var.geobcnlabel_refcad]

    column_items = [codi_districte, districte, codi_barri, barri, illa, illa_area, parcela, parcela_area, ref_cad]

    return column_items

def prepare_tblResult(self, count, lid):

    class_type = type(self).__name__

    nomcomplet = lid[count]['nomComplet']
    districte = lid[count][var.geobcnlabel_districte][var.geobcnlabel_descripcio]
    barri = lid[count][var.geobcnlabel_barri][var.geobcnlabel_nom]
    codi_postal = '080' + lid[count]['districtePostal']
    coord_x = str(round(lid[count]['localitzacio']['x'], var.round_x))
    coord_y = str(round(lid[count]['localitzacio']['y'], var.round_y))

    if class_type == var.type_reverse or class_type == var.type_address:

        codi_districte = lid[count][var.geobcnlabel_districte][var.geobcnlabel_codi]
        codi_barri = lid[count][var.geobcnlabel_barri][var.geobcnlabel_codi]
        area_estadistica_basica = lid[count]['seccioEst']
        seccio_censal = lid[count]['seccioCensal']
        illa = lid[count]['illa'][var.geobcnlabel_codi]
        parcela = lid[count]['parcelaId']
        solar = lid[count]['solar']
        ref_cad = lid[count][var.geobcnlabel_refcad]
        codi_carrer = lid[count][var.geobcnlabel_carrer][var.geobcnlabel_codi]
        abreviatura_carrer = lid[count][var.geobcnlabel_carrer]['tipusVia']['abreviatura']
        nom_abreviatura_carrer = lid[count][var.geobcnlabel_carrer]['tipusVia'][var.geobcnlabel_nom]
        nom_carrer = lid[count][var.geobcnlabel_carrer]['nom27']
        nom_llarg_carrer = lid[count][var.geobcnlabel_carrer]['nomLlarg']
        nom_complet_carrer = lid[count][var.geobcnlabel_carrer]['nomComplet']
        numero_inicial = lid[count]['numeroPostalInicial']
        lletra_inicial = lid[count]['lletraPostalInicial']
        numero_final = lid[count]['numeroPostalFinal']
        lletra_final = lid[count]['lletraPostalFinal']
        numeracio_postal = lid[count]['numeracioPostal']
        tipus_numero_adreca = lid[count]['tipusNumero']
        codi_adreca = lid[count]['id']
        proj_coord = lid[count]['localitzacio']['proj']

        if class_type == var.type_reverse:

            coord_x_clicked = ''
            coord_y_clicked = ''
            dist = lid[count]['extraInfo']['distancia'] + ' m'
            row_items = [nomcomplet, dist, codi_postal, codi_districte, districte, codi_barri, barri, area_estadistica_basica, seccio_censal, illa, parcela, solar, ref_cad, codi_carrer, abreviatura_carrer, nom_abreviatura_carrer, nom_carrer, nom_llarg_carrer, nom_complet_carrer, numero_inicial, lletra_inicial, numero_final, lletra_final, numeracio_postal, tipus_numero_adreca, codi_adreca, coord_x, coord_y, coord_x_clicked, coord_y_clicked, proj_coord]

        else:

            row_items = [nomcomplet, codi_postal, codi_districte, districte, codi_barri, barri, area_estadistica_basica, seccio_censal, illa, parcela, solar, ref_cad, codi_carrer, abreviatura_carrer, nom_abreviatura_carrer, nom_carrer, nom_llarg_carrer, nom_complet_carrer, numero_inicial, lletra_inicial, numero_final, lletra_final, numeracio_postal, tipus_numero_adreca, codi_adreca, coord_x, coord_y, proj_coord]

    elif class_type == var.type_locator:

        row_items = [nomcomplet, codi_postal, districte, barri]

    point = QgsGeometry.fromPointXY(QgsPointXY(float(coord_x),float(coord_y)))

    return row_items, point

def prepare_address_buttons():

    download_button = QPushButton(var.download_icon, '')
    download_button.setFixedSize(25,24)
    download_button.setIconSize(QSize(16,16))
    download_button.setStyleSheet('QPushButton {background-color: #FFFFFF; border: 1px solid #D8D8D8;}')

    google_maps_button = QPushButton(var.google_maps_icon, '')
    google_maps_button.setFixedSize(25,24)
    google_maps_button.setIconSize(QSize(21,20))
    google_maps_button.setStyleSheet('QPushButton {background-color: #FFFFFF; border: 1px solid #D8D8D8;}')

    google_street_view_button = QPushButton(var.google_street_view_icon, '')
    google_street_view_button.setFixedSize(25,24)
    google_street_view_button.setIconSize(QSize(21,20))
    google_street_view_button.setStyleSheet('QPushButton {background-color: #FFFFFF; border: 1px solid #D8D8D8;}')

    catastro_button = QPushButton(var.catastro_icon, '')
    catastro_button.setFixedSize(25,24)
    catastro_button.setIconSize(QSize(21,20))
    catastro_button.setStyleSheet('QPushButton {background-color: #FFFFFF; border: 1px solid #D8D8D8;}')

    return download_button, google_maps_button, google_street_view_button, catastro_button

def prepare_catastro_button():

    catastro_button = QPushButton(var.catastro_icon, '')
    catastro_button.setFixedSize(25,24)
    catastro_button.setIconSize(QSize(21,20))
    catastro_button.setStyleSheet('QPushButton {background-color: #FFFFFF; border: 1px solid #D8D8D8;}')

    return catastro_button

def fill_tblclickedpoint(self):

    self.ui.tblclickedpoint.setUpdatesEnabled(False)
    self.ui.tblclickedpoint.clearContents()
    self.ui.tblclickedpoint.setColumnCount(1)

    self.column_items = prepare_tblclickedpoint(self.lid)

    for count in range(len(self.column_items)):

        if count == var.pos_refcad_tblclickedpoint:

            hlayout = QHBoxLayout()
            hlayout.setContentsMargins(3, 3, 10, 3)

            catastro_button = prepare_catastro_button()
            catastro_button.clicked.connect(partial(onAction_catastroButton, self, var.type_reverse_clicked))

            if len(self.column_items[count]) != var.long_refcad:
                catastro_button.setEnabled(False)

            hlayout.addWidget(QLabel(self.column_items[count]))
            hlayout.addWidget(catastro_button)

            catastro_widget = QWidget()
            catastro_widget.setLayout(hlayout)
            self.ui.tblclickedpoint.setCellWidget(count, 0, catastro_widget)

        else:

            self.ui.tblclickedpoint.setItem(0, count, QTableWidgetItem(self.column_items[count]))

    self.ui.tblclickedpoint.resizeColumnsToContents()
    self.ui.tblclickedpoint.resizeRowsToContents()
    self.ui.tblclickedpoint.setUpdatesEnabled(True)

def fill_tblResult(self, response_adreces, pos_address, pos_refcad):

    class_type = type(self).__name__

    self.ui.tblResult.setUpdatesEnabled(False)
    self.ui.tblResult.clearContents()
    self.ui.tblResult.setRowCount(self.len_response_adreces)

    for count in range(self.len_response_adreces):

        row_items, geom_point = prepare_tblResult(self, count, response_adreces)

        self.stored_addresses.append(row_items)

        if class_type == var.type_reverse:

            self.stored_addresses[count][var.pos_xclicked_tblResult_reverse] = self.coordinate_x
            self.stored_addresses[count][var.pos_yclicked_tblResult_reverse] = self.coordinate_y

        self.stored_geometry_addresses.append(geom_point)

        for count1 in range(len(self.stored_addresses[count])):

            if count1 == pos_address:

                hlayout = QHBoxLayout()
                hlayout.setContentsMargins(10, 5, 10, 5)

                download_button, google_maps_button, google_street_view_button, catastro_button = prepare_address_buttons()

                download_button.clicked.connect(partial(save_one_result, self))
                google_maps_button.clicked.connect(partial(onAction_google_maps, self))
                google_street_view_button.clicked.connect(partial(onAction_google_street_view, self))
                catastro_button.clicked.connect(partial(onAction_catastroButton, self, ''))

                if len(self.stored_addresses[count][pos_refcad]) != var.long_refcad:
                    catastro_button.setEnabled(False)

                hlayout.addWidget(QLabel(self.stored_addresses[count][count1]))
                hlayout.addWidget(download_button)
                hlayout.addWidget(google_maps_button)
                hlayout.addWidget(google_street_view_button)
                hlayout.addWidget(catastro_button)

                google_widget = QWidget()
                google_widget.setLayout(hlayout)
                self.ui.tblResult.setCellWidget(count, count1, google_widget)

            elif count1 == pos_refcad:

                hlayout = QHBoxLayout()
                hlayout.setContentsMargins(10, 5, 10, 5)

                catastro_button = prepare_catastro_button()
                catastro_button.clicked.connect(partial(onAction_catastroButton, self, ''))

                if len(self.stored_addresses[count][count1]) != var.long_refcad:
                    catastro_button.setEnabled(False)

                hlayout.addWidget(QLabel(self.stored_addresses[count][count1]))
                hlayout.addWidget(catastro_button)

                catastro_widget = QWidget()
                catastro_widget.setLayout(hlayout)
                self.ui.tblResult.setCellWidget(count, count1, catastro_widget)

            else:

                self.ui.tblResult.setItem(count, count1, QTableWidgetItem(self.stored_addresses[count][count1]))

    self.ui.tblResult.resizeColumnsToContents()
    self.ui.tblResult.resizeRowsToContents()
    self.ui.tblResult.scrollTo(self.ui.tblResult.model().index(0,0))
    self.ui.tblResult.setUpdatesEnabled(True)

def rubbers_labels_reverse(self):

    for count in range(self.len_response_adreces):

        self.point_rubberband.addGeometry(self.stored_geometry_addresses[count], var.results_crs)

        annot = QgsTextAnnotation()
        lbl = QTextDocument()
        symbol = QgsMarkerSymbol()
        symbol.setSize(0)
        lbltext = self.stored_addresses[count][0]
        lbl.setPlainText(lbltext)

        self.labels.append(annot)
        self.labels[count].setMapPosition(self.stored_geometry_addresses[count].asPoint())
        self.labels[count].setMapPositionCrs(var.results_crs)
        self.labels[count].setDocument(lbl)
        self.labels[count].setFrameSizeMm(QSizeF(lbl.size().width()*(25.4/self.logicalDpiX()),lbl.size().height()*(25.4/self.logicalDpiY())))
        self.labels[count].setMarkerSymbol(symbol)

        self.annot_manager.addAnnotation(self.labels[count])

def save_one_result(self):

    index, i, j = identify_cell(self, '')

    if index.isValid():

        self.stored_individual_address = self.stored_addresses[index.row()]
        self.stored_individual_geometry = self.stored_geometry_addresses[index.row()]
        save_results(self)
        self.stored_individual_address = []
        self.stored_individual_geometry = []
        return_focus(self, i, j, '')

def onAction_google_maps(self):

    index, i, j = identify_cell(self, '')

    if index.isValid():

        class_type = type(self).__name__

        if class_type == var.type_reverse:

            nomcomplet = self.stored_addresses[index.row()][0]
            codi_postal = self.stored_addresses[index.row()][2]

        else:

            nomcomplet = self.stored_addresses[index.row()][0]
            codi_postal = self.stored_addresses[index.row()][1]

        gm1 = nomcomplet + ' ' + codi_postal + ' ' + 'Barcelona'
        gm1 = gm1.replace(' ','+')
        gm_web = 'https://www.google.com/maps/search/?api=1&query=' + gm1
        webbrowser.open(gm_web)
        return_focus(self, i, j, '')

def onAction_google_street_view(self):

    index, i, j = identify_cell(self, '')

    if index.isValid():

        pt = self.stored_geometry_addresses[i].asPoint()
        tr = QgsCoordinateTransform(var.results_crs, var.google_crs, QgsProject.instance())
        reprojected_pt = tr.transform(pt)
        coord = str(reprojected_pt.y()) + ',' + str(reprojected_pt.x())
        gm_web = 'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=' + coord
        webbrowser.open(gm_web)
        return_focus(self, i, j, '')

def onAction_catastroButton(self, type_button):

    index, i, j = identify_cell(self, type_button)

    if index.isValid():

        class_type = type(self).__name__

        if class_type == var.type_reverse:

            if type_button == var.type_reverse_clicked:

                codi_ref_cad = self.column_items[var.pos_refcad_tblclickedpoint]

            else:

                codi_ref_cad = self.stored_addresses[index.row()][var.pos_refcad_tblResult_reverse]

        elif class_type == var.type_address:

            codi_ref_cad = self.stored_addresses[index.row()][var.pos_refcad_tblResult]

        else:

            codi_ref_cad = '00000000000000'

        rc1 = codi_ref_cad[0:7]
        rc2 = codi_ref_cad[-7:]
        rf_web = 'https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCListaBienes.aspx?del=8&muni=900&rc1=' + rc1 + '&rc2=' + rc2
        webbrowser.open(rf_web)
        return_focus(self, i, j, type_button)

def save_results(self):

    class_type = type(self).__name__

    if class_type == var.type_reverse:

        identify_selected_table(self)

    attributes = []
    address_id_list = []
    camps_usats = [self.header_address_code_text]

    if class_type == var.type_reverse:

        layer_name = self.layer_name_reverse_text

    else:

        layer_name = self.layer_name_address_text

    layer = QgsProject.instance().mapLayersByName(layer_name)

    if not layer:

        for count in range(self.column_count):

            if class_type == var.type_reverse:

                attributes.append(QgsField(self.HorizontalHeaderLabels_reverse_address[count][0], self.HorizontalHeaderLabels_reverse_address[count][2]))

            else:

                attributes.append(QgsField(self.HorizontalHeaderLabels_search_address[count][0], self.HorizontalHeaderLabels_search_address[count][2]))

        self.addresslayer = QgsVectorLayer('point?crs=' + var.results_crs_code + '&index=yes', layer_name, 'memory')
        self.addressProvider = self.addresslayer.dataProvider()
        self.addressProvider.setEncoding(var.encoding)
        self.addressProvider.addAttributes(attributes)
        self.addresslayer.updateFields()
        fields = self.addresslayer.fields()

    else:

        self.addresslayer = layer[0]
        self.addressProvider = self.addresslayer.dataProvider()
        fields = self.addresslayer.fields()
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry).setSubsetOfAttributes(camps_usats, fields)
        features = self.addresslayer.getFeatures(request)

        for feature in features:

            if class_type == var.type_reverse:

                address_id_list.append(feature[25])

            else:

                address_id_list.append(feature[24])

    if self.stored_individual_address:

        addresses_saved = [self.stored_individual_address]
        geometry_saved = [self.stored_individual_geometry]

    else:

        addresses_saved = self.stored_addresses
        geometry_saved = self.stored_geometry_addresses

    feature_flag = 0

    for count in range(len(addresses_saved)):

        if class_type == var.type_reverse:

            address_id = addresses_saved[count][25]

        else:

            address_id = addresses_saved[count][24]

        if address_id not in address_id_list:

            feat = QgsFeature(fields)
            pt = geometry_saved[count]
            feat.setGeometry(pt)

            for count1 in range(self.column_count):
                feat[count1] = addresses_saved[count][count1]

            self.addressProvider.addFeatures([feat])
            feature_flag += 1

    if feature_flag > 0:

        self.addresslayer.updateExtents()
        QgsProject.instance().addMapLayer(self.addresslayer)
        self.addresslayer.triggerRepaint()
        self.canvas.refresh()

def complementary_request(self, request_type, codi1, codi2, i, j):

    from geobarcelona.utils.task import GeoBarcelonaDownloadTask

    url = url_complementary_request(request_type, codi1, codi2)
    error_msg = self.geometry_error_text

    if self.complementary_task is None:

        self.complementary_task = GeoBarcelonaDownloadTask(url, type(self).__name__)
        self.complementary_task.taskCompleted.connect(partial(complementary_request_response, self, request_type, i , j))
        self.complementary_task.taskTerminated.connect(partial(clear_error_complementary_request, self, error_msg))
        self.taskManager.addTask(self.complementary_task)

def complementary_request_response(self, request_type, i , j):

    error_code = self.complementary_task.response.error()

    if error_code == 0:

        content = self.complementary_task.response.content()
        locations = hr_load_json(self, content, var.type_json_complementary)

        if locations is None:

            self.onAction_tblResult(i, 0)

            return None

        self.secc = locations[var.geobcnlabel_resultats]

        if len(self.secc) == 1:

            self.secc = locations[var.geobcnlabel_resultats][0]
            draw_rubber_polygon(self, request_type, var.type_tblResult, i, j)
            self.complementary_task = None

        else:

            error_msg = self.geometry_error_text
            clear_error_complementary_request(self, error_msg)
            self.onAction_tblResult(i, 0)

    else:

        error_msg = self.complementary_task.response.errorString()
        clear_error_complementary_request(self, error_msg)
        self.onAction_tblResult(i, 0)

def draw_rubber_polygon(self, result_type, table_type, i, j):

    class_type = type(self).__name__

    try:

        delete_rubber_polygons(self)

        if table_type == var.type_tblResult:

            if result_type == var.request_type_seccio_censal or result_type == var.request_type_parcela:

                geom_coordinates = self.secc[var.geobcnlabel_geometria][var.geobcnlabel_coordinates][0]

            else:

                if class_type == var.type_reverse:

                    geom_coordinates = self.lid[var.pos_lid_adreces][i][result_type][var.geobcnlabel_geometria][var.geobcnlabel_coordinates][0]

                elif class_type == var.type_address:

                    geom_coordinates = self.lid[i][result_type][var.geobcnlabel_geometria][var.geobcnlabel_coordinates][0]

                else:

                    raise

        elif table_type == var.type_tblclickedpoint:

            geom_coordinates = self.lid[var.ctg[i]][0][var.geobcnlabel_geometria][var.geobcnlabel_coordinates][0]

        else:

            raise

        self.polygon_geom = QgsGeometry.fromPolygonXY([[QgsPointXY(pt[0],pt[1]) for pt in geom_coordinates]])
        self.polygon_rubberband.addGeometry(self.polygon_geom, var.results_crs)
        rec = self.polygon_rubberband.asGeometry().boundingBox()
        self.canvas.setExtent(rec)
        self.canvas.refresh()

    except:

        error_msg = self.geometry_error_text
        clear_error_complementary_request(self, error_msg)

        if table_type == var.type_tblclickedpoint:

            zoom_result(self, self.clicked_point_rubberband)

        else:

            self.onAction_tblResult(i, 0)

def zoom_result(self, point_geometry):

    rec = point_geometry.asGeometry().boundingBox()
    self.canvas.setExtent(rec)
    self.canvas.zoomScale(var.zoom_scale)
    self.canvas.refresh()

def identify_selected_table(self):

    if len(self.ui.tblResult.selectedIndexes()) == 1:

        self.ui.tblResult.setFocus()

    elif len(self.ui.tblclickedpoint.selectedIndexes()) == 1:

        self.ui.tblclickedpoint.setFocus()

def identify_cell(self, type_button):

    clickedButton = self.sender()

    if type_button == var.type_reverse_clicked:

        index = self.ui.tblclickedpoint.indexAt(clickedButton.parent().pos())

    else:

        index = self.ui.tblResult.indexAt(clickedButton.parent().pos())

    if index.isValid():

        i = index.row()
        j = index.column()

    else:

        i = None
        j = None

    return index, i, j

def return_focus(self, i, j, type_button):

    if type_button == var.type_reverse_clicked:

        self.ui.tblResult.clearSelection()
        delete_rubber_selected_point(self)
        self.ui.tblclickedpoint.setCurrentCell(i, j)
        self.ui.tblclickedpoint.setFocus()
        self.onAction_tblclickedpoint(i, j)

    else:

        self.ui.tblResult.setCurrentCell(i, j)
        self.ui.tblResult.setFocus()
        self.onAction_tblResult(i, j)

        class_type = type(self).__name__

        if class_type == var.type_reverse:

            self.ui.tblclickedpoint.clearSelection()