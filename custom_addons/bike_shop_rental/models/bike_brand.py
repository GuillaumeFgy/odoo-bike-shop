# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BikeBrand(models.Model):
    """Modèle représentant une marque de vélo"""
    _name = 'bike.brand'
    _description = 'Marque de Vélo'
    _order = 'name'

    name = fields.Char(string='Nom de la Marque', required=True, translate=True)
    description = fields.Text(string='Description')
    country = fields.Char(string='Pays d\'Origine')
    website = fields.Char(string='Site Web')
    logo = fields.Binary(string='Logo')
    active = fields.Boolean(string='Actif', default=True)

    # Statistiques
    bike_count = fields.Integer(
        string='Nombre de Vélos',
        compute='_compute_bike_count'
    )

    @api.depends('name')
    def _compute_bike_count(self):
        """Compte le nombre de vélos pour cette marque"""
        for brand in self:
            brand.bike_count = self.env['bike.bike'].search_count([
                ('brand_id', '=', brand.id)
            ])

    def action_view_bikes(self):
        """Ouvre la vue des vélos pour cette marque"""
        return {
            'name': f'Vélos {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'bike.bike',
            'view_mode': 'tree,form',
            'domain': [('brand_id', '=', self.id)],
            'context': {'default_brand_id': self.id}
        }

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'Cette marque existe déjà!')
    ]
