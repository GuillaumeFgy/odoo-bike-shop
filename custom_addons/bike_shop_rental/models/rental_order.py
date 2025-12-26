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
    
    # ✅ CORRECTION #1: Email en champ normal (pas related)
    partner_phone = fields.Char(string='Téléphone')
    partner_email = fields.Char(string='Email', size=254)

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
    
    # ✅ CORRECTION #2: Format durée lisible
    duration_display = fields.Char(
        string='Durée',
        compute='_compute_duration_display',
        store=False
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

    # ✅ CORRECTION #3: Séparer facture et note de crédit
    invoice_id = fields.Many2one(
        'account.move',
        string='Facture',
        readonly=True,
        copy=False
    )
    credit_note_id = fields.Many2one(
        'account.move',
        string='Note de Crédit (Avoir)',
        readonly=True,
        copy=False
    )
    invoice_status = fields.Selection([
        ('no', 'Rien à Facturer'),
        ('to_invoice', 'À Facturer'),
        ('invoiced', 'Facturé'),
        ('refunded', 'Remboursé'),
    ], string='Statut Facturation', default='no', compute='_compute_invoice_status', store=True)

    # Notes
    notes = fields.Text(string='Notes')
    damage_report = fields.Text(string='Rapport de Dommages')

    # ==================== ONCHANGE ====================
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """Pré-remplit les informations du client (mais restent modifiables)"""
        if self.partner_id:
            self.partner_email = self.partner_id.email
            self.partner_phone = self.partner_id.phone
        else:
            self.partner_email = False
            self.partner_phone = False

    # ==================== COMPUTE METHODS ====================
    
    @api.depends('state', 'invoice_id', 'credit_note_id')
    def _compute_invoice_status(self):
        """Calcule le statut de facturation"""
        for record in self:
            if record.credit_note_id:
                record.invoice_status = 'refunded'
            elif record.invoice_id:
                record.invoice_status = 'invoiced'
            elif record.state == 'done':
                record.invoice_status = 'to_invoice'
            else:
                record.invoice_status = 'no'

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

    @api.depends('start_date', 'end_date')
    def _compute_duration_display(self):
        """Formate la durée pour un affichage lisible (ex: 2 jours 5 heures)"""
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                total_seconds = delta.total_seconds()
                
                # Calculer jours, heures, minutes
                days = int(total_seconds // 86400)  # 86400 sec = 1 jour
                remaining_seconds = total_seconds % 86400
                hours = int(remaining_seconds // 3600)
                minutes = int((remaining_seconds % 3600) // 60)
                
                # Formater selon la durée
                parts = []
                
                if days > 0:
                    parts.append("%d jour%s" % (days, 's' if days > 1 else ''))
                
                if hours > 0:
                    parts.append("%d heure%s" % (hours, 's' if hours > 1 else ''))
                
                if days == 0 and hours == 0 and minutes > 0:
                    parts.append("%d minute%s" % (minutes, 's' if minutes > 1 else ''))
                
                record.duration_display = ' '.join(parts) if parts else '0 minute'
            else:
                record.duration_display = 'Non défini'

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

    # ==================== CONSTRAINTS ====================
    
    @api.constrains('start_date', 'end_date')
    def _check_rental_dates(self):
        """
        ✅ CORRECTION #4: Validation complète des dates
        Vérifie que les dates de location sont cohérentes
        """
        for record in self:
            if record.end_date and record.start_date:
                # Vérification 1 : Date fin > Date début
                if record.end_date <= record.start_date:
                    raise exceptions.ValidationError(
                        "❌ Erreur de dates !\n\n"
                        "La date de fin (%s) doit être APRÈS la date de début (%s)." % (
                            record.end_date.strftime('%d/%m/%Y à %H:%M'),
                            record.start_date.strftime('%d/%m/%Y à %H:%M')
                        )
                    )
                
                # Vérification 2 : Pas de chevauchement avec d'autres locations
                overlapping = self.env['rental.order'].search([
                    ('bike_id', '=', record.bike_id.id),
                    ('id', '!=', record.id),
                    ('state', 'in', ['confirmed', 'ongoing']),
                    '|',
                        '&', ('start_date', '<=', record.start_date), ('end_date', '>', record.start_date),
                        '&', ('start_date', '<', record.end_date), ('end_date', '>=', record.end_date),
                ])
                
                if overlapping:
                    raise exceptions.ValidationError(
                        "❌ Conflit de réservation !\n\n"
                        "Le vélo '%s' est déjà réservé pour la période du %s au %s.\n\n"
                        "Contrat existant : %s\n"
                        "Période : du %s au %s" % (
                            record.bike_id.name,
                            record.start_date.strftime('%d/%m/%Y %H:%M'),
                            record.end_date.strftime('%d/%m/%Y %H:%M'),
                            overlapping[0].name,
                            overlapping[0].start_date.strftime('%d/%m/%Y %H:%M'),
                            overlapping[0].end_date.strftime('%d/%m/%Y %H:%M')
                        )
                    )

    # ==================== CRUD ====================
    
    @api.model_create_multi
    def create(self, vals_list):
        """Génère automatiquement le numéro de contrat"""
        for vals in vals_list:
            if vals.get('name', 'Nouveau') == 'Nouveau':
                vals['name'] = self.env['ir.sequence'].next_by_code('rental.order') or 'Nouveau'
        return super(RentalOrder, self).create(vals_list)

    # ==================== ACTIONS ====================
    
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
        """
        ✅ CORRECTION #5: Facture UNIQUEMENT au retour du vélo
        Crée une facture client (type 'out_invoice')
        """
        self.ensure_one()
        
        # Vérification CRITIQUE : Location terminée
        if self.state != 'done':
            raise exceptions.UserError(
                "⚠️ Impossible de créer une facture !\n\n"
                "Vous devez d'abord terminer la location (retour du vélo).\n\n"
                "État actuel : %s\n"
                "Action requise : Cliquez sur 'Terminer la Location'" % 
                dict(self._fields['state'].selection).get(self.state)
            )
        
        # Vérifier qu'une facture n'existe pas déjà
        if self.invoice_id:
            raise exceptions.UserError(
                "Une facture existe déjà pour cette location.\n\n"
                "Facture : %s\n"
                "Date : %s" % (
                    self.invoice_id.name,
                    self.invoice_id.invoice_date.strftime('%d/%m/%Y') if self.invoice_id.invoice_date else 'Non datée'
                )
            )

        # Créer la facture client
        invoice_vals = {
            'move_type': 'out_invoice',  # FACTURE CLIENT
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': 'Location %s - %s (du %s au %s)' % (
                    self.bike_id.name,
                    self.name,
                    self.start_date.strftime('%d/%m/%Y'),
                    self.actual_return_date.strftime('%d/%m/%Y') if self.actual_return_date else self.end_date.strftime('%d/%m/%Y')
                ),
                'quantity': 1,
                'price_unit': self.subtotal,
            })],
        }
        
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture Client',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_create_credit_note(self):
        """
        ✅ CORRECTION #6: Créer une note de crédit (AVOIR)
        Sépare clairement facture (out_invoice) et avoir (out_refund)
        """
        self.ensure_one()
        
        # Vérifier qu'une facture existe
        if not self.invoice_id:
            raise exceptions.UserError(
                "⚠️ Impossible de créer une note de crédit !\n\n"
                "Vous devez d'abord créer une facture.\n"
                "Action requise : Cliquez sur 'Créer Facture'"
            )
        
        # Vérifier qu'une note de crédit n'existe pas déjà
        if self.credit_note_id:
            raise exceptions.UserError(
                "Une note de crédit existe déjà.\n\n"
                "Note de crédit : %s\n"
                "Date : %s" % (
                    self.credit_note_id.name,
                    self.credit_note_id.invoice_date.strftime('%d/%m/%Y') if self.credit_note_id.invoice_date else 'Non datée'
                )
            )

        # Créer la note de crédit (AVOIR)
        credit_note_vals = {
            'move_type': 'out_refund',  # NOTE DE CRÉDIT (AVOIR)
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'reversed_entry_id': self.invoice_id.id,  # Lien avec la facture d'origine
            'invoice_line_ids': [(0, 0, {
                'name': 'Remboursement - Location %s - %s' % (
                    self.bike_id.name,
                    self.name
                ),
                'quantity': 1,
                'price_unit': self.subtotal,
            })],
        }
        
        credit_note = self.env['account.move'].create(credit_note_vals)
        self.credit_note_id = credit_note.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Note de Crédit (Avoir)',
            'res_model': 'account.move',
            'res_id': credit_note.id,
            'view_mode': 'form',
            'target': 'current',
        }