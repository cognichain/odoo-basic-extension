# -*- coding: utf-8 -*-

from odoo import models, fields, api

from qiniu import Auth


class QiniuConfigSetting(models.TransientModel):

    _inherit = 'res.config.settings'

    access_key = fields.Char('Access Key')
    secret_key = fields.Char('Secret Key')
    bucket = fields.Char('Bucket')
    domain = fields.Char('Domain', help="资源域名")

    @api.model
    def get_values(self):
        res = super(QiniuConfigSetting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            access_key=ICPSudo.get_param('web_qiniu_uploader.access_key', default=''),
            secret_key=ICPSudo.get_param('web_qiniu_uploader.secret_key', default=''),
            bucket=ICPSudo.get_param('web_qiniu_uploader.bucket', default=''),
            domain=ICPSudo.get_param('web_qiniu_uploader.domain', default='https://')
        )
        return res

    @api.multi
    def set_values(self):
        super(QiniuConfigSetting, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("web_qiniu_uploader.access_key", self.access_key)
        ICPSudo.set_param("web_qiniu_uploader.secret_key", self.secret_key)
        ICPSudo.set_param("web_qiniu_uploader.bucket", self.bucket)
        ICPSudo.set_param("web_qiniu_uploader.domain", self.domain)

    @api.model
    def get_qiniu_token(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        access_key = ICPSudo.get_param('web_qiniu_uploader.access_key', default='')
        secret_key = ICPSudo.get_param('web_qiniu_uploader.secret_key', default='')
        bucket = ICPSudo.get_param('web_qiniu_uploader.bucket', default='')
        if access_key and secret_key and bucket:
            # 构建鉴权对象
            q = Auth(access_key, secret_key)
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket)
            return {
                'token': token,
                'domain': ICPSudo.get_param('web_qiniu_uploader.domain', default='https://')
            }
        return False
