odoo.define('web_widget_many2many_tags_open', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var FormFieldMany2ManyTags = relational_fields.FormFieldMany2ManyTags;

    FormFieldMany2ManyTags.include({
        _onOpenColorPicker: function (ev) {
            if (this.mode === 'readonly' && this.nodeOptions.open_view) {
                ev.preventDefault();
                ev.stopPropagation();
                var self = this;
                var tagID = $(ev.currentTarget).parent().data('id');
                this._rpc({
                    model: this.field.relation,
                    method: 'get_formview_action',
                    args: [[tagID]],
                    context: this.record.getContext(this.recordParams),
                }).then(function (action) {
                    self.trigger_up('do_action', {action: action});
                });
            } else {
                this._super.apply(this, arguments);
            }
        }
    });
});