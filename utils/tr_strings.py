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

from qgis.PyQt.QtCore import QCoreApplication, QVariant

from geobarcelona.utils import var

def tr_strings_GeoBarcelona(self):

    self.open_close_panel_text = QCoreApplication.translate('GeoBarcelona',u'Open/Close panel')
    self.help_text = QCoreApplication.translate('GeoBarcelona',u'Help')
    self.about_title_text = QCoreApplication.translate('GeoBarcelona',u'About')
    self.open_close_panel_extended_text = QCoreApplication.translate('GeoBarcelona',u'Open/Close GeoBarcelona panel')
    self.about_title_extended_text = QCoreApplication.translate('GeoBarcelona',u'GeoBarcelona - About')
    self.about_version_text = QCoreApplication.translate('GeoBarcelona',u'Version 2.0 - June 2022')
    self.about_description_text = QCoreApplication.translate('GeoBarcelona',u'QGIS plugin to search and zoom to any address in Barcelona city.<br>Based on the RESTful web service "GeoBCN" (<a href="https://w33.bcn.cat/GeoBcn">https://w33.bcn.cat/GeoBcn</a>) provided by the Barcelona City Council.')
    self.about_link_help_code_text = QCoreApplication.translate('GeoBarcelona',u'Help and code repository')
    self.about_link_bugtracker_text = QCoreApplication.translate('GeoBarcelona',u'Bug tracker')
    self.about_title_credits_text = QCoreApplication.translate('GeoBarcelona',u'Development and maintenance')
    self.about_title_acknowledgements_text = QCoreApplication.translate('GeoBarcelona',u'Acknowledgements')
    self.about_content_acknowledgements_text = QCoreApplication.translate('GeoBarcelona',u'Barcelona City Council, especially in memoriam of Xavi Llinares.')
    self.about_html = u'<html><body style="margin-right:15px;"><div style="text-align:center;"><img src="' + var.icons_dir + '/icon_geobarcelona_full.png" width="87" height="87"></div><h1 style="text-align:center;">GeoBarcelona</h1><p style="text-align:center">' + self.about_version_text + '</p><p style="text-align:center">' + self.about_description_text + '</p><p style="text-align:center"><a href="https://github.com/javicasnov/GeoBarcelona">' + self.about_link_help_code_text + '</a></p><p style="text-align:center"><a href="https://github.com/javicasnov/GeoBarcelona/issues">' + self.about_link_bugtracker_text + '</a></p><h3 style="text-align:center">' + self.about_title_credits_text + '</h3><p style="text-align:center">Javier Casado (<a href="mailto:javicasnov@hotmail.com">javicasnov@hotmail.com</a>)</p><h3 style="text-align:center">' + self.about_title_acknowledgements_text + '</h3><p style="text-align:center">' + self.about_content_acknowledgements_text + '</p></body></html>'

def tr_strings_GeoBarcelonaDockWidget(self):

    self.tab_address_search_text = QCoreApplication.translate('GeoBarcelonaDockWidget', u'Address search')
    self.tab_reverse_address_search_text = QCoreApplication.translate('GeoBarcelonaDockWidget', u'Reverse address search')
    
def tr_strings_GeoBarcelonaDownloadTask(self):

    self.task_canceled_text = QCoreApplication.translate('GeoBarcelonaDownloadTask', u'Request canceled. Connection has been aborted or closed.')
    self.task_exception_text = QCoreApplication.translate('GeoBarcelonaDownloadTask', u'Exception: %s.')
    
def tr_strings_GeoBarcelonaLocatorFilter(self):

    self.lbl_noresult_locator_text = QCoreApplication.translate('GeoBarcelonaLocatorFilter', u'No addresses found')
    
