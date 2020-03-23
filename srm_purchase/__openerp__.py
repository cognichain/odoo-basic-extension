# coding=utf-8

{
    'name': 'SRM Purchase Collaboration',
    'version': '0.1',
    'summary': 'An extension to Odoo Purchase App to allow you collaborate with suppliers on RFQ, Purchase Order, Shipment via a supplier portal.',
    'description': """""",
    'author': 'Cognichain',
    'website': 'http://www.cognichain.com/',
    'depends': ['purchase', 'stock', 'website'],
    'data': [
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',

        'views/templates.xml',
        'views/new_res_config_settings_views.xml',
        'views/parent_menus.xml',

        'views/portal/purchase_portal_templates.xml',
        'views/portal/home.xml',
        'views/portal/purchase_quote.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
    'installable': True,
    'auto_install': False,
}
