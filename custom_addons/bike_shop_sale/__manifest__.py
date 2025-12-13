# -*- coding: utf-8 -*-
{
    'name': 'Bike Shop - Sales Management',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Gestion des ventes de vélos et accessoires',
    'description': """
        Module de gestion des ventes pour le magasin de vélos
        ======================================================

        Ce module permet de gérer :
        * La vente de vélos neufs et d'occasion
        * La vente d'accessoires (casques, antivols, éclairages, etc.)
        * La vente de pièces détachées
        * La gestion du stock
        * La facturation
        * Le reporting des ventes

        Fonctionnalités :
        -----------------
        - Catalogue produits étendu avec caractéristiques spécifiques aux vélos
        - Gestion des commandes clients
        - Suivi du stock en temps réel
        - Reporting des ventes par catégorie et par produit
        - Historique client
    """,
    'author': 'Bike Shop Team',
    'website': 'https://github.com/MattLambot/odoo-bike-shop',
    'depends': [
        'base',
        'sale_management',
        'stock',
        'product',
        'account',
        'bike_shop_rental',  # Dépend du module de location pour partager les catégories
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/menu_views.xml',

        # Reports
        'reports/sale_report_templates.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
