from odoo import fields, models
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = "stock.move"

    ordered_qty = fields.Float('Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'))
