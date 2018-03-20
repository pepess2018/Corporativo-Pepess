# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        if not self.user_has_groups("sales_customization_mexytul.group_mexytul_credit_limit"):
            for order in self:
                amount_total = sum(self.search([('partner_id', '=', order.partner_id.id), ('state', '=', 'sale')]).mapped('amount_total'))
                if (order.partner_id.credit_limit - amount_total) < order.amount_total:
                    raise Warning(_("The Selected customer exceeds the credit limit set or have amount due"))
                if order.order_line.filtered(lambda ol: ol.price_unit < (ol.product_id.base_price or 1)):
                    raise Warning(_("The Unit price of one or more product is Zero"))
        return super(SaleOrder, self).action_confirm()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, values):
        if not self.user_has_groups("sales_customization_mexytul.group_mexytul_credit_limit"):
            product_id = self.env['product.product'].browse(int(values['product_id']))
            if values['price_unit'] < (product_id.base_price or 1):
                raise Warning(_("The Unit Price is below the base price"))
        return super(SaleOrderLine, self).create(values)