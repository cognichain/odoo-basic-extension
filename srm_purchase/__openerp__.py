# coding=utf-8

{
    'name': 'SRM Purchase',
    'version': '0.1',
    'summary': '采购协同增强模块',
    'description': """""",
    'author': 'Cognichain',
    'website': 'http://www.cognichain.com/',
    'depends': ['purchase', 'website'],
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',

        'views/templates.xml',
        'views/res_config_settings_views.xml',

        'views/portal/purchase_portal_templates.xml',
        'views/portal/home.xml',
        'views/portal/purchase_quote.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
    'installable': True,
    'auto_install': False,
}
