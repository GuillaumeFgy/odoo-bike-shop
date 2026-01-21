# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ShopOrder(models.Model):
    """Commande de vente du magasin"""
    _name = 'shop.order'
    _description = 'Commande de Vente'
    _order = 'date desc, id desc'

    name = fields.Char(string='Numéro', required=True, copy=False, readonly=True, default='Nouveau')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)

    # Client
    customer_name = fields.Char(string='Client', required=True)
    customer_phone = fields.Char(string='Téléphone')
    customer_email = fields.Char(string='Email')

    # Lignes de commande
    line_ids = fields.One2many('shop.order.line', 'order_id', string='Lignes')

    # Totaux
    total = fields.Float(string='Total (€)', compute='_compute_total', store=True)

    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True)

    notes = fields.Text(string='Notes')

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for order in self:
            order.total = sum(line.subtotal for line in order.line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('shop.order') or 'Nouveau'
        return super().create(vals_list)

    def action_confirm(self):
        for order in self:
            # Déduire le stock
            for line in order.line_ids:
                if line.product_id:
                    line.product_id.quantity -= line.quantity
            order.state = 'confirmed'

    def action_done(self):
        for order in self:
            order.state = 'done'

    def action_cancel(self):
        for order in self:
            # Remettre le stock si annulé depuis confirmé
            if order.state == 'confirmed':
                for line in order.line_ids:
                    if line.product_id:
                        line.product_id.quantity += line.quantity
            order.state = 'cancelled'

    def action_draft(self):
        for order in self:
            order.state = 'draft'


class ShopOrderLine(models.Model):
    """Ligne de commande"""
    _name = 'shop.order.line'
    _description = 'Ligne de Commande'

    order_id = fields.Many2one('shop.order', string='Commande', required=True, ondelete='cascade')
    product_id = fields.Many2one('shop.product', string='Produit', required=True)
    quantity = fields.Integer(string='Quantité', required=True, default=1)
    unit_price = fields.Float(string='Prix unitaire (€)', required=True)
    subtotal = fields.Float(string='Sous-total (€)', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.price
