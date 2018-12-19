odoo.define('web_qiniu_uploader', function (require) {
    "use strict";

    var core = require('web.core');
    var framework = require('web.framework');
    var FormRenderer = require('web.FormRenderer');
    var rpc = require('web.rpc');

    var QWeb = core.qweb;

    FormRenderer.include({
        _fileSelect: function () {
            this.selectedFile = $('.oe_import_file')[0].files[0];
            $('.oe_import_file_show').val(this.selectedFile !== undefined && this.selectedFile.name || '');
            $('.oe_import_file_confirm').prop('disabled', false);
        },
        _fileUpload: function (e) {
            var self = this;
            framework.blockUI();
            rpc.query({
                model: 'res.config.settings',
                method: 'get_qiniu_token',
                args: []
            }).then(function (res) {
                if (res) {
                    var token = res.token,
                        domain = res.domain;
                    var file = self.selectedFile;
                    // 上传文件到七牛
                    var fname = file.name,
                        putExtra = {fname: fname, params: {}, mimeType: null};
                    var observable = qiniu.upload(file, null, token, putExtra, {});
                    var subscription = observable.subscribe(function (res) {
                        /**
                         * 上传进度回调
                         * @param res {object} res.total 包含 loaded、total、percent 三个属性
                         */
                    }, function (err) {
                        /**
                         * 上传失败回调
                         * @param err {object} 当产生 xhr 请求错误时，err 包含 code、message、isRequestError 三个属性
                         */
                        console.error(err);
                        framework.unblockUI();
                    }, function (res) {
                        /**
                         * 上传完成回调
                         * @param res {object} 根据上传策略有所不同，一般会包含 hash 和 key 两个属性
                         */
                        var urlId = self.idsForLabels.url;
                        self.$el.find("#" + urlId).val([domain, res.key].join('/')).trigger('change');
                        framework.unblockUI();
                    });
                } else {
                    // 获取 token 失败
                    framework.unblockUI();
                    throw new Error('获取 Token 失败，请检查七牛云相关配置');
                }
            });
        },
        /**
         * @private
         * @param {Object} node
         * @returns {jQueryElement}
         */
        _renderTagUploader: function (node) {
            var $uploader = $(QWeb.render('QiniuUploader', {}));
            $uploader.find('.oe_import_file').on('change', this._fileSelect.bind(this));
            $uploader.find('.oe_import_file_confirm').on('click', this._fileUpload.bind(this));
            return $uploader;
        }
    });
});