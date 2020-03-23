# -*- coding:utf-8 -*-

import datetime

from scenterpy.client import SCenterClient

api_client_pool = {}


class BaseDao:
    def __init__(self, env=None):
        self.env = env
        self.username = self.env['ir.config_parameter'].get_param("srm_scenter.account__username")
        self.password = self.env['ir.config_parameter'].get_param("srm_scenter.account__password")
        self.scenter_url = self.env['ir.config_parameter'].get_param("srm_scenter.scenter_domain")

        db_name = env.registry.db_name
        client_token = api_client_pool.get(db_name, None)

        if client_token:
            token = client_token.get('token')
            expires = client_token.get('expires')
            if token and expires:
                # token 过期前2分钟刷新token
                if expires - datetime.datetime.utcnow() < datetime.timedelta(0, 120):
                    self.connect(db_name)
                else:
                    self.api_client = SCenterClient(username=self.username, password=self.password, token=token,
                                                    expires=expires, base_url=self.scenter_url)
            else:
                self.connect(db_name)
        else:
            self.connect(db_name)

    def connect(self, db_name):
        self.api_client = SCenterClient(username=self.username, password=self.password,
                                        base_url=self.scenter_url)

        # 每次连接即刷新token，更新token到缓存
        api_client_pool[db_name] = {
            'token': self.api_client.token,
            'expires': self.api_client.expires
        }
