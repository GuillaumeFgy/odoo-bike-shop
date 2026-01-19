# -*- coding: utf-8 -*-
{
    'name': 'Bike Shop - Vente',
    'version': '19.0.1.0.0',
    'summary': 'Vente de vélos et accessoires',
    'depends': [
        'sale_management',
        'stock',
        'bike_shop_rental',
    ],
    'data': [
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
