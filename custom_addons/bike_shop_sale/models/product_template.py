# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """Extension du modèle produit pour catégoriser les produits du magasin"""
    _inherit = 'product.template'

    bike_shop_type = fields.Selection([
        ('bike', 'Vélo'),
        ('accessory', 'Accessoire'),
        ('part', 'Pièce Détachée'),
    ], string='Type')
