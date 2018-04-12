# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	print_discount = fields.Boolean(string="Print Discount", default=True)
	print_image = fields.Boolean(string="Print Image", help="If ticked, you can see the product image in report of sale order/quotation", default=True)
	image_sizes = fields.Selection([('image', "Big Size Image"), ('image_small', "Small Size Image"), ('image_medium', "Medium Size Image")], 
		string='Image Size', default='image_medium', help="Image size to be displayed in report")
