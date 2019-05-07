odoo.define('srm_purchase.purchase', function (require) {
    "use strict";

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var utils = require('srm_purchase.utils');

    var qweb = core.qweb;


    var formatStr = utils.format_str;
    var getAttachment = utils.get_attachment;
    var blockUI = utils.showLoading;
    var unblockUI = utils.hideLoading;
    var showToast = utils.showToast;

    // 禁止按钮操作
    var operateFreeze = function () {
        $('.po-operand button').prop('disabled', true);
    };

    var refusePurchaseOrder = function () {
        // 拒绝订单
        event.stopPropagation();
        blockUI();
        var self = this;
        ajax.rpc('/my/purchase/action', {
            id: $('#orderId').val(),
            action: 'refuse'
        }).then(function (res) {
            unblockUI();
            if (res.status === 'OK') {
                showToast(res.msg, 1500);
                operateFreeze();
            } else {
                Dialog.alert(self, res.msg, { title: '失败' });
            }
        });
    };

    var getDeliveryData = function () {
        var self = this;
        var $rows = $('.delivery-order-line');
        var data = {};
        var error_flag = false;
        _.each($rows, function (tr) {
            var $row = $(tr);
            var line_id = $row.data('id');
            var $amount = $row.find('input.delivery-amount');
            if ($amount.length) {
                var qty_unship = parseFloat($row.find('span#qty_unship')[0].innerText);
                var amount = parseFloat($amount.val());
                if (amount > qty_unship || amount < 1) {
                    Dialog.alert(self, '请输入正确的发货数量（1～待发货数量）！', { title: '失败' });
                    error_flag = true;
                    return;
                }
                data[line_id] = amount;
            }
        });
        if (error_flag === true) {
            return 'error';
        }
        return data;
    };

    /**
     * 采购订单页面按钮操作
     */

    $('button.po-accept').on('click', function (event) {
        // 确认订单
        event.stopPropagation();
        blockUI();
        var self = this;
        ajax.rpc('/my/purchase/action', {
            id: $('#orderId').val(),
            action: 'accept'
        }).then(function (res) {
            unblockUI();
            if (res.status === 'OK') {
                showToast(res.msg, 2000);
                operateFreeze();
            } else {
                Dialog.alert(self, res.msg, { title: '失败' });
            }
        });
    });
    $('button.po-refuse').on('click', function (event) {
        // 放弃报价
        event.stopPropagation();
        new Dialog(this, {
            title: '拒绝订单？',
            $content: '<p>是否确认拒绝订单？</p>',
            buttons: [
                { text: '确定', classes : "btn-danger", click: refusePurchaseOrder, close:true },
                { text: '取消', classes : "btn-default", close: true }
            ]
        }).open();
    });

    /**
     * 发货页面操作
     */

    $('.delivery-confirm').on('click', function (event) {
        event.stopPropagation();
        var self = this;
        var deliveryData = getDeliveryData();
        if (deliveryData === 'error') {
            return;
        }
        blockUI();
        ajax.rpc('/my/delivery/action', {
            id: $('#orderId').val(),
            action: 'submit',
            vals: deliveryData
        }).then(function (res) {
            unblockUI();
            if (res.status === 'OK') {
                showToast(res.msg, 2000);
                // $(self).prop('disabled', true);
                window.location.href = location.href+'?time='+((new Date()).getTime());
            } else {
                Dialog.alert(self, res.msg, { title: '失败' });
            }
        });
    });

    /**
     * 提交报价单价页面操作
     */

    $('.price-unit-quote-confirm').on('click', function (event) {
        event.stopPropagation();
        blockUI();
        var self = this;
        var priceUnitQuoteData = getPriceUnitQuoteData();
        var date = new Date();
        ajax.rpc('/my/purchase_quote/action', {
            id: $('#purchaseQuoteOrderId').val(),
            now_user_id: $('#nowUserId').val(),
            action: 'submit',
            vals: priceUnitQuoteData,
            now_date: date.toLocaleString()
        }).then(function (res) {
            unblockUI();
            if (res.status === 'OK') {
                showToast(res.msg, 2000);
                // $(self).prop('disabled', true);
                window.location.href = location.href+'?time='+((new Date()).getTime());
            } else {
                Dialog.alert(self, res.msg, { title: '失败' });
            }
        });
    });

    var getPriceUnitQuoteData = function () {
        var $rows = $('.price-unit-quote-line');
        var data = {};
        _.each($rows, function (div) {
            var $row = $(div);
            var line_id = $row.data('id');
            var $price_unit = $row.find('input.price-unit-quote');
            if ($price_unit.length) {
                var price_unit = $price_unit.val();
                data[line_id] = parseFloat(price_unit);
            }
        });
        return data;
    };

});
