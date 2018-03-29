# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mexytul Sales',
    'summary': 'Mexytul Sales',
    'sequence': 100,
    'description': """
Mexytul Sales Customization
===========================
* Sale Order, Sale Order Margin
* Sale Order Check the Credit Limit of Customer
* Calculate base price on product from base on margin and cost price
* Base price check on order line if customer haven't rights
    """,
    'category': 'Sales',
    'depends': ['sale', 'base'],
    'data': [
        "data/data.xml",
        "views/partner_view.xml",
        "views/product_view.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
