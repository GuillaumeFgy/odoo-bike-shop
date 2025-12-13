# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RentalReport(models.Model):
    """Rapport d'analyse des locations"""
    _name = 'rental.report'
    _description = 'Rapport de Location'
    _auto = False
    _order = 'start_date desc'

    name = fields.Char(string='Numéro de Contrat', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Client', readonly=True)
    bike_id = fields.Many2one('bike.bike', string='Vélo', readonly=True)
    bike_category_id = fields.Many2one('bike.category', string='Catégorie', readonly=True)
    start_date = fields.Datetime(string='Date de Début', readonly=True)
    end_date = fields.Datetime(string='Date de Fin', readonly=True)
    rental_type = fields.Selection([
        ('hourly', 'Horaire'),
        ('daily', 'Journalier'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
    ], string='Type de Location', readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('ongoing', 'En Cours'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], string='État', readonly=True)
    duration_days = fields.Float(string='Durée (Jours)', readonly=True)
    total_amount = fields.Float(string='Montant Total', readonly=True)
    subtotal = fields.Float(string='Sous-total', readonly=True)

    def init(self):
        """Initialise la vue SQL pour le rapport"""
        self._cr.execute("""
            CREATE OR REPLACE VIEW rental_report AS (
                SELECT
                    ro.id as id,
                    ro.name as name,
                    ro.partner_id as partner_id,
                    ro.bike_id as bike_id,
                    b.category_id as bike_category_id,
                    ro.start_date as start_date,
                    ro.end_date as end_date,
                    ro.rental_type as rental_type,
                    ro.state as state,
                    ro.duration_days as duration_days,
                    ro.total_amount as total_amount,
                    ro.subtotal as subtotal
                FROM rental_order ro
                LEFT JOIN bike_bike b ON ro.bike_id = b.id
            )
        """)


class BikeOccupancyReport(models.Model):
    """Rapport de taux d'occupation des vélos"""
    _name = 'bike.occupancy.report'
    _description = 'Rapport d\'Occupation des Vélos'
    _auto = False

    bike_id = fields.Many2one('bike.bike', string='Vélo', readonly=True)
    bike_category_id = fields.Many2one('bike.category', string='Catégorie', readonly=True)
    total_rentals = fields.Integer(string='Nombre de Locations', readonly=True)
    total_days_rented = fields.Float(string='Total Jours Loués', readonly=True)
    total_revenue = fields.Float(string='Revenu Total', readonly=True)
    avg_rental_duration = fields.Float(string='Durée Moyenne (jours)', readonly=True)

    def init(self):
        """Initialise la vue SQL pour le taux d'occupation"""
        self._cr.execute("""
            CREATE OR REPLACE VIEW bike_occupancy_report AS (
                SELECT
                    row_number() OVER () as id,
                    b.id as bike_id,
                    b.category_id as bike_category_id,
                    COUNT(ro.id) as total_rentals,
                    COALESCE(SUM(ro.duration_days), 0) as total_days_rented,
                    COALESCE(SUM(ro.subtotal), 0) as total_revenue,
                    COALESCE(AVG(ro.duration_days), 0) as avg_rental_duration
                FROM bike_bike b
                LEFT JOIN rental_order ro ON b.id = ro.bike_id
                    AND ro.state IN ('confirmed', 'ongoing', 'done')
                GROUP BY b.id, b.category_id
            )
        """)
