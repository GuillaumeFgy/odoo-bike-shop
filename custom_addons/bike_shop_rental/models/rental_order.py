# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class RentalOrder(models.Model):
    """Contrat de location de vélo"""
    _name = 'rental.order'
    _description = 'Contrat de Location'
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Numéro', required=True, copy=False, readonly=True, default='Nouveau')

    # Client
    partner_id = fields.Many2one('res.partner', string='Client', required=True)
    partner_phone = fields.Char(string='Téléphone')
    partner_email = fields.Char(string='Email')

    # Vélo
    bike_id = fields.Many2one('bike.bike', string='Vélo', required=True, domain="[('state', '=', 'available')]")
    bike_category = fields.Char(related='bike_id.category_id.name', string='Catégorie', store=True)

    # Période de location
    start_date = fields.Datetime(string='Date de Début', required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(string='Date de Fin', required=True)
    actual_return_date = fields.Datetime(string='Date de Retour Réelle')

    # Durée
    duration_hours = fields.Float(string='Durée (Heures)', compute='_compute_duration', store=True)
    duration_days = fields.Float(string='Durée (Jours)', compute='_compute_duration', store=True)

    # Tarification
    rental_type = fields.Selection([
        ('hourly', 'Horaire'),
        ('daily', 'Journalier'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
    ], string='Type', required=True, default='daily')

    unit_price = fields.Float(string='Prix Unitaire (€)', compute='_compute_unit_price', store=True, readonly=False)
    quantity = fields.Float(string='Quantité', compute='_compute_quantity', store=True)
    subtotal = fields.Float(string='Sous-total (€)', compute='_compute_subtotal', store=True)
    total_amount = fields.Float(string='Total (€)', compute='_compute_subtotal', store=True)

    # État
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('ongoing', 'En Cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True)

    # Notes
    notes = fields.Text(string='Notes')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Pré-remplit les informations du client"""
        if self.partner_id:
            self.partner_email = self.partner_id.email
            self.partner_phone = self.partner_id.phone

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """Calcule la durée en heures et en jours"""
        for rental in self:
            if rental.start_date and rental.end_date:
                delta = rental.end_date - rental.start_date
                rental.duration_hours = delta.total_seconds() / 3600
                rental.duration_days = delta.total_seconds() / 86400
            else:
                rental.duration_hours = 0
                rental.duration_days = 0

    @api.depends('bike_id', 'rental_type')
    def _compute_unit_price(self):
        """Récupère le prix unitaire selon le type de location"""
        for rental in self:
            if rental.bike_id:
                if rental.rental_type == 'hourly':
                    rental.unit_price = rental.bike_id.hourly_rate
                elif rental.rental_type == 'daily':
                    rental.unit_price = rental.bike_id.daily_rate
                elif rental.rental_type == 'weekly':
                    rental.unit_price = rental.bike_id.weekly_rate
                elif rental.rental_type == 'monthly':
                    rental.unit_price = rental.bike_id.monthly_rate
            else:
                rental.unit_price = 0

    @api.depends('rental_type', 'duration_hours', 'duration_days')
    def _compute_quantity(self):
        """Calcule la quantité selon le type de location"""
        for rental in self:
            if rental.rental_type == 'hourly':
                rental.quantity = rental.duration_hours
            elif rental.rental_type == 'daily':
                rental.quantity = max(1, round(rental.duration_days, 0))
            elif rental.rental_type == 'weekly':
                rental.quantity = max(1, round(rental.duration_days / 7, 1))
            elif rental.rental_type == 'monthly':
                rental.quantity = max(1, round(rental.duration_days / 30, 1))
            else:
                rental.quantity = 1

    @api.depends('unit_price', 'quantity')
    def _compute_subtotal(self):
        """Calcule le total"""
        for rental in self:
            rental.subtotal = rental.unit_price * rental.quantity
            rental.total_amount = rental.subtotal

    @api.constrains('start_date', 'end_date')
    def _check_rental_dates(self):
        """Vérifie que les dates sont cohérentes"""
        for record in self:
            if record.end_date and record.start_date:
                if record.end_date <= record.start_date:
                    raise exceptions.ValidationError("La date de fin doit être après la date de début.")

    @api.model_create_multi
    def create(self, vals_list):
        """Génère automatiquement le numéro de contrat"""
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('rental.order') or 'Nouveau'
        return super(RentalOrder, self).create(vals_list)

    def action_confirm(self):
        """Confirme la location"""
        for rental in self:
            if rental.state == 'draft':
                rental.state = 'confirmed'

    def action_start_rental(self):
        """Démarre la location"""
        for rental in self:
            if rental.state == 'confirmed':
                rental.state = 'ongoing'
                rental.bike_id.state = 'rented'

    def action_end_rental(self):
        """Termine la location"""
        for rental in self:
            if rental.state == 'ongoing':
                rental.state = 'done'
                rental.actual_return_date = fields.Datetime.now()
                rental.bike_id.state = 'available'

    def action_cancel(self):
        """Annule la location"""
        for rental in self:
            if rental.state in ['draft', 'confirmed']:
                rental.state = 'cancelled'
