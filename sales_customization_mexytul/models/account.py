# -*- coding: utf-8 -*-
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id:
            self.l10n_mx_edi_usage = self.partner_id.l10n_mx_edi_usage
