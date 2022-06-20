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

def classFactory(iface):
    """Load GeoBarcelona class from file GeoBarcelona.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from geobarcelona.geobarcelona import GeoBarcelona
    return GeoBarcelona(iface)