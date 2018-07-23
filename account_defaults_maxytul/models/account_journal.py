# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    income_account_id = fields.Many2one("account.account", "Income Account", help="Specify income account you want to hit when \ntransaction done for the warehouse where this journal set")
    expense_account_id = fields.Many2one("account.account", "Expense Account", help="Specify expense account you want to hit when \ntransaction done for the warehouse where this journal set")
