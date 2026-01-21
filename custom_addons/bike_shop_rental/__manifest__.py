# -*- coding: utf-8 -*-
{
    'name': 'Bike Shop - Location',
    'version': '19.0.1.0.0',
    'summary': 'Location de vélos',
    'depends': [
        'base',
        'sale_management',
        'stock',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/bike_category_data.xml',
        'data/product_data.xml',
        'views/bike_views.xml',
        'views/rental_order_views.xml',
        'views/menu_views.xml',
        'views/reports/rental_report_views.xml',
        'reports/rental_contract_report.xml',
        'reports/rental_report_templates.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'bike_shop_rental/static/src/scss/bike_shop.scss',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
