# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    out_invoice_journal_id = fields.Many2one(comodel_name='account.journal', string="Customer invoice journal")
    out_refund_journal_id = fields.Many2one(comodel_name='account.journal', string="Customer credit note journal")
    in_invoice_journal_id = fields.Many2one(comodel_name='account.journal', string="Vendor bill journal")
    in_refund_journal_id = fields.Many2one(comodel_name='account.journal', string="Vendor credit note journal")
    stock_valuation_account_id = fields.Many2one(comodel_name='account.account', string="Stock valuation account")
    valuation_in_account_id = fields.Many2one(
        'account.account', 'Stock Input Account',
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)],
        help="Used for real-time inventory valuation. When set on a warehouse, "
             "this account will be used to hold the value of products being moved from an internal location "
             "into this location, instead of the generic Stock Output Account set on the product. "
             "This has no effect for internal locations.")
    valuation_out_account_id = fields.Many2one(
        'account.account', 'Stock Output Account',
        domain=[('internal_type', '=', 'other'), ('deprecated', '=', False)],
        help="Used for real-time inventory valuation. When set on a warehouse, "
             "this account will be used to hold the value of products being moved out of this location "
             "and into an internal location, instead of the generic Stock Output Account set on the product. "
             "This has no effect for internal locations.")


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _get_accounting_data_for_valuation(self):
        journal_id, acc_src, acc_dest, acc_valuation = super(StockMove, self)._get_accounting_data_for_valuation()
        if self.warehouse_id.stock_valuation_account_id:
            acc_valuation = self.warehouse_id.stock_valuation_account_id.id
        if self.warehouse_id.valuation_out_account_id:
            acc_dest = self.warehouse_id.valuation_out_account_id.id
        if self.warehouse_id.valuation_in_account_id:
            acc_src = self.warehouse_id.valuation_in_account_id.id
        return journal_id, acc_src, acc_dest, acc_valuation
