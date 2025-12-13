# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BikeCategory(models.Model):
    """Catégorie de vélos (VTT, Route, Électrique, etc.)"""
    _name = 'bike.category'
    _description = 'Catégorie de Vélo'
    _order = 'sequence, name'

    name = fields.Char(string='Nom', required=True, translate=True)
    sequence = fields.Integer(string='Séquence', default=10)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)

    # Tarification par défaut pour cette catégorie
    hourly_rate = fields.Float(string='Tarif Horaire (€)', default=5.0)
    daily_rate = fields.Float(string='Tarif Journalier (€)', default=25.0)
    weekly_rate = fields.Float(string='Tarif Hebdomadaire (€)', default=100.0)
    monthly_rate = fields.Float(string='Tarif Mensuel (€)', default=300.0)

    # Compteurs
    bike_count = fields.Integer(
        string='Nombre de Vélos',
        compute='_compute_bike_count',
        store=True
    )

    @api.depends('name')
    def _compute_bike_count(self):
        """Calcule le nombre de vélos dans cette catégorie"""
        for category in self:
            category.bike_count = self.env['bike.bike'].search_count([
                ('category_id', '=', category.id)
            ])

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Le nom de la catégorie doit être unique!')
    ]
