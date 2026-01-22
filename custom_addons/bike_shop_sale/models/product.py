# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


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
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
    ], string='État', default='draft', required=True)

    @api.depends('price', 'cost')
    def _compute_margin(self):
        for product in self:
            product.margin_amount = product.price - product.cost
            if product.cost > 0:
                product.margin_percent = ((product.price - product.cost) / product.cost) * 100
            else:
                product.margin_percent = 0.0

    margin_amount = fields.Float(string='Marge (€)', compute='_compute_margin', store=True)
    margin_percent = fields.Float(string='Marge (%)', compute='_compute_margin', store=True)

    @api.constrains('price')
    def _check_price(self):
        """Vérifie que le prix de vente est positif"""
        for product in self:
            if product.price < 0:
                raise exceptions.ValidationError(
                    "Le prix de vente ne peut pas être négatif."
                )

    @api.constrains('cost')
    def _check_cost(self):
        """Vérifie que le prix d'achat est positif"""
        for product in self:
            if product.cost < 0:
                raise exceptions.ValidationError(
                    "Le prix d'achat ne peut pas être négatif."
                )

    @api.constrains('quantity')
    def _check_quantity(self):
        """Vérifie que la quantité n'est pas négative"""
        for product in self:
            if product.quantity < 0:
                raise exceptions.ValidationError(
                    "La quantité en stock ne peut pas être négative."
                )

    @api.constrains('price', 'cost')
    def _check_margin(self):
        """Vérifie que la marge n'est pas négative (prix de vente >= prix d'achat)"""
        for product in self:
            if product.price < product.cost:
                raise exceptions.ValidationError(
                    "Le prix de vente ne peut pas être inférieur au prix d'achat. "
                    f"Prix de vente: {product.price}€, Prix d'achat: {product.cost}€"
                )

    def unlink(self):
        """Empêche la suppression des produits utilisés dans des commandes actives"""
        for product in self:
            # Chercher les lignes de commande qui utilisent ce produit
            order_lines = self.env['shop.order.line'].search([
                ('product_id', '=', product.id),
                ('order_id.state', 'not in', ['cancelled', 'done'])
            ])
            if order_lines:
                raise exceptions.ValidationError(
                    f"Impossible de supprimer le produit '{product.name}' car il est utilisé "
                    f"dans {len(order_lines)} ligne(s) de commande active(s)."
                )
        return super().unlink()

    def action_confirm_and_return(self):
        """Confirme le produit et retourne à la liste des produits"""
        self.ensure_one()
        self.state = 'confirmed'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'shop.product',
            'view_mode': 'list,kanban,form',
            'target': 'current',
        }
