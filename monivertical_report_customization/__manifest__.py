{
    'name': 'Monivertical Report Customization',
    'category': 'Sales',
    'description': """
Monivertical Report Customization
=================================
- Sale Report Customization
    """,
    'depends': ['web', 'sale_management',  'point_of_sale', 'stock', 'fleet', 'delivery'],
    'data': [
            # Report
            'report/classic_report_template.xml',
            'report/fency_report_template.xml',
            'report/modern_report_template.xml',
            'report/odoo_std_report_template.xml',
            'report/fxo_custom_report_sale_order.xml',
            'report/saleorder_report_inherit.xml',
            'report/report.xml',
            'report/report_delivery_slip_custom.xml',
            # views
            'views/stock_picking_views.xml',
            'views/res_company_views.xml',
            'views/delivery_carrier_views.xml'
        ],
    'qweb': [],

    'installable': True,
    'application': False,
}