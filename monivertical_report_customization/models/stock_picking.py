# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    sunat_operation_type = fields.Char('Tipo de Producto')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    doc_number = fields.Char('Doc Number')
    driver_id = fields.Many2one('stock.picking.driver', string="Picking Driver")
    partner_shipping_id = fields.Many2one('res.partner')
