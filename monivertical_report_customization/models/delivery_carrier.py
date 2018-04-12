# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class DeliveryCarrier(models.Model):
	_inherit = 'delivery.carrier'

	partner_id = fields.Many2one('res.partner', string="Transporter Company")