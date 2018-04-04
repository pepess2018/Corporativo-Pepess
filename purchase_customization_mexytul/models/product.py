# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    importation_tax_igi = fields.Float(string="Importation Tax (IGI%)", help="Importation Tax (IGI%)- This will be a field in the product form which will be inputted by client")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    importation_tax_igi = fields.Float(string="Importation Tax (IGI%)", help="Importation Tax (IGI%)- This will be a field in the product form which will be inputted by client")