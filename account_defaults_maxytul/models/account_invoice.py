# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.addons.account.models.account_invoice import TYPE2JOURNAL
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def default_get(self, default_fields):
        res = super(AccountInvoice, self).default_get(default_fields)
        if res.get('purchase_id', False) and res.get('type', False) == 'in_invoice':
            purchase_order = self.env['purchase.order'].browse(res['purchase_id'])
            if purchase_order.picking_type_id and purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id:
                print(purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id.name)
                res['journal_id'] = purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id.id
        return res

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.env.context.get('default_purchase_id', False):
            purchase_order = self.env['purchase.order'].browse(self.env.context['default_purchase_id'])
            if self.type == 'in_invoice' and purchase_order.picking_type_id:
                if purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id:
                    self.journal_id = purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id
        return res

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        sale_line_ids = invoice.invoice_line_ids.mapped('sale_line_ids')
        purchase_line_ids = invoice.invoice_line_ids.mapped('purchase_line_id')
        journal_inv_mapping = {
            'in_invoice': 'in_refund_journal_id',
            'out_invoice': 'out_refund_journal_id',
        }
        if sale_line_ids and sale_line_ids.ids:
            warehouse = sale_line_ids.mapped('order_id.warehouse_id')[0]
            if getattr(warehouse, journal_inv_mapping[invoice.type], False):
                journal_id = getattr(warehouse, journal_inv_mapping[invoice.type]).id
        if purchase_line_ids and purchase_line_ids.ids:
            purchase_id = purchase_line_ids.mapped('order_id')[0]
            warehouse = purchase_id.picking_type_id.warehouse_id
            if getattr(warehouse, journal_inv_mapping[invoice.type], False):
                journal_id = getattr(warehouse, journal_inv_mapping[invoice.type]).id
        return super(AccountInvoice, self)._prepare_refund(invoice, date_invoice=date_invoice, date=date, description=description, journal_id=journal_id)
