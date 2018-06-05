# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.l10n_mx_edi_usage = self.partner_id.l10n_mx_edi_usage

    warehouse_address_id = fields.Many2one(
        'res.partner',
        string='Warehouse Address',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Warehouse address for current invoice.")

    total_products = fields.Integer(compute='_compute_number_of_products', string="Total Products")
    total_lines = fields.Integer(compute='_compute_total_lines', string='Total Lines')
    type_of_voucher = fields.Selection([('ingreso', 'ingreso'), ('egreso', 'egreso')], string="Type of Voucher")
    total_due = fields.Float(compute='_compute_total_due', string="Total Due")

    @api.multi
    def _compute_total_due(self):
        for invoice in self:
            total_due = 0
            for aml in invoice.partner_id.unreconciled_aml_ids:
                amount = aml.currency_id and aml.amount_residual_currency or aml.amount_residual
                total_due += not aml.blocked and amount or 0

            invoice.total_due = total_due

    @api.multi
    def _compute_number_of_products(self):
        for invoice in self:
            invoice.total_products = sum(invoice.invoice_line_ids.mapped('quantity'))

    @api.multi
    def _compute_total_lines(self):
        for invoice in self:
            invoice.total_lines = len(invoice.invoice_line_ids)
