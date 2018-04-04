# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mexytul Purchase',
    'summary': 'Mexytul Purchase',
    'sequence': 101,
    'description': """
Mexytul Purchase Customization
==============================
* Purchase Order
    """,
    'category': 'Purchases',
    'depends': ['purchase_requisition', 'purchase', 'base'],
    'data': [
        "views/partner_view.xml",
        # "views/purchase_view.xml",
        "views/product_view.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
