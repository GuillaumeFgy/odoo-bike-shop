# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import base64
import os


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
    brand_id = fields.Many2one(
        'bike.brand',
        string='Marque',
        tracking=True,
        ondelete='restrict'
    )
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

    def _get_default_image_for_model(self, model_name, category_name):
        """
        Retourne une image par défaut basée sur le modèle ou la catégorie du vélo.

        Args:
            model_name: Nom du modèle (ex: "Mountain X5", "City Commuter")
            category_name: Nom de la catégorie (ex: "VTT", "Vélo de Ville")

        Returns:
            Binary image data or False
        """
        # Mapping des mots-clés vers les noms d'images
        # L'ordre est important : les plus spécifiques en premier (e-bike avant urban)
        image_mapping = [
            # Électrique (priorité haute - à vérifier en premier)
            ('e-bike', 'electric_bike.jpg'),
            ('ebike', 'electric_bike.jpg'),
            ('electric', 'electric_bike.jpg'),
            ('électrique', 'electric_bike.jpg'),

            # Mountain
            ('mountain', 'mountain_bike.jpg'),
            ('mtb', 'mountain_bike.jpg'),
            ('vtt', 'mountain_bike.jpg'),

            # Road
            ('road', 'road_bike.jpg'),
            ('route', 'road_bike.jpg'),

            # Kids
            ('kids', 'kids_bike.jpg'),
            ('enfant', 'kids_bike.jpg'),
            ('junior', 'kids_bike.jpg'),

            # City (moins spécifique - à vérifier en dernier)
            ('city', 'city_bike.jpg'),
            ('ville', 'city_bike.jpg'),
            ('commuter', 'city_bike.jpg'),
            ('urbain', 'city_bike.jpg'),
            ('urban', 'city_bike.jpg'),
        ]

        # Cherche d'abord dans le nom du modèle
        model_lower = (model_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in model_lower:
                return self._load_default_image(image_file)

        # Sinon cherche dans la catégorie
        category_lower = (category_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in category_lower:
                return self._load_default_image(image_file)

        # Image par défaut si rien ne correspond
        return self._load_default_image('default_bike.jpg')

    def _load_default_image(self, image_filename):
        """
        Charge une image depuis le dossier static/img du module.

        Args:
            image_filename: Nom du fichier image

        Returns:
            Binary image data encoded in base64 or False
        """
        try:
            # Chemin vers le dossier static/img du module
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
        """
        Assigne automatiquement une image quand le modèle ou la catégorie change.
        Ne remplace pas l'image si elle a été manuellement définie.
        """
        # Ne pas remplacer une image existante (sauf si c'est une création)
        if self.image and self._origin.id:
            return

        if self.model or self.category_id:
            category_name = self.category_id.name if self.category_id else ''
            default_image = self._get_default_image_for_model(self.model, category_name)
            if default_image:
                self.image = default_image

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create pour assigner automatiquement une image si aucune n'est fournie.
        """
        for vals in vals_list:
            # Si aucune image n'est fournie, en assigner une automatiquement
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

    def action_assign_default_image(self):
        """
        Action pour assigner manuellement l'image par défaut.
        Utile pour mettre à jour les vélos existants.
        """
        for bike in self:
            category_name = bike.category_id.name if bike.category_id else ''
            default_image = bike._get_default_image_for_model(bike.model, category_name)
            if default_image:
                bike.image = default_image
        return True

    _sql_constraints = [
        ('serial_number_unique', 'UNIQUE(serial_number)',
         'Le numéro de série doit être unique!')
    ]
