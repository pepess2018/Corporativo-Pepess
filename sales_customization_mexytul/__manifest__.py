# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mexytul Sales',
    'summary': 'Mexytul Sales',
    'sequence': 100,
    'version': '1.0',
    'description': """
Mexytul Sales Customization
===========================
* Sale Order, Sale Order Margin
* Sale Order Check the Credit Limit of Customer
* Calculate base price on product from base on margin and cost price
* Base price check on order line if customer haven't rights
* As the soon as the delivery is validated, it should create a draft invoice with invoiceable lines automatically.
  This should be in draft stage.
* In case there is a return for the delivery then a draft credit note should be automatically created.
    """,
    'category': 'Sales',
    'depends': ['delivery', 'l10n_mx_edi'],
    'data': [
        "data/data.xml",
        "data/actions.xml",
        "views/partner_view.xml",
        "views/product_view.xml",
        "views/account_view.xml",
        "reports/invoice_report.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
