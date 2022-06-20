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

from qgis.PyQt.QtGui import QIcon, QMovie

from qgis.core import QgsCoordinateReferenceSystem

from pathlib import Path

user_agent_address = b'Mozilla/5.0 QGIS GeoBarcelona Address'
user_agent_reverse = b'Mozilla/5.0 QGIS GeoBarcelona Dock Reverse Address'
user_agent_locator = b'Mozilla/5.0 QGIS GeoBarcelona Locator Filter'
plugin_menu_name_text = u'GeoBarcelona'

void_results_text = '---'
void_results_text_2 = '-'
start_capture_text_space = '  '
clear_capt_text_space = ' '
save_all_results_text_space = '  '

search_radius = 100
max_results_address = 25
max_results_reverse = 10
locator_timer = 15
zoom_scale = 1000
timer_delay = 800

plugin_dir = Path(os.path.dirname(__file__)).parents[0]
icons_dir = ':/plugins/geobarcelona/resources/icons'
encoding = 'utf-8'
results_crs_code = 'EPSG:25831'
results_crs = QgsCoordinateReferenceSystem(results_crs_code)
google_crs = QgsCoordinateReferenceSystem('EPSG:4326')
long_refcad = 14
round_x = 4
round_y = 4
type_reverse = 'GeoBarcelonaReverseAddressSearch'
type_reverse_clicked = 'reverse_clicked'
type_address = 'GeoBarcelonaAddressSearch'
type_locator = 'GeoBarcelonaLocatorFilter'
request_type_districte = 'districte'
request_type_barri = 'barri'
request_type_seccio_censal = 'secc'
request_type_illa = 'illa'
request_type_parcela = 'parc'
type_tblResult = 'tblResult'
type_tblclickedpoint = 'tblclickedpoint'
type_json_main = 'main_request'
type_json_complementary = 'complementary_request'

ctg = [1,1,2,2,3,3,4,4,4]

pos_label_text = 0
pos_tooltip = 1

geobcnlabel_resultats = 'resultats'
geobcnlabel_codi = 'codi'
geobcnlabel_descripcio = 'descripcio'
geobcnlabel_nom = 'nom'
geobcnlabel_area = 'area'
geobcnlabel_refcad = 'referenciaCadastral'
geobcnlabel_adreces = 'adreces'
geobcnlabel_geometria = 'geometria'
geobcnlabel_coordinates = 'coordinates'
geobcnlabel_districte = 'districte'
geobcnlabel_barri = 'barri'
geobcnlabel_carrer = 'carrer'

pos_refcad_tblclickedpoint = 8

pos_address_tblResult_reverse = 0
pos_refcad_tblResult_reverse = 12
pos_x_tblResult_reverse = 26
pos_y_tblResult_reverse = 27
pos_xclicked_tblResult_reverse = 28
pos_yclicked_tblResult_reverse = 29
pos_crs_tblResult_reverse = 30

pos_address_tblResult = 0
pos_refcad_tblResult = 11

pos_lid_adreces = 0
pos_lid_districtes = 1
pos_lid_barris = 2
pos_lid_illa = 3
pos_lid_parcela = 4

loading_icon = QMovie(os.path.join(icons_dir, 'cercant.gif'))
search_icon = QIcon(os.path.join(icons_dir, 'search.png'))
catastro_icon = QIcon(os.path.join(icons_dir, 'catastro.png'))
info_icon = QIcon(os.path.join(icons_dir, 'about.png'))
google_maps_icon = QIcon(os.path.join(icons_dir, 'maps.png'))
google_street_view_icon = QIcon(os.path.join(icons_dir, 'street.png'))
download_icon = QIcon(os.path.join(icons_dir, 'download.png'))
capture_icon = QIcon(os.path.join(icons_dir, 'capture.png'))
clear_icon = QIcon(os.path.join(icons_dir, 'clear.png'))
plugin_icon = QIcon(os.path.join(icons_dir, 'icon.png'))
help_icon = QIcon(os.path.join(icons_dir, 'help.png'))

help_web = 'https://github.com/javicasnov/GeoBarcelona'