def tr_strings_GeoBarcelonaDock(self):

    class_type = type(self).__name__
    
    self.header_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'Address')
    self.header_dist_clicked_point_text = QCoreApplication.translate('GeoBarcelonaDock', u'Distance to clicked point')
    self.header_postal_code_text = QCoreApplication.translate('GeoBarcelonaDock', u'Postal code')
    self.header_district_code_text = QCoreApplication.translate('GeoBarcelonaDock', u'District code')
    self.header_district_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'District name')
    self.header_neighbourhood_code_text = QCoreApplication.translate('GeoBarcelonaDock', u'Neighbourhood code')
    self.header_neighbourhood_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'Neighbourhood name')
    self.header_basic_stat_area_text = QCoreApplication.translate('GeoBarcelonaDock', u'Basic statistical area')
    self.header_census_section_text = QCoreApplication.translate('GeoBarcelonaDock', u'Census section')
    self.header_block_text = QCoreApplication.translate('GeoBarcelonaDock', u'Block')
    self.header_building_parcel_text = QCoreApplication.translate('GeoBarcelonaDock', u'Building parcel')
    self.header_building_lot_text = QCoreApplication.translate('GeoBarcelonaDock', u'Building lot')
    self.header_ref_cad_text = QCoreApplication.translate('GeoBarcelonaDock', u'Land registry reference')
    self.header_street_code_text = QCoreApplication.translate('GeoBarcelonaDock', u'Street code')
    self.header_street_abbr_text = QCoreApplication.translate('GeoBarcelonaDock', u'Street abbreviation')
    self.header_street_abbr_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'Street abbreviation name')
    self.header_street_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'Street name')
    self.header_street_long_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'Street long name')
    self.header_street_full_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'Street full name')
    self.header_init_postal_number_text = QCoreApplication.translate('GeoBarcelonaDock', u'Initial postal number')
    self.header_init_postal_letter_text = QCoreApplication.translate('GeoBarcelonaDock', u'Initial postal letter')
    self.header_final_postal_number_text = QCoreApplication.translate('GeoBarcelonaDock', u'Final postal number')
    self.header_final_postal_letter_text = QCoreApplication.translate('GeoBarcelonaDock', u'Final postal letter')
    self.header_postal_numbering_text = QCoreApplication.translate('GeoBarcelonaDock', u'Postal numbering')
    self.header_address_num_type_text = QCoreApplication.translate('GeoBarcelonaDock', u'Address type')
    self.header_address_code_text = QCoreApplication.translate('GeoBarcelonaDock', u'Address code')
    self.header_x_coord_text = QCoreApplication.translate('GeoBarcelonaDock', u'X coordinate')
    self.header_y_coord_text = QCoreApplication.translate('GeoBarcelonaDock', u'Y coordinate')
    self.header_x_coord_clicked_text = QCoreApplication.translate('GeoBarcelonaDock', u'X coordinate (clicked point)')
    self.header_y_coord_clicked_text = QCoreApplication.translate('GeoBarcelonaDock', u'Y coordinate (clicked point)')
    self.header_crs_text = QCoreApplication.translate('GeoBarcelonaDock', u'CRS')

    self.tooltip_postal_code_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>Code assigned to different areas that serves to facilitate and mechanize the distribution of mail.</p><p>It consists of five digits: the first two refer to the province and the last three correspond to delivery areas assigned by Correos, the Spanish National Postal Company.</p></body></html>')
    self.tooltip_district_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The district is the largest territorial unit within the city of Barcelona.</p><p>In the current territorial organization, which dates back to 1984, the municipality is administratively divided into 10 districts.</p></body></html>')
    self.tooltip_neighbourhood_name_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The neighborhood is the second largest territorial unit, after the district, within the city of Barcelona.</p><p>In the current territorial organization, which dates back to 2006, the municipality is administratively divided into 73 neighborhoods.</p></body></html>')
    self.tooltip_basic_stat_area_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The basic statistical area is the territorial unit located below the neighborhoods in the municipal territorial hierarchy.</p><p>The municipality is divided into 233 areas, designed for purely statistical purposes, since they are uniform in terms of population, urban and sociological criteria.</p></body></html>')
    self.tooltip_census_section_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The census section is the territorial unit located below the basic statistical areas in the municipal territorial hierarchy.</p><p>They are designed for statistical and electoral purposes and are defined based on criteria of regularity and homogeneity, generally with a population between 1000 and 2500 inhabitants. The last revision was carried out in 2014, defining 1068 census sections. These are divided by districts, that is, starting in each district from number 1.</p></body></html>')
    self.tooltip_block_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The block is the territorial unit located below the census sections in the municipal territorial hierarchy.</p><p>A block is the urban space delimited by streets on all sides. The municipality is divided into 5439 blocks.</p></body></html>')
    self.tooltip_building_parcel_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The building parcel is, with the lot, the territorial unit located below the blocks in the municipal territorial hierarchy.</p><p>Refers to a portion of land that can already be built, not be built but be buildable, or be not buildable. The numbering of these is divided by blocks, that is, starting in each block from number 1.</p></body></html>')
    self.tooltip_building_lot_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The building lot is, with the parcel, the territorial unit located below the blocks in the municipal territorial hierarchy.</p><p>Refers to a portion of land that is equipped with basic urban services. This means that a building can already be built, or not be built but be buildable.</p></body></html>')
    self.tooltip_ref_cad_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The land registry reference is the official and mandatory identifier of real estate.</p><p>It consists of a alphanumeric code composed of 20 characters, of which the first 14 are used to identify a parcel or lot.</p></body></html>')
    self.tooltip_address_num_type_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>The different types of number of an address can be:</p><il><li>0: Self-identifying entity - no numbering</li><li>1: Odd number</li><li>2: Even number</li><li>3: Apartment block</li><li>4: Ring road entrances/exits</li><li>5: Kilometre point</li><li>6: Block</li><li>7: Special use</li></il></body></html>')
    self.tooltip_crs_text = QCoreApplication.translate('GeoBarcelonaDock', u'<html><head/><body><p>A Coordinate Reference System (CRS) defines, with the help of coordinates, how a two-dimensional projected map is related to real places on Earth.</p><p>The decision of which projection and which coordinate reference system to use depends on the regional extent of the working area and the analysis wanted to perform.</p></body></html>')
    
    self.HorizontalHeaderLabels_reverse_address = [[self.header_address_text, None, QVariant.String],
        [self.header_dist_clicked_point_text, None, QVariant.String],
        [self.header_postal_code_text, self.tooltip_postal_code_text, QVariant.String],
        [self.header_district_code_text, None, QVariant.String],
        [self.header_district_name_text, self.tooltip_district_name_text, QVariant.String],
        [self.header_neighbourhood_code_text, None, QVariant.String],
        [self.header_neighbourhood_name_text, self.tooltip_neighbourhood_name_text, QVariant.String],
        [self.header_basic_stat_area_text, self.tooltip_basic_stat_area_text, QVariant.String],
        [self.header_census_section_text, self.tooltip_census_section_text, QVariant.String],
        [self.header_block_text, self.tooltip_block_text, QVariant.String],
        [self.header_building_parcel_text, self.tooltip_building_parcel_text, QVariant.String],
        [self.header_building_lot_text, self.tooltip_building_lot_text, QVariant.String],
        [self.header_ref_cad_text, self.tooltip_ref_cad_text, QVariant.String],
        [self.header_street_code_text, None, QVariant.String],
        [self.header_street_abbr_text, None, QVariant.String],
        [self.header_street_abbr_name_text, None, QVariant.String],
        [self.header_street_name_text, None, QVariant.String],
        [self.header_street_long_name_text, None, QVariant.String],
        [self.header_street_full_name_text, None, QVariant.String],
        [self.header_init_postal_number_text, None, QVariant.String],
        [self.header_init_postal_letter_text, None, QVariant.String],
        [self.header_final_postal_number_text, None, QVariant.String],
        [self.header_final_postal_letter_text, None, QVariant.String],
        [self.header_postal_numbering_text, None, QVariant.String],
        [self.header_address_num_type_text, self.tooltip_address_num_type_text, QVariant.String],
        [self.header_address_code_text, None, QVariant.String],
        [self.header_x_coord_text, None, QVariant.String],
        [self.header_y_coord_text, None, QVariant.String],
        [self.header_x_coord_clicked_text, None, QVariant.String],
        [self.header_y_coord_clicked_text, None, QVariant.String],
        [self.header_crs_text, self.tooltip_crs_text, QVariant.String]]
    
    self.geometry_error_text = QCoreApplication.translate('GeoBarcelonaDock', u'Geometry not available.')
    
    if class_type == var.type_address:
    
        self.search_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'Search address: simpler addresses give faster results, e.g, "Aragó 44" instead of "C/ Aragó, 44"')
        self.searching_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'Searching...')
        self.lbl_1result_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'1 address found')
        self.lbl_maxresult_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'Displaying first %d addresses found')
        self.lbl_elseresult_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'%d addresses found')
        self.lbl_noresult_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'No addresses found')
        self.layer_name_address_text = QCoreApplication.translate('GeoBarcelonaDock', u'geobcn_addresses')
        
        self.HorizontalHeaderLabels_search_address = [self.HorizontalHeaderLabels_reverse_address[0],
            self.HorizontalHeaderLabels_reverse_address[2],
            self.HorizontalHeaderLabels_reverse_address[3],
            self.HorizontalHeaderLabels_reverse_address[4],
            self.HorizontalHeaderLabels_reverse_address[5],
            self.HorizontalHeaderLabels_reverse_address[6],
            self.HorizontalHeaderLabels_reverse_address[7],
            self.HorizontalHeaderLabels_reverse_address[8],
            self.HorizontalHeaderLabels_reverse_address[9],
            self.HorizontalHeaderLabels_reverse_address[10],
            self.HorizontalHeaderLabels_reverse_address[11],
            self.HorizontalHeaderLabels_reverse_address[12],
            self.HorizontalHeaderLabels_reverse_address[13],
            self.HorizontalHeaderLabels_reverse_address[14],
            self.HorizontalHeaderLabels_reverse_address[15],
            self.HorizontalHeaderLabels_reverse_address[16],
            self.HorizontalHeaderLabels_reverse_address[17],
            self.HorizontalHeaderLabels_reverse_address[18],
            self.HorizontalHeaderLabels_reverse_address[19],
            self.HorizontalHeaderLabels_reverse_address[20],
            self.HorizontalHeaderLabels_reverse_address[21],
            self.HorizontalHeaderLabels_reverse_address[22],
            self.HorizontalHeaderLabels_reverse_address[23],
            self.HorizontalHeaderLabels_reverse_address[24],
            self.HorizontalHeaderLabels_reverse_address[25],
            self.HorizontalHeaderLabels_reverse_address[26],
            self.HorizontalHeaderLabels_reverse_address[27],
            self.HorizontalHeaderLabels_reverse_address[30]]

    elif class_type == var.type_reverse:

        self.capt_button_text = QCoreApplication.translate('GeoBarcelonaDock', u'Start capturing addresses')
        self.capt_button_text_2 = QCoreApplication.translate('GeoBarcelonaDock', u'Click any point on the map')
        self.capt_button_text_3 = QCoreApplication.translate('GeoBarcelonaDock', u'Searching addresses...')
        self.clear_capt_button_text = QCoreApplication.translate('GeoBarcelonaDock', u'Clear results')
        self.save_all_button_text = QCoreApplication.translate('GeoBarcelonaDock', u'Save all addresses')
        self.lbl_instructions_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'Click the button below to select any point on canvas inside Barcelona city. Right-click to escape capturing addresses.')
        self.lbl_tblresult_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'Closest addresses')
        self.lbl_tblclickedpoint_text = QCoreApplication.translate('GeoBarcelonaDock', u'Clicked point data')
        self.lbl_1result_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'1 address found in a %dm radius')
        self.lbl_maxresult_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'Displaying the %d nearest address found in a %dm radius')
        self.lbl_elseresult_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'%d addresses found in a %dm radius')
        self.lbl_noresult_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'No addresses found in a %dm radius')
        self.layer_name_reverse_text = QCoreApplication.translate('GeoBarcelonaDock', u'geobcn_reverse_addresses')
        self.header_block_area_text = QCoreApplication.translate('GeoBarcelonaDock', u'Block area')
        self.header_building_parcel_area_text = QCoreApplication.translate('GeoBarcelonaDock', u'Building parcel area')

        self.VerticalHeaderLabels_reverse_address = [[self.HorizontalHeaderLabels_reverse_address[3][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[3][var.pos_tooltip]],
            [self.HorizontalHeaderLabels_reverse_address[4][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[4][var.pos_tooltip]],
            [self.HorizontalHeaderLabels_reverse_address[5][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[5][var.pos_tooltip]],
            [self.HorizontalHeaderLabels_reverse_address[6][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[6][var.pos_tooltip]],
            [self.HorizontalHeaderLabels_reverse_address[9][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[9][var.pos_tooltip]],
            [self.header_block_area_text, None],
            [self.HorizontalHeaderLabels_reverse_address[10][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[10][var.pos_tooltip]],
            [self.header_building_parcel_area_text, None],
            [self.HorizontalHeaderLabels_reverse_address[12][var.pos_label_text], self.HorizontalHeaderLabels_reverse_address[12][var.pos_tooltip]]]

def tr_strings_GeoBarcelonaCommon(self):

    self.timeout_error_text = QCoreApplication.translate('GeoBarcelonaCommon', u'Request timeout reached. Connection has been aborted or closed.')
    self.json_error_text = QCoreApplication.translate('GeoBarcelonaCommon', u'Error in json loads.')