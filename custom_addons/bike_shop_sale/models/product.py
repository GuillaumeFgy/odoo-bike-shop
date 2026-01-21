# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ShopProduct(models.Model):
    """Produit du magasin de vélos"""
    _name = 'shop.product'
    _description = 'Produit'
    _order = 'name'

    name = fields.Char(string='Nom', required=True)
    product_type = fields.Selection([
        ('bike', 'Vélo'),
        ('accessory', 'Accessoire'),
        ('part', 'Pièce Détachée'),
    ], string='Type', required=True, default='accessory')

    description = fields.Text(string='Description')
    price = fields.Float(string='Prix de vente (€)', required=True, default=0.0)
    cost = fields.Float(string='Prix d\'achat (€)', default=0.0)
    quantity = fields.Integer(string='Quantité en stock', default=0)

    active = fields.Boolean(string='Actif', default=True)

    @api.depends('price', 'cost')
    def _compute_margin(self):
        for product in self:
            product.margin = product.price - product.cost

    margin = fields.Float(string='Marge (€)', compute='_compute_margin')

    def action_confirm_and_return(self):
        """Sauvegarde le produit et retourne à la liste des produits"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'shop.product',
            'view_mode': 'list,kanban,form',
            'target': 'current',
        }
