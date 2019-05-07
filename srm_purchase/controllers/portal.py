# coding=utf-8

import re
import logging
from collections import OrderedDict

from odoo import exceptions, http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.purchase.controllers.portal import CustomerPortal

_logger = logging.getLogger(__name__)


class PurchaseCustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PurchaseCustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id.parent_id or request.env.user.partner_id

        PO = request.env['purchase.order']
        po_count = PO.search_count([
            ('partner_id', '=', partner.id),
            ('state', 'in', ['purchase', 'done', 'cancel', 'refuse', 'pending'])
        ])
        purchase_quote_count = PO.search_count([
            ('partner_id', '=', partner.id),
            ('state', 'in', ['sent', 'to approve', 'cancel'])
        ])

        values.update({
            'purchase_count': po_count,
            'purchase_quote_count': purchase_quote_count,
        })
        return values

    def _is_mobile(self):
        """
        判断当前用户是否从移动端访问
        :return:
        """
        re_mobile = re.compile(r"(iPhone|iPad|iPod|Android|Mobile|wxwork|MicroMessenger)", re.I)
        ua = request.httprequest.user_agent.string
        return True if re_mobile.search(ua) else False

    @http.route(['/my/purchase', '/my/purchase/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id.parent_id or request.env.user.partner_id
        PO = request.env['purchase.order']

        domain = [('partner_id', '=', partner.id)]

        archive_groups = self._get_archive_groups('purchase.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': '单号', 'order': 'name asc, id asc'},
            'amount_total': {'label': '金额', 'order': 'amount_total desc, id desc'},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {  # seq: 搜索项在页面上的排序
            'all': {'label': _('All'), 'domain': [('state', 'in', ['purchase', 'done', 'cancel', 'refuse', 'pending'])], 'seq': 1},
            'purchase': {'label': '采购订单', 'domain': [('state', '=', 'purchase')], 'seq': 2},
            'done': {'label': '已锁定', 'domain': [('state', '=', 'done')], 'seq': 3},
            'cancel': {'label': '已取消', 'domain': [('state', '=', 'cancel')], 'seq': 4},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        purchase_count = PO.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/purchase",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=purchase_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager
        order_ids = PO.search(domain, limit=self._items_per_page, offset=pager['offset'], order=order)

        values.update({
            'date': date_begin,
            'order_ids': order_ids,
            'page_name': 'po',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items(), key=lambda item: item[1]['seq'])),
            'filterby': filterby,
            'default_url': '/my/purchase'
        })
        delivery_status_dict = {}
        for each_order in order_ids:
            if each_order.state in ['cancel']:
                delivery_status_dict[each_order.id] = '已取消'
            else:
                delivery_status = self.check_the_purchase_order_delivery_status(order=each_order)
                if delivery_status == 'all_delivery':
                    delivery_status_dict[each_order.id] = '全部发货'
                elif delivery_status == 'no_delivery':
                    delivery_status_dict[each_order.id] = '待发货'
                elif delivery_status == 'partial_delivery':
                    delivery_status_dict[each_order.id] = '部分发货'
                else:
                    delivery_status_dict[each_order.id] = '其他'
        values.update({'delivery_status_dict': delivery_status_dict})
        return request.render("srm_purchase.portal_my_po", values)

    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="user", website=True)
    def portal_my_purchase_order(self, order_id=None, **kw):
        order = request.env['purchase.order'].browse(order_id)
        try:
            order.check_access_rights('read')
            order.check_access_rule('read')
        except exceptions.AccessError:
            return request.redirect('/my')
        order_cancelled = False
        if order.state in ['cancel']:
            delivery_status = '已取消'
            can_delivery = False
            order_cancelled = True
        else:
            delivery_status = self.check_the_purchase_order_delivery_status(order=order)
            if delivery_status == 'all_delivery':
                can_delivery = False
                delivery_status = '全部发货'
            else:
                can_delivery = True
                if delivery_status == 'no_delivery':
                    delivery_status = '待发货'
                else:
                    delivery_status = '部分发货'
        values = {
            'order': order.sudo(),
            'page_name': 'po',
            'delivery_status': delivery_status,
            'can_delivery': can_delivery,
            'order_cancelled': order_cancelled,
        }
        return request.render("srm_purchase.portal_po_page", values)

    @http.route('/my/purchase/action', type='json', auth="user", method=['POST'])
    def portal_po_action(self, **kw):
        params = request.params
        po_id = params.get('id', None)
        order_id = request.env['purchase.order'].sudo().browse(int(po_id))
        action = params.get('action', 'accept')
        if not order_id:
            return {
                'status': 'fail',
                'msg': '采购单不存在'
            }
        if action == 'accept':
            order_id.action_accept()
            return {
                'status': 'OK',
                'msg': '已确认订单，请尽快安排发货事宜'
            }
        if action == 'refuse':
            order_id.action_refuse()
            return {
                'status': 'OK',
                'msg': '已取消订单'
            }
        return {
            'status': 'fail',
            'msg': '未知操作'
        }

    @http.route('/my/delivery/ship/<int:order_id>', type='http', auth="user", website=True)
    def portal_my_delivery_ship(self, order_id=None, **kw):
        order = request.env['purchase.order'].browse(order_id)
        try:
            order.check_access_rights('read')
            order.check_access_rule('read')
        except exceptions.AccessError:
            return request.redirect('/my')
        delivery_status = self.check_the_purchase_order_delivery_status(order=order)
        if delivery_status == 'all_delivery':
            all_delivered = True
        else:
            all_delivered = False
        values = {
            'order': order.sudo(),
            'page_name': 'po',
            'is_delivery': True,
            'all_delivered': all_delivered,
        }
        return request.render("srm_purchase.portal_delivery_ship_page", values)

    @http.route('/my/delivery/action/<int:order_id>', type='http', auth="user", website=True, method=['POST'], csrf=False)
    def portal_delivery_action_form(self, order_id, **kw):
        order_id = request.env['purchase.order'].sudo().browse(int(order_id))
        values = {
            'page_name': 'po',
            'delivery_result_page': True,
            'order': order_id,
        }
        delivery_data = {}
        for k, v in kw.items():
            if k.startswith('line-'):
                key = int(float(k.split('-')[1]))
                delivery_data[key] = int(float(v))
        order_id.ship(delivery_data)
        return request.render("srm_purchase.portal_delivery_result_page", values)

    @http.route(['/my/purchase_quotation', '/my/purchase_quotation/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_purchase_quote_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id.parent_id or request.env.user.partner_id
        PO = request.env['purchase.order']

        domain = [('partner_id', '=', partner.id)]

        archive_groups = self._get_archive_groups('purchase.order', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': '单号', 'order': 'name asc, id asc'},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {  # seq: 搜索项在页面上的排序
            'all': {'label': _('All'), 'domain': [('state', 'in', ['sent', 'to approve', 'cancel'])], 'seq': 1},
            'sent': {'label': '询价中', 'domain': [('state', '=', 'sent')], 'seq': 2},
            'to approve': {'label': '审批中', 'domain': [('state', '=', 'to approve')], 'seq': 3},
            'cancel': {'label': '已取消', 'domain': [('state', '=', 'cancel')], 'seq': 4},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        # count for pager
        purchase_count = PO.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/purchase_quotation",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=purchase_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager
        order_ids = PO.search(domain, limit=self._items_per_page, offset=pager['offset'], order=order)

        values.update({
            'date': date_begin,
            'order_ids': order_ids,
            'page_name': 'purchase_quote',
            'pager': pager,
            'archive_groups': archive_groups,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items(), key=lambda item: item[1]['seq'])),
            'filterby': filterby,
            'default_url': '/my/purchase_quotation'
        })
        return request.render("srm_purchase.portal_purchase_quote_base", values)

    @http.route(['/my/purchase_quotation/<int:order_id>'], type='http', auth="user", website=True)
    def portal_my_purchase_quote_order(self, order_id=None, **kw):
        order = request.env['purchase.order'].browse(order_id)
        try:
            order.check_access_rights('read')
            order.check_access_rule('read')
        except exceptions.AccessError:
            return request.redirect('/my')
        if order.state in ['sent']:
            order_status = '询价中'
            can_quote = True
        elif order.state in ['cancel']:
            order_status = '已取消'
            can_quote = False
        elif order.state in ['to approve']:
            order_status = '审批进行中'
            can_quote = False
        else:
            order_status = '其他'
            can_quote = False
        values = {
            'order': order.sudo(),
            'page_name': 'purchase_quote',
            'order_status': order_status,
            'can_quote': can_quote,
        }
        return request.render("srm_purchase.portal_purchase_quote_detail_base", values)

    @http.route('/my/purchase_quote/action', type='json', auth="user", method=['POST'])
    def portal_purchase_quote_action(self, **kw):
        params = request.params
        po_id = params.get('id', None)
        now_date = params.get('now_date', None)
        action = params.get('action', 'submit')
        model_dict = {
            'submit': 'purchase.order'
        }
        model = model_dict[action]
        order_id = request.env[model].sudo().browse(int(po_id))
        if not order_id:
            return {
                'status': 'fail',
                'msg': '询价单不存在'
            }
        if action == 'submit':
            all_data = []
            purchase_quote_data = params.get('vals', {})
            for line_id, line_price_unit in purchase_quote_data.items():
                all_data.append((1, int(line_id), {'price_unit': line_price_unit}))
            if all_data:
                order_id.write({'order_line': all_data})
                now_user = request.env['res.users'].sudo().browse(int(http.request.uid))
                body = "{} 提交了报价，提交时间：{}".format(now_user.name, now_date)
                order_id.message_post(body=body)
            return {
                'status': 'OK',
                'msg': '报价已提交'
            }
        return {
            'status': 'fail',
            'msg': '未知操作'
        }

    def check_the_purchase_order_delivery_status(self, order):
        """
        检查采购订单的发货情况
        :param order: 采购订单
        :return: all_delivery   : 全部发货
                 partial_delivery   : 部分发货
                 no_delivery    : 没有发货
        """
        all, none = True, True
        for each_line in order.order_line:
            if each_line.qty_unship != 0:
                all = False
            if each_line.qty_unship != each_line.product_qty:
                none = False
        if all is True:
            return 'all_delivery'
        elif none is True:
            return 'no_delivery'
        else:
            return 'partial_delivery'
