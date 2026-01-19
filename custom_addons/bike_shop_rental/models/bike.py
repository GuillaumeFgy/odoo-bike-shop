# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import base64
import os


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
    image = fields.Binary(string='Photo')

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

    def _get_default_image_for_model(self, model_name, category_name):
        """Retourne une image par défaut basée sur le modèle ou la catégorie du vélo"""
        image_mapping = [
            ('e-bike', 'electric_bike.jpg'),
            ('ebike', 'electric_bike.jpg'),
            ('electric', 'electric_bike.jpg'),
            ('électrique', 'electric_bike.jpg'),
            ('mountain', 'mountain_bike.jpg'),
            ('mtb', 'mountain_bike.jpg'),
            ('vtt', 'mountain_bike.jpg'),
            ('road', 'road_bike.jpg'),
            ('route', 'road_bike.jpg'),
            ('kids', 'kids_bike.jpg'),
            ('enfant', 'kids_bike.jpg'),
            ('city', 'city_bike.jpg'),
            ('ville', 'city_bike.jpg'),
            ('urbain', 'city_bike.jpg'),
        ]

        model_lower = (model_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in model_lower:
                return self._load_default_image(image_file)

        category_lower = (category_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in category_lower:
                return self._load_default_image(image_file)

        return self._load_default_image('default_bike.jpg')

    def _load_default_image(self, image_filename):
        """Charge une image depuis le dossier static/img du module"""
        try:
            module_path = os.path.dirname(os.path.dirname(__file__))
            image_path = os.path.join(module_path, 'static', 'img', image_filename)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as image_file:
                    return base64.b64encode(image_file.read())
        except Exception:
            pass
        return False

    @api.onchange('model', 'category_id')
    def _onchange_model_assign_image(self):
        """Assigne automatiquement une image quand le modèle ou la catégorie change"""
        if self.image and self._origin.id:
            return
        if self.model or self.category_id:
            category_name = self.category_id.name if self.category_id else ''
            default_image = self._get_default_image_for_model(self.model, category_name)
            if default_image:
                self.image = default_image

    @api.model_create_multi
    def create(self, vals_list):
        """Assigne automatiquement une image si aucune n'est fournie"""
        for vals in vals_list:
            if not vals.get('image'):
                model_name = vals.get('model', '')
                category_id = vals.get('category_id')
                category_name = ''
                if category_id:
                    category = self.env['bike.category'].browse(category_id)
                    category_name = category.name if category else ''
                default_image = self._get_default_image_for_model(model_name, category_name)
                if default_image:
                    vals['image'] = default_image
        return super(Bike, self).create(vals_list)

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
