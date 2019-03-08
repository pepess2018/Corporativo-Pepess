# -*- coding: utf-8 -*-

from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_done(self):
        """Override to create auto invoice after delviery of the products
           As the soon as the delivery is validated, it should create a draft invoice with invoiceable lines automatically
           In case there is a return for the delivery then a draft credit note should be automatically created.
        """
        res = super(StockPicking, self).action_done()
        self = self.sudo()
        for picking in self:
            sale_id = picking.sale_id
            if sale_id and sale_id.invoice_status == 'to invoice' and any(l.invoice_status == 'to invoice' for l in sale_id.order_line):
                if sale_id.invoice_count:
                    final = True
                else:
                    final = False
                context = {}
                if any([line.to_refund for line in picking.move_lines]):
                    _type_journal_mapping = {
                        'incoming': 'out_refund_journal_id',
                        'outgoing': 'in_refund_journal_id'
                    }
                    journal_id = getattr(picking.picking_type_id.warehouse_id, _type_journal_mapping[picking.picking_type_code], False)
                    account_id = False
                    if journal_id:
                        if picking.picking_type_code == 'incoming':
                            account_id = journal_id.expense_account_id or journal_id.default_debit_account_id
                        elif picking.picking_type_code == 'outgoing':
                            account_id = journal_id.income_account_id or journal_id.default_credit_account_id
                        context = {
                            'refund_journal_id': journal_id.id,
                        }
                    if account_id:
                        context.update({'ref_inv_acc_id': account_id.id})
                if context:
                    invoice_ids = sale_id.with_context(context).action_invoice_create(final=final)
                else:
                    invoice_ids = sale_id.action_invoice_create(final=final)
                for invoice in self.env['account.invoice'].browse(invoice_ids):
                    invoice.action_invoice_open()
        return res
