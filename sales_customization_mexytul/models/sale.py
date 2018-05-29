# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        group_mexytul_credit_limit = self.user_has_groups("sales_customization_mexytul.group_mexytul_credit_limit")
        group_system = self.user_has_groups("base.group_system")
        for order in self:
            if not group_mexytul_credit_limit:
                if (order.partner_id.credit  > order.partner_id.credit_limit):
                    raise Warning(_("The Selected customer exceeds the credit limit set or have amount due"))
                if order.order_line.filtered(lambda ol: ol.price_unit < (ol.product_id.base_price) and not ol.is_delivery):
                    raise Warning(_("The Unit price of one or more product is Zero"))
                # if not group_system:
            # I want that if qty is not available in warehouse order cannot be confirmed even Admin user should not be able to confirm the order.
            order.order_line.product_qty_check_availability()
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    base_price = fields.Monetary(string='Sale Base Price', related='product_id.base_price', digits=dp.get_precision('Product Price'), store=True)

    @api.multi
    def product_qty_check_availability(self):
        msg = ''
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for oline in self.filtered(lambda ol: ol.product_id.type == 'product'):
            product = oline.product_id.with_context(warehouse=oline.order_id.warehouse_id.id)
            product_qty = oline.product_uom._compute_quantity(oline.product_uom_qty, oline.product_id.uom_id)
            if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
                is_available = oline._check_routing()
                if not is_available:
                    title = 'Not enough inventory!'
                    message = 'You plan to sell %s %s but you only have %s %s available in %s warehouse.' % \
                            (oline.product_uom_qty, oline.product_uom.name, product.virtual_available, product.uom_id.name, oline.order_id.warehouse_id.name)
                    msg = _("Sale Cannot be confirmed \n \n %s Has %s \n \n %s" % (oline.product_id.name, title, message))
                    break
        if not msg:
            return True
        raise Warning(msg)

    @api.one
    @api.constrains('price_unit', 'base_price')
    def validate_prices(self):
        if not self.user_has_groups("sales_customization_mexytul.group_mexytul_credit_limit") and self.filtered(lambda ol: ol.price_unit < ol.product_id.base_price and not self.is_delivery):
            raise Warning(_("The Products : {} has the Unit Price less than the Base Sale Price.".format(", ".join([ ol.product_id.name for ol in self.filtered(lambda ol: ol.price_unit < ol.product_id.base_price)]))))
