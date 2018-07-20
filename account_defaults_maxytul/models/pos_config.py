# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse served")


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _prepare_invoice(self):
        invoice_data = super(PosOrder, self)._prepare_invoice()
        warehouse_id = self.session_id.config_id.warehouse_id
        type_journal_mapping = {
            'out_invoice': 'out_invoice_journal_id',
            'out_refund': 'out_refund_journal_id'
        }
        if warehouse_id and getattr(warehouse_id, type_journal_mapping[invoice_data['type']], False):
            invoice_data['journal_id'] = getattr(warehouse_id, type_journal_mapping[invoice_data['type']])
        return invoice_data
