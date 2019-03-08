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
                if purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id.expense_account_id:
                    self.invoice_line_ids.update({'account_id': purchase_order.picking_type_id.warehouse_id.in_invoice_journal_id.expense_account_id.id})
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
        values = super(AccountInvoice, self)._prepare_refund(invoice, date_invoice=date_invoice, date=date, description=description, journal_id=journal_id)
        # inv_journal = self.env['account.journal'].browse(values['journal_id'])
        for inv_line in values['invoice_line_ids']:
            inv_line_values = inv_line[2]
            inv_line_values['account_id'] = self.env['account.invoice.line'].with_context({'type': values['type'], 'journal_id': values['journal_id']})._default_account()
            # if inv_journal.income_account_id and inv_line_acc == inv_journal.income_account_id.id:
            #     inv_line_values['account_id'] = inv_journal.expense_account_id and inv_journal.expense_account_id.id or inv_line_acc
            # elif inv_journal.expense_account_id and inv_line_acc == inv_journal.expense_account_id.id:
            #     inv_line_values['account_id'] = inv_journal.income_account_id and inv_journal.income_account_id.id or inv_line_acc
        return values


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.model
    def _default_account(self):
        if self._context.get('journal_id'):
            journal = self.env['account.journal'].browse(self._context.get('journal_id'))
            if self._context.get('type') in ('out_invoice', 'in_refund'):
                return journal.income_account_id and journal.income_account_id.id or journal.default_credit_account_id.id
            return journal.expense_account_id and journal.expense_account_id.id or journal.default_debit_account_id.id
