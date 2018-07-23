# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.warehouse_id.out_invoice_journal_id:
            invoice_vals.update({
                'journal_id': self.warehouse_id.out_invoice_journal_id.id
            })
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        invoice_line_values = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.order_id.warehouse_id and self.order_id.warehouse_id.out_invoice_journal_id:
            invoice_account = invoice_line_values['account_id']
            invoice_line_values['account_id'] = self.order_id.warehouse_id.out_invoice_journal_id.income_account_id and self.order_id.warehouse_id.out_invoice_journal_id.income_account_id.id or invoice_account
        return invoice_line_values
