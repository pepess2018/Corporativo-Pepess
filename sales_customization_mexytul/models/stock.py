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
        for picking in self:
            sale_id = picking.sale_id
            if sale_id and sale_id.invoice_status == 'to invoice' and any(l.invoice_status == 'to invoice' for l in sale_id.order_line):
                if sale_id.invoice_count:
                    final = True
                else:
                    final = False
                invoice_ids = sale_id.action_invoice_create(final=final)
                for invoice in self.env['account.invoice'].browse(invoice_ids):
                    invoice.action_invoice_open()
        return res
