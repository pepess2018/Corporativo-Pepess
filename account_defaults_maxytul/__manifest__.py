# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Maxytul: Accounting defaults",
    'summary': "Web",
    'description': """
Maxytul: Accounting defaults
============================
- set default accounting journal and debit/credit accounts based on warehouse.
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['sale_stock', 'stock_account', 'purchase', 'point_of_sale'],
    'data': [
        'views/stock_warehouse_views.xml',
        'views/account_views.xml',
        'views/pos_config_views.xml'
    ],
    'license': 'OEEL-1',
}