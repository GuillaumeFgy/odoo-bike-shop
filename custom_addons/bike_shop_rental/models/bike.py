# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Bike(models.Model):
    """Modèle représentant un vélo disponible à la location"""
    _name = 'bike.bike'
    _description = 'Vélo'
    _order = 'name'

    name = fields.Char(string='Nom', required=True)
    category_id = fields.Many2one('bike.category', string='Catégorie', required=True)

    # Caractéristiques
    model = fields.Char(string='Modèle')
    year = fields.Integer(string='Année')
    frame_size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ], string='Taille Cadre')
    color = fields.Char(string='Couleur')
    serial_number = fields.Char(string='Numéro de Série')

    # État et disponibilité
    state = fields.Selection([
        ('available', 'Disponible'),
        ('rented', 'Loué'),
        ('maintenance', 'En Maintenance'),
    ], string='État', default='available', required=True)

    # Tarification (hérite de la catégorie)
    hourly_rate = fields.Float(string='Tarif Horaire (€)', compute='_compute_rates', store=True, readonly=False)
    daily_rate = fields.Float(string='Tarif Journalier (€)', compute='_compute_rates', store=True, readonly=False)
    weekly_rate = fields.Float(string='Tarif Hebdomadaire (€)', compute='_compute_rates', store=True, readonly=False)
    monthly_rate = fields.Float(string='Tarif Mensuel (€)', compute='_compute_rates', store=True, readonly=False)

    # Informations complémentaires
    description = fields.Text(string='Description')

    # Statistiques
    rental_count = fields.Integer(string='Nombre de Locations', compute='_compute_rental_count')

    active = fields.Boolean(string='Actif', default=True)

    @api.depends('category_id.hourly_rate', 'category_id.daily_rate',
                 'category_id.weekly_rate', 'category_id.monthly_rate')
    def _compute_rates(self):
        """Hérite les tarifs de la catégorie"""
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
            bike.rental_count = self.env['rental.order'].search_count([('bike_id', '=', bike.id)])

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
            'view_mode': 'list,form',
            'domain': [('bike_id', '=', self.id)],
        }

    _sql_constraints = [
        ('serial_number_unique', 'UNIQUE(serial_number)', 'Le numéro de série doit être unique!')
    ]
