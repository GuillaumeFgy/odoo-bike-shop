# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, exceptions


class RentalOrder(models.Model):
    """Contrat de location de vélo"""
    _name = 'rental.order'
    _description = 'Contrat de Location'
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Numéro', required=True, copy=False, readonly=True, default='Nouveau')

    # Client
    partner_id = fields.Many2one('res.partner', string='Client Existant')
    customer_name = fields.Char(string='Nom du Client', compute='_compute_customer_name', store=True, readonly=False)
    partner_phone = fields.Char(string='Téléphone')
    partner_email = fields.Char(string='Email')

    # Vélo
    bike_id = fields.Many2one('bike.bike', string='Vélo', domain="[('state', '=', 'available')]")
    bike_category = fields.Char(related='bike_id.category_id.name', string='Catégorie', store=True)

    # Période de location
    start_date = fields.Datetime(string='Date de Début', default=fields.Datetime.now)
    end_date = fields.Datetime(string='Date de Fin')
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
    ], string='Type', default='daily')

    unit_price = fields.Float(string='Prix Unitaire (€)', compute='_compute_unit_price', store=True, readonly=False)
    quantity = fields.Float(string='Quantité', compute='_compute_quantity', store=True)
    subtotal = fields.Float(string='Sous-total (€)', compute='_compute_subtotal', store=True)
    total_amount = fields.Float(string='Total (€)', compute='_compute_subtotal', store=True)

    # État
    state = fields.Selection([
        ('cancelled', 'Annulé'),
        ('ongoing', 'En Cours'),
        ('confirmed', 'Confirmé'),
        ('done', 'Terminé'),
        ('draft', 'Brouillon'),
    ], string='État', default='draft', required=True)

    # Notes
    notes = fields.Text(string='Notes')

    @api.depends('partner_id')
    def _compute_customer_name(self):
        """Calcule le nom du client depuis partner_id s'il existe"""
        for record in self:
            if record.partner_id and not record.customer_name:
                record.customer_name = record.partner_id.name
            elif not record.customer_name:
                record.customer_name = ''

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Pré-remplit les informations du client"""
        if self.partner_id:
            self.customer_name = self.partner_id.name
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

    @api.constrains('start_date', 'end_date', 'state')
    def _check_rental_dates(self):
        """Vérifie que les dates sont cohérentes (sauf si annulé)"""
        for record in self:
            if record.state != 'cancelled' and record.end_date and record.start_date:
                if record.end_date <= record.start_date:
                    raise exceptions.ValidationError("La date de fin doit être après la date de début.")

    @api.constrains('rental_type', 'start_date', 'end_date', 'state')
    def _check_rental_type_duration(self):
        """Vérifie que le type de location correspond à la durée (sauf si annulé)"""
        for record in self:
            if record.state != 'cancelled' and record.start_date and record.end_date and record.rental_type:
                duration_days = record.duration_days
                # Afficher en jours entiers dans le message
                duration_days_int = int(duration_days)

                if record.rental_type == 'monthly' and duration_days < 30:
                    raise exceptions.ValidationError(
                        "Pour une location mensuelle, la durée doit être d'au moins 30 jours. "
                        f"Durée actuelle : {duration_days_int} jour(s)."
                    )
                elif record.rental_type == 'weekly' and duration_days < 7:
                    raise exceptions.ValidationError(
                        "Pour une location hebdomadaire, la durée doit être d'au moins 7 jours. "
                        f"Durée actuelle : {duration_days_int} jour(s)."
                    )
                elif record.rental_type == 'daily' and duration_days < 1:
                    raise exceptions.ValidationError(
                        "Pour une location journalière, la durée doit être d'au moins 1 jour. "
                        f"Durée actuelle : {duration_days_int} jour(s)."
                    )

    @api.constrains('partner_email', 'state')
    def _check_email(self):
        """Vérifie le format de l'email (sauf si annulé)"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            if record.state != 'cancelled' and record.partner_email and not re.match(email_regex, record.partner_email):
                raise exceptions.ValidationError(
                    f"L'email '{record.partner_email}' n'est pas valide. "
                    "Format attendu : exemple@domaine.com"
                )

    @api.constrains('partner_phone', 'state')
    def _check_phone(self):
        """Vérifie le format du téléphone (sauf si annulé)"""
        # Accepte les formats: +33612345678, 0612345678, +33 6 12 34 56 78, etc.
        phone_regex = r'^(\+\d{1,3}[\s.-]?)?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}$'
        for record in self:
            if record.state != 'cancelled' and record.partner_phone:
                # Enlever les espaces pour vérifier qu'il y a assez de chiffres
                phone_digits = re.sub(r'[^\d]', '', record.partner_phone)
                if len(phone_digits) < 10:
                    raise exceptions.ValidationError(
                        f"Le numéro de téléphone '{record.partner_phone}' n'est pas valide. "
                        "Il doit contenir au moins 10 chiffres."
                    )
                if not re.match(phone_regex, record.partner_phone):
                    raise exceptions.ValidationError(
                        f"Le numéro de téléphone '{record.partner_phone}' n'est pas valide. "
                        "Format attendu : +33612345678 ou 0612345678"
                    )

    @api.constrains('customer_name', 'state')
    def _check_customer_name(self):
        """Vérifie que le nom du client n'est pas vide (sauf si annulé)"""
        for record in self:
            if record.state != 'cancelled':
                if not record.customer_name or not record.customer_name.strip():
                    raise exceptions.ValidationError(
                        "Le nom du client est obligatoire."
                    )
                if len(record.customer_name.strip()) < 2:
                    raise exceptions.ValidationError(
                        "Le nom du client doit contenir au moins 2 caractères."
                    )
                # Vérifier que le nom ne contient pas de chiffres
                if any(char.isdigit() for char in record.customer_name):
                    raise exceptions.ValidationError(
                        f"Le nom du client '{record.customer_name}' n'est pas valide. "
                        "Le nom ne peut pas contenir de chiffres."
                    )

    @api.constrains('bike_id', 'state')
    def _check_bike_id(self):
        """Vérifie qu'un vélo est sélectionné (sauf si annulé)"""
        for record in self:
            if record.state != 'cancelled' and not record.bike_id:
                raise exceptions.ValidationError(
                    "Vous devez sélectionner un vélo."
                )

    @api.constrains('start_date', 'end_date', 'rental_type', 'state')
    def _check_required_fields(self):
        """Vérifie que les champs requis sont remplis (sauf si annulé)"""
        for record in self:
            if record.state != 'cancelled':
                if not record.start_date:
                    raise exceptions.ValidationError(
                        "La date de début est obligatoire."
                    )
                if not record.end_date:
                    raise exceptions.ValidationError(
                        "La date de fin est obligatoire."
                    )
                if not record.rental_type:
                    raise exceptions.ValidationError(
                        "Le type de location est obligatoire."
                    )

    @api.constrains('start_date', 'state')
    def _check_start_date(self):
        """Vérifie que la date de début n'est pas dans le passé pour les nouveaux contrats"""
        for record in self:
            # Seulement pour les nouveaux contrats en brouillon (pas annulés)
            if record.state == 'draft' and record.start_date and record.start_date < fields.Datetime.now():
                raise exceptions.ValidationError(
                    "La date de début ne peut pas être dans le passé."
                )

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
                # Vérifier que le vélo est toujours disponible
                if rental.bike_id.state != 'available':
                    raise exceptions.ValidationError(
                        f"Le vélo '{rental.bike_id.name}' n'est plus disponible. "
                        f"État actuel : {dict(rental.bike_id._fields['state'].selection).get(rental.bike_id.state)}"
                    )
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
