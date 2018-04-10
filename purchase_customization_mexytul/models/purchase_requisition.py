# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


# The main Purchase Agreement fields:
class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    # Supplier: Vendor Name is selected. This will be inputted by the Customer. (B3)
    forwarder_id = fields.Many2one('res.partner', string="Forwarder", help="The transport Company Saved as vendor- This will be inputted by the Customer.")
    container_capacity = fields.Char(string="Container Capacity",
                                    help="""This is the capacity of the Container; 
                                    this can be a product like 40 HQ has capacity of 70 cubic meter or 
                                    it can be on the Vendor Level History (Historial De Fletes) as shown as an additional tab on the vendor Form(B5)""")
    # container_capacity = This is the capacity of the Container; this can be a product like 40 HQ has capacity of 70 cubic meter or 
    # it can be on the Vendor Level History (Historial De Fletes) as shown as an additional tab on the vendor Form(B5)
    # Each have a Volume, Total Cost , Ocean Freight and date. (Jigar to see which one is the best)- This will be inputted by the customer 
    # and will be selected on the Purchase agreement)
    ocean_freight_cost = fields.Float(string="Ocean Freight Cost",
                                        help="""taken from the the Vendor History File above which is Costo Maritimo in above screenshot,
                                                selected based on the capacity selected on the History file. (B6)""")
    truck_freight_cost = fields.Float(string="Truck Freight Cost", help="Truck Freight Cost: It is Computed by the Total Cost-Ocean Freight Cost as shown below.(B7)")
    exchange_rate_cost = fields.Float(string="Exchange Rate", help="Exchange Rate: Cost of MXN in USD- This will be inputted by the Customer. (B8)")
    dta_factor = fields.Float(string="DTA Factor", help="DTA Factor: Inputted by the Customer as 0.08 or 0.09. (B9)")
    customs_agent_cost = fields.Float(string="Customs Agent Cost", help="Customs Agent Cost: : This is the cost for custom procedures. This will be inputted by the client. (B10)")
