# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    warehouse_address_id = fields.Many2one(
        'res.partner',
        string='Warehouse Address',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Warehouse address for current invoice.")

    total_products = fields.Integer(compute='_compute_number_of_products', string="Total Products")
    total_lines = fields.Integer(compute='_compute_total_lines', string='Total Lines')
    type_of_voucher = fields.Selection([('ingreso', 'ingreso'), ('egreso', 'egreso')], string="Type of Voucher")
    total_due = fields.Monetary(compute='_compute_total_due', string="Total Due")
    balance_expiration = fields.Monetary(compute='_compute_balance_expiration', string="Balance Expiration")
    # payment_method = fields.Selection([
    #     ('01 Efectivo', '01 Efectivo'),
    #     ('02 Cheque', '02 Cheque'),
    #     ('03 Transferencia', '03 Transferencia'),
    #     ('04 Tarjeta de Crédito', '04 Tarjeta de Crédito'),
    #     ('99 Por definir', '99 Por definir')], string="Payment Method")
    payment_method = fields.Selection(related='partner_id.payment_method', string="Payment Method", store=True, readonly=True)

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.l10n_mx_edi_usage = self.partner_id.l10n_mx_edi_usage
            self.payment_method = self.partner_id.payment_method

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

    @api.multi
    def _compute_balance_expiration(self):
        for invoice in self:
            invoice.balance_expiration = invoice.total_due - invoice.amount_total


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    tax_amount = fields.Monetary(compute='_compute_tax_amount', string="Tax Amount", store=True, readonly=True)

    @api.depends('price_total', 'price_subtotal', 'invoice_line_tax_ids')
    def _compute_tax_amount(self):
        for line in self.filtered(lambda ln: ln.invoice_line_tax_ids):
            line.tax_amount =  line.price_total - line.price_subtotal
            # taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
