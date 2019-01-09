# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request


class ResUsersLog(models.Model):

    _inherit = 'res.users.log'

    ip = fields.Char('IP', readonly=True)
    location = fields.Char('Location', readonly=True)
    user_agent = fields.Char('User Agent', readonly=True)


class Users(models.Model):

    _inherit = 'res.users'

    @api.model
    def _update_last_login(self):
        self.env['res.users.log'].create({
            'ip': request.httprequest.remote_addr,
            'user_agent': request.httprequest.user_agent.string
        })
