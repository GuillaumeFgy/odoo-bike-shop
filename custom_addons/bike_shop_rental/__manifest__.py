# -*- coding: utf-8 -*-
{
    'name': 'Bike Shop - Rental Management',
    'version': '19.0.1.0.0',
    'category': 'Sales/Rental',
    'summary': 'Gestion de location de vélos pour le magasin',
    'description': """
        Module de gestion de location de vélos
        =======================================

        Ce module permet de gérer :
        * Les vélos disponibles à la location
        * Les contrats de location (courte et longue durée)
        * La tarification par heure/jour/mois
        * La disponibilité des vélos
        * Le suivi des clients et de leur historique de location

        Fonctionnalités :
        -----------------
        - Catalogue de vélos avec catégories
        - Gestion des contrats de location
        - Calcul automatique des tarifs
        - Suivi de la disponibilité en temps réel
        - Reporting de taux d'occupation
    """,
    'author': 'Bike Shop Team',
    'website': 'https://github.com/MattLambot/odoo-bike-shop',
    'depends': [
        'base',
        'sale_management',
        'product',
        'stock',
        'account',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/bike_category_data.xml',
        'data/product_data.xml',

        # Views
        'views/bike_views.xml',
        'views/rental_order_views.xml',
        'views/menu_views.xml',
        'views/reports/rental_report_views.xml',

        # Reports
        'reports/rental_contract_report.xml',
        'reports/rental_report_templates.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
