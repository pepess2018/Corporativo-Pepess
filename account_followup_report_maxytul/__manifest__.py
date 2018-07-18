# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Maxytul: Account Followup Report",
    'summary': "Web",
    'description': """
Maxytul: Account Followup Report
================================
-Followup report with following extra columns.
--Days Expired VS Invoiced Date 
--Assigned Fee 
--Invoice/Credit Note 
--Total Invoiced 
--Discount 
--Total Amount with Discount 
--Payments 
--Balance due 
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['sale_management', 'account_reports'],
    'data': [
    ],
    'license': 'OEEL-1',
}