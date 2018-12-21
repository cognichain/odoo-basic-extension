odoo.define('web_form_dynamic_button', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');

    var _t = core._t;

    FormController.include({
        /**
         * 根据表达式处理按钮 ``edit`` 和 ``create`` 的显示或隐藏
         * 在 ``<form />`` 中添加属性 ``edit_expr="expr"`` 或 ``create_expr="expr"``
         * 其中 ``expr`` 为表达式，如 ``state=='draft'``
         * @private
         */
        _updateButtons: function () {
            this._super.apply(this, arguments);
            if (this.mode === 'readonly' && this.$buttons && this.hasButtons) {
                var self = this;
                var attrs = this.renderer.arch.attrs;
                var actions = ['edit', 'create'];
                _.each(actions, function (action) {
                    var expr = attrs[action + '_expr'];
                    var act_res = expr ? self._evalActionExpr(expr) : self.activeActions[action];
                    self.$buttons.find('.o_form_button_' + action).toggleClass('o_hidden', !act_res);
                });
            }
        },
        /**
         * 根据表达式处理按钮 ``delete`` 和 ``duplicate`` 的显示或隐藏
         * 在 ``<form />`` 中添加属性 ``delete_expr="expr"`` 或 ``duplicate_expr="expr"``
         * 其中 ``expr`` 为表达式，如 ``state=='draft'``
         * @private
         */
        _updateSidebar: function () {
            if (this.sidebar) {
                this.sidebar.do_toggle(this.mode === 'readonly');
            }
            if (this.mode === 'readonly' && this.sidebar && this.hasSidebar) {
                var self = this;
                var attrs = this.renderer.arch.attrs;
                var actions = ['delete', 'duplicate'];
                var otherItems = [];
                _.each(actions, function (action) {
                    var expr = attrs[action + '_expr'];
                    var act_res = expr ? self._evalActionExpr(expr) : self.activeActions[action];
                    if (act_res) {
                        var capAct = _.string.capitalize(action);
                        otherItems.push({
                            label: _t(capAct),
                            callback: self['_on' + capAct + 'Record'].bind(self),
                        });
                    }
                });
                this.sidebar.items.other = otherItems;
                this._updateEnv();
            }
        },
        _evalActionExpr: function (expr) {
            var expression = py.parse(py.tokenize(expr));
            return py.PY_isTrue(py.evaluate(expression, this.renderer.state.evalContext));
        }
    });
});