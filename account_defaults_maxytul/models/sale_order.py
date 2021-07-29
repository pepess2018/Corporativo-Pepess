# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.warehouse_id.out_invoice_journal_id:
            invoice_vals.update({
                'journal_id': self.warehouse_id.out_invoice_journal_id.id
            })
        if self.env.context.get('refund_journal_id'):
            invoice_vals.update({
                'journal_id': self.env.context['refund_journal_id'],
            })
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **qty):
        invoice_line_values = super(SaleOrderLine, self)._prepare_invoice_line(**qty)
        print(invoice_line_values,'\n\n\n')
        if self.order_id.warehouse_id and self.order_id.warehouse_id.out_invoice_journal_id:
            product = self.product_id.with_company(self.company_id.id)
            account = product.property_account_income_id or product.categ_id.property_account_income_categ_id
            invoice_line_values['account_id'] = self.order_id.warehouse_id.out_invoice_journal_id.income_account_id and self.order_id.warehouse_id.out_invoice_journal_id.income_account_id.id or account.id
        if self.env.context.get('ref_inv_acc_id'):
            invoice_line_values['account_id'] = self.env.context['ref_inv_acc_id']
        return invoice_line_values
