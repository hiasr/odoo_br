from odoo import fields, models, api

class SaleOrderLine(models.Model):
	_inherit="sale.order.line"

	discount = fields.Float(
        store=False,
        readonly=True,
    )
