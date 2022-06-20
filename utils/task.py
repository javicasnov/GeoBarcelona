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

from qgis.core import QgsTask, QgsFeedback

from geobarcelona.utils import tr_strings
from geobarcelona.utils import utils

class GeoBarcelonaDownloadTask(QgsTask):

    def __init__(self, url, type):

        super().__init__('GeoBarcelona Download Task', QgsTask.CanCancel)
        self.url = url
        self.type = type
        self.feedback = QgsFeedback()
        tr_strings.tr_strings_GeoBarcelonaDownloadTask(self)

    def run(self):

        try:

            self.response = utils.networkRequest(self.url, self.feedback, self.type)

            if self.isCanceled():
                return False

            return True

        except Exception as e:

            self.exception = e

            return False

    def finished(self, result):

        if self.isCanceled():

            utils.info(self, self.task_canceled_text)
            utils.message_bar(self, self.task_canceled_text)
            return

        elif not result:

            utils.info(self, (self.task_exception_text) % str(self.exception))
            utils.message_bar(self, (self.task_exception_text) % str(self.exception))
            return

    def cancel(self):

        super().cancel()
        self.feedback.cancel()