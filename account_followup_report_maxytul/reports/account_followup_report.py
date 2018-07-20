# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools import float_round
from odoo.tools.misc import formatLang, format_date


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def get_columns_name(self, options):
        headers = super(AccountFollowupReport, self).get_columns_name(options)
        headers.extend([
            {'name': _(' Days Expired VS Invoiced Date '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Assigned Fee '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Invoice/Credit Note '), 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Total Invoiced '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Discount '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Total Amount with Discount '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Payments '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'},
            {'name': _(' Balance due '), 'class': 'number', 'style': 'text-align:right; white-space:nowrap;'}
            ])
        return headers

    def get_lines(self, options, line_id=None):
        # Get date format for the lang
        partner = options.get('partner_id') and self.env['res.partner'].browse(options['partner_id']) or False
        if not partner:
            return []
        lang_code = partner.lang or self.env.user.lang or 'en_US'

        lines = []
        res = {}
        today = datetime.today().strftime('%Y-%m-%d')
        line_num = 0
        for l in partner.unreconciled_aml_ids:
            if self.env.context.get('print_mode') and l.blocked:
                continue
            currency = l.currency_id or l.company_id.currency_id
            if currency not in res:
                res[currency] = []
            res[currency].append(l)
        for currency, aml_recs in res.items():
            total = 0
            total_issued = 0
            aml_recs = sorted(aml_recs, key=lambda aml: aml.blocked)
            for aml in aml_recs:
                amount = aml.currency_id and aml.amount_residual_currency or aml.amount_residual
                date_due = format_date(self.env, aml.date_maturity or aml.date, lang_code=lang_code)
                total += not aml.blocked and amount or 0
                is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                is_payment = aml.payment_id
                if is_overdue or is_payment:
                    total_issued += not aml.blocked and amount or 0
                if is_overdue:
                    date_due = {'name': date_due, 'class': 'color-red date', 'style': 'white-space:nowrap;text-align:center;color: red;'}
                if is_payment:
                    date_due = ''
                amount = formatLang(self.env, amount, currency_obj=currency)
                line_num += 1
                pricelist = ''
                public_pricelist = self.env.ref('product.list0', raise_if_not_found=False)
                if aml.invoice_id and public_pricelist:
                    pricelist = _('Public Pricelist') if aml.invoice_id.partner_id.property_product_pricelist == public_pricelist else _('Tarifa de venta')
                # Total invoice imount without discount
                total_invoice = sum([inv_line.quantity * inv_line.price_unit for inv_line in aml.invoice_id.invoice_line_ids])
                total_invoice = total_invoice + aml.invoice_id.amount_tax
                # total discount
                total_discount = sum([inv_line.discount and inv_line.price_unit*(inv_line.discount/100) * inv_line.quantity or 0.00 for inv_line in aml.invoice_id.invoice_line_ids])
                columns = [
                    format_date(self.env, aml.date, lang_code=lang_code),
                    date_due,
                    aml.invoice_id.name or aml.name,
                    aml.expected_pay_date and aml.expected_pay_date + ' ' + aml.internal_note or '',
                    {'name': aml.blocked, 'blocked': aml.blocked},
                    amount,
                    aml.invoice_id and (datetime.strptime(aml.date_maturity, "%Y-%m-%d") - datetime.strptime(aml.invoice_id.date_invoice, "%Y-%m-%d")).days or 0,
                    pricelist,
                    aml.invoice_id.number,
                    self.format_value(total_invoice, currency=currency),
                    self.format_value(total_discount, currency=currency),
                    aml.invoice_id.amount_total,
                    aml.invoice_id.payment_ids and sum(aml.invoice_id.payment_ids.mapped('amount')) or 0.00,
                    amount
                    ]
                if self.env.context.get('print_mode'):
                    columns = columns[:3]+columns[5:]
                lines.append({
                    'id': aml.id,
                    'name': aml.move_id.name,
                    'caret_options': 'followup',
                    'move_id': aml.move_id.id,
                    'type': is_payment and 'payment' or 'unreconciled_aml',
                    'unfoldable': False,
                    'columns': [type(v) == dict and v or {'name': v} for v in columns],
                })
            totalXXX = formatLang(self.env, total, currency_obj=currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': 'total',
                'unfoldable': False,
                'level': 0,
                'columns': [{'name': v} for v in ['']*(10 if self.env.context.get('print_mode') else 12) + [total >= 0 and _('Total Due') or '', totalXXX]],
            })
            if total_issued > 0:
                total_issued = formatLang(self.env, total_issued, currency_obj=currency)
                line_num += 1
                lines.append({
                    'id': line_num,
                    'name': '',
                    'class': 'total',
                    'unfoldable': False,
                    'level': 0,
                    'columns': [{'name': v} for v in ['']*(10 if self.env.context.get('print_mode') else 12) + [_('Total Overdue'), total_issued]],
                })
        return lines
