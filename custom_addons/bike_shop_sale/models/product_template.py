# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    """Extension du modèle produit pour les vélos et accessoires"""
    _inherit = 'product.template'

    # Type de produit pour le magasin de vélos
    bike_shop_type = fields.Selection([
        ('bike', 'Vélo'),
        ('accessory', 'Accessoire'),
        ('part', 'Pièce Détachée'),
        ('service', 'Service'),
        ('other', 'Autre'),
    ], string='Type de Produit Bike Shop')

    # Champs spécifiques aux vélos
    is_bike = fields.Boolean(string='Est un Vélo', compute='_compute_is_bike', store=True)
    bike_category_id = fields.Many2one(
        'bike.category',
        string='Catégorie de Vélo',
        help='Catégorie du vélo (Ville, VTT, Route, etc.)'
    )
    bike_brand = fields.Char(string='Marque')
    bike_model = fields.Char(string='Modèle')
    bike_year = fields.Integer(string='Année de Fabrication')
    bike_frame_size = fields.Selection([
        ('xs', 'XS (Extra Small)'),
        ('s', 'S (Small)'),
        ('m', 'M (Medium)'),
        ('l', 'L (Large)'),
        ('xl', 'XL (Extra Large)'),
    ], string='Taille du Cadre')
    bike_color = fields.Char(string='Couleur')
    bike_weight = fields.Float(string='Poids (kg)')
    bike_condition = fields.Selection([
        ('new', 'Neuf'),
        ('used_excellent', 'Occasion - Excellent'),
        ('used_good', 'Occasion - Bon'),
        ('used_fair', 'Occasion - Correct'),
    ], string='État', default='new')

    # Champs pour les accessoires et pièces
    accessory_type = fields.Selection([
        ('helmet', 'Casque'),
        ('lock', 'Antivol'),
        ('light', 'Éclairage'),
        ('pump', 'Pompe'),
        ('bag', 'Sacoche'),
        ('bottle', 'Bidon'),
        ('computer', 'Compteur'),
        ('clothing', 'Vêtement'),
        ('other', 'Autre'),
    ], string='Type d\'Accessoire')

    part_type = fields.Selection([
        ('tire', 'Pneu'),
        ('tube', 'Chambre à Air'),
        ('brake', 'Frein'),
        ('chain', 'Chaîne'),
        ('gear', 'Vitesse'),
        ('pedal', 'Pédale'),
        ('saddle', 'Selle'),
        ('handlebar', 'Guidon'),
        ('wheel', 'Roue'),
        ('other', 'Autre'),
    ], string='Type de Pièce')

    # Caractéristiques techniques
    is_electric = fields.Boolean(string='Électrique')
    battery_capacity = fields.Float(string='Capacité Batterie (Wh)')
    max_speed = fields.Float(string='Vitesse Max (km/h)')
    range_km = fields.Float(string='Autonomie (km)')

    # Garantie
    warranty_months = fields.Integer(string='Garantie (mois)', default=24)
    warranty_info = fields.Text(string='Informations Garantie')

    @api.depends('bike_shop_type')
    def _compute_is_bike(self):
        """Détermine si le produit est un vélo"""
        for product in self:
            product.is_bike = product.bike_shop_type == 'bike'

    @api.onchange('bike_category_id')
    def _onchange_bike_category(self):
        """Met à jour le nom du produit avec la catégorie"""
        if self.bike_category_id and self.bike_brand and self.bike_model:
            self.name = f"{self.bike_brand} {self.bike_model} - {self.bike_category_id.name}"


class ProductProduct(models.Model):
    """Extension du modèle variante de produit"""
    _inherit = 'product.product'

    # Hérite tous les champs du template
    bike_shop_type = fields.Selection(related='product_tmpl_id.bike_shop_type', store=True)
    is_bike = fields.Boolean(related='product_tmpl_id.is_bike', store=True)
