from odoo import api, fields, models
from odoo.tools import float_compare


class Product(models.Model):
    _name = "product.product"
    _inherit = ['product.product']
