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

from qgis.PyQt.QtCore import QSettings, QTranslator, QLocale, QCoreApplication, Qt, QTimer
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox

from geobarcelona.resources import resources

from geobarcelona.gui.geobarcelona_dockwidget import GeoBarcelonaDockWidget
from geobarcelona.core.geobarcelona_locator import GeoBarcelonaLocatorFilter
from geobarcelona.utils import var
from geobarcelona.utils import tr_strings

import webbrowser
import os.path

class GeoBarcelona(object):

    def __init__(self, iface):

        self.iface = iface

        if QSettings().value('locale/overrideFlag', type=bool):
            locale = QSettings().value('locale/userLocale', 'en')
        else:
            locale = QLocale.system().name()

        localePath = os.path.join(var.plugin_dir, 'i18n', 'geobarcelona_{}.qm'.format(locale[0:2]))

        if os.path.exists(localePath):

            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)

        tr_strings.tr_strings_GeoBarcelona(self)
        
        self.actions = []

        self.toolbar = self.iface.pluginToolBar()

        self.pluginIsActive = False
        self.dockwidget = None

        self.filter = GeoBarcelonaLocatorFilter(self.iface)
        self.iface.registerLocatorFilter(self.filter)

    def initGui(self):

        self.geobcn_menu = QMenu(var.plugin_menu_name_text)
        self.geobcn_menu.setIcon(var.plugin_icon)

        self.openpanel_item = QAction(var.plugin_icon, self.open_close_panel_text, self.iface.mainWindow())
        self.openpanel_item.triggered.connect(self.run)

        self.help_item = QAction(var.help_icon, self.help_text, self.iface.mainWindow())
        self.help_item.triggered.connect(self.help)

        self.about_item = QAction(var.info_icon, self.about_title_text, self.iface.mainWindow())
        self.about_item.triggered.connect(self.about)

        self.toolbar_item = QAction(var.plugin_icon, self.open_close_panel_extended_text, self.iface.mainWindow())
        self.toolbar_item.triggered.connect(self.run)
        self.toolbar.addAction(self.toolbar_item)

        self.actions = [self.openpanel_item, self.help_item, self.about_item]
        self.geobcn_menu.addActions(self.actions)

        self.menu = self.iface.pluginMenu()
        self.menu.addMenu(self.geobcn_menu)

    def onClosePlugin(self):

        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        self.pluginIsActive = False

    def unload(self):

        self.menu.removeAction(self.geobcn_menu.menuAction())
        self.toolbar.removeAction(self.toolbar_item)
        self.iface.deregisterLocatorFilter(self.filter)

    def run(self):

        if not self.pluginIsActive:

            self.pluginIsActive = True

            if self.dockwidget == None:

                self.dockwidget = GeoBarcelonaDockWidget(self.iface)
                self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)

            self.dockwidget.closingPlugin.connect(self.onClosePlugin)
            QTimer.singleShot(0,self.dockwidget.text_focus)
            self.dockwidget.show()

        else:

            self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)
            self.pluginIsActive = False
            self.dockwidget.delete_data()
            self.dockwidget.hide()

    def help(self):

        webbrowser.open(var.help_web)

    def about(self):

        about_dialog = QMessageBox()
        about_dialog.setIcon(QMessageBox.NoIcon)
        about_dialog.setStandardButtons(QMessageBox.Close)
        about_dialog.setWindowTitle(self.about_title_extended_text)
        about_dialog.setText(self.about_html)
        about_dialog.exec_()