# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    tipo_de_proveedor = fields.Selection([('naviero', "Naviero (Water)"), ('nacional', "Nacional(National)"), ('extranjero', "Extranjero (Other Country)"), ('aduanal', "Aduanal (Custom Agent)")], string="Tipo De Proveedor")
        # Here in the Vendor Form (res.partner there is a field called Tipo De Proveedor which has drop down selection- Naviero (Water), Nacional(National), Extranjero (Other Country),Aduanal (Custom Agent) And History File(discussed in the next point)(B4)
