# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    margin = fields.Float(string='Margin %', related='categ_id.margin', help="Product base price = Margin'%'*cost price")
    base_price = fields.Monetary(string='Sale Base Price', compute='_compute_product_base_price',
                                                        digits='Product Price')

    @api.depends('margin', 'standard_price')
    def _compute_product_base_price(self):
        for product in self:
            product.base_price = product.standard_price + (product.standard_price*product.margin/100) or product.lst_price

    # @api.onchange('categ_id')
    # def onchange_categ_id(self):
    #     if self.categ_id:
    #         self.margin = self.categ_id.margin

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # def _default_margin(self):
    #     return self.product_tmpl_id and self.product_tmpl_id.margin

    margin = fields.Float(string='Margin %', related='categ_id.margin', help="Product base price = Margin'%'*cost price")
    base_price = fields.Monetary(string='Sale Base Price', compute='_compute_product_base_price',
                                                        digits='Product Price')

    @api.depends('margin', 'standard_price')
    def _compute_product_base_price(self):
        for product in self:
            product.base_price = product.standard_price + (product.standard_price*product.margin/100) or product.list_price

    # @api.onchange('categ_id')
    # def onchange_categ_id(self):
    #     if self.categ_id:
    #         self.margin = self.categ_id.margin

class ProductCategory(models.Model):
    _inherit = 'product.category'

    margin = fields.Float(string='Margin %', help="Product base price = Margin'%'*cost price")