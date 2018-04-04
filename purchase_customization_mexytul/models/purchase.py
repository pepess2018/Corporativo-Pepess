# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    qty_of_product = fields.Float(string="Quantity of Product", help="Inputted by the client(A15)")
    product_name_id = fields.Many2one('product.product', string="Product Name", help="""Inputted by the client- \n
                                         If the particular product is not supplied by this vendor and has no vendor pricelist defined for this combination. \n
                                         It should give warning message: 'This product cannot be purchased from the selected Vendor' (B15)""")
    # ------------------------------------------------
    # => After this all the fields are Computed Field:
    # ------------------------------------------------
    unit_cost_usd = fields.Float(string="Unit Cost(USD)", help="Unit Cost(USD) = Unit Cost of the product by Vendor- This will be taken from the pricelist(C15)")
    total_cost_usd = fields.Float(string="Total Cost(USD)", help="Total Cost(USD) = Unit Cost(USD)* Quantity of Product(D15=C15*A15)")
    other_costs_usd = fields.Float(string="Other Costs(USD)", help="""Other Costs(USD) = Shows the Cost of the Product with all possible vendor so for example: 
                                                        By Vendor A- 9.5 USD for Vendor B-7.5 USD and so on. 
                                                        This can be a text field showing Price per all possible vendor. (E15)""")

    unit_volume = fields.Float(string="Unit Volume", help="Unit Volume - Taken from the Product form in cubic meter(F15)")
    total_volume = fields.Float(string="Total Volume", help="Total Volume - Unit Volume* Quantity (G15= F15*A15)")

    unit_ocean_freight_usd = fields.Float(string="Unit Ocean Freight(USD)", help="Unit Ocean Freight(USD) - (Ocean freight cost/total container cost) *unit volume (H15= B6/ (Volume of Container in m3)*F15")
    unit_truck_freight_usd = fields.Float(string="Unit Truck Freight(USD)", help="Unit Truck Freight(USD) - (Truck freight cost/exchange rate/total container cost) *unit volume (I15= (B7/A15)/ Volume of Container in m3*F15)")
    total_freight_cost_usd = fields.Float(string="Total Freight Cost(USD)", help="Total Freight Cost(USD) - (Unit ocean freight+ unit truck freight) * qty (J15 = H15+I15*A15)")

    unit_cost_mxn = fields.Float(string="Unit Cost(MXN)", help="Unit Cost(MXN)- Unit cost(USD)*exchange rate(K15=C15*A15)")
    total_cost_mxn= fields.Float(string="Total Cost(MXN)", help="Total Cost(MXN)- Unit Cost(MXN)*Qty(L15=K15*A15)")

    unit_ocean_freight_mxn = fields.Float(string="Unit Ocean Freight(MXN)", help="Unit Ocean Freight(MXN)- Unit ocean freight(USD)*exchange rate(M15=H15*A15)")
    unit_truck_freight_mxn = fields.Float(string="Unit Truck Freight(MXN)", help="Unit Truck Freight(MXN)- Unit truck freight(USD)*exchange rate (N15= I15*A15)")
    total_freight_cost_mxn = fields.Float(string="Total Freight Cost(MXN)", help="Total Freight Cost(MXN)- (Unit ocean freight(MXN)+unit truck freight(MXN)) *qty (P15=M15+N15*A15)")

    unit_freight_cost_mxn = fields.Float(string="Unit Freight Cost(MXN)", help="Unit Freight Cost(MXN)- Unit ocean freight(MXN)+unit truck freight(MXN) (O15=M15+N15)")
    unit_customs_agent_mxn = fields.Float(string="Unit Customs Agent(MXN)", help="Unit Customs Agent(MXN)- (Customs Agent Cost /total container cost) *unit volume (Q15=(B10/Volume of Container in m3)*F15)")
    
    total_customs_agent_mxn = fields.Float(string="Total Custom Agent(MXN)", help="Total Custom Agent(MXN)- Unit Customs Agent(MXN)* qty(R15=Q15*A15)")
    igi_mxn = fields.Float(string="IGI (MXN)", help="IGI(MXN)- (unit cost(MXN)+unit ocean freight(MX)) *IGI%(T15=(K15+M15)*(S15/100))")
 
    sum_cost_before_tax = fields.Float(string="Sum of Costs before Taxes(MXN)", help="Sum of Costs before Taxes(MXN)- Unit Cost(MXN)+Unit Ocean Freight(MXN )(U15= K15+M15)")
    dta_factor = fields.Float(string="DTA Factor", help="DTA Factor-Sum of Costs before Taxes(MXN) * DTA factor (V15= U15*B9)")
    unit_sum_cost_mxn = fields.Float(string="Unit Sum Cost(MXN)", help="Unit Sum Cost(MXN)- Unit Cost(MXN) + Unit Freight Cost(MXN)+Unit Customs Agent(MXN)+ IGI(MXN)+DTA Factor (W15= K15+O15+T15+V15+Q15)")

    total_sum_cost_mxn = fields.Float(string="Total Sum Cost(MXN)", help="Total Sum Cost(MXN)- Sum of Costs before Taxes(MXN)*Qty (X15= U15*A15)")
    price_list_mxn = fields.Float(string="Price list(MXN)", help="Price list(MXN)- The Sale Price of product on Product form(Y15))")
    minimum_price_mxn = fields.Float(string="Minimum Price(MXN)", help="Minimum Price(MXN)- This the the field base price on the product form this is the part of earlier sales dev request(Z15)")

    margin_prctge = fields.Float(string="Minimum Price(MXN)", help="% Margin- (Minimum Price(MXN)*100)/ (Sum of Costs before Taxes(MXN)-100) (AA15= =Z15*100/U15-100)")
    margin_diff_prctge = fields.Float(string="Minimum Difference Price(MXN)", help="% Margin Difference- Difference between Margin '%' and 35% (target margin) (AB15= =(35-AA15))") 

    target_price_usd = fields.Float(string="Target Price(USD)", help="Target Price(USD)- Unit cost(USD)-% margin difference (AC15=(C15-AB15%)")
