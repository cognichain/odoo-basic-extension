odoo.define('web_widget_colored_field', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var basic_fields = require('web.basic_fields');
    var fieldRegistry = require('web.field_registry');
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

    var FieldColorChar = FieldChar.extend({
        _renderReadonly: function () {
            if (this.value) {
                var $colorNode = this._getColorNode(this.record, this.nodeOptions);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            }
        }
    });

    var FieldColorFloat = FieldFloat.extend({
        _renderReadonly: function () {
            if (this.value) {
                var $colorNode = this._getColorNode(this.record, this.nodeOptions);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            }
        }
    });

    var FieldColorInteger = FieldInteger.extend({
        _renderReadonly: function () {
            if (this.value) {
                var $colorNode = this._getColorNode(this.record, this.nodeOptions);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            }
        }
    });

    fieldRegistry
        .add('color_char', FieldColorChar)
        .add('color_float', FieldColorFloat)
        .add('color_integer', FieldColorInteger);

    var FieldColorSelection = FieldSelection.extend({
        _renderReadonly: function () {
            if (this.value) {
                var $colorNode = this._getColorNode(this.record, this.nodeOptions);
                if ($colorNode) {
                    this.$el.html($colorNode)
                } else {
                    this._super()
                }
            }
        }
    });

    fieldRegistry.add('color_selection', FieldColorSelection);
});