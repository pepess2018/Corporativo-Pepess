# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
	_inherit = "res.company"

	sale_template = fields.Selection([('classic', "Clásico"), ('fency', "Lujoso"), ('modern', "Moderno"), ('odoo_standard', "Odoo Standard")], string='Venta', default='odoo_standard')
	custom_footer = fields.Boolean(string="Custom footer", help="Check this to define the report footer manually. Otherwise it will be filled in automatically.", default=True)
