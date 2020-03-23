from odoo import api, fields, models
from odoo.tools import float_compare


class Product(models.Model):
    _name = "product.product"
    _inherit = ['product.product']

    @api.multi
    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False):
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        sup_infos = self.env['product.supplierinfo']
        for seller in self.seller_ids:
            # Set quantity in UoM of seller
            quantity_uom_seller = quantity
            if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
                quantity_uom_seller = uom_id._compute_quantity(quantity_uom_seller, seller.product_uom)

            if seller.date_start and seller.date_start > date:
                continue
            if seller.date_end and seller.date_end < date:
                continue
            if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
                continue
            if float_compare(quantity_uom_seller, seller.min_qty, precision_digits=precision) == -1:
                continue
            if seller.product_id and seller.product_id != self:
                continue

            sup_infos |= seller
        res = sup_infos.sorted(lambda r: (r.id, r.min_qty))
        return res[-1] if res else res
