# coding=utf-8

from odoo import api, fields, models, exceptions


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ['purchase.order']
    _finish_func = 'approval_finish'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'refuse': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    state = fields.Selection(selection_add=[('pending', '待确认'), ('refuse', '已拒绝')])

    @api.multi
    def _ship_create_picking(self, vals):
        self.ensure_one()
        StockPicking = self.env['stock.picking']
        order = self
        if any([ptype in ['product', 'consu'] for ptype in order.order_line.mapped('product_id.type')]):
            res = order._prepare_picking()
            picking = StockPicking.create(res)
            moves = order.order_line._create_stock_moves(picking, vals)
            moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
            seq = 0
            for move in sorted(moves, key=lambda move: move.date_expected):
                seq += 5
                move.sequence = seq
            moves._action_assign()
            picking.message_post_with_view('mail.message_origin_link',
                                           values={'self': picking, 'origin': order},
                                           subtype_id=self.env.ref('mail.mt_note').id)
        return True

    @api.multi
    def ship(self, vals):
        """
        调用此方法，并传入对应包含发货行&数量的dict，创建对应送货单（库存单）/欠单
        若是第一次发货，建立库存单，后续补充发货都为欠单
        :param dict vals: {line_id: count}
        :return:
        """
        self.ensure_one()
        self._ship_create_picking(vals)
        return True

    @api.multi
    def _create_picking(self):
        """
        重写采购模块内创建送货方法。
        原：采购订单确认订单时，会创建送货信息。
        现：不自动创建收货信息，改为供应商填送货后，创建对应的送货信息。
        """
        pass

    @api.multi
    def button_done(self):
        self.ensure_one()
        for line in self.order_line:
            if line.product_qty != line.qty_received:
                raise exceptions.ValidationError('未发货完毕不能锁定该采购单！')
        res = super(PurchaseOrder, self).button_done()
        return res

    @api.multi
    def action_view_picking(self):
        '''
        This function returns an action that display existing picking orders of given purchase order ids.
        When only one found, show the picking immediately.
        '''
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]

        # override the context to get rid of the default filtering on operation type
        result['context'] = {}
        pick_ids = self.mapped('picking_ids')
        # choose the view_mode accordingly
        if not pick_ids or len(pick_ids) > 1:
            result['domain'] = "[('id','in',%s), ('state', '!=', 'cancel')]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = pick_ids.id
        return result

    @api.multi
    def action_accept(self):
        self.ensure_one()
        self.write({'state': 'purchase'})
        return True

    @api.multi
    def action_refuse(self):
        self.ensure_one()
        self.write({'state': 'refuse'})
        return True

    @api.multi
    def button_confirm(self):
        super(PurchaseOrder, self).button_confirm()
        context = {
            'active_model': self._name,
            'active_ids': self.ids,
            'active_id': self.id,
        }
        ICPSudo = self.env['ir.config_parameter'].sudo()
        use_approval_workflow_module = ICPSudo.get_param('srm_purchase.use_approval_workflow_module', default='')
        for record in self:
            if record.state in ['to approve'] and use_approval_workflow_module == 'True':
                record.get_approval_strategy().with_context(**context).action_create_approval_workflow()
        return True

    @api.multi
    def button_approve(self, force=False):
        context = {
            'active_model': self._name,
            'active_ids': self.ids,
            'active_id': self.id,
        }
        ICPSudo = self.env['ir.config_parameter'].sudo()
        use_approval_workflow_module = ICPSudo.get_param('srm_purchase.use_approval_workflow_module', default='')
        for record in self:
            if record.state in ['to approve'] and self._context.get('is_server_action', False) is False:
                if use_approval_workflow_module == 'True':
                    return record.with_context(**context).return_approval_window()
        return super(PurchaseOrder, self).button_approve(force=force)

    def get_approval_strategy(self):
        module_name = 'approval'
        if not self.env.get('ir.module.module').sudo().search([('name', '=', module_name), ('state', '=', 'installed')]):
            raise exceptions.ValidationError('请先安装审批流模块！')
        model_id = self.env['ir.model'].search([('model', '=', self._name)]).id
        approval_strategy_objs = self.env.get('approval.strategy').sudo().search([('model_id', '=', model_id), ('enable', '=', True)])
        if len(approval_strategy_objs) < 1:
            if not self.env.get('approval.strategy').sudo().search([('model_id', '=', model_id)]):
                raise exceptions.ValidationError('请先创建审批策略！')
            else:
                raise exceptions.ValidationError('请先启动审批策略！')
        elif len(approval_strategy_objs) > 1:
            # 如果一个单据存在多个审批策略，先暂时去第一个审批策略。
            approval_strategy_objs = approval_strategy_objs[0]
        return approval_strategy_objs

    def return_approval_window(self):
        return self.get_approval_strategy().action_approval_window()
