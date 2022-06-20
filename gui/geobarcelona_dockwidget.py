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
import sys

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QApplication, QWidget, QVBoxLayout
from qgis.PyQt.QtCore import pyqtSignal

from geobarcelona.core.geobarcelona_address import GeoBarcelonaAddressSearch
from geobarcelona.core.geobarcelona_reverse_address import GeoBarcelonaReverseAddressSearch
from geobarcelona.utils import var
from geobarcelona.utils import tr_strings

FORM, BASE = uic.loadUiType(os.path.join(var.plugin_dir, 'ui\\geobarcelona_dockwidget_base.ui'))

class GeoBarcelonaDockWidget(BASE, FORM):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        
        super(GeoBarcelonaDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.setupPlug()

    def setupPlug(self):

        self.ui = self
        tr_strings.tr_strings_GeoBarcelonaDockWidget(self)

        self.address_widget = GeoBarcelonaAddressSearch(self.iface)
        tab_address_layout = QVBoxLayout()
        tab_address_layout.addWidget(self.address_widget)
        tab_address_widget = QWidget()
        tab_address_widget.setLayout(tab_address_layout)
        self.ui.tabWidget.addTab(tab_address_widget, self.tab_address_search_text)

        self.reverse_address_widget = GeoBarcelonaReverseAddressSearch(self.iface)
        tab_reverse_address_layout = QVBoxLayout()
        tab_reverse_address_layout.addWidget(self.reverse_address_widget)
        tab_reverse_address_widget = QWidget()
        tab_reverse_address_widget.setLayout(tab_reverse_address_layout)
        self.ui.tabWidget.addTab(tab_reverse_address_widget, self.tab_reverse_address_search_text)

        self.ui.tabWidget.setCurrentIndex(0)

    def text_focus(self):
        self.address_widget.ui.txtSearch.setFocus()

    def delete_data(self):
        self.address_widget.closeEvent_address()
        self.reverse_address_widget.closeEvent_reverse_address()
        self.ui.tabWidget.setCurrentIndex(0)

    def closeEvent(self, event):
        self.delete_data()
        self.closingPlugin.emit()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = GeoBarcelonaDockWidget()
    app.addDockWidget(dialog)
    dialog.show()
    sys.exit(app.exec_())