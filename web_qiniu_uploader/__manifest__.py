# -*- coding: utf-8 -*-
{
    'name': "Qiniu attachment uploader in form views",
    'summary': "Allows you to upload attachment with ``ir.attachment`` field on form views",

    'author': "深圳市知链科技有限公司",
    'website': "https://github.com/cognichain/odoo-basic-extension",

    'category': 'Tools',
    'version': '11.0.1.0.1',
    'license': 'LGPL-3',

    'depends': ['web'],

    'data': [
        'views/views.xml',
        'views/web_qiniu_uploader.xml'
    ],
    'qweb': ['static/src/xml/base.xml'],
    'demo': [],
}