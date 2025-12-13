# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from datetime import timedelta


class RentalOrder(models.Model):
    """Contrat de location de vélo"""
    _name = 'rental.order'
    _description = 'Contrat de Location'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(
        string='Numéro de Contrat',
        required=True,
        copy=False,
        readonly=True,
        default='Nouveau'
    )

    # Client
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True
    )
    partner_phone = fields.Char(related='partner_id.phone', string='Téléphone')
    partner_email = fields.Char(related='partner_id.email', string='Email')

    # Vélo
    bike_id = fields.Many2one(
        'bike.bike',
        string='Vélo',
        required=True,
        tracking=True,
        domain="[('state', '=', 'available')]"
    )
    bike_category = fields.Char(
        related='bike_id.category_id.name',
        string='Catégorie de Vélo',
        store=True
    )

    # Période de location
    start_date = fields.Datetime(
        string='Date de Début',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    end_date = fields.Datetime(
        string='Date de Fin',
        required=True,
        tracking=True
    )
    actual_return_date = fields.Datetime(
        string='Date de Retour Réelle',
        tracking=True
    )

    # Durée
    duration_hours = fields.Float(
        string='Durée (Heures)',
        compute='_compute_duration',
        store=True
    )
    duration_days = fields.Float(
        string='Durée (Jours)',
        compute='_compute_duration',
        store=True
    )

    # Type de location et tarification
    rental_type = fields.Selection([
        ('hourly', 'Horaire'),
        ('daily', 'Journalier'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
    ], string='Type de Location', required=True, default='daily', tracking=True)

    unit_price = fields.Float(
        string='Prix Unitaire (€)',
        compute='_compute_unit_price',
        store=True,
        readonly=False
    )
    quantity = fields.Float(
        string='Quantité',
        compute='_compute_quantity',
        store=True
    )
    subtotal = fields.Float(
        string='Sous-total (€)',
        compute='_compute_subtotal',
        store=True
    )
    deposit_amount = fields.Float(
        string='Caution (€)',
        default=100.0,
        tracking=True
    )
    total_amount = fields.Float(
        string='Total (€)',
        compute='_compute_total',
        store=True
    )

    # État du contrat
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('ongoing', 'En Cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True, tracking=True)

    # Facturation
    invoice_id = fields.Many2one(
        'account.move',
        string='Facture',
        readonly=True
    )
    invoice_status = fields.Selection([
        ('not_invoiced', 'Non Facturé'),
        ('invoiced', 'Facturé'),
        ('paid', 'Payé'),
    ], string='État de Facturation', default='not_invoiced', tracking=True)

    # Notes
    notes = fields.Text(string='Notes')
    damage_report = fields.Text(string='Rapport de Dommages')

    @api.model_create_multi
    def create(self, vals_list):
        """Génère automatiquement le numéro de contrat"""
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('rental.order') or 'Nouveau'
        return super(RentalOrder, self).create(vals_list)

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
        """Calcule le sous-total"""
        for rental in self:
            rental.subtotal = rental.unit_price * rental.quantity

    @api.depends('subtotal', 'deposit_amount')
    def _compute_total(self):
        """Calcule le total (incluant la caution)"""
        for rental in self:
            rental.total_amount = rental.subtotal + rental.deposit_amount

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Vérifie que la date de fin est après la date de début"""
        for rental in self:
            if rental.start_date and rental.end_date:
                if rental.end_date <= rental.start_date:
                    raise exceptions.ValidationError(
                        "La date de fin doit être postérieure à la date de début."
                    )

    @api.constrains('bike_id', 'start_date', 'end_date')
    def _check_bike_availability(self):
        """Vérifie que le vélo est disponible pour la période demandée"""
        for rental in self:
            if rental.bike_id and rental.start_date and rental.end_date:
                # Cherche les locations qui se chevauchent
                overlapping = self.search([
                    ('id', '!=', rental.id),
                    ('bike_id', '=', rental.bike_id.id),
                    ('state', 'in', ['confirmed', 'ongoing']),
                    ('start_date', '<', rental.end_date),
                    ('end_date', '>', rental.start_date),
                ])
                if overlapping:
                    raise exceptions.ValidationError(
                        f"Le vélo {rental.bike_id.name} n'est pas disponible pour cette période.\n"
                        f"Conflit avec la location : {overlapping[0].name}"
                    )

    def action_confirm(self):
        """Confirme la location"""
        for rental in self:
            if rental.state == 'draft':
                rental.write({
                    'state': 'confirmed',
                })

    def action_start_rental(self):
        """Démarre la location"""
        for rental in self:
            if rental.state == 'confirmed':
                rental.write({
                    'state': 'ongoing',
                })
                rental.bike_id.write({'state': 'rented'})

    def action_end_rental(self):
        """Termine la location"""
        for rental in self:
            if rental.state == 'ongoing':
                rental.write({
                    'state': 'done',
                    'actual_return_date': fields.Datetime.now(),
                })
                rental.bike_id.write({'state': 'available'})

    def action_cancel(self):
        """Annule la location"""
        for rental in self:
            if rental.state in ['draft', 'confirmed']:
                rental.write({'state': 'cancelled'})

    def action_create_invoice(self):
        """Crée une facture pour la location"""
        self.ensure_one()
        if self.invoice_id:
            raise exceptions.UserError("Une facture a déjà été créée pour cette location.")

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': f'Location {self.bike_id.name} - {self.rental_type}',
                'quantity': self.quantity,
                'price_unit': self.unit_price,
            })],
        })

        self.write({
            'invoice_id': invoice.id,
            'invoice_status': 'invoiced',
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
