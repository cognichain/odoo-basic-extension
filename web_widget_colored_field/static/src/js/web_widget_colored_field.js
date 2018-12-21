odoo.define('web_widget_colored_field', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var basic_fields = require('web.basic_fields');
    var relational_fields = require('web.relational_fields');

    var FieldChar = basic_fields.FieldChar;
    var FieldFloat = basic_fields.FieldFloat;
    var FieldInteger = basic_fields.FieldInteger;
    var FieldSelection = relational_fields.FieldSelection;

    AbstractField.include({
        _getColorNode: function (record, options) {
            var fieldColor = options.color;
            var fieldTitle = options.title;
            var fieldExpr = options.expr;

            var expr = py.parse(py.tokenize(fieldExpr));
            var res = py.PY_isTrue(py.evaluate(expr, record.evalContext));

            if (res) {
                // Make sure that multiple whitespace don't be escape
                var $color = $('<pre/>', {
                    css: {
                        "color": fieldColor,
                        "padding": "inherit",
                        "background": "none",
                        "border": "none",
                        "border-radius": "unset",
                        "font-size": "inherit",
                        "margin": 0
                    },
                    html: this._formatValue(this.value)
                });
                if (fieldTitle) {
                    return $color.tooltip({html: true}).attr('data-original-title', '<p>' + fieldTitle + '</p>');
                }
                return $color;
            } else {
                return false;
            }
        }
    });

    FieldChar.include({
        _renderReadonly: function () {
            var options = this.nodeOptions;
            if (this.value && 'color' in options) {
                var $colorNode = this._getColorNode(this.record, options);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            } else {
                this._super()
            }
        }
    });

    FieldFloat.include({
        _renderReadonly: function () {
            var options = this.nodeOptions;
            if (this.value && 'color' in options) {
                var $colorNode = this._getColorNode(this.record, options);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            } else {
                this._super()
            }
        }
    });

    FieldInteger.include({
        _renderReadonly: function () {
            var options = this.nodeOptions;
            if (this.value && 'color' in options) {
                var $colorNode = this._getColorNode(this.record, options);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            } else {
                this._super()
            }
        }
    });

    FieldSelection.include({
        _renderReadonly: function () {
            var options = this.nodeOptions;
            if (this.value && 'color' in options) {
                var $colorNode = this._getColorNode(this.record, options);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            } else {
                this._super()
            }
        }
    });

});