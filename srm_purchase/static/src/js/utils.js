odoo.define('srm_purchase.utils', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    /**
     * 格式化字符串
     * 字面量版：$.format ( "为什么{language}没有format" , { language : "javascript" } );
     * 数组版：$.format ( "为什么{0}没有format" ,  [ "javascript" ] );
     * @param source
     * @param args
     * @returns {*}
     */
    function format_str(source, args) {
        var result = source;
        if (typeof(args) === "object") {
            if (args.length === undefined) {
                for (var key in args) {
                    if (args[key] !== undefined) {
                        var reg = new RegExp("({" + key + "})", "g");
                        result = result.replace(reg, args[key]);
                    }
                }
            } else {
                for (var i = 0; i < args.length; i++) {
                    if (args[i] !== undefined) {
                        var reg = new RegExp("({[" + i + "]})", "g");
                        result = result.replace(reg, args[i]);
                    }
                }
            }
        }
        return result;
    }

    /**
     * 全屏遮罩 loading
     * @param msg 提示信息
     */
    function showLoading(msg) {
        var $loading = $('<div/>').append($('<div/>', {
            class: 'oe_blockui_spin',
            css: {height: '50px'},
            html: '<img src="/web/static/src/img/spin.png" style="animation: fa-spin 1s infinite steps(12);"><br>'
        })).append($('<div/>', {
            class: 'oe_throbber_message',
            css: {color: 'white'},
            text: msg || '加载中...'
        }));
        $.blockUI({
            css: {
                border: 'none',
                backgroundColor: '',
                'z-index': 9999
            },
            overlayCSS: {
                'z-index': 6666
            },
            message: $loading
        });
    }

    /**
     * 隐藏 loading
     */
    function hideLoading() {
        $.unblockUI();
    }

    /**
     * 显示提示信息
     * @param msg 描述内容
     * @param timeout 消失时间，单位 ms，默认 1500ms
     */
    function showToast (msg, timeout) {
        $.blockUI({
            css: {
                width: '10%',
                border: 'none',
                padding: '15px',
                background: '#000',
                '-webkit-border-radius': '10px',
                '-moz-border-radius': '10px',
                opacity: 0.6,
                color: '#fff',
                top: '30%',
                left: '45%'
            },
            overlayCSS: {
                opacity: 0
            },
            message: msg || 'OK'
        });
        setTimeout($.unblockUI, timeout || 1500);
    }

    /**
     * 通过附件 ID 下载文件
     * @param id
     * @param filename 文件名
     * @param options 下载完成后的回调，成功时执行 options.complete, 错误时执行 options.error
     */
    function get_attachment (id, filename, options) {
        ajax.get_file({
            'url': '/web/content',
            'data': {
                'model': 'ir.attachment',
                'id': parseInt(id),
                'field': 'datas',
                'filename_field': 'datas_fname',
                'filename': filename || '未命名',
                'download': true
            },
            'complete': options && options.complete || null,
            'error': options && options.error || null
        });
    }

    return {
        format_str: format_str,
        showLoading: showLoading,
        hideLoading: hideLoading,
        showToast: showToast,
        get_attachment: get_attachment
    }
});