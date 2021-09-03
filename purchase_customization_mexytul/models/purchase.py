# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

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


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # qty_of_product = fields.Float(string="Quantity of Product", compute="compute_total_cost_usd", store=True, help="Inputted by the client(product_qty)")
    # product_name_id = fields.Many2one('product.product', string="Product Name", compute="compute_total_cost_usd", store=True, help="""Inputted by the client- \n
    #                                      If the particular product is not supplied by this vendor and has no vendor pricelist defined for this combination. \n
    #                                      It should give warning message: 'This product cannot be purchased from the selected Vendor' (B15)""")
    # # ------------------------------------------------
    # # => After this all the fields are Computed Field:
    # # ------------------------------------------------
    # unit_cost_usd = fields.Float(string="Unit Cost(USD)", compute="compute_total_cost_usd", store=True, help="Unit Cost(USD) = Unit Cost of the product by Vendor- This will be taken from the pricelist(C15)")


    total_cost_usd = fields.Float(string="Total Cost(USD)",  compute="compute_total_cost_usd", store=True, help="Total Cost(USD) = Unit Cost(USD)* Quantity of Product(D15=C15*product_qty)")
    other_costs_usd = fields.Char(string="Other Costs(USD)", compute="compute_other_costs_usd", store=True, help="""Other Costs(USD) = Shows the Cost of the Product with all possible vendor so for example: 
                                                        By Vendor A- 9.5 USD for Vendor B-7.5 USD and so on. 
                                                        This can be a text field showing Price per all possible vendor. (E15)""")

    @api.depends('product_id')
    def compute_other_costs_usd(self):
        """Other Costs(USD) = Shows the Cost of the Product with all possible vendor so for example: 
            By Vendor A- 9.5 USD for Vendor B-7.5 USD and so on. 
            This can be a text field showing Price per all possible vendor. (E15)"""
        for rec in self:
            product_data = rec.product_id.variant_seller_ids.read(['name', 'min_qty', 'price'])
            rec.other_costs_usd = product_data and '\n'.join([pd['name'][1]+": "+str(pd['price']) for pd in product_data])

    unit_volume = fields.Float(string="Unit Volume", compute="compute_unit_volume", store=True,
        help="Unit Volume - Taken from the Product form in cubic meter(F15)")

    @api.depends('product_id')
    def compute_unit_volume(self):
        # Unit Volume - Taken from the Product form in cubic meter
        for rec in self:
            rec.unit_volume = rec.product_id.cubic_meter

    total_volume = fields.Float(string="Total Volume", compute="compute_total_volume", store=True,
        help="Total Volume - Unit Volume* Quantity (G15= F15*product_qty)")

    @api.depends('unit_volume', 'product_qty')
    def compute_total_volume(self):
        for rec in self:
            rec.total_volume = rec.unit_volume * rec.product_qty

    unit_ocean_freight_usd = fields.Float(string="Unit Ocean Freight(USD)", compute="compute_unit_ocean_freight_usd", store=True,
        help="Unit Ocean Freight(USD) - (Ocean freight cost/total container cost) *unit volume (H15= B6/ (Volume of Container in m3)*F15")

    @api.depends('order_id.ocean_freight_cost', 'unit_volume')
    def compute_unit_ocean_freight_usd(self):
        for rec in self:
            if rec.product_id.volume > 0:
                rec.unit_ocean_freight_usd = (rec.order_id.ocean_freight_cost/rec.product_id.volume) * rec.unit_volume

    unit_truck_freight_usd = fields.Float(string="Unit Truck Freight(USD)", compute="compute_unit_truck_freight_usd", store=True,
        help="Unit Truck Freight(USD) - (Truck freight cost/exchange rate/total container cost) *unit volume (I15= (B7/product_qty)/ Volume of Container in m3*F15)")

    @api.depends('order_id.truck_freight_cost', 'product_qty', 'unit_volume')
    def compute_unit_truck_freight_usd(self):
        for rec in self:
            if rec.product_qty > 0 and (rec.product_id.volume*rec.unit_volume) > 0:
                rec.unit_truck_freight_usd = (rec.order_id.truck_freight_cost/rec.product_qty)/rec.product_id.volume*rec.unit_volume

    total_freight_cost_usd = fields.Float(string="Total Freight Cost(USD)", compute="compute_total_freight_cost_usd", store=True,
        help="Total Freight Cost(USD) - (Unit ocean freight+ unit truck freight) * qty (J15 = H15+I15*product_qty)")

    @api.depends('unit_truck_freight_usd', 'unit_ocean_freight_usd', 'product_qty')
    def compute_total_freight_cost_usd(self):
        for rec in self:
            rec.total_freight_cost_usd = (rec.unit_ocean_freight_usd+rec.unit_truck_freight_usd)*rec.product_qty

    unit_cost_mxn = fields.Float(string="Unit Cost(MXN)", compute="compute_unit_cost_mxn", store=True,
        help="Unit Cost(MXN)- Unit cost(USD)*exchange rate(K15=C15*product_qty)")

    @api.depends('price_unit', 'product_qty')
    def compute_unit_cost_mxn(self):
        for rec in self:
            rec.total_volume = rec.price_unit*rec.product_qty

    total_cost_mxn= fields.Float(string="Total Cost(MXN)", compute="compute_total_cost_mxn", store=True,
        help="Total Cost(MXN)- Unit Cost(MXN)*Qty(L15=K15*product_qty)")

    @api.depends('unit_cost_mxn', 'product_qty')
    def compute_total_cost_mxn(self):
        for rec in self:
            rec.total_cost_mxn = rec.unit_cost_mxn*rec.product_qty

    unit_ocean_freight_mxn = fields.Float(string="Unit Ocean Freight(MXN)", compute="compute_unit_ocean_freight_mxn", store=True,
        help="Unit Ocean Freight(MXN)- Unit ocean freight(USD)*exchange rate(M15=H15*product_qty)")

    @api.depends('unit_ocean_freight_usd', 'product_qty')
    def compute_unit_ocean_freight_mxn(self):
        for rec in self:
            rec.unit_ocean_freight_mxn = rec.unit_ocean_freight_usd*rec.product_qty

    unit_truck_freight_mxn = fields.Float(string="Unit Truck Freight(MXN)", compute="compute_unit_truck_freight_mxn", store=True,
        help="Unit Truck Freight(MXN)- Unit truck freight(USD)*exchange rate (N15= I15*product_qty)")

    @api.depends('unit_truck_freight_usd', 'product_qty')
    def compute_unit_truck_freight_mxn(self):
        for rec in self:
            rec.unit_truck_freight_mxn = rec.unit_truck_freight_usd*rec.product_qty

    total_freight_cost_mxn = fields.Float(string="Total Freight Cost(MXN)", compute="compute_total_freight_cost_mxn", store=True, 
        help="Total Freight Cost(MXN)- (Unit ocean freight(MXN)+unit truck freight(MXN)) *qty (P15=M15+N15*product_qty)")
    
    @api.depends('unit_truck_freight_mxn', 'unit_ocean_freight_mxn', 'product_qty')
    def compute_total_freight_cost_mxn(self):
        for rec in self:
            rec.total_freight_cost_mxn = rec.unit_truck_freight_mxn+rec.unit_ocean_freight_mxn*rec.product_qty


    unit_freight_cost_mxn = fields.Float(string="Unit Freight Cost(MXN)", compute="compute_unit_freight_cost_mxn", store=True,
        help="Unit Freight Cost(MXN)- Unit ocean freight(MXN)+unit truck freight(MXN) (O15=M15+N15)")
    
    @api.depends('unit_truck_freight_mxn', 'unit_ocean_freight_mxn')
    def compute_unit_freight_cost_mxn(self):
        for rec in self:
            rec.unit_freight_cost_mxn = rec.unit_truck_freight_mxn+rec.unit_ocean_freight_mxn

    unit_customs_agent_mxn = fields.Float(string="Unit Customs Agent(MXN)", compute="compute_unit_customs_agent_mxn", store=True,
        help="Unit Customs Agent(MXN)- (Customs Agent Cost /total container cost) *unit volume (Q15=(B10/Volume of Container in m3)*F15)")
    
    @api.depends('order_id.customs_agent_cost', 'unit_volume')
    def compute_unit_customs_agent_mxn(self):
        for rec in self:
            if rec.product_id.volume > 0:
                rec.unit_customs_agent_mxn = (rec.order_id.customs_agent_cost/rec.product_id.volume)*rec.unit_volume
    
    total_customs_agent_mxn = fields.Float(string="Total Custom Agent(MXN)", compute="compute_total_customs_agent_mxn", store=True,
        help="Total Custom Agent(MXN)- Unit Customs Agent(MXN)* qty(R15=Q15*product_qty)")

    @api.depends('unit_customs_agent_mxn', 'product_qty')
    def compute_total_customs_agent_mxn(self):
        for rec in self:
            rec.total_customs_agent_mxn = rec.unit_customs_agent_mxn*rec.product_qty

    igi_mxn = fields.Float(string="IGI (MXN)", compute="compute_igi_mxn", store=True,
        help="IGI(MXN)- (unit cost(MXN)+unit ocean freight(MX)) *IGI%(T15=(K15+M15)*(S15/100))")

    @api.depends('unit_cost_mxn', 'unit_ocean_freight_mxn')
    def compute_igi_mxn(self):
        for rec in self:
            rec.igi_mxn = (rec.unit_cost_mxn+rec.unit_ocean_freight_mxn)*(rec.product_id.importation_tax_igi/100)

    sum_cost_before_tax = fields.Float(string="Sum of Costs before Taxes(MXN)", compute="compute_sum_cost_before_tax", store=True,
        help="Sum of Costs before Taxes(MXN)- Unit Cost(MXN)+Unit Ocean Freight(MXN )(U15= K15+M15)")

    @api.depends('unit_cost_mxn', 'unit_ocean_freight_mxn')
    def compute_sum_cost_before_tax(self):
        for rec in self:
            rec.sum_cost_before_tax = rec.unit_cost_mxn+rec.unit_ocean_freight_mxn

    dta_factor = fields.Float(string="DTA Factor", compute="compute_dta_factor", store=True,
        help="DTA Factor-Sum of Costs before Taxes(MXN) * DTA factor (V15= U15*B9)")

    @api.depends('sum_cost_before_tax', 'order_id.dta_factor')
    def compute_dta_factor(self):
        for rec in self:
            rec.dta_factor = rec.sum_cost_before_tax+rec.order_id.dta_factor

    unit_sum_cost_mxn = fields.Float(string="Unit Sum Cost(MXN)", compute="compute_unit_sum_cost_mxn", store=True,
        help="Unit Sum Cost(MXN)- Unit Cost(MXN) + Unit Freight Cost(MXN)+Unit Customs Agent(MXN)+ IGI(MXN)+DTA Factor (W15= K15+O15+T15+V15+Q15)")

    @api.depends('unit_cost_mxn', 'unit_freight_cost_mxn', 'igi_mxn', 'dta_factor', 'unit_customs_agent_mxn')
    def compute_unit_sum_cost_mxn(self):
        for rec in self:
            rec.unit_sum_cost_mxn = rec.unit_cost_mxn+rec.unit_freight_cost_mxn+rec.igi_mxn+rec.dta_factor+rec.unit_customs_agent_mxn

    total_sum_cost_mxn = fields.Float(string="Total Sum Cost(MXN)", compute="compute_total_sum_cost_mxn", store=True,
        help="Total Sum Cost(MXN)- Sum of Costs before Taxes(MXN)*Qty (X15= U15*product_qty)")

    @api.depends('sum_cost_before_tax', 'product_qty')
    def compute_total_sum_cost_mxn(self):
        for rec in self:
            rec.total_sum_cost_mxn = rec.sum_cost_before_tax+rec.product_qty

    price_list_mxn = fields.Float(string="Price list(MXN)",
        help="Price list(MXN)- The Sale Price of product on Product form(Y15))")

    minimum_price_mxn = fields.Float(string="Minimum Price(MXN)",
        help="Minimum Price(MXN)- This the the field base price on the product form this is the part of earlier sales dev request(Z15)")

    margin_prctge = fields.Float(string="Minimum Price(MXN)", compute="compute_margin_prctge", store=True,
        help="% Margin- (Minimum Price(MXN)*100)/ (Sum of Costs before Taxes(MXN)-100) (Aproduct_qty =Z15*100/U15-100)")

    @api.depends('minimum_price_mxn', 'sum_cost_before_tax')
    def compute_margin_prctge(self):
        for rec in self:
            if rec.sum_cost_before_tax > 0:
                rec.margin_prctge = rec.minimum_price_mxn*100/rec.sum_cost_before_tax-100

    margin_diff_prctge = fields.Float(string="Minimum Difference Price(MXN)", compute="compute_margin_diff_prctge", store=True,
        help="% Margin Difference- Difference between Margin '%' and 35% (target margin) (AB15= =(35-Aproduct_qty))")

    @api.depends('margin_prctge')
    def compute_margin_diff_prctge(self):
        for rec in self:
            rec.margin_diff_prctge = 35-rec.margin_prctge

    target_price_usd = fields.Float(string="Target Price(USD)", compute="compute_target_price_usd", store=True,
        help="Target Price(USD)- Unit cost(USD)-% margin difference (AC15=(C15-AB15%)")

    @api.depends('margin_diff_prctge', 'price_unit')
    def compute_target_price_usd(self):
        for rec in self:
            rec.target_price_usd = rec.price_unit-(rec.price_unit*rec.margin_diff_prctge/100)

    @api.depends('product_id', 'product_qty', 'price_unit')
    def compute_total_cost_usd(self):
        for rec in self:
            rec.total_cost_usd = rec.product_qty*rec.price_unit