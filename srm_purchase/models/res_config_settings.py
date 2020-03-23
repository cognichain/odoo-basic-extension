# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_approval_workflow = fields.Boolean('采购单启用审批流程')

    po_2_platform = fields.Boolean('采购单对接公共平台')

    use_approval_workflow_module = fields.Boolean('启用审批流模块', help='启用此选项，将使用审批流模块的审批流程替换原有审批流程。')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            use_approval_workflow=ICPSudo.get_param('srm_purchase.use_approval_workflow', default=False),
            po_2_platform=ICPSudo.get_param('srm_purchase.po_2_platform', default=False),
            use_approval_workflow_module=ICPSudo.get_param('srm_purchase.use_approval_workflow_module', default=False),
        )
        return res

    # @api.multi
    # def set_values(self):
    #     super(ResConfigSettings, self).set_values()
    #     ICPSudo = self.env['ir.config_parameter'].sudo()
    #     ICPSudo.set_param("srm_purchase.use_approval_workflow", self.use_approval_workflow)
    #     ICPSudo.set_param("srm_purchase.po_2_platform", self.po_2_platform)
    #     self.env.ref('srm_purchase.submenu_purchase_approval').write({
    #         'active': self.use_approval_workflow
    #     })

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("srm_purchase.use_approval_workflow_module", self.use_approval_workflow_module)
