# coding=utf-8

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    qty_unship = fields.Float(compute='_compute_qty_unship', string="unship Qty",
                              digits=dp.get_precision('Product Unit of Measure'), store=True)

    @api.depends('order_id.state', 'move_ids.state', 'move_ids.product_uom_qty')
    def _compute_qty_unship(self):
        for line in self:
            if line.order_id.state not in ['purchase', 'done']:
                continue
            if line.product_id.type not in ['consu', 'product']:
                continue
            received = 0.0
            for move in line.move_ids:
                if move.state == 'assigned':
                    received += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                if move.state == 'done':
                    if move.location_dest_id.usage == "supplier":
                        if move.to_refund:
                            received -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
                    else:
                        received += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
            line.qty_unship = line.product_qty - received

    @api.multi
    def _prepare_stock_moves(self, picking, count=None):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        if not res or count is None:
            return res

        res[0]['product_uom_qty'] = count
        res[0]['quantity_done'] = count
        return res

    @api.multi
    def _create_stock_moves(self, picking, stock_count=None):
        """
        :param picking:
        :param dict stock_count: {line_id: count}
        :return:
        """
        if stock_count is None:
            return super(PurchaseOrderLine, self)._create_stock_moves(picking)

        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            count = stock_count.get(line.id, 0)
            if count == 0:
                continue
            for val in line._prepare_stock_moves(picking, count):
                new_move = moves.create(val)
                new_move.ordered_qty = line.product_qty
                done += new_move
        return done
