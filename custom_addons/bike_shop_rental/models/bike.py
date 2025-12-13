# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Bike(models.Model):
    """Modèle représentant un vélo disponible à la location"""
    _name = 'bike.bike'
    _description = 'Vélo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom/Référence', required=True, tracking=True)
    category_id = fields.Many2one(
        'bike.category',
        string='Catégorie',
        required=True,
        tracking=True
    )
    product_id = fields.Many2one(
        'product.product',
        string='Produit Associé',
        domain=[('type', '=', 'product')],
        help='Produit Odoo associé pour la gestion du stock'
    )

    # Caractéristiques techniques
    brand = fields.Char(string='Marque', tracking=True)
    model = fields.Char(string='Modèle', tracking=True)
    year = fields.Integer(string='Année', tracking=True)
    frame_size = fields.Selection([
        ('xs', 'XS (Extra Small)'),
        ('s', 'S (Small)'),
        ('m', 'M (Medium)'),
        ('l', 'L (Large)'),
        ('xl', 'XL (Extra Large)'),
    ], string='Taille du Cadre')
    color = fields.Char(string='Couleur')
    serial_number = fields.Char(string='Numéro de Série', tracking=True)

    # État et disponibilité
    state = fields.Selection([
        ('available', 'Disponible'),
        ('rented', 'Loué'),
        ('maintenance', 'En Maintenance'),
        ('retired', 'Retiré'),
    ], string='État', default='available', required=True, tracking=True)

    condition = fields.Selection([
        ('new', 'Neuf'),
        ('excellent', 'Excellent'),
        ('good', 'Bon'),
        ('fair', 'Correct'),
        ('poor', 'Mauvais'),
    ], string='Condition', default='good', tracking=True)

    # Tarification (hérite de la catégorie mais peut être personnalisée)
    hourly_rate = fields.Float(
        string='Tarif Horaire (€)',
        compute='_compute_rates',
        store=True,
        readonly=False
    )
    daily_rate = fields.Float(
        string='Tarif Journalier (€)',
        compute='_compute_rates',
        store=True,
        readonly=False
    )
    weekly_rate = fields.Float(
        string='Tarif Hebdomadaire (€)',
        compute='_compute_rates',
        store=True,
        readonly=False
    )
    monthly_rate = fields.Float(
        string='Tarif Mensuel (€)',
        compute='_compute_rates',
        store=True,
        readonly=False
    )

    # Informations complémentaires
    description = fields.Text(string='Description')
    notes = fields.Text(string='Notes Internes')
    image = fields.Binary(string='Photo')

    # Compteurs et statistiques
    rental_count = fields.Integer(
        string='Nombre de Locations',
        compute='_compute_rental_count'
    )
    total_rental_days = fields.Float(
        string='Total Jours Loués',
        compute='_compute_rental_stats'
    )
    last_rental_date = fields.Date(
        string='Dernière Location',
        compute='_compute_rental_stats'
    )

    active = fields.Boolean(string='Actif', default=True)

    @api.depends('category_id.hourly_rate', 'category_id.daily_rate',
                 'category_id.weekly_rate', 'category_id.monthly_rate')
    def _compute_rates(self):
        """Hérite les tarifs de la catégorie si pas personnalisés"""
        for bike in self:
            if bike.category_id:
                if not bike.hourly_rate:
                    bike.hourly_rate = bike.category_id.hourly_rate
                if not bike.daily_rate:
                    bike.daily_rate = bike.category_id.daily_rate
                if not bike.weekly_rate:
                    bike.weekly_rate = bike.category_id.weekly_rate
                if not bike.monthly_rate:
                    bike.monthly_rate = bike.category_id.monthly_rate

    def _compute_rental_count(self):
        """Compte le nombre de locations pour ce vélo"""
        for bike in self:
            bike.rental_count = self.env['rental.order'].search_count([
                ('bike_id', '=', bike.id)
            ])

    def _compute_rental_stats(self):
        """Calcule les statistiques de location"""
        for bike in self:
            rentals = self.env['rental.order'].search([
                ('bike_id', '=', bike.id),
                ('state', 'in', ['confirmed', 'ongoing', 'done'])
            ])
            bike.total_rental_days = sum(rentals.mapped('duration_days'))
            bike.last_rental_date = max(rentals.mapped('start_date')) if rentals else False

    @api.constrains('state', 'condition')
    def _check_state_condition(self):
        """Vérifie que les vélos en mauvais état ne sont pas disponibles"""
        for bike in self:
            if bike.condition == 'poor' and bike.state == 'available':
                raise exceptions.ValidationError(
                    f"Le vélo {bike.name} est en mauvais état et ne peut pas être disponible à la location."
                )

    def action_set_available(self):
        """Marque le vélo comme disponible"""
        self.write({'state': 'available'})

    def action_set_maintenance(self):
        """Envoie le vélo en maintenance"""
        self.write({'state': 'maintenance'})

    def action_view_rentals(self):
        """Ouvre la vue des locations pour ce vélo"""
        return {
            'name': f'Locations de {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'rental.order',
            'view_mode': 'tree,form',
            'domain': [('bike_id', '=', self.id)],
            'context': {'default_bike_id': self.id}
        }

    _sql_constraints = [
        ('serial_number_unique', 'UNIQUE(serial_number)',
         'Le numéro de série doit être unique!')
    ]
