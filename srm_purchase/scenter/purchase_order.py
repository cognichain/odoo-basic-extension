# coding=utf-8

from . import BaseDao


class PurchaseOrderDao(BaseDao):

    def create(self, data):
        return self.api_client.purchase_order.create(data)

    def update(self, slug, data):
        return self.api_client.purchase_order.update(slug, data)
