# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockPickingDriver(models.Model):
    _name = 'stock.picking.driver'

    name = fields.Char(required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', sting="Vehículo")
    carrier_id = fields.Many2one('delivery.carrier', string="Tipo de Distribución")
    company_id = fields.Many2one('res.company', string="Company")
    date_transport = fields.Date('F.Inicio de Transporte')
    partner_id = fields.Many2one('res.partner', string="Conductor")
    picking_ids = fields.One2many('stock.picking', 'driver_id', string="Pickings")
