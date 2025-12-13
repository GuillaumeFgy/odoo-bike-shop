# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    """Extension des commandes de vente"""
    _inherit = 'sale.order'

    # Compteur de vélos dans la commande
    bike_count = fields.Integer(
        string='Nombre de Vélos',
        compute='_compute_bike_count',
        store=True
    )

    @api.depends('order_line.product_id.is_bike')
    def _compute_bike_count(self):
        """Compte le nombre de vélos dans la commande"""
        for order in self:
            order.bike_count = sum(
                line.product_uom_qty
                for line in order.order_line
                if line.product_id.is_bike
            )


class SaleOrderLine(models.Model):
    """Extension des lignes de commande"""
    _inherit = 'sale.order.line'

    is_bike = fields.Boolean(
        string='Est un Vélo',
        related='product_id.is_bike',
        store=True
    )
    bike_category = fields.Char(
        string='Catégorie',
        related='product_id.bike_category_id.name',
        store=True
    )